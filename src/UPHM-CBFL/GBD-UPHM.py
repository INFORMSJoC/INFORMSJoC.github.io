''' This is for UPHM and UNLM instances (Note that the data used for UNLM is the same as UPHM) 
    
    * J: number of facilities. 
    * I: number of customer zones. 
    * P: number of facilities to be open.
    (for the comnination of (I,J,P), refer to the manuscript)
    * b is the buying power
    * d is the distacne matrix
    * A is the attractivess of facility
 
'''

import numpy as np

def GenerateData(I,J,distance_decacy_base):
    np.random.seed(5)
    Location_Cus_x = np.random.uniform(0,100,I)
    np.random.seed(6)    
    Location_Cus_y = np.random.uniform(0,100,I)
    np.random.seed(7)
    Location_Loc_x = np.random.uniform(0,100,J)
    np.random.seed(8)
    Location_Loc_y = np.random.uniform(0,100,J)
    d = np.zeros((I,J))
    for i in range(I):
        for j in range(J):
           d[i,j] = np.sqrt((Location_Cus_x[i] - Location_Loc_x[j])**2 + (Location_Cus_y[i] - Location_Loc_y[j])**2)
    np.random.seed(9)    
    b = np.random.uniform(1, 1000, I) 
    np.random.seed(10)        
    A = np.random.uniform(1, 100, J) 
    return(d,b,A)


