import numpy as np 
import matplotlib.pyplot as plt
import math

# defining constants
g = 9.81 # gravity
y = 0.05 # atmospheric viscous force constant
m = 0.5  # mass 
T = 0.05 # Time step
N = 200  # number of steps
# X_(k+1) = AX_(k) + BU_(k) + C
m_A = np.array([[1,T,0,0],[0,1 - y*T/m,0,0],[0,0,1,T],[0,0,0,1 - y*T/m]])
m_B = np.array([[0,0],[T/m,0],[0,0],[0,T/m]]).reshape(4,2)
v_C = np.array([0,0,0,-g*T]).reshape(4,1)

# defining initial covariances
m_Q = 0.5*np.eye(4)
m_R = 0.5*np.eye(2)

class EKF :
    def __init__(self,ini_x,ini_u,ini_z,ini_w) :
        self.v_X = np.array([ini_x,ini_u,ini_z,ini_w]).reshape(4,1)
        self.m_P = 0.01*np.eye(4)

    def predict(self,v_U,m_Q) :
        # X_(k+1) = AX_(k) + BU_(k) + C
        self.v_X = m_A.dot(self.v_X) + m_B.dot(v_U) + v_C
        # P_(k|k-1) = F_(k)P_(k-1|k-1)F_(k)_T + Q_(k)
        # here F_k comes out to be A itself
        self.m_P = m_A.dot(self.m_P.dot(m_A.T)) + m_Q
        return
    
    def update(self,m_R,v_Z) :
        # defining H as dz/dX  
        # defining innovation
        v_e = v_Z - np.array([math.sqrt((float(self.v_X[0])**2 + float(self.v_X[2])**2)),float(self.v_X[2])]).reshape(2,1)
        c = math.sqrt(float(self.v_X[0])**2 + float(self.v_X[2])**2)
        m_H = np.array([[float(self.v_X[0])/c,0,float(self.v_X[2])/c,0],[0,0,1,0]]).reshape(2,4)
        # innovation covariance
        m_S = m_H.dot(self.m_P.dot(m_H.T)) + m_R
        # Kalman gain
        m_K = self.m_P.dot(m_H.T.dot(np.linalg.inv(m_S)))
        # updating the state and covariance
        self.v_X = np.add(self.v_X,m_K.dot(v_e))
        self.m_P = (np.eye(4) - m_K.dot(m_H)).dot(self.m_P)
        return

# input initial state parameters
x = float(input("x"))
u = float(input("u"))
z = float(input("z"))
w = float(input("w"))
ekf = EKF(x,u,z,w)
# input control parameters
F_x = float(input("thrust_F_x"))
F_z = float(input("thrust_F_z"))
v_U = np.array([F_x,F_z]).reshape(2,1)

# taking measurements
t = np.arange(0,10,0.05)
r_m = []
z_m = []
z_1_m = z + np.random.normal(scale = 1)
x_1_m = x + np.random.normal(scale = 1)

for j in range(N) :
    r_m.append(math.sqrt((x_1_m**2 + z_1_m**2)))
    z_m.append(z_1_m)
    x_1_m += u*T
    u += (float(v_U[0]) - y*u)*T/m
    z_1_m += w*T
    w += (float(v_U[1]) - y*w - m*g)*T/m
    
r_m_e = r_m + np.random.normal(scale = 15, size = len(t))
z_m_e = z_m + np.random.normal(scale = 15, size = len(t))

v_Z = []

for k in range(N) :
    v_Z.append(np.array([r_m_e[k],z_m_e[k]]).reshape(2,1))

v_X_arr = []
m_P_arr = []
v_X_plot = []

for i in range(N) :
    ekf.predict(v_U,m_Q)
    ekf.update(m_R,v_Z[i])
    v_X_arr.append(ekf.v_X)
    v_X_plot.append(math.sqrt(float(ekf.v_X[0])**2 + float(ekf.v_X[2])**2))
    m_P_arr.append(ekf.m_P.trace()/2.0)

# plotting the estimates

# expected trajectory
plt.plot(t,r_m)
plt.plot(t,z_m)
plt.title('expected trajectory')
plt.legend(['position','altitude'],loc = 'upper left')
plt.show()

# measurements
plt.plot(t,r_m_e)
plt.title("measurements")
plt.xlabel("time step")
plt.ylabel("position")
plt.show()

plt.plot(t,z_m_e)
plt.title("measurements")
plt.xlabel("time step")
plt.ylabel("altitude")
plt.show()

# state 
plt.plot(t,list(zip(*v_X_arr))[0])
plt.plot(t,list(zip(*v_X_arr))[1])
plt.plot(t,list(zip(*v_X_arr))[2])
plt.plot(t,list(zip(*v_X_arr))[3])
plt.title("State")
plt.legend(['x','vel_x','altitude','vel_z'], loc = "upper left")
plt.xlabel("time step")
plt.ylabel("state")
plt.show()

# covariance
plt.plot(t,m_P_arr)
plt.xlabel("time step")
plt.ylabel("covariance")
plt.show()

# comparing estimates with original and measurements
plt.plot(t,v_X_plot)
plt.plot(t,r_m)
plt.title('comparing estimates with original')
plt.legend(['estimate','original'], loc = 'upper left')
plt.xlabel('time step')
plt.show()