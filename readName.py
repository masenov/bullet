import os
files = os.listdir('build_cmake/experiments')
print (files)
print (len(files))
file = files[2]
rest_pos = 9
fric_pos = file.find('fric')
tilt_pos = file.find('tilt')
mass_pos = file.find('mass')
end_pos = file.find('.txt')
rest = float(file[rest_pos:fric_pos])
fric = float(file[fric_pos+5:tilt_pos])
tilt = float(file[tilt_pos+4:mass_pos])
mass = float(file[mass_pos+4:end_pos])
print (rest,fric,tilt,mass)
print (file.find('fric'))
