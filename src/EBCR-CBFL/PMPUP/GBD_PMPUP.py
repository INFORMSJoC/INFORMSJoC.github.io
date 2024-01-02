''' This is for PMPUP instances.
    
    * There are 30 instances, indexed by 333, 433, 533, ..., 3233.
    * Each instance is stored in a txt file.   

These instances are the "p-Median Problem with Users Preferences" dataset 
from benchmark library "Discrete Location Problems". 
See http://old.math.nsc.ru/AP/benchmarks/Bilevel/bilevel-eng.html     
'''

import numpy as np

I = 100            # number of customer zones    (fixed at 100)
J = 100            # number of leader facilities (fixed at 100)

timelimit = 3600
####################################################

def Generate_data(file_name):
    file = open(file_name, "r")  # read the txt file.  
    b = np.zeros((100,100))      # if facility j is not accessibale to zone i, set b[i,j] = 0 , which is larger than others
    u = np.zeros((100,100))      # if facility j is not accessibale to zone i, set u[i,j] = 0, which is larger than others
    A = np.zeros((100,100))      # indicate whether facility j is accessibale to zone i
    ### read data
    Lines = file.readlines() 
    Length = len(Lines)
    for n in range(Length):
        if n == 0:
           P = int(((Lines[n].strip()).split())[0])
        else:
           j = int(((Lines[n].strip()).split())[0])-1
           i = int(((Lines[n].strip()).split())[1])-1
           b[i,j] = 6 - float(((Lines[n].strip()).split())[2])
           u[i,j] = 12-float(((Lines[n].strip()).split())[3])
           A[i,j] = 1      
    return(u,b,A,P)

