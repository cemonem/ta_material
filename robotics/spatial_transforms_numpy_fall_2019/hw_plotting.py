import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from hw1_sample_cases import *
from hw1_soln import *
from matplotlib.animation import FuncAnimation

def plot_frame(ax3d, tfm_mat, **kwargs):
    
    size = 0.2
    
    x_l = ax3d.quiver(*tfm_mat[0:3,3],*(size*tfm_mat[0:3,0].T), colors=[(1,0,0,1)], **kwargs)
    y_l = ax3d.quiver(*tfm_mat[0:3,3],*(size*tfm_mat[0:3,1].T), colors=[(0,1,0,1)], **kwargs)
    z_l = ax3d.quiver(*tfm_mat[0:3,3],*(size*tfm_mat[0:3,2].T), colors=[(0,0,1,1)], **kwargs)
    
    return (x_l,y_l,z_l)

def update_frame(ax3d, frame, tfm_mat):
    
    for arrow in frame:
        arrow.remove()
    
    return plot_frame(ax3d, tfm_mat)
    

def plot_object(ax3d, tfm_mat, **kwargs):
    
    
    size = 0.5
    
    pts = size*np.asarray([[0.5,0.5,-0.5],
                           [-0.5,0.5,-0.5],
                           [-0.5,-0.5,-0.5],
                           [0.5,-0.5,-0.5],
                           [0,0,0.5]])
    
    pts = (tfm_mat[0:3,0:3].dot(pts.T)).T+tfm_mat[0:3,3]
    
    faces = [[0,1,2,3],[0,1,4],[1,2,4],[2,3,4],[3,0,4]]
    
    face1 = Poly3DCollection([pts[faces[0],:]])
    face1.set_edgecolor('k')
    face1.set_facecolor('m')
    ax3d.add_collection3d(face1)

    face2 = Poly3DCollection([pts[faces[1],:]])
    face2.set_edgecolor('k')
    face2.set_facecolor('c')
    ax3d.add_collection3d(face2)

    face3 = Poly3DCollection([pts[faces[2],:]])
    face3.set_edgecolor('k')
    face3.set_facecolor('y')
    ax3d.add_collection3d(face3)

    face4 = Poly3DCollection([pts[faces[3],:]])
    face4.set_edgecolor('k')
    face4.set_facecolor('k')
    ax3d.add_collection3d(face4)

    face5 = Poly3DCollection([pts[faces[4],:]])
    face5.set_edgecolor('k')
    face5.set_facecolor('w')
    ax3d.add_collection3d(face5)
    
    return (face1,face2,face3,face4,face5)

def update_object(ax3d, obj, tfm_mat):
    
    for face in obj:
        face.remove()
    
    return plot_object(ax3d, tfm_mat)

def plot_sphere(ax3d,pt,radius):
    
    u, v = np.mgrid[0:2*np.pi:10j, 0:np.pi:10j]
    x = np.cos(u)*np.sin(v)*radius+pt[0]
    y = np.sin(u)*np.sin(v)*radius+pt[1]
    z = np.cos(v)*radius+pt[2]
    
    sph = ax3d.plot_surface(x, y, z, color=(0.7,0.7,0.7,0.7))
    
    return sph

def update_sphere(ax3d, sph, pt, radius):
    
    sph.remove()
    
    return plot_sphere(ax3d, pt, radius)

def plot_arm(ax3d,M1,M12,M2,h,d,grabbing):
    
    sph = None
    rod1 = np.vstack((M1[0:3,3],M12[0:3,3])).T
    rod2 = np.vstack((M12[0:3,3],M2[0:3,3])).T
    rod1_l = ax3d.plot(*rod1,color=(0.6,0.4,0,1))[0]
    
    if grabbing:
        rod2_l = ax3d.plot(*rod2,color=(0.7,0.5,0.2,1))[0]
    else:
        rod2_l = ax3d.plot(*rod2,color=(0.3,0.6,0.6,1))[0]

    
    f1 = plot_frame(ax,M1)
    f12 = plot_frame(ax,M12)
    f2 = plot_frame(ax,M2)
    
    if h:
        sph = plot_sphere(ax3d, M2[0:3,3], d)

    return (rod1_l,rod2_l,f1,f12,f2,sph)

def update_arm(ax3d,arm,M1,M12,M2,h,d,grabbing):
    
    rod1_l,rod2_l,f1,f12,f2,sph = arm
    
    rod1 = np.vstack((M1[0:3,3],M12[0:3,3])).T
    rod2 = np.vstack((M12[0:3,3],M2[0:3,3])).T
    
    rod1_l.remove()
    rod2_l.remove()
    rod1_l = ax3d.plot(*rod1,color=(0.6,0.4,0,1),lw=3)[0]
    
    if grabbing:
        rod2_l = ax3d.plot(*rod2,color=(0.9,0.8,0,1),lw=3)[0]
    else:
        
        rod2_l = ax3d.plot(*rod2,color=(0.3,0.7,0.3),lw=3)[0]
    
    f1 = update_frame(ax3d,f1,M1)
    f12 = update_frame(ax3d,f12,M12)
    f2 = update_frame(ax3d,f2,M2)
    
    if sph:
        sph.remove()
        sph = None
    
    if h:
        sph = plot_sphere(ax3d, M2[0:3,3], d)
    
    return (rod1_l,rod2_l,f1,f12,f2,sph)


def plot_simulation(fig, ax3d, a_init, inputs, d, o_all, M12_all, M2_all, parent_all):
    
    arms = [plot_arm(ax3d,a_init[:,:,i],M12_all[:,:,0,i],M2_all[:,:,0,i],inputs[3,0,i],d,False) for i in range(M12_all.shape[-1])]
    obj = plot_object(ax3d, o_all[:,:,0])
    obj_tr = ax3d.plot([],[],[],color=(0,0,0),lw=0.5)[0]
    
    def update(t):
        nonlocal arms, obj,obj_tr,d
        for i in range(M12_all.shape[-1]):
            
            arms[i] = update_arm(ax3d,arms[i],a_init[:,:,i],M12_all[:,:,t,i],M2_all[:,:,t,i],inputs[3,t,i],d,parent_all[t] == i)
        
        obj = update_object(ax3d, obj, o_all[:,:,t])
        obj_tr.set_data_3d(o_all[0,3,0:t],o_all[1,3,0:t],o_all[2,3,0:t])
    
    return FuncAnimation(fig, update, frames=range(M12_all.shape[-2]))

if __name__ == "__main__":
    
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111,projection='3d')
    
    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    
    globalf = np.eye(4)
    globalf[0:3,3] = [3,3,3]
    
    plot_frame(ax,globalf)
    
    
    
    (o_all,M12_all,M2_all,parent_all) = simulate(o_init,a_init,inputs,d)
    
    
    
    ani = plot_simulation(fig,ax,a_init,inputs,d,o_all,M12_all,M2_all,parent_all)
    #plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
    #ani.save('hw1_sample.mp4',writer='ffmpeg')
    plt.show()
    
