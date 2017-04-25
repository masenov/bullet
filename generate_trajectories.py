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
    for i in range(len(weights)):
        if i == 0:
            h = relu(np.dot(input,weights[i]))
        elif i == len(weights) - 1:
            h = np.dot(h, weights[i])
        else:
            h = relu(np.dot(h,weights[i]))
    return h

def update_traj(current, next_point):
    num_of_points = int((len(current) - 4)/3)
    for i in range(num_of_points - 1):
        current[i*3:(i+1)*3] = current[(i+1)*3:(i+2)*3]
    current[(num_of_points-1)*3:num_of_points*3] = next_point
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

weights = []
for i in range(7):
    w = np.load('nn_weights/w_' + str(i) + '_49000.npy')
    weights.append(w)
file = fileFromVars(0.0, 0.0, 0.0, 0.0, 8)
print (file)
start = getPoint(file,2)
print (start)
data = loadData(0,0,file)
size = 100
#import pdb; pdb.set_trace()
colors = cm.rainbow(np.linspace(0, 1, size))
fig = plt.figure()
ax = plt.axes()
ax.scatter(data[:size,0],data[:size,1],c=colors)
pylab.show()



test_data = np.array(start[3:])
colors = cm.rainbow(np.linspace(0, 1, size))
fig = plt.figure()
ax = plt.axes()

start_x = start[0]
start_y = start[1]

# fig2 = plt.figure(num=0)
# ax = plt.axes()
# ax.scatter(x,y,c=colors)
# pylab.show()
x = []
y = []
#x.append(start[0])
#y.append(start[1])
for i in range(size):
    output = iterate_nn(test_data)
    test_data = update_traj(test_data,output)
    print (output)
    #print (test_data)
    #ax.scatter(output[0], output[1], output[2], c=colors)
    start_x = start_x + output[0]/60.0
    start_y = start_y + output[1]/60.0
    x.append(start_x)
    y.append(start_y)
ax.scatter(x,y,c=colors)
pylab.show()
