#ifndef IMPORT_OBJ_EXAMPLE_H
#define IMPORT_OBJ_EXAMPLE_H
enum ObjToRigidBodyOptionsEnu
  {
    bjUseConvexHullForRendering=1,
    ptimizeConvexObj=2,
    omputePolyhedralFeatures=4,
  };

class CommonExampleInterface*    ImportObjCreateFunc(struct CommonExampleOptions& options);


#endif //IMPORT_OBJ_EXAMPLE_H
