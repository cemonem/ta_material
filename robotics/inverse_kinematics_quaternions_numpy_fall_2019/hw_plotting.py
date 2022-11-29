import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation
from hw3_soln import *
import pickle

def plot_frame(ax3d, tfm_mat, **kwargs):
    
    size = 0.5
    
    x_l = ax3d.quiver(*tfm_mat[0:3,3],*(size*tfm_mat[0:3,0].T), colors=[(1,0,0,1)], **kwargs)
    y_l = ax3d.quiver(*tfm_mat[0:3,3],*(size*tfm_mat[0:3,1].T), colors=[(0,1,0,1)], **kwargs)
    z_l = ax3d.quiver(*tfm_mat[0:3,3],*(size*tfm_mat[0:3,2].T), colors=[(0,0,1,1)], **kwargs)
    
    return (x_l,y_l,z_l)

def update_frame(ax3d, frame, tfm_mat):
    
    for arrow in frame:
        arrow.remove()
    
    return plot_frame(ax3d, tfm_mat)

def plot_leg(ax3d,leg):
    
    rod1 = np.vstack((leg.Tfm_a1[0:3,3],leg.pos_a2)).T
    rod2 = np.vstack((leg.pos_a2,leg.pos_tip)).T

    pos_a1 = [[i] for i in leg.Tfm_a1[0:3,3]]
    pos_a2 = [[i] for i in leg.pos_a2]
    pos_tip = [[i] for i in leg.pos_tip]
    
    a1_frame = plot_frame(ax3d,leg.Tfm_a1)
    a1_center = ax3d.plot(*pos_a1,color=(0.5,0.2,0.5),marker='o')[0]
    l1_line = ax3d.plot(*rod1,color=(0.5,0.2,0,1))[0]
    l2_line = ax3d.plot(*rod2,color=(0.5,0.4,0,1))[0]
    a2_center = ax3d.plot(*pos_a2,color=(0.8,0.5,0.2),marker='o')[0]
    tip_center = ax3d.plot(*pos_tip,color=(0.8,0.2,0.2),marker='o')[0]

    return (a1_frame,a1_center,l1_line,a2_center,l2_line,tip_center)

def update_leg(ax3d, leglines, leg):

    for elem in leglines[1:]:
        elem.remove()

    rod1 = np.vstack((leg.Tfm_a1[0:3,3],leg.pos_a2)).T
    rod2 = np.vstack((leg.pos_a2,leg.pos_tip)).T

    pos_a1 = [[i] for i in leg.Tfm_a1[0:3,3]]
    pos_a2 = [[i] for i in leg.pos_a2]
    pos_tip = [[i] for i in leg.pos_tip]

    
    a1_center = ax3d.plot(*pos_a1,color=(0.5,0.2,0.5),marker='o')[0]
    l1_line = ax3d.plot(*rod1,color=(0.5,0.2,0,1))[0]
    l2_line = ax3d.plot(*rod2,color=(0.5,0.4,0,1))[0]
    a2_center = ax3d.plot(*pos_a2,color=(0.8,0.5,0.2),marker='o')[0]
    tip_center = ax3d.plot(*pos_tip,color=(0.8,0.2,0.2),marker='o')[0]
    
    a1_frame = update_frame(ax3d, leglines[0], leg.Tfm_a1)
    
    return (a1_frame,a1_center,l1_line,a2_center,l2_line,tip_center)

def plot_sphere(ax3d,pt,radius):
    
    u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)*radius+pt[0]
    y = np.sin(u)*np.sin(v)*radius+pt[1]
    z = np.cos(v)*radius+pt[2]
    
    sph = ax3d.plot_surface(x, y, z, color=(0.7,0.7,0.7,0.7))
    
    return sph

def update_sphere(ax3d, sph, pt, radius):
    
    sph.remove()
    
    return plot_sphere(ax3d, pt, radius)

def plot_sphinx(ax3d,sphinx):
    pts = np.asarray([sphinx.p1.Tfm_a1[0:3,3],
                      sphinx.p2.Tfm_a1[0:3,3],
                      sphinx.p3.Tfm_a1[0:3,3]])
    

    
    body = Poly3DCollection([pts])
    body.set_alpha(0.5)
    body.set_edgecolor('k')
    body.set_facecolor('g')
    ax3d.add_collection3d(body)
    
    center = [[i] for i in sphinx.Tfm[0:3,3]]
    body_center = ax3d.plot(*center,color=(0,0.7,0.9),marker='o')[0]
    
    p1_draw = plot_leg(ax3d,sphinx.p1)
    p2_draw = plot_leg(ax3d,sphinx.p2)
    p3_draw = plot_leg(ax3d,sphinx.p3)
    sphinx_frame = plot_frame(ax3d,sphinx.Tfm)
    
    return (body,body_center,p1_draw,p2_draw,p3_draw,sphinx_frame)
    
    

