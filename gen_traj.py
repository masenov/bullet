import numpy as np
import math
from api import *

def relu(x):
    for i in range(len(x)):
        x[i] = np.max((0.0,x[i]))
    return x

def iterate_nn(input):
    h = relu(np.dot(input,w_h))
    h2 = relu(np.dot(h, w_h2))
    h3 = relu(np.dot(h2, w_h3))
    h4 = relu(np.dot(h3, w_h4))
    h5 = relu(np.dot(h4, w_h5))
    output = np.dot(h5, w_o)
    return output

w_h = np.load('1000_225/1w_h_303.npy')
w_h2 = np.load('1000_225/1w_h2_303.npy')
w_h3 = np.load('1000_225/1w_h3_303.npy')
w_h4 = np.load('1000_225/1w_h4_303.npy')
w_h5 = np.load('1000_225/1w_h5_303.npy')
w_o = np.load('1000_225/1w_o_303.npy')


print (w_h)
files = getAllFiles()
filename =fileFromVars(0.0,0.8,0.8,0.0,2)
input = startOfFile(filename,start=4)
iterations = 100
traj = np.zeros((iterations,3))
colors = cm.rainbow(np.linspace(0, 1, iterations))
for i in range(iterations):
    output = iterate_nn(input)
    traj[i,:] = output[:3]
    input[0:6] = input[6:12]
    input[6:12] = output

plot(210, files, filename)
fig1 = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter(traj[:,0],traj[:,1],traj[:,2],c=colors)
pylab.show(block=False)

fig2 = plt.figure()
ax = plt.axes()
ax.scatter(traj[:,0],traj[:,1],c=colors)
pylab.show(block=True)


