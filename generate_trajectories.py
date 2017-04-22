import numpy as np
from api import *
import tensorflow as tf
import math

def sigmoid(z):
    s = 1.0 / (1.0 + np.exp(-1.0*z))
    return s

def relu(z):
    for i in range(len(z)):
        z[i] = max(0,z[i])
    return z

def iterate_nn(input):
    h = relu(np.dot(input,w_h))
    h2 = relu(np.dot(h, w_h2))
    #h3 = relu(np.dot(h2, w_h3))
    #h4 = relu(np.dot(h3, w_h4))
    output = np.dot(h2, w_h3)
    return output

def update_traj(current, next_point):
    num_of_points = int((len(current) - 4)/6)
    for i in range(num_of_points - 1):
        current[i*6:(i+1)*6] = current[(i+1)*6:(i+2)*6]
    current[(num_of_points-1)*6:num_of_points*6] = next_point
    return current

def getPoint(filename, length):
    count = 0
    data = np.zeros((6,length))
    output = []
    print (filename)
    with open('build_cmake/' + folder + '/' + filename, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if count < length:
                data[0,count] = float(row[0])
                data[1,count] = float(row[1])
                data[2,count] = float(row[2])
                data[3,count] = float(row[3])
                data[4,count] = float(row[4])
                data[5,count] = float(row[5])
                count += 1
            else:
                for i in range(length):
                    for j in range(6):
                        output.append(float(data[j,i]))
                for i in range(4):
                    output.append(float(row[i+6]))
                return output


w_h = np.load('nn_weights/w2_0.npy')
w_h2 = np.load('nn_weights/w2_1.npy')
w_h3 = np.load('nn_weights/w2_2.npy')
#w_h4 = np.load('nn_weights/w_3.npy')
#w_o = np.load('nn_weights/w_4.npy')
file = fileFromVars(0.0, 0.8, 0.8, 0.0, 7)
print (file)
start = getPoint(file,2)
print (start)
data = loadData(0,0,file)
size = 100

colors = cm.rainbow(np.linspace(0, 1, size))
fig = plt.figure()
ax = plt.axes()
ax.scatter(data[:size,0],data[:size,1],c=colors)
pylab.show()



test_data = np.array(start)
colors = cm.rainbow(np.linspace(0, 1, size))
fig = plt.figure()
ax = plt.axes()



# fig2 = plt.figure(num=0)
# ax = plt.axes()
# ax.scatter(x,y,c=colors)
# pylab.show()
x = []
y = []
x.append(start[0])
y.append(start[1])
for i in range(size):
    output = iterate_nn(test_data)
    test_data = update_traj(test_data,output)
    print (output)
    #print (test_data)
    #ax.scatter(output[0], output[1], output[2], c=colors)
    x.append(output[0])
    y.append(output[1])
ax.scatter(x,y,c=colors)
pylab.show()
