import os
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab

def getAllFiles(directory):
    files = os.listdir(directory)
    return files

def getFile(files, fileNumber):
    file = files[fileNumber]
    return file

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
    files = getAllFiles('build_cmake/experiments')
    vars = varsFromFile(files,1)
    for i in range(end-start):
        train[i,:,:] = loadData(files,start+i)
    return train

