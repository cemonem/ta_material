import numpy as np

class GoalBiasedGreedySteerKNeighborhoodRRTStarBase:
    def __init__(self, seed):
        '''Constructor with seed, to be supplied to the np.random.RandomState object held inside. Feel free to add things.'''
        self.random = np.random.RandomState(seed)
    def distance(self, c1, c2):
        '''returns the distance between two configurations c1, c2.'''
        pass
    def steer(self, c0, c, step_size):
        '''starting from the configuration c0, gets closer to
        c in discrete steps of size step_size in terms of distance(c0, c). returns the last no-collision
        configuration. If no collisions are hit during steering, returns c2. If
        steering is not possible at all, returns None.'''
        pass
    def allclose(self, c1, c2):
        '''returns True if two configurations are numerically very close (just use np.allclose default values).'''
        pass

    def sample(self, p):
        '''either returns goal configuration with some goal bias probability p or returns
        a no collision configuration sample with 1-p. The goal bias becomes 0 as soon as goal node is found.'''
        pass
    def neighborhood(self, c, k):
        '''returns a list of k closest nodes to configuration c in terms of distance(q.value, c)'''
        pass

    def init_rrt(self, c_init, c_goal):
        '''initializes/resets rrt with the root node holding c_init and goal configuration c_goal.'''
        pass
    def valid(self, c):
        '''returns True if configuration c is non-colliding.'''
        pass
    def collision_free(self, c1, c2, step_size):
        '''returns True if the linear trajectory between c1 and c2 are collision free.'''
        pass
    def add_node(self, p, k, step_size):
        '''adds a node to the rrt with goal bias probability p, near function with k closest neighbors,
        and step_size for greedy steering. returns the new configuration that is now part of the tree.'''
        pass
    def get_path_to_goal(self):
        '''returns the path to goal node as a list of tuples of configurations[(c_init, c1),(c1, c2),...,(cn,c_goal)].
        If the goal is not reachable yet, returns None.'''
        pass

    def is_goal_reachable(self):
        '''returns True if goal configuration is reachable.'''
        pass

    def simplify_path(self, path, step_size):
        '''greedily removes redundant edges from a configuration path represented as a list of tuples
        of configurations [(c_init,c1),(c1,c2),(c2,c3)...(cn,c_goal)], as described
        Principles of Robot Motion, Theory, Algorithms and Implementations (2005), p. 213,
        Figure 7.7.(use the default version, always try to connect to c_goal, not the other way around'''
        pass


    def get_all_edges(self):
        '''returns all of the edges in the tree as a list of tuples of configurations [(c1,c2),(c3,c4)...]. The
        order of the edges, The order of edges in the list and their direction is not important.'''
        pass

    def get_goal_cost(self):
        '''returns the non-simplified goal path length in terms of distance. Returns np.Inf if goal is not reachable.'''
        pass
