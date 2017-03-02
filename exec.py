import os
os.system("echo 'hello world'")
with open('examples/BasicDemo/BasicExample.cpp', 'r') as fin:
    data = fin.read().splitlines(True)
# print (data[0:12])
print (data[13:21])
# print (data[22:])

gTilt = 40
gRampFriction = 0.474
gRampRestitution = 1.2
gBoxFriction = 1.3
gBoxRestitution = 1
gSphereFriction = 1
gSphereRollingFriction = 0.368
gSphereRestitution = 1.5


variables = ['static btScalar gTilt = ' + str(gTilt) + '.0f/180.0f*SIMD_PI; // tilt the ramp 20 degrees\n', 'static btScalar gRampFriction = ' + str(gRampFriction) + '; // set ramp friction to 1\n', 'static btScalar gRampRestitution = ' + str(gRampRestitution) + '; // set ramp restitution to 0 (no restitution)\n', 'static btScalar gBoxFriction = ' + str(gBoxFriction) + '; // set box friction to 1\n', 'static btScalar gBoxRestitution = ' + str(gBoxRestitution) + '; // set box restitution to 0\n', 'static btScalar gSphereFriction = ' + str(gSphereFriction) + '; // set sphere friction to 1\n', 'static btScalar gSphereRollingFriction =' + str(gSphereRollingFriction) + '; // set sphere rolling friction to 1\n', 'static btScalar gSphereRestitution = ' + str(gSphereRestitution) + '; // set sphere restitution to 0\n','\n']

print (variables)
with open('examples/BasicDemo/BasicExample.cpp', 'w') as fout:
    fout.writelines(data[0:12])
    fout.writelines(variables)
    fout.writelines(data[20:])

#os.system("./basedemo.sh")
import subprocess
import time
argument = '...'
proc = subprocess.Popen(['./basedemo.sh', '', argument], shell=True)
time.sleep(7) # <-- There's no time.wait, but time.sleep.
pid = proc.pid # <--- access `pid` attribute to get the pid of the child process.
proc.terminate()


import psutil

PROCNAME = "AppBasicExampleGui"

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()
