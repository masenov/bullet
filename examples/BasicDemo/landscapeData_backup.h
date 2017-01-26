#include "LinearMath/btScalar.h"

#define Landscape01VtxCount 4
#define Landscape01IdxCount 4

btScalar Landscape01Vtx[] = {
0.0f,0.0f,0.0f,
0.0f,50.0f,0.0f,
0.0f,10.0f,50.0f,
};

btScalar Landscape01Nml[] = {
1.0f,1.0f,1.0f,
1.0f,1.0f,1.0f,
1.0f,1.0f,1.0f,
};

btScalar Landscape01Tex[] = {
1.0f,1.0f,
1.0f,1.0f,
1.0f,1.0f,
};

unsigned short Landscape01Idx[] = {
0,1,2,
1,2,3,
2,3,4,
};
