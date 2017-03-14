import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import pylab


def plot(file,files):
    file = 'data_rest0.0fric_0.0tilt0.0mass0.0'
    x = []
    y = []
    z = []
    with open('build_cmake/experiments/' + file + '.txt', 'rt') as csvfile:
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

plot(2,# 2)