def update_sphinx(ax3d,sphinx_draw,sphinx):
    
    (body,body_center,p1_draw,p2_draw,p3_draw,sphinx_frame) = sphinx_draw
    body.remove()
    body_center.remove()
    
    pts = np.asarray([sphinx.p1.Tfm_a1[0:3,3],
                      sphinx.p2.Tfm_a1[0:3,3],
                      sphinx.p3.Tfm_a1[0:3,3]])
    

    
    body = Poly3DCollection([pts])
    body.set_alpha(0.5)
    body.set_edgecolor('k')
    body.set_facecolor('g')
    ax3d.add_collection3d(body)
    
    center = [[i] for i in sphinx.Tfm[0:3,3]]
    body_center = ax3d.plot(*center,color=(0,0.7,0.9),marker='o')[0]
    
    p1_draw = update_leg(ax3d,p1_draw,sphinx.p1)
    p2_draw = update_leg(ax3d,p2_draw,sphinx.p2)
    p3_draw = update_leg(ax3d,p3_draw,sphinx.p3)
    sphinx_frame = update_frame(ax3d,sphinx_frame,sphinx.Tfm)
    
    return (body,body_center,p1_draw,p2_draw,p3_draw,sphinx_frame)
    

def leg_f_kine_interactive_test():
    
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')

    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_zlim(-3,3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    theta_1 = 0
    theta_2 = 0
    theta_3 = np.pi
    tfm = np.eye(4)
    leg = Leg(tfm,1,theta_1,theta_2,theta_3)
    print(leg.pos_tip,leg.pos_a2,leg.Tfm_a1)
    leglines = plot_leg(ax,leg)
    
    def onpress(event):
        nonlocal theta_1,theta_2,theta_3,leglines,tfm
        #print(type(event.key),event.key)
        tfm = np.copy(tfm)
        if event.key == 'c':
            theta_1 = theta_1+0.05
        elif event.key == 'v':
            theta_2 = theta_2+0.05
        elif event.key == 'b':
            theta_3 = theta_3+0.05
        elif event.key == 'w':
            tfm[0,3] = tfm[0,3]+0.1
        elif event.key == 's':
            tfm[2,3] = tfm[2,3]-0.1
        elif event.key == 'd':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('y',0.01).as_dcm())
        elif event.key == 'a':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('z',0.01).as_dcm())
            
        leg.set_f_kine(theta_1,theta_2,theta_3)
        leg.set_Tfm_a1(tfm)
        leglines= update_leg(ax, leglines, leg)
        fig.canvas.draw()
        fig.canvas.flush_events()
        

    fig.canvas.mpl_connect('key_press_event',onpress)
    plt.show()

def leg_i_kine_interactive_test():
    
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111,projection='3d')
    
    follow_pt = np.array([3,4,12])/13*1.5

    ax.set_xlim(-3,3)
    ax.set_ylim(-3,3)
    ax.set_zlim(-3,3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    tfm = np.eye(4)
    leg = Leg(tfm,1)
    leg.set_i_kine(follow_pt)
    print(leg.pos_tip,leg.pos_a2,leg.Tfm_a1)
    leglines = plot_leg(ax,leg)
    sph = plot_sphere(ax,leg.Tfm_a1[0:3,3],leg.l*2)
    fw_pt = [[i] for i in follow_pt]
    ax.plot(*fw_pt,marker='x')
    
    def onpress(event):
        nonlocal leglines,tfm,sph
        tfm = np.copy(tfm)
        print(type(event.key),event.key)
        if event.key == '8':
            tfm[0,3] = tfm[0,3]+0.1
        elif event.key == '5':
            tfm[0,3] = tfm[0,3]-0.1
        elif event.key == '6':
            tfm[1,3] = tfm[1,3]+0.1
        elif event.key == '4':
            tfm[1,3] = tfm[1,3]-0.1
        elif event.key == '7':
            tfm[2,3] = tfm[2,3]-0.1
        elif event.key == '9':
            tfm[2,3] = tfm[2,3]+0.1
        elif event.key == '1':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('z',0.1).as_dcm())
        elif event.key == '2':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('y',0.1).as_dcm())
        elif event.key == '3':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('x',0.1).as_dcm())
        
        leg.set_Tfm_a1(tfm)
        leg.set_i_kine(follow_pt)

        leglines= update_leg(ax, leglines, leg)
        sph = update_sphere(ax, sph, leg.Tfm_a1[0:3,3],leg.l*2)
        fig.canvas.draw()
        fig.canvas.flush_events()
        

    fig.canvas.mpl_connect('key_press_event',onpress)
    plt.show()
    
