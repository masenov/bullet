flat_x = x.flatten()
flat_y = y.flatten()
flat_z = z.flatten()
size = flat_x.shape[0]

filename = 'landscapeData.h'

open(filename, 'w').close()

f = open(filename, 'a')

f.write('#include "LinearMath/btScalar.h"\n#define Landscape01VtxCount 4\n#define Landscape01IdxCount 4\nbtScalar Landscape01Vtx[] = {\n')
for i in range(size):
    f.write(str(flat_x[i])+'f,'+str(flat_y[i])+'f,'+str(flat_z[i])+'f,\n')
f.write('};\n')

f.write('btScalar Landscape01Nml[] = {\n')
for i in range(size):
    f.write('1.0f,1.0f,1.0f,\n')
f.write('};\n')

f.write('btScalar Landscape01Tex[] = {\n')
for i in range(size):
    f.write('1.0f,1.0f,1.0f,\n')
f.write('};\n')

f.write('unsigned short Landscape01Idx[] = {\n')
for i in range(size):
    f.write(str(i)+','+str(i+1)+','+str(i+2)+',\n')
f.write('};\n')


f.close()
