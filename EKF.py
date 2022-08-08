import numpy as np 
import matplotlib.pyplot as plt

# defining constants
g = 9.81 # gravity
y = 0.05 # atmospheric viscous force constant
m = 0.5  # mass 
T = 0.05 # Time step
N = 100  # number of steps
# X_(k+1) = AX_(k) + BU_(k) + C
m_A = np.array([[1 - y*T/m,0,0,0],[0,1 - y*T/m,0,0],[0,0,1 - y*T/m,0],[0,0,T - y*T*T/m,1]])
m_B = np.array([[T/m,0,0],[0,T/m,0],[0,0,T/m],[0,0,T*T/m]]).reshape(4,3)
v_C = np.array([0,0,-g*T,-g*T*T]).reshape(4,1)

# defining initial covariances
m_Q = 0.05*np.eye(4)
m_R = 0.05*np.eye(4)

class EKF :
    def __init__(self,ini_u,ini_v,ini_w,ini_z) :
        self.v_X = np.array([ini_u,ini_v,ini_w,ini_z]).reshape(4,1)
        self.m_P = 0.01*np.eye(4)

    def predict(self,v_U,m_Q) :
        # X_(k+1) = AX_(k) + BU_(k) + C
        self.v_X = m_A.dot(self.v_X) + m_B.dot(v_U) + v_C
        print(self.v_X)
        # P_(k|k-1) = F_(k)P_(k-1|k-1)F_(k)_T + Q_(k)
        # here F_k comes out to be A itself
        self.m_P = m_A.dot(self.m_P.dot(m_A.T)) + m_Q
        return
    
    def update(self,m_R,v_Z,c) :
        # defining H as dz/dX  
        m_H = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,c],[0,0,1/c,1]])
        # defining innovation
        v_e = v_Z - m_H.dot(self.v_X)
        print(v_e)
        # innovation covariance
        m_S = m_H.dot(self.m_P.dot(m_H.T)) + m_R
        # Kalman gain
        m_K = self.m_P.dot(m_H.T.dot(np.linalg.inv(m_S)))
        print(m_K)
        # updating the state and covariance
        print(m_K.dot(v_e))
        self.v_X = self.v_X + m_K.dot(v_e)
        self.m_P = (np.eye(4) - m_K.dot(m_H)).dot(self.m_P)
        print(self.v_X)
        return

# input initial state parameters
u = float(input("u"))
v = float(input("v"))
w = float(input("w"))
z = float(input("z"))
ekf = EKF(u,v,w,z)
# input control parameters
F_x = float(input("thrust_F_x"))
F_y = float(input("thrust_F_y"))
F_z = float(input("thrust_F_z"))
v_U = np.array([F_x,F_y,F_z]).reshape(3,1)

# taking measurements
t = np.arange(0,5,0.05)
u_m = []
v_m = []
w_m = []
z_m = []

for j in range(N) :
    u += (F_x - y*u)*T/m
    u_m.append(u)
    v += (F_y - y*v)*T/m
    v_m.append(v)
    z += w*T + (F_z - y*w - m*g)*T*T/m
    z_m.append(z)
    print(z)
    w += (F_z - y*w - m*g)*T/m
    w_m.append(w)
    
u_m += np.random.normal(scale = 1, size = len(t))
v_m += np.random.normal(scale = 1, size = len(t))
w_m += np.random.normal(scale = 1, size = len(t))
z_m += np.random.normal(scale = 1, size = len(t))

v_Z = []

for k in range(N) :
    v_Z.append(np.array([u_m[k],v_m[k],w_m[k],z_m[k]]).reshape(4,1))

v_X_arr = []
m_P_arr = []

for i in range(N) :
    c = float(-y/m + (v_U[2]/m - g)/ekf.v_X[2])
    ekf.predict(v_U,m_Q)
    ekf.update(m_R,v_Z[i],c)
    print(z_m[i],ekf.v_X[2],ekf.v_X[3])
    v_X_arr.append(ekf.v_X)
    m_P_arr.append(ekf.m_P.trace()/2.0)

# plotting the estimates

# measurements
plt.plot(t,u_m)
plt.plot(t,v_m)
plt.plot(t,w_m)
plt.plot(t,z_m)
plt.title("measurements")
plt.xlabel("time step")
plt.ylabel("measurement vector")
plt.show()

# state 
plt.plot(t,list(zip(*v_X_arr))[0])
plt.plot(t,list(zip(*v_X_arr))[1])
plt.plot(t,list(zip(*v_X_arr))[2])
plt.plot(t,list(zip(*v_X_arr))[3])
plt.title("State")
plt.legend(['vel_x','vel_y','vel_z','altitude'], loc = "upper right")
plt.xlabel("time step")
plt.ylabel("state")
plt.show()

# covariance
plt.plot(t,m_P_arr)
plt.xlabel("time step")
plt.ylabel("covariance")
plt.show()

# estimate and measurement
plt.plot(t,z_m)
plt.plot(t,list(zip(*v_X_arr))[3])
plt.legend(['measure','state'])
plt.show()