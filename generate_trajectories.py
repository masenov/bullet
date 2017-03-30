import numpy as np
from api import *
import tensorflow as tf
import math

def sigmoid(z):
    s = 1.0 / (1.0 + np.exp(-1.0*z))
    return s

def iterate_nn(input):
    test_data = np.array(data[9002,:34])
    h = sigmoid(np.dot(input,w_h))
    h2 = sigmoid(np.dot(h, w_h2))
    output = np.dot(h2, w_o)
    return output

def update_traj(current, next_point):
    num_of_points = int((len(current) - 4)/3)
    print (num_of_points)
    for i in range(num_of_points - 1):
        current[i*3:(i+1)*3] = current[(i+1)*3:(i+2)*3]
    current[(num_of_points-1)*3:num_of_points*3] = next_point
    return current



w_h = np.load('w_h.npy')
w_h2 = np.load('w_h2.npy')
w_o = np.load('w_o.npy')

data = seqData()
test_data = np.array(data[9002,:34])

colors = cm.rainbow(np.linspace(0, 1, len(x)))
fig = plt.figure()
ax = plt.axes(projection='3d')



# fig2 = plt.figure(num=0)
# ax = plt.axes()
# ax.scatter(x,y,c=colors)
# pylab.show()
# for i in range(100):
    output = iterate_nn(test_data)
    test_data = update_traj(test_data,output)
    print (test_data)
    ax.scatter(output[0], output[1], output[2], c=colors)
pylab.show()
