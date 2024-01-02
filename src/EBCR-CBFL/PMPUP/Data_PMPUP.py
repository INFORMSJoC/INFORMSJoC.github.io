''' This is for PMPUP instances.
    
    * There are 30 instances, indexed by 333, 433, 533, ..., 3233.
    * Each instance is stored in a txt file.   

These instances are the "p-Median Problem with Users Preferences" dataset 
from benchmark library "Discrete Location Problems". 
See http://old.math.nsc.ru/AP/benchmarks/Bilevel/bilevel-eng.html     
'''

import numpy as np
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
    
    file_name = '533.txt'                   # get the data of instance '533'
    u, b, A, P = Generate_data(file_name)   # the functon returns u (utility) and b (net profit)
                                            # A (the accessibility matrix) and P (number of facilities to open)
    print(u.shape)
    print(b.shape)    
    print(A.shape)
    print(P)
    
    
    
