import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def simulate_moving_to_a_point(q_init, goal, K_pv, K_pth, t_eval, d, options):
    
    """
    Simulates a differential drive moving toward a point with P control.
    
    Parameters:
        q_init(np.ndarray): initial state [x y theta] of the robot.
        goal(np.ndarray): goal point [x y].
        K_pv(np.double): velocity gain.
        K_pth(np.double): steering gain.
        t_eval(np.ndarray): the time instances to be solved by solver. has shape (n,).
            d(np.double): the simulation should terminate if the distance of
            the robot to the goal is less than this value.
        options(dict): options for the solver. Directly pass it as keyword args.
    Returns:
        t(np.ndarray): solved time instances. This should be the same as t_eval
        unless the simulation is terminated by an event function. has shape (m,).
        q(np.ndarray):robot pose solutions for each element of t. has shape (3,m).
        bunch(scipy.integrate._ivp.ivp.OdeResult): bunch object returned by the solver.
    
    """
    
    
    def diffeqn(t,q):
        return dq
    
    def term_event(t,q):
        return np.linalg.norm(q[0:2]-goal) - d
    
    term_event.terminal = True
    term_event.direction = -1
    
    bunch = solve_ivp(diffeqn, t_eval[[0,-1]], q_init, t_eval=t_eval, events=[term_event],**options)
    t = bunch.t
    q = bunch.y[0:3,:]
    
    return (t,q,bunch)
    
def simulate_moving_with_a_trajectory(q_init, goal_pts, K_pv, K_pth, t_eval, d, options):
    """
    Simulates a differential drive moving with a trajectory with P control.
    
    Parameters:
        q_init(np.ndarray): initial state [x y theta] of the robot.
        goal_pts(np.ndarray): goal points with rows [x y]. has shape (l,2).
        K_pv(np.double): velocity gain.
        K_pth(np.double): steering gain.
        t_eval(np.ndarray): the time instances to be solved by solver. has shape (n,).
        d(np.double): the partial simulation should terminate for the current 
            goal point if the distance of the robot to the goal is less than this value.
            Then it should restart with the next point as the goal point in goal_pts. 
            If this was the last point, the simulation should truly terminate.
        options(dict): options for the solver. Directly pass it as keyword args.
    Returns:
        t(np.ndarray): solved time instances. This should be the same as t_eval
        unless the robot reaches the last point earlier than t_eval[-1]. has shape (m,).
        q(np.ndarray):robot pose solutions for each element of t. has shape (3,m).
        inds(np.ndarray): the index of the current goal in goal_pts at that time instance.
            has shape (m,).
        bunches(list): All bunch objects returned along with the partial solutions.
    
    """    
    return (t,q,inds,bunches)
    
