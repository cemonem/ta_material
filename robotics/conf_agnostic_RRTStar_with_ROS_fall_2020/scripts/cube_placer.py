#!/usr/bin/env python
from ceng460_hw2_environment import *
import ceng460_hw2_utils
import numpy as np
from rrt_base import *

class RRTStar6D(GoalBiasedGreedySteerKNeighborhoodRRTStarBase):

    def __init__(self, seed):
        '''Feel free to put additional things here.'''
        GoalBiasedGreedySteerKNeighborhoodRRTStarBase.__init__(self,seed)
        self.hw2 = Ceng460Hw2Environment()

if __name__=="__main__":
    rrt = RRTStar6D(460)
    rrt.hw2.move_joints((0,-0.3,0,0,0,np.pi/2))
