'''************************************************************************
This is the data generation file for the manuscript

  "Profit-Maximizing Parcel Locker Location Problem under Threshold Luce Model"

There are two datasets, i.e., D1 and D2. 

Both datasets are generated with fixed random seeds.

I, J are the number of customers and the number of candicate facilities

Customers and facilities are generated in a 2-D plane.

Distance is computed as the Euclidean distance.    

Each function below (D1 and D2) returns:
    Distance: distance matrix between customers and facilites (dimension I*J)
    Demand: dmenad size of each customer (dimension I)
    Location_Customer_x: x axis of the location of customers  (dimension I)
    Location_Customer_y: y axis of the location of customers  (dimension I)
    Location_Locker_x:   x axis of the location of lockers    (dimension J)
    Location_Locker_y:   y axis of the location of lockers    (dimension J)
************************************************************************'''

import numpy as np

def D1():
    I, J = 200, 100
    np.random.seed(5)
    Location_Customer_x = np.random.uniform(0,30,I)
    np.random.seed(6)    
    Location_Customer_y = np.random.uniform(0,30,I)
    np.random.seed(7)
    Location_Locker_x = np.random.uniform(0,30,J)
    np.random.seed(8)
    Location_Locker_y = np.random.uniform(0,30,J)
    Distance = np.zeros((I,J))
    for i in range(I):
        for j in range(J):
           Distance[i,j] = np.sqrt((Location_Customer_x[i] - Location_Locker_x[j])**2 + (Location_Customer_y[i] - Location_Locker_y[j])**2)
    np.random.seed(9)    
    Demand = np.random.uniform(1, 1000, I)    
    return(Distance,Demand,Location_Customer_x, Location_Customer_y, Location_Locker_x, Location_Locker_y)
            
def D2():
    I, J = 400, 150
    np.random.seed(5)
    Location_Customer_x = np.random.uniform(0,40,I)
    np.random.seed(6)    
    Location_Customer_y = np.random.uniform(0,40,I)
    np.random.seed(7)
    Location_Locker_x = np.random.uniform(0,40,J)
    np.random.seed(8)
    Location_Locker_y = np.random.uniform(0,40,J)
    Distance = np.zeros((I,J))
    for i in range(I):
        for j in range(J):
           Distance[i,j] = np.sqrt((Location_Customer_x[i] - Location_Locker_x[j])**2 + (Location_Customer_y[i] - Location_Locker_y[j])**2)
    np.random.seed(9)    
    Demand = np.random.uniform(1, 1000, I)    
    return(Distance,Demand,Location_Customer_x, Location_Customer_y, Location_Locker_x, Location_Locker_y)