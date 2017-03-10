import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab

x = []
y = []
z = []
with open('build_cmake/experiments/data_rest0.0fric_0.0tilt18.0mass0.0.txt', 'rt') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        x.append(float(row[0]))
        y.append(float(row[1]))
        z.append(float(row[2]))

colors = cm.rainbow(np.linspace(0, 1, len(x)))
fig = plt.figure()
ax = plt.axes(projection='3d')



ax.scatter(x, y, z, c=colors)
pylab.show()

fig2 = plt.figure()
ax = plt.axes()
ax.scatter(x,y,c=colors)
pylab.show()
