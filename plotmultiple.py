import csv
import pylab
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

colors = cm.rainbow(np.linspace(0, 1,10))
fig2 = plt.figure()
ax = plt.axes()
for i in range(10):
    x = []
    y = []
    z = []
    with open('build_cmake/experiments/data'+str(i)+'.txt', 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))


    ax.scatter(x,y,c=colors[i])
pylab.show()
