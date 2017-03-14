import os
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab

def getAllFiles():
    directory = 'build_cmake/experiments'
    files = os.listdir(directory)
    return files

def varsFromFile(files, fileNumber):
    file = files[fileNumber]
    rest_pos = 9
    fric_pos = file.find('fric')
    tilt_pos = file.find('tilt')
    mass_pos = file.find('mass')
    end_pos = file.find('.txt')
    rest = float(file[rest_pos:fric_pos])
    fric = float(file[fric_pos+5:tilt_pos])
    tilt = float(file[tilt_pos+4:mass_pos])
    mass = float(file[mass_pos+4:end_pos])
    return (rest,fric,tilt,mass)

def loadData(files, fileNumber):
    directory = 'build_cmake/experiments'
    file = files[fileNumber]
    data = np.zeros((1000,10))
    count = 0
    with open(directory + '/' + file, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if (count==1000):
                break
            for i in range(10):
                data[count][i] = float(row[i])
            count+=1
    return data

def Data(start,end):
    train = np.zeros((end-start,1000,10))
    files = getAllFiles()
    vars = varsFromFile(files,1)
    for i in range(end-start):
        print (i)
        train[i,:,:] = loadData(files,start+i)
    return train

def plot(fileNumber, files, every=1):
    file = files[fileNumber]
    x = []
    y = []
    z = []
    count = 0
    with open('build_cmake/experiments/' + file, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            count += 1
            if count==every:
                x.append(float(row[0]))
                y.append(float(row[1]))
                z.append(float(row[2]))
                count = 0

    colors = cm.rainbow(np.linspace(0, 1, len(x)))
    fig = plt.figure()
    ax = plt.axes(projection='3d')



    ax.scatter(x, y, z, c=colors)
    pylab.show()

    fig2 = plt.figure()
    ax = plt.axes()
    ax.scatter(x,y,c=colors)
    pylab.show()

#files = getAllFiles()
#plot(110, files, every=5)
