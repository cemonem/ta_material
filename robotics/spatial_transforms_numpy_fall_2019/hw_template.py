import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

def simulate(o_init, a_init, inputs, d):
    """
    Simulates the arms.
    
    Parameters:
        o_init (np.ndarray): A 4 x 4 transformation matrix describing 
        the state of o relative to global frame.
        
        a_init (np.ndarray): A 4 x 4 x n_r matrix. Each a_init[:, :, i] 
        is a 4 x 4 transformation of the free end of rod_1 relative to
        global frame. (M1 in the Figure 1 of assignment text.)
        
        inputs(np.ndarray): A 4 x m x n_r matrix. Each inputs[:,:,i]
        is a 4 x m matrix describing l1,l2,theta and h of arm i, 
        during time steps 0..m-1. inputs[:,j,i] corresponds to a column
        vector [l1[j],l2[j],theta[j],h[j]] for time step j for arm i.
        theta is in radians.
        
        d (np.double): The radius of the sphere at the free end of rod_2.
        
    Returns:
        o_all (np.nd.array): A 4 x 4 x m matrix. Each o_all[:,:,i] is a
        4 x 4 transform of the o relative to global frame at time step i
        
        M12_all (np.nd_array): A 4 x 4 x m x n_r matrix. Each M12_all[:,:,i,j]
        is a 4 x 4 transform of M12 relative to global frame (defined
        in the assignment text) at time step i for arm j
        
        M2_all (np.nd_array): A 4 x 4 x m x n_r matrix. Each M2_all[:,:,i,j]
        is a 4 x 4 transform of M2 relative to global frame (defined
        in the assignment text) at time step i for arm j
        
        parent_all (np.nd_array): A 1xm array indicating which arm is
        grabbing o. parent_all[i] = j if arm j is grabbing the object at
        time step i. If o is not being grabbed by any arm at i,
        parent_all[i] = -1.
        
    """
    
    return (o_all, M12_all, M2_all, parent_all)

def T_1(l1):
    """
    Returns:
    tfm_mat (np.ndarray): T_1 in the assignment, Theory-a part.
    """
    
    return tfm_mat

def T_2(l2,theta):
    """
    Returns:
    tfm_mat (np.ndarray): T_2 in the assignment, Theory-a part.
    theta is in radians.
    """
    
    return tfm_mat

def T_3(l1,l2,theta):
    """
    Returns:
    tfm_mat (np.ndarray): T_3 in the assignment, Theory-a part.
    theta is in radians.
    """
    
    return tfm_mat


