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

def getFile(directory, fileNumber):
    files = getAllFiles('build_cmake/experiments')
    file = files[fileNumber]
    return file

def varsFromFile(fileNumber):
    file = getFile('build_cmake/experiments',fileNumber)
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


vars = varsFromFile(1)
print (vars[0])