### example of usuage
if __name__ == "__main__":
    
    I, J, P = 100, 50, 5                               # generate an instance with 100 customers and 50 facilities, and 5 facilties are to be open
    distance_decacy_base = 2
    d, b, A = GenerateData(I,J,distance_decacy_base)
          
    
    ### solve the instance by GBD in the paper
    import gurobipy as grb


    u = np.zeros((I,J))
    for j in range(J):
        u[:,j] = A[j]/d[:,j]**distance_decacy_base
    
    u_0 = np.ones(I)
    for i in range(I):
        u[i,:] = u[i,:]/u_0[i]
    ###############################################################################
    delta = np.zeros((I,J,J))
    for i in range(I):
        for j in range(J):
            for k in range(J):
                if (A[j] >= A[k]) and (1/d[i,j] >= 1/d[i,k]) and (u[i,j] > u[i,k]): 
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
        Phi = b*(1-1/(np.sum(u*y_sol,axis=1)+1))
        der_R = np.zeros((I,J))
        for i in range(I):
            der_R[i] = b[i]*u[i]/(u[i]@y_sol[i]+1)**2 
        return(y_sol,Phi,der_R)          
    
    def get_dominating_set(i,J_11,J_10):
        J_110 = J_11.copy()
        J_100 = J_10.copy()
        dominating_set = []
        while len(J_100) > 0:    
            m = J_110[np.argmax(np.sum((delta[i,J_110])[:,J_100],axis=1))]
            dominating_set.append(m) 
            J_110.remove(m)
            J_100 = list(set(J_100) - (set(set_Delta[i][m]) & set(J_100)))
        return(dominating_set) 
        
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
                    dominating_set = get_dominating_set(i,J_11,J_10)                   
                    for j in dominating_set:
                        mu[i,j] = np.max(der_R[i,list(set(J_10) & set(set_Delta[i][j]))])                                                
                ### compute lamda
                lamda[i,J_11] = der_R[i,J_11] - alpha[i,J_11]*v[i]                                                    # set J_11        
                lamda[i,J_00] = np.maximum(der_R[i,J_00] - (delta[i,J_11].T@mu[i,J_11])[J_00] - alpha[i,J_00]*v[i],0) # set J_00  
            ### Case 2
            else:
                ### v[i] = 0            
                if len(J_10) >= 1: 
                    dominating_set = get_dominating_set(i,J_11,J_10)                
                    for j in dominating_set:
                        mu[i,j] = np.max(der_R[i,list(set(J_10) & set(set_Delta[i][j]))])                
                ### compute lamda
                lamda[i,J_11] = der_R[i,J_11]                                                     # set J_11
                lamda[i,J_00] = np.maximum(der_R[i,J_00] - (delta[i,J_11].T@mu[i,J_11])[J_00],0)  # set J_00
    
        return(lamda,mu,Phi)
    ###############################################################################
    ###############################################################################
    alpha = np.zeros((I,J))
    for i in range(I):
        m = np.argmax([len(set_Delta[i][j]) for j in range(J)])
        varrho = [m]
        while len(set_Delta[i][m]) > 0:
            m = set_Delta[i][m][np.argmax([len(set_Delta[i][j]) for j in set_Delta[i][m]])]        
            varrho.append(m)
        alpha[i,varrho] = 1
    
    Q = np.minimum(np.sum(delta,axis=2),P)
    ###############################################################################                                
    ###############################################################################                                                 
    import cvxpy as cp
    x_bar = cp.Parameter(J)
    y = cp.Variable((I,J),nonneg = True)
    constraint = []
    for i in range(I):
        constraint += [delta[i]@y[i] <= cp.multiply(Q[i],1-x_bar)] 
    constraint += [cp.sum(cp.multiply(alpha,y),axis=1) <= 1]     
    constraint += [y <= np.ones((I,1))@cp.reshape(x_bar,(1,J))]      
    obj_func = b@(1-cp.inv_pos(cp.sum(cp.multiply(u,y),axis=1)+1))
    prob = cp.Problem(cp.Maximize(obj_func),constraint)
               
    ###############################################################################  
    # define LP relaxation master problem for generating intial Benders cuts before branch and cut
    cut_pool_LP = []
    rm = grb.Model()
    rx = rm.addVars(J,lb=0,ub=1,name='X')
    rw = rm.addVars(I,ub = np.sum(b))
    rm.update()
    rm.setParam('OutputFlag', 0)
    rm.setObjective(grb.quicksum(rw[i] for i in range(I)),grb.GRB.MAXIMIZE)   
    rm.addConstr(grb.quicksum(rx[j] for j in range(J)) == P)
    ###############################################################################  
    # define the true master problem
    m = grb.Model()
    x = m.addVars(J,vtype=grb.GRB.BINARY)
    w = m.addVars(I,ub = b)
    m.update()
    m.setParam('OutputFlag', 1)
    m.setParam('TimeLimit', 7200)
    m.setParam('displayInterval',50)
    m.setParam('Threads', 1)
    m.setParam('IntFeasTol', 1e-9)     # default 1e-5
    m.setParam('FeasibilityTol', 1e-9) # default 1e-5
    m.setParam('OptimalityTol', 1e-9)  # default 1e-5
    m.setObjective(grb.quicksum(w[i] for i in range(I)),grb.GRB.MAXIMIZE)
    m.addConstr(grb.quicksum(x[j] for j in range(J)) == P)
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
        prob.solve(solver=cp.MOSEK, verbose = 0,warm_start= True)     
        mu = np.zeros((I,J))
        for i in range(I):
            mu[i] =  constraint[i].dual_value
        lamda = constraint[-1].dual_value   
        Phi = b * (1-cp.inv_pos(cp.sum(cp.multiply(u,y),axis=1)+1)).value
        subgradient = lamda - mu * Q
        for i in range(I):
            if rw[i].x > Phi[i]*(1+1e-5):
                rm.addConstr(rw[i] <= Phi[i] + grb.quicksum(subgradient[i,j]*(rx[j] - x_sol[j]) for j in range(J)))  
                m.addConstr(w[i] <= Phi[i] + grb.quicksum(subgradient[i,j]*(x[j] - x_sol[j]) for j in range(J)))
                cut_number += 1
            
        LB = max(LB, np.sum(Phi)) 
        print("Itr", itr, "with rgap",round((UB -LB)/UB*100,2))
    stage1_time = TM.time() - start_time
    ###############################################################################               
        
    def lazy_cut(model, where):  
        if where == grb.GRB.Callback.MIPSOL:       
            x_vals = model.cbGetSolution(m._x)
            x_sol = np.array([round(x_vals[j]) for j in range(J)])         
            ### solve DSP
            lamda, mu, Phi = Dual_SP(x_sol)  
            ### Cut coefficient
            subgradient = lamda - mu * Q        
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
    print("############################################")
    print("Profit is",round(m.ObjVal,1),"by 2StageBenders")
    print("Solve time is", round(m.Runtime + stage1_time,1))
    print("Stage 1 total time", round(stage1_time,1))
    print("rgap", round(m.MIPGap*100,2))
    print("Number of branch and cut nodes is ", round(m.NodeCount))
    print("Number of cuts is ", round(m._number_of_cuts + cut_number))
    print("Number of facilities is", np.sum(x_sol))