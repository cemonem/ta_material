import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
from rrt_base import GoalBiasedGreedySteerKNeighborhoodRRTStarBase
CIRCLE_OBSTACLES = [(-1,0.5,0.5),(1.0,1.0,0.5),(-0.8,-0.8,1),(1,0,0.6),(1,-1,1)]
CFREE_XY_MIN = -2
CFREE_XY_MAX = 2



class RRTStar2D(GoalBiasedGreedySteerKNeighborhoodRRTStarBase):
    def __init__(self,seed):
        '''Feel free to put additional things here.'''
        GoalBiasedGreedySteerKNeighborhoodRRTStarBase.__init__(self,seed)

    def sample(self, p):
        if not self.is_goal_reachable() and self.random.random_sample() < p:
            return ???
        else:
            return self.random.uniform(low=CFREE_XY_MIN, high=CFREE_XY_MAX, size=(2,))

    def distance(self, c1, c2):
        return np.sqrt(np.sum((c1-c2)**2))

    def valid(self, c):
        for obs in CIRCLE_OBSTACLES:
            if np.sqrt((c[0]-obs[0])**2+(c[1]-obs[1])**2) < obs[2]:
                return False
        return True

    def allclose(self,c1, c2):
        return np.allclose(c1,c2)



if __name__ == "__main__":
    c_init = np.array([0,0])
    c_goal = np.array([0,-1.5])
    p = 0.5
    k = 20
    step_size = 0.1

    rrt = RRTStar2D(460)
    rrt.init_rrt(c_init, c_goal)

    fig, ax = plt.subplots()

    for obs in CIRCLE_OBSTACLES:
        ax.add_patch(plt.Circle((obs[0],obs[1]), radius=obs[2], fc="y"))

    edge_lines = LineCollection([],colors=[(0,0,1)],linewidth=0.5)
    goal_path = LineCollection([],colors=[(1,0,0)])
    simplified_goal_path = LineCollection([],colors=[(0,1,0)])

    ax.add_collection(edge_lines)
    ax.add_collection(goal_path)
    ax.add_collection(simplified_goal_path)
    ax.set_aspect("equal")
    ax.set_xlim(CFREE_XY_MIN, CFREE_XY_MAX)
    ax.set_ylim(CFREE_XY_MIN, CFREE_XY_MAX)
    ax.scatter(c_init[0], c_init[1], facecolor="r")
    ax.scatter(c_goal[0], c_goal[1], facecolor="g")
    title = ax.text(0.5,0.95, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':3},
                transform=ax.transAxes, ha="center")
    paused = False
    def animate(frame_no):
        rrt.add_node(p,k,step_size)
        if rrt.is_goal_reachable():
            goal_edges = rrt.get_path_to_goal()
            goal_path.set_segments(goal_edges)
            simplified_goal_path.set_segments(rrt.simplify_path(goal_edges, step_size))
        edge_lines.set_segments(rrt.get_all_edges())
        title.set_text("p=%s, k=%s, step_size=%s, nodes=%s goal_cost=%.2f"%(p,k,step_size,frame_no+1,rrt.get_goal_cost()))
        return edge_lines,goal_path,title,simplified_goal_path
    #if you want to animate, uncomment (disable offline calculation and plot below first)
    #anim = animation.FuncAnimation(fig, animate,frames=3000, interval=1, blit=True)

    def toggle_pause(self):
        global paused
        paused = not paused
        if paused:
            anim.event_source.stop()
        else:
            anim.event_source.start()

    #fig.canvas.mpl_connect('button_press_event', toggle_pause) if you want to pause in certain situations

    #calculate offline and plot after:
    NUM_NODES = 1000
    for i in range(NUM_NODES):
        rrt.add_node(p,k,step_size)

    edge_lines.set_segments(rrt.get_all_edges())
    goal_edges = rrt.get_path_to_goal()
    goal_path.set_segments(goal_edges)
    simplified_goal_path.set_segments(rrt.simplify_path(goal_edges, step_size))
    title.set_text("p=%s, k=%s, step_size=%s, nodes=%s, goal_cost=%.2f"%(p,k,step_size,NUM_NODES,rrt.get_goal_cost()))
    fig.set_size_inches(8,8)
    plt.show()
