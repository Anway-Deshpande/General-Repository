#import modules
import numpy as np
import matplotlib.pyplot as plt

#defining class
class KF:
    def __init__(self,initial_x,initial_v,v_acc_var,sigma_P,amp):
        #initial state vector and covariance(assumed accurately known)
        self.v_X = np.array([initial_x,initial_v]).reshape(2,1)
        self.m_P = np.array([[sigma_P,0],[0,sigma_P]])
        self.v_acc_var = v_acc_var
        self.amp = amp

    def predict(self,dt):
        #predicting the states
        m_F = np.array([[1,dt],[0,1]])
        m_G = np.array([[0.5 * dt * dt],[dt]]).reshape(2,1)
        new_v_X = m_F.dot(self.v_X) 
        new_m_P = np.add((m_F.dot(self.m_P)).dot(m_F.T),m_G.dot(m_G.T) * self.v_acc_var)

        self.v_X = new_v_X
        self.m_P = new_m_P

    
    def update(self,x_m,R_m):
        #updating the estimates
        z = np.array([x_m,0]).reshape(2,1)
        m_H = np.array([[1,0],[0,0]])
        e = np.add(z,-m_H.dot(self.v_X))
        S = np.add((m_H).dot(self.m_P).dot(m_H.T),R_m)

        L = (self.m_P.dot(m_H.T)).dot(np.linalg.inv(S))

        new_v_X_1 = np.add(self.v_X,L.dot(e))
        new_m_P_1 = (np.add(np.eye(2),-L.dot(m_H))).dot(self.m_P)

        self.v_X = new_v_X_1
        self.m_P = new_m_P_1

# initialising the class

kf = KF(0,float(input('Enter initial velocity: ')),1,float(input('Enter initial covariance: ')),float(input('Enter amplitude: ')))
DT = 0.1
NUM_STEPS = 63*4
R_m = np.array([[0.01,0],[0,0.01]])

# plotting the original trajectories

t = np.arange(0,8*np.pi,0.1)
x_m = np.sin(t)*kf.amp
x_m_e = (np.sin(t) + np.random.normal(scale = 0.07, size = len(t)))*kf.amp
plt.plot(t,x_m)
plt.title('Expected Trajectory')
plt.xlabel('time step')
plt.ylabel('position')
plt.show()

# calculating the estimates

mean = []
cov = []


for i in range(NUM_STEPS):
    kf.predict(DT)
    kf.update(x_m_e[i],R_m)
    mean.append(kf.v_X)
    cov.append(kf.m_P.trace()/2.0)

#plotting the curves

plt.plot(t,x_m_e)
plt.title('measurements')
plt.xlabel('time step')
plt.ylabel('position')
plt.show()

plt.plot(t,list(zip(*mean))[0])
plt.plot(t,list(zip(*mean))[1])
plt.title('State estimates')
plt.legend(['position','velocity'],loc = 'upper right')
plt.xlabel('time step')
plt.ylabel('state ')
plt.show()

plt.plot(t,cov)
plt.title('covariance')
plt.xlabel('time step')
plt.ylabel('covariance')
plt.show()

plt.tight_layout() 