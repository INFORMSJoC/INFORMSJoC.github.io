''' This is for Rnd-EBCR instances.

    * J: number of facilities. It is fixed at 100
    * I: number of customer zones. We use 100, 150, 200, 300, 400
    * P: number of facilities to be open. We use 3, 5, 7, 10, 15, 20
    
 Therefore, the total number instances are 5 times 6, which is 30.
'''

import numpy as np

def Generate_data(I,J):
    np.random.seed(100)
    x_axis_customer = np.random.uniform(1,100,I)
    np.random.seed(200)
    y_axis_customer = np.random.uniform(1,100,I)
    np.random.seed(300)
    x_axis_facility = np.random.uniform(1,100,J)
    np.random.seed(400)
    y_axis_facility = np.random.uniform(1,100,J)
    l = np.zeros((I,J))
    for i in range(I):
        for j in range(J):
            l[i,j] = np.sqrt(np.square(x_axis_customer[i] - x_axis_facility[j]) + np.square(y_axis_customer[i] - y_axis_facility[j]))
    np.random.seed(600)
    u = np.zeros((I,J))
    for i in range(I):
        for j in range(J):            
            u[i,j] =  1/(np.random.uniform(0.4*l[i,j],1.6*l[i,j]))          
    b = 150 - l
    return(u,b)

### example of usuage
if __name__ == "__main__":
    J = 100
    
    I, P = 200, 3             # generate an instance with 200 customers, and 3 facilties are to be open
    u, b = Generate_data(I,J) # the functon returns u (utility) and b (net profit)
    
    print(u.shape)
    print(b.shape)



  
    