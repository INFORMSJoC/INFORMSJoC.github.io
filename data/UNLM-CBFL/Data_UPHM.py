''' This is for UPHM instances.
    
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
    d, b, A = GenerateData(I,J,distance_decacy_base)   # the functon returns u (utility) and b (net profit)
    
    print(d.shape)
    print(b.shape)
    print(A.shape)    
    print(P)    
    
    
    
        
        
        
    

