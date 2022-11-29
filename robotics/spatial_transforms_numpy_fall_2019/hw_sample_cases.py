import numpy as np
from scipy.spatial.transform import Rotation as R

a_init1 = np.eye(4)
a_init1[0:3,0:3] = R.from_euler('y',-np.pi/2).as_dcm()
a_init1[2,3] = -1

a_init2 = np.eye(4)
a_init2[0:3,0:3] = R.from_euler('ZX',[np.pi/2,-np.pi/2]).as_dcm()
a_init2[2,3] = 2
a_init2[1,3] = -2

a_init3 = np.eye(4)
a_init3[0:3,0:3] = R.from_euler('x',np.pi).as_dcm()
a_init3[0,3] = -1
a_init3[1,3] = 2


th1 = np.concatenate((np.mgrid[0:11*np.pi:100j],
                     np.mgrid[11*np.pi:0:100j],
                     np.mgrid[0:11*np.pi:100j],
                     np.mgrid[11*np.pi:0:100j]))

l11 = np.concatenate((np.mgrid[1:5:100j],
                     np.mgrid[5:1:100j],
                     np.mgrid[1:5:100j],
                     np.mgrid[5:1:100j]))

l21 = np.ones(l11.shape[0])
h1 = np.concatenate((np.ones(100),
                    np.ones(50),
                    np.zeros(50),
                    np.ones(100),
                    np.zeros(100)))
h1[100] = 0

inputs1 = np.vstack((l11,l21,th1,h1))



# ~ th2 = np.zeros(th1.shape[0])

th3 = np.zeros(th1.shape[0])
l13 = 1+np.concatenate((np.zeros(150),
                       np.sin(np.mgrid[0:5*np.pi:50j]),
                       np.zeros(150),
                       np.sin(np.mgrid[0:5*np.pi:50j])))
l23 = np.concatenate((np.ones(100),
                     np.mgrid[1:3:50j],
                     np.mgrid[3:1:50j],
                     np.ones(100),
                     np.mgrid[1:3:50j],
                     np.mgrid[3:1:50j],))
h3 = np.concatenate((np.zeros(100),
                    np.zeros(50),
                    np.ones(50),
                    np.zeros(100),
                    np.zeros(50),
                    np.ones(50)))
 
inputs3 = np.vstack((l13,l23,th3,h3))

th2 = np.concatenate((np.mgrid[0:-np.pi:100j],
                     np.mgrid[-np.pi:0:50j],
                     np.zeros(50),
                     np.mgrid[0:-np.pi:100j],
                     np.mgrid[-np.pi:0:50j],
                     np.zeros(50)))
l12 = np.ones(l11.shape[0])
l22 = 2*np.ones(l11.shape[0])
h2 = np.concatenate((np.zeros(100),
                    np.ones(50),
                    np.zeros(50),
                    np.zeros(100),
                    np.ones(50),
                    np.zeros(50)))

inputs2 = np.vstack((l12,l22,th2,h2))

o_init = np.eye(4)
o_init[1,3] = 1

a_init = np.zeros((4,4,3))
a_init[:,:,0] = a_init1
a_init[:,:,1] = a_init2
a_init[:,:,2] = a_init3

inputs = np.zeros((4,l11.shape[0],3))
inputs[:,:,0] = inputs1
inputs[:,:,1] = inputs2
inputs[:,:,2] = inputs3

d = 0.2






