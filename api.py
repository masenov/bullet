import os
import csv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab

folder = 'experiments3'

def getAllFiles():
    directory = 'build_cmake/'+folder
    files = os.listdir(directory)
    return files

def varsFromFile(files, fileNumber):
    file = files[fileNumber]
    rest_pos = 9
    fric_pos = file.find('fric')
    tilt_pos = file.find('tilt')
    mass_pos = file.find('mass')
    exp_pos = file.find('exp')
    end_pos = file.find('.txt')
    rest = float(file[rest_pos:fric_pos])
    fric = float(file[fric_pos+5:tilt_pos])
    tilt = float(file[tilt_pos+4:mass_pos])
    #mass = float(file[mass_pos+4:end_pos])
    mass = float(file[mass_pos+4:exp_pos])
    return (rest,fric,tilt,mass)

def fileFromVars(mass, rest, fric, tilt, exp):
   tilt = tilt*45.0
   filename = "data_rest" + str(rest) + "fric_" + str(fric) + "tilt" + str(tilt)+ "mass"+str(mass)+ "exp" + str(exp) + ".txt"
   return filename

def loadData(files, fileNumber, filename=None):
    directory = 'build_cmake/'+folder
    if filename==None:
        file = files[fileNumber]
    else:
        file = filename
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


def startOfFile(filename,start=1):
    count = 0
    data = np.zeros(16)
    with open('build_cmake/' + folder + '/' + filename, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if count<start:
                count += 1
                continue
            data[(count-start)*6:(count-start)*6+6] = row[0:6]
            count += 1
            if count==start+2:
                data[12:16] = row[6:10]
                break
    return data



def plot(fileNumber, files, filename=None, every=1):
    if filename is None:
        file = files[fileNumber]
    else:
        file = filename
    x = []
    y = []
    z = []
    count = 0
    with open('build_cmake' + folder + '/' + file, 'rt') as csvfile:
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
    pylab.show(block=False)
    fig2 = plt.figure(num=0)
    ax = plt.axes()
    ax.scatter(x,y,c=colors)
    pylab.show(block=False)

def clearData():
    with open('data.txt', 'w') as fout:
                    fout.writelines("")



def sequenceData(filename, length):
    count2 = 0
    count = 0
    data = np.zeros((6,length))
    print (filename)
    with open('build_cmake/' + folder + '/' + filename, 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            count2 += 1
            if count < length:
                data[0,count] = float(row[0])
                data[1,count] = float(row[1])
                data[2,count] = float(row[2])
                data[3,count] = float(row[3])
                data[4,count] = float(row[4])
                data[5,count] = float(row[5])
                count += 1
            else:
                with open('data.txt', 'a') as fout:
                    for i in range(length):
                        for j in range(6):
                            fout.writelines(str(data[j,i]) + ', ')
                    for i in range(9):
                        fout.writelines(row[i+6] + ', ')
                    fout.writelines(row[15])
                    fout.writelines('\n')
                data[:,:length-1] = data[:,1:]
                data[0,length-1] = float(row[10])
                data[1,length-1] = float(row[11])
                data[2,length-1] = float(row[12])
                data[3,length-1] = float(row[13])
                data[4,length-1] = float(row[14])
                data[5,length-1] = float(row[15])

def seqData(filename):
    file = filename + '.txt'

    num_lines = sum(1 for line in open(filename + '.txt'))

    with open(filename + '.txt', 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            len_data = len(row)
            break
    print (len_data)
    data = np.zeros((num_lines,len_data))
    count = 0
    with open(filename + '.txt', 'rt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            for i in range(len_data):
                data[count][i] = float(row[i])
            count+=1
    return data


def deteleFiles(files):
    for i in range(10000):
        file = files[i]
        exp_pos = file.find('exp')
        keep_file = file[exp_pos+3]
        if keep_file != '0':
            os.remove('build_cmake/' + folder + '/' + file)

    print (len(files))


# files = getAllFiles()
# print (len(files))
# print (files[0])
# print (varsFromFile(files,0))
# print (fileFromVars(0.1,0.1,0.1,0.7,20))
# #for i in range(0,10):
#     plot(210, files, every=1, filename=fileFromVars(0.1,0.1,0.1,i/10.0))
# clearData()
# for rest in range(0,10):
#     for fric in range(0,10):
#          for tilt in range(0,1):
#              for exp in range(0,100):
#                  sequenceData(fileFromVars(0/10.0,rest/10.0,fric/10.0,tilt/10.0,exp),2)
# data = seqData()
# print (len(data))
