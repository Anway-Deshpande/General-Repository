import math
import numpy as np

class quaternion:
    def __init__(self, q0, q1, q2, q3):
        self.q0 = q0
        self.q1 = q1
        self.q2 = q2
        self.q3 = q3

quat = quaternion(float(input('enter q0 ')),float(input('enter q1 ')),float(input('enter q2 ')),float(input('enter q3 ')))

class rot_vec:
    def __init__(self,quat):
        self.theta = 2*math.acos(quat.q0)
        self.vec = [quat.q1,quat.q2,quat.q3]
        for i in range(0,3):
            self.vec[i] /= round(math.sin(self.theta/2),4)
    def calc(self):
        return self.theta,self.vec

eul_ax = rot_vec(quat)

class rot_mat:
    def __init__(self,eul_ax):
        self.mat_ele = []
        ct = math.cos(eul_ax.theta)
        st = math.sin(eul_ax.theta)
        u1 = eul_ax.vec[0]
        u2 = eul_ax.vec[1]
        u3 = eul_ax.vec[2]
        self.mat_ele.append(round(ct+u1**2 * (1-ct),4))
        self.mat_ele.append(round(u1*u2*(1-ct)-u3*st,4))
        self.mat_ele.append(round(u1*u3*(1-ct)+u2*st,4))
        self.mat_ele.append(round(u2*u1*(1-ct)+u3*st,4))
        self.mat_ele.append(round(ct+u2**2 * (1-ct),4))
        self.mat_ele.append(round(u2*u3*(1-ct)-u1*st,4))
        self.mat_ele.append(round(u3*u1*(1-ct)-u2*st,4))
        self.mat_ele.append(round(u3*u2*(1-ct)+u1*st,4))
        self.mat_ele.append(round(ct+u3**2 * (1-ct),4))
    def print_matrix(self):
         self.mat_ele = np.array(self.mat_ele)
         print('Rotation matrix: ')
         print(self.mat_ele.reshape(3,3))
RM = rot_mat(eul_ax)

class eul_ang:
    def __init__(self,quat):
        self.theta = math.asin(2*(quat.q0*quat.q2-quat.q1*quat.q3))
        self.phi = math.atan2(2*(quat.q0*quat.q1+quat.q2*quat.q3),1-2*(quat.q1**2 + quat.q2**2))
        self.psi = math.atan2(2*(quat.q0*quat.q3+quat.q1*quat.q2),1-2*(quat.q2**2 + quat.q3**2))
        self.angles = [self.phi,self.theta,self.psi]
    def print_eul_ang(self):
        print('Euler angles (axes rotated in order xyz): ',self.angles)

EA = eul_ang(quat)
EA.print_eul_ang()
print('Theta and Euler axis: ',eul_ax.calc())
RM.print_matrix()
