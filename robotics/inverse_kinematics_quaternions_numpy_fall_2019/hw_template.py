import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt

# Use numpy arrays for matrices and vectors unless indicated otherwise!
# All angles are in radians.

class Leg:
    def __init__(self,Tfm_init, l, theta_1 = 0, theta_2 = 0, theta_3 = np.pi):
        '''
        constructor for the class.
        Tfm_init is the initial global transform of joint a1 of shape (4,4).
        l is the length of the links l1,l2.
        theta_n are the initial joint angles in the leg.
        '''
        self.l = l
        self.Tfm_a1 = Tfm_init
        self.pos_a2 = None #position vector of knee joint (a2) of shape (3,). 
        self.pos_tip = None #position vector of the tip of shape (3,).
        self.set_f_kine(theta_1, theta_2, theta_3)
        
        #update all of these fields in the setters below
        #return a bool indicating whether the update is successful.
        
    def set_Tfm_a1(self, Tfm_a1):
        '''
        changes the transformation of the base of the leg, keeps
        the joint angles constant. 
        Tfm_a1 is the new global transform of the joint a1.
        Always returns True.
        '''
        return True
        
    def set_f_kine(self, theta_1, theta_2, theta_3):
        '''
        updates the positions and transformations according to the
        new angles and the transform of the base joint. 
        Always returns True.
        '''
        return True
        
    def set_i_kine(self, pos_tip):
        '''
        updates the angles so that the tip points to pos_tip of shape (3,).
        if this is not achievable, does nothing and returns false.
        returns true otherwise.
        '''
        if self.is_reachable(pos_tip):
            self.set_f_kine(*self.i_kine(pos_tip))
            return True
        else:
            return False
    
    def is_reachable(self, pos_tip):
        '''
        returns True if pos_tip is reachable by the leg tip. returns
        False otherwise.
        See set_i_kine.
        '''
        return False
    
    def i_kine(self, pos_tip):
        '''
        calculates inverse kinematics for the leg.
        See set_i_kine.
        '''
        return (theta_1,theta_2,theta_3)


class Sphinx:

    def __init__(self, Tfm_init,d1,d2,l):
        '''
        constructor for the sphinx.
        Tfm_init is the initial global transform of the body.
        d1,d2 are the parameters of the body.
        l is the link lengths for the legs.
        
        Initialize with tip of the legs fixed at global z = 0 and
        their global x,y are the same as their base joint (the a1 joint)
        Tfm_init will be given such that this is guaranteed to be
        achievable.
        '''
        
        self.Tfm = Tfm_init
        self.d1 = d1
        self.d2 = d2
        self.l = l
        
        self.p1 = None # The fields for the legs. All of them are Leg objects. Initialize them accordingly.
        self.p2 = None
        self.p3 = None
    
    def set_Tfm_fixed_legs(self, Tfm):
        '''
        Tfm is the proposed transform of the body with shape (4,4).
        
        updates the positions and transformations of the legs and body
        according to the new global Tfm, while keeping leg tips fixed on the
        ground, without violating joint constraints. If this is achievable,
        returns True and updates the relevant fields. Otherwise, keeps
        the relevant fields as is and returns False.
        '''
        return False
        
def quaternion_slerp(quat_1,quat_2,alpha):
    '''
    quot_1,quot_2 are quoternions w<a,b,c> represented as numpy arrays [w,a,b,c] with shape (4,)
    alpha is the interpolation value, an np.double taking values between 0 and 1.
    
    returns the quoternion interpolation of quat_1 and quat_2
    if alpha == 0, this function returns quat_1,
    if alpha == 1, this function returns quat_2.
    '''
    pass

def position_lerp(pos_1,pos_2,alpha):
    '''
    returns the linear interpolation between pos_1,pos_2 of size (3,).
    alpha is the interpolation value, an np.double taking values between 0 and 1.
    if alpha == 0, this function returns pos_1,
    if alpha == 1, this function returns pos_2.
    '''
    pass

def interpolate_Tfms(Tfm_1,Tfm_2,alpha):
    '''
    returns the simultaneous positional and orientational interpolation between Tfm_1,Tfm_2 of size (4,4).
    alpha is the interpolation value, an np.double taking values between 0 and 1.
    if alpha == 0, this function returns Tfm_1,
    if alpha == 1, this function returns Tfm_2.
    '''
    pass
    



	