def plot_sphinx_test():
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111,projection='3d')
    
    ax.set_xlim(-7.5,7.5)
    ax.set_ylim(-7.5,7.5)
    ax.set_zlim(0,15)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    Tfm = np.eye(4)
    Tfm[0:3,3] = [0,-2,1.5]
    sphinx = Sphinx(Tfm,2,6,1)
    plot_sphinx(ax,sphinx)   
    plt.show()

def move_sphinx_test():
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111,projection='3d')
    
    ax.set_xlim(-7.5,7.5)
    ax.set_ylim(-7.5,7.5)
    ax.set_zlim(0,15)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    Tfm = np.eye(4)
    Tfm[0:3,3] = [0,-2,1.1]
    sphinx = Sphinx(Tfm,2,6,1)
    sphinx_draw = plot_sphinx(ax,sphinx)
    key_frames = []
    
    def onpress(event):
        nonlocal Tfm,sphinx_draw
        tfm = np.copy(Tfm)
        #print(type(event.key),event.key)
        if event.key == '4':
            tfm[0,3] = tfm[0,3]+0.1
        elif event.key == '6':
            tfm[0,3] = tfm[0,3]-0.1
        elif event.key == '8':
            tfm[1,3] = tfm[1,3]+0.1
        elif event.key == '5':
            tfm[1,3] = tfm[1,3]-0.1
        elif event.key == '7':
            tfm[2,3] = tfm[2,3]-0.1
        elif event.key == '9':
            tfm[2,3] = tfm[2,3]+0.1
        elif event.key == '1':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('x',0.01).as_dcm())
        elif event.key == '2':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('y',0.01).as_dcm())
        elif event.key == '3':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('z',0.01).as_dcm())
        elif event.key == 'ctrl+1':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('x',-0.01).as_dcm())
        elif event.key == 'ctrl+2':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('y',-0.01).as_dcm())
        elif event.key == 'ctrl+3':
            tfm[0:3,0:3] = tfm[0:3,0:3].dot(R.from_euler('z',-0.01).as_dcm())
        elif event.key == 'ctrl+5':
            print('current tfm:')
            print(sphinx.Tfm)
        elif event.key == 'ctrl+7':
            print('current tfm,adding to interesting key frames:')
            print(sphinx.Tfm)
            key_frames.append(sphinx.Tfm)
            
        
        if not sphinx.set_Tfm_fixed_legs(tfm):
            print("won't budge! :(")
            print(sphinx.Tfm)
        else:
            Tfm = tfm
            sphinx_draw = update_sphinx(ax,sphinx_draw,sphinx)
            fig.canvas.draw()
            fig.canvas.flush_events()
        
    
    fig.canvas.mpl_connect('key_press_event',onpress)
    plt.show()
    with open('key_frames.dat','wb') as f:
        pickle.dump(key_frames,f)

def sphinx_dance_test():
    
    with open('key_frames.dat','rb') as f:
        key_frames = pickle.load(f)
    
    print(key_frames)

    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111,projection='3d')
    
    frame_count = []
    
    ax.set_xlim(-7.5,7.5)
    ax.set_ylim(-7.5,7.5)
    ax.set_zlim(0,15)
    ax.set_xlabel('x (m)')
    ax.set_ylabel('y (m)')
    ax.set_zlabel('z (m)')
    
    sphinx = Sphinx(key_frames[0],2,6,1)
    
    frames = []
    for i in range(len(key_frames)-1):
        num_betweens = 50
        if i < len(frame_count):
             num_betweens = frame_count[i]
        frames.extend([interpolate_Tfms(key_frames[i],key_frames[i+1],j) for j in np.mgrid[0:1:num_betweens*(1j)]])
    
    sphinx_draw = plot_sphinx(ax,sphinx)
    
    def update(i):
        nonlocal sphinx_draw
        if not sphinx.set_Tfm_fixed_legs(frames[i]):
            print(f"key {i} failed")
        sphinx_draw = update_sphinx(ax,sphinx_draw,sphinx)
    
    ani = FuncAnimation(fig, update,frames = len(frames))
    plt.show()
    #plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
    #ani.save('sphinx_dance.mp4',writer='ffmpeg',fps=30)

if __name__ == "__main__":
    
    #leg_f_kine_interactive_test()
    #leg_i_kine_interactive_test()
    #plot_sphinx_test()
    #move_sphinx_test()
    sphinx_dance_test()
