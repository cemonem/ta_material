import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from hw2soln import *
import pickle

def plot_bot(q):
    SIZE = 0.3
    pts = np.array([[-1,1],[-1,-1],[1,0]]).T
    pts = SIZE*pts
    rotmat=np.array([[np.cos(q[2]),-np.sin(q[2])],\
                     [np.sin(q[2]),np.cos(q[2])]])
    pts = rotmat.dot(pts)

    pts[0,:] = pts[0,:]+q[0]
    pts[1,:] = pts[1,:]+q[1]
    plt.gca().add_patch(plt.Polygon(pts.T,color='g'))
    
if __name__=="__main__":


    
    with open('ceng.dat','rb') as f:
        ceng = pickle.load(f)
        
    ceng = 0.1*ceng #scale it down, too big :)
    
    #interpolated pts for the path
    NUM_INTERPOLATIONS = 3
    
    pt_ind = np.mgrid[0:len(ceng)*(NUM_INTERPOLATIONS+1):(NUM_INTERPOLATIONS+1)]
    fceng = interp1d(pt_ind,ceng.T)
    ceng2 = fceng(np.mgrid[0:len(ceng)*(NUM_INTERPOLATIONS+1)-NUM_INTERPOLATIONS]).T
    
    plt.plot(ceng2[:,0],ceng2[:,1],'-x')
    
    # some values to play with
    q_init = np.array([4.,14.,0])
    goal = np.array([5.,5.])
    K_pv = 0.5
    K_pth = 4
    t_eval = np.mgrid[0:1000:0.04]
    d = 0.01
    
    #you can put rtol,atol if needed
    #options = {'rtol':1e-10}
    options = {}
    
    # first task
    #(t,q,bunch) = simulate_moving_to_a_point(q_init, goal, K_pv, K_pth, t_eval, d, options)
    
    # second task
    (t,q,inds,bunches) = simulate_moving_with_a_trajectory(q_init, ceng2, K_pv, K_pth, t_eval, d, options)
    
    
    plt.plot(q[0,:], q[1,:])
    for a in q[:,0::1000].T:
        plot_bot(a)
    plt.axis('equal')
    plt.title(f'K_ptv = {K_pth}, K_pv = {K_pv}')
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.show()
