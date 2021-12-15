import math
def degree_to_hudu(x):
    return (x/180*math.pi)
import numpy as np
def get_rotation_matrix(x_theta,y_theta,z_theta):
    x_theta=degree_to_hudu(x_theta)
    y_theta=degree_to_hudu(y_theta)
    z_theta=degree_to_hudu(z_theta)
    R_y=np.eye(3,3)
    R_x=np.eye(3,3)
    R_z=np.eye(3,3)
    R_y[0][0]=math.cos(y_theta)
    R_y[0][2]=math.sin(y_theta)
    R_y[2][0]=-math.sin(y_theta)
    R_y[2][2]=math.cos(y_theta)

    
    R_x[1][1]=math.cos(x_theta)
    R_x[1][2]=math.sin(x_theta)
    R_x[1][2]=-math.sin(x_theta)
    R_x[2][2]=math.cos(x_theta)
  
  
    R_z[0][0]=math.cos(z_theta)
    R_z[1][0]=math.sin(z_theta)
    R_z[0][1]=-math.sin(z_theta)
    R_z[1][1]=math.cos(z_theta)
    
    ans=np.matmul(R_y,R_x)
    ans=np.matmul(ans,R_z)
    print(R_y)
    print(R_x)
    print(R_z)
    
    b=np.zeros([4,4])
    b[0:3,0:3]=ans
    b[3,3]=1
    anss=b.reshape(16).tolist()
    
    print(ans)  

    return anss
get_rotation_matrix(35,0,0)