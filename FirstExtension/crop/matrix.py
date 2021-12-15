import math
def degree_to_hudu(x):
    return (x/180*math.pi)
import numpy as np
import vtk, qt, ctk, slicer
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
def my_updateFinalTransform(input_volume,matrix_vector):
# self.centerOfRotationMarkupsNode = slicer.util.getNode("F")
# print(self.centerOfRotationMarkupsNode)
# This transform can be  edited in Transforms module
# self.rotationTransformNode = slicer.util.getNode("LinearTransform_3")
    # This transform has to be applied to the image, model, etc.
# self. finalTransformNode = slicer.util.getNode("LinearTransform_4")
    rotationMatrix = vtk.vtkMatrix4x4()
    rotationMatrix.DeepCopy(matrix_vector)
    # self.rotationTransformNode.GetMatrixTransformToParent(rotationMatrix)
    # rotationMatrix.Identity ()
    # rotationMatrix.SetElement(1,1,0.707)
    # rotationMatrix.SetElement(1,2,-0.707)
    # rotationMatrix.SetElement(2,1,0.707)
    # rotationMatrix.SetElement(2,2,0.707)
    rotationCenterPointCoord = [0.0, 0.0, 0.0]
    # self.centerOfRotationMarkupsNode.GetNthControlPointPositionWorld(0, rotationCenterPointCoord)
    finalTransform = vtk.vtkTransform()
    finalTransform.Translate(rotationCenterPointCoord)
    finalTransform.Concatenate(rotationMatrix)
    finalTransform.Translate(-rotationCenterPointCoord[0], -rotationCenterPointCoord[1], -rotationCenterPointCoord[2])
    # self.finalTransformNode.SetAndObserveMatrixTransformToParent(finalTransform.GetMatrix())
    input_volume.ApplyTransformMatrix(finalTransform.GetMatrix())
    print(finalTransform.GetMatrix())
def get_totoal_matrix(Four_by_Four_Matrix):
    r_m=np.ones(3,3)
    import math
def degree_to_hudu(x):
    return (x/180*math.pi)
import numpy as np
import vtk, qt, ctk, slicer
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
    R_x[2][1]=math.sin(x_theta)
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
def my_updateFinalTransform(input_volume,matrix_vector):
# self.centerOfRotationMarkupsNode = slicer.util.getNode("F")
# print(self.centerOfRotationMarkupsNode)
# This transform can be  edited in Transforms module
# self.rotationTransformNode = slicer.util.getNode("LinearTransform_3")
    # This transform has to be applied to the image, model, etc.
# self. finalTransformNode = slicer.util.getNode("LinearTransform_4")
    rotationMatrix = vtk.vtkMatrix4x4()
    rotationMatrix.DeepCopy(matrix_vector)
    # self.rotationTransformNode.GetMatrixTransformToParent(rotationMatrix)
    # rotationMatrix.Identity ()
    # rotationMatrix.SetElement(1,1,0.707)
    # rotationMatrix.SetElement(1,2,-0.707)
    # rotationMatrix.SetElement(2,1,0.707)
    # rotationMatrix.SetElement(2,2,0.707)
    rotationCenterPointCoord = [0.0, 0.0, 0.0]
    # self.centerOfRotationMarkupsNode.GetNthControlPointPositionWorld(0, rotationCenterPointCoord)
    finalTransform = vtk.vtkTransform()
    finalTransform.Translate(rotationCenterPointCoord)
    finalTransform.Concatenate(rotationMatrix)
    finalTransform.Translate(-rotationCenterPointCoord[0], -rotationCenterPointCoord[1], -rotationCenterPointCoord[2])
    # self.finalTransformNode.SetAndObserveMatrixTransformToParent(finalTransform.GetMatrix())
    input_volume.ApplyTransformMatrix(finalTransform.GetMatrix())
    print(finalTransform.GetMatrix())