### example of usuage
if __name__ == "__main__":
    
    file_name = '533.txt'                  
    u, b, A, P = Generate_data(file_name)
    

    ### solve the instance by GBD in the paper
    import gurobipy as grb
    
    I, J = u.shape
    ###############################################################################
    delta = np.zeros((I,J,J))
    for i in range(I):
        for j in range(J):
            for k in range(J):
                if u[i,j] > u[i,k]:
                    delta[i,j,k] = 1
    set_Delta = []
    for i in range(I):
        set_Delta_i = []
        for j in range(J):
            set_Delta_ij = []
            for k in range(J):
                if delta[i,j,k] == 1:
                    set_Delta_ij.append(k)
            set_Delta_i.append(set_Delta_ij)
        set_Delta.append(set_Delta_i)                 
    ###############################################################################
    ###############################################################################
    ###############################################################################
    def Primal_SP(x_sol):
        y_sol = np.ones((I,J))
        for j in range(J):      # facility j is not open
            if x_sol[j] < 0.5:
                y_sol[:,j] = 0
            else:               # facility j is open
                for i in range(I):
                    y_sol[i,set_Delta[i][j]] = 0  
        Phi = np.sum(b*y_sol,axis=1)
        der_f = b
        return(y_sol,Phi,der_f) 
    
    def Dual_SP(x_sol):
        y_sol, Phi, der_R = Primal_SP(x_sol)
        lamda, mu, v = np.zeros((I,J)), np.zeros((I,J)), np.zeros(I)   
        for i in range(I):    
            J_00, J_10, J_11 = [], [], []
            for j in range(J):
                if x_sol[j] == 0:            # 0 = x_j = y_{ij} = 0
                    J_00.append(j)
                if x_sol[j] > y_sol[i,j]:    # 1 = x_j > y_{ij} = 0
                    J_10.append(j)
                if y_sol[i,j] == 1:          # 1 = x_j = y_{ij} = 1
                    J_11.append(j)
            ### Case 1
            if alpha[i]@y_sol[i] == 1:
                ### get v
                v[i] = np.min(der_R[i,[j for j in J_11 if alpha[i,j] == 1]]) 
                if len(J_10) >= 1: 
                    ### get m_i        
                    m_i = J_11[np.argmax(u[i,J_11])]
                    ### compute mu
                    mu[i,m_i] = max(0,np.max(der_R[i,J_10] - alpha[i,J_10]*v[i]))        
                ### compute lamda
                lamda[i,J_11] = der_R[i,J_11] - alpha[i,J_11]*v[i]                                          # set J_11        
                lamda[i,J_00] = np.maximum(der_R[i,J_00] - (delta[i].T@mu[i])[J_00] - alpha[i,J_00]*v[i],0) # set J_00  
            ### Case 2
            else: 
                ### v[i] = 0
                ### get m_i
                if len(J_10) >= 1: 
                    m_i = J_11[np.argmax(u[i,J_11])]        
                    ### compute mu
                    mu[i,m_i] = np.max(der_R[i,J_10])       
                ### compute lamda
                lamda[i,J_11] = der_R[i,J_11]                                         # set J_11        
                lamda[i,J_00] = np.maximum(der_R[i,J_00] - (delta[i].T@mu[i])[J_00],0) # set J_00             
        return(lamda,mu,Phi)               
    ###############################################################################
    ###############################################################################
    ###############################################################################
    alpha = np.ones((I,J))
    
    import cvxpy as cp
    x_bar = cp.Parameter(J)
    y = cp.Variable((I,J),nonneg = True)
    constraint = []
    for i in range(I):
        constraint += [delta[i]@y[i] <= 1-x_bar]
    constraint += [cp.sum(y,axis=1) == 1]
    constraint += [y <= np.ones((I,1))@cp.reshape(x_bar,(1,J))]
    obj_func = cp.sum(cp.multiply(b,y))
    prob = cp.Problem(cp.Maximize(obj_func),constraint)
    
    ####################################################
    ###############################################################################  
    # define LP relaxation master problem for generating intial Benders cuts before branch and cut
    rm = grb.Model()
    rx = rm.addVars(J,lb=0,ub=1,name='X')
    rw = rm.addVars(I,ub = 10000000000)
    rm.update()
    rm.setParam('OutputFlag', 0)
    rm.setParam('TimeLimit', timelimit)  
    rm.setObjective(grb.quicksum(rw[i] for i in range(I)),grb.GRB.MAXIMIZE)   
    rm.addConstr(grb.quicksum(rx[j] for j in range(J)) == P)
    for i in range(I):
        rm.addConstr(grb.quicksum(A[i,j]*rx[j] for j in range(J)) >= 1)
    ###############################################################################  
    # define the true master problem
    m = grb.Model()
    x = m.addVars(J,vtype=grb.GRB.BINARY)
    w = m.addVars(I,ub = 10000000000)
    m.update()
    m.setParam('TimeLimit', 7200)
    m.setParam('displayInterval',50)
    m.setParam('IntFeasTol', 1e-9)     # default 1e-5
    m.setParam('FeasibilityTol', 1e-9) # default 1e-5
    m.setParam('OptimalityTol', 1e-9)  # default 1e-5
    m.setParam('Threads', 1)           # use single thread
    m.setObjective(grb.quicksum(w[i] for i in range(I)),grb.GRB.MAXIMIZE)
    m.addConstr(grb.quicksum(x[j] for j in range(J)) == P)
    for i in range(I):
        m.addConstr(grb.quicksum(A[i,j]*x[j] for j in range(J)) >= 1)
    ###############################################################################  
    
    import time as TM
    start_time = TM.time()  
    UB, LB = 10000000, 0.01
    itr = 0
    cut_number = 0
    x_sol = np.zeros(J)
    while (UB -LB)/UB > 1e-4:
        itr += 1
        rm.optimize()
        UB = min(UB,rm.ObjVal)
        for j in range(J):
            x_sol[j] = rx[j].x      
        ### solve SP
        x_bar.value = x_sol
        prob.solve(solver=cp.GUROBI, verbose = 0,warm_start= True)
        mu = np.zeros((I,J))
        for i in range(I):
            mu[i] =  constraint[i].dual_value
        lamda = constraint[-1].dual_value   
        Phi = np.sum(b*y.value,axis=1)
        subgradient = lamda - mu
        for i in range(I):
            if rw[i].x > Phi[i]*(1+1e-5):
                rm.addConstr(rw[i] <= Phi[i] + grb.quicksum(subgradient[i,j]*(rx[j] - x_sol[j]) for j in range(J)))  
                m.addConstr(w[i] <= Phi[i] + grb.quicksum(subgradient[i,j]*(x[j] - x_sol[j]) for j in range(J)))
                cut_number += 1
            
        LB = max(LB, np.sum(Phi)) 
        print("Itr", itr, "with rgap",round((UB -LB)/UB*100,2))
    stage1_time = TM.time() - start_time
    print("Stage 1 time is", round(stage1_time,1))
    ###############################################################################               
        
    def lazy_cut(model, where):  
        if where == grb.GRB.Callback.MIPSOL:
            x_vals = model.cbGetSolution(m._x)
            x_sol = np.array([round(x_vals[j]) for j in range(J)]) 
            ### solve DSP
            lamda, mu, Phi = Dual_SP(x_sol)  
            ### Cut coefficient
            subgradient = lamda - mu         
            ### Add cut
            w_vals = model.cbGetSolution(m._w)
            for i in range(I):
                if w_vals[i] > Phi[i] * (1+1e-5):
                    m.cbLazy(w[i] <= Phi[i] + grb.quicksum(subgradient[i,j]*(x[j] - x_sol[j]) for j in range(J))) 
                    m._number_of_cuts += 1
    
    m._x = x
    m._w = w
    m._number_of_cuts = 0
    m.Params.lazyConstraints = 1
    m.optimize(lazy_cut) 
    ###### get the y matrix and compute the coverage
    x_sol = np.zeros(J)
    for j in range(J):
        x_sol[j] = round(x[j].x)  
    
    y_sol, Phi, der_R = Primal_SP(x_sol)
    print("##############################################")
    print("Profit is",round(m.ObjVal,1))
    print("Solve time is", round(m.Runtime + stage1_time,1))
    print("Stage 1 time is", round(stage1_time,1))
    print("Number of branch and cut nodes is ", round(m.NodeCount))
    print("Number of cuts is ", round(m._number_of_cuts + cut_number))
    print("Number of facilities is", np.sum(x_sol))
