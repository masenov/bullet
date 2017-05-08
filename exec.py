import os
os.system("echo 'hello world'")
with open('examples/BasicDemo/BasicExample.cpp', 'r') as fin:
    data = fin.read().splitlines(True)
# print (data[0:12])
print (data[13:21])
# print (data[22:])

gTilt = 20
gRampFriction = 0.474
gRampRestitution = 1.2
gBoxFriction = 1.3
gBoxRestitution = 1
gSphereFriction = 1
gSphereRollingFriction = 0.368
gSphereRestitution = 1.5

for i in range(0,1):
    for mass in range(0,1):
        for rest in range(25,50):
            for fric in range(0,50):
                for tilt in range(0,50):
                    gRampRestitution = rest/50.0
                    gSphereRestitution = rest/50.0
                    gRampFriction = fric/50.0
                    gSphereFriction = fric/50.0
                    gTilt = tilt/50.0*45.0
                    sphereMass = mass/10.0
                    filename = "experiments5/data_rest" + str(gRampRestitution) + "fric_" + str(gRampFriction) + "tilt" + str(gTilt)+ "mass"+str(sphereMass)+"exp"+str(i)+".txt"

                    variables = ['static btScalar gTilt = ' + str(gTilt) + 'f/180.0f*SIMD_PI; // tilt the ramp 20 degrees\n', 'static btScalar gRampFriction = ' + str(gRampFriction) + '; // set ramp friction to 1\n', 'static btScalar gRampRestitution = ' + str(gRampRestitution) + '; // set ramp restitution to 0 (no restitution)\n', 'static btScalar gSphereFriction = ' + str(gSphereFriction) + '; // set sphere friction to 1\n', 'static btScalar gSphereRollingFriction =' + str(gSphereRollingFriction) + '; // set sphere rolling friction to 1\n', 'static btScalar gSphereRestitution = ' + str(gSphereRestitution) + '; // set sphere restitution to 0\n', 'static btScalar sphereMass = ' + str(sphereMass) + 'f;\n', 'static std::string filename = "'+filename+'";\n']

                    print (variables)
                    with open('examples/BasicDemo/BasicExample.cpp', 'w') as fout:
                        fout.writelines(data[0:15])
                        fout.writelines(variables)
                        fout.writelines(data[23:])

                    #os.system("./basedemo.sh")
                    import subprocess
                    import time
                    argument = '...'
                    proc = subprocess.Popen(['./basedemo.sh', '', argument], shell=True)
                    time.sleep(30) # <-- There's no time.wait, but time.sleep.
                    pid = proc.pid # <--- access `pid` attribute to get the pid of the child process.
                    proc.terminate()


                    import psutil

                    PROCNAME = "AppBasicExampleGui"

                    for proc in psutil.process_iter():
                        # check whether the process name matches
                        if proc.name() == PROCNAME:
                            proc.kill()
