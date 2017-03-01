#include "ImportObjExample.h"
#include <vector>
#include "../OpenGLWindow/GLInstancingRenderer.h"
#include"Wavefront/tiny_obj_loader.h"
#include "../OpenGLWindow/GLInstanceGraphicsShape.h"
#include "btBulletDynamicsCommon.h"
#include "../OpenGLWindow/SimpleOpenGL3App.h"
#include "Wavefront2GLInstanceGraphicsShape.h"
#include "../../Utils/b3ResourcePath.h"
#include "Bullet3Common/b3FileUtils.h"

#include "stb_image/stb_image.h"

#include "../CommonInterfaces/CommonRigidBodyBase.h"
#include "../ImportMeshUtility/b3ImportMeshUtility.h"
#include<iostream>

#include "LinearMath/btVector3.h"
#include "LinearMath/btAlignedObjectArray.h" 
#include "../CommonInterfaces/CommonRigidBodyBase.h"

#include "../Utils/b3ResourcePath.h"
#include "Bullet3Common/b3FileUtils.h"
#include "../Importers/ImportObjDemo/LoadMeshFromObj.h"
#include "../OpenGLWindow/GLInstanceGraphicsShape.h"

using namespace std;
static btScalar gTilt = 270.0f/180.0f*SIMD_PI; // tilt the ramp 20 degrees

static btScalar gRampFriction = 1; // set ramp friction to 1

static btScalar gRampRestitution = 0; // set ramp restitution to 0 (no restitution)

static btScalar gBoxFriction = 1; // set box friction to 1

static btScalar gBoxRestitution = 0; // set box restitution to 0

static btScalar gSphereFriction = 1; // set sphere friction to 1

static btScalar gSphereRollingFriction = 1; // set sphere rolling friction to 1

static btScalar gSphereRestitution = 0; // set sphere restitution to 0

static btRigidBody* ramp = NULL;
static btRigidBody* gSphere = NULL;


class ImportObjSetup : public CommonRigidBodyBase
{
  int m_options;
    std::string m_fileName;
   
   
public:
    ImportObjSetup(struct GUIHelperInterface* helper, const char* fileName);
    virtual ~ImportObjSetup();
    
	virtual void initPhysics();

	virtual void resetCamera()
	{
		float dist = 13;
		float pitch = 531;
		float yaw = 28;
		float targetPos[3]={-2,2,-2};
		m_guiHelper->resetCamera(dist,pitch,yaw,targetPos[0],targetPos[1],targetPos[2]);
	}

};

ImportObjSetup::ImportObjSetup(struct GUIHelperInterface* helper, const char* fileName)
:CommonRigidBodyBase(helper)
{
    if (fileName)
    {
        m_fileName = fileName;
    } else
    {
        m_fileName = "surface.obj";//"sponza_closed.obj";//sphere8.obj";
    }
}

ImportObjSetup::~ImportObjSetup()
{
    
}



int loadAndRegisterMeshFromFile2(const std::string& fileName, CommonRenderInterface* renderer)
{
	int shapeId = -1;
	
	b3ImportMeshData meshData;
	if (b3ImportMeshUtility::loadAndRegisterMeshFromFileInternal(fileName, meshData))
	{
		int textureIndex = -1;
		
		if (meshData.m_textureImage)
		{
			textureIndex = renderer->registerTexture(meshData.m_textureImage,meshData.m_textureWidth,meshData.m_textureHeight);
		}
		
		shapeId = renderer->registerShape(&meshData.m_gfxShape->m_vertices->at(0).xyzw[0], 
										  meshData.m_gfxShape->m_numvertices, 
										  &meshData.m_gfxShape->m_indices->at(0), 
										  meshData.m_gfxShape->m_numIndices,
										  B3_GL_TRIANGLES,
										  textureIndex);
    cout<<meshData.m_gfxShape->m_vertices->at(0).xyzw[0];
		delete meshData.m_gfxShape;
		delete meshData.m_textureImage;
	}
	return shapeId;
}



void ImportObjSetup::initPhysics()
{
	m_guiHelper->setUpAxis(1);
	this->createEmptyDynamicsWorld();
	m_guiHelper->createPhysicsDebugDrawer(m_dynamicsWorld);
	m_dynamicsWorld->getDebugDrawer()->setDebugMode(btIDebugDraw::DBG_DrawWireframe);
  ///create a few basic rigid bodies
	btBoxShape* groundShape = createBoxShape(btVector3(btScalar(50.),btScalar(50.),btScalar(50.)));

	//groundShape->initializePolyhedralFeatures();
	//btCollisionShape* groundShape = new btStaticPlaneShape(btVector3(0,1,0),50);
	m_collisionShapes.push_back(groundShape);

	btTransform groundTransform;
	groundTransform.setIdentity();
	groundTransform.setOrigin(btVector3(0,-50,0));

	{
		btScalar mass(0.);
		createRigidBody(mass,groundTransform,groundShape, btVector4(0,0,1,1));
	}

  { //create a sphere above the inclined plane
    btSphereShape* sphereShape = new btSphereShape(btScalar(0.2));

		m_collisionShapes.push_back(sphereShape);

		btTransform startTransform;
		startTransform.setIdentity();

		btScalar sphereMass(1.f);

		startTransform.setOrigin(
                             btVector3(btScalar(-3), btScalar(5), btScalar(-2)));

		gSphere = createRigidBody(sphereMass, startTransform, sphereShape);
		gSphere->forceActivationState(DISABLE_DEACTIVATION); // to prevent the sphere on the ramp from disabling
		gSphere->setFriction(gSphereFriction);
		gSphere->setRestitution(gSphereRestitution);
		gSphere->setRollingFriction(gSphereRollingFriction);
	}


//load our obj mesh
	const char* fileName = "surface.obj";//sphere8.obj";//sponza_closed.obj";//sphere8.obj";
    char relativeFileName[1024];
    if (b3ResourcePath::findResourcePath(fileName, relativeFileName, 1024))
    {
		char pathPrefix[1024];
		b3FileUtils::extractPath(relativeFileName, pathPrefix, 1024);
	}
	
	GLInstanceGraphicsShape* glmesh = LoadMeshFromObj(relativeFileName, "");
	printf("[INFO] Obj loaded: Extracted %d verticed from obj file [%s]\n", glmesh->m_numvertices, fileName);

	const GLInstanceVertex& v = glmesh->m_vertices->at(2);
	btConvexHullShape* shape = new btConvexHullShape((const btScalar*)(&(v.xyzw[0])), glmesh->m_numvertices, sizeof(GLInstanceVertex));

	float scaling[4] = {1,1,1,1};
	
	btVector3 localScaling(scaling[0],scaling[1],scaling[2]);
	shape->setLocalScaling(localScaling);
	    
    if (m_options & ptimizeConvexObj)
    {
        shape->optimizeConvexHull();
    }

    if (m_options & omputePolyhedralFeatures)
    {
        shape->initializePolyhedralFeatures();    
    }
	
	
	
	//shape->setMargin(0.001);
	m_collisionShapes.push_back(shape);

	btTransform startTransform;
	btScalar	mass(0.f);
	btQuaternion incline;
  static btScalar yRot = 45.0f/180.0f*SIMD_PI; // tilt the ramp 20 degrees
  static btScalar gTilt = 90.0f/180.0f*SIMD_PI; // tilt the ramp 20 degrees
  //incline.setRotation(btVector3(1,0,0),gTilt);
  incline.setEulerZYX(gTilt,yRot,0);
  //incline.setRotation(btVector3(0,1,0),yRot);
  startTransform.setRotation(incline);
  bool isDynamic = (mass != 0.f);
	btVector3 localInertia(0,0,0);
	if (isDynamic)
		shape->calculateLocalInertia(mass,localInertia);
  
	float color[4] = {1,1,1,1};
	float orn[4] = {0,0,0,1};
	float pos[4] = {0,0,0,0};
	btVector3 position(pos[0],pos[1],pos[2]);
	startTransform.setOrigin(position);
  btRigidBody* body = createRigidBody(mass,startTransform,shape);


	
	bool useConvexHullForRendering = ((m_options & bjUseConvexHullForRendering)!=0);
    
	    
	if (!useConvexHullForRendering)
    {
		int shapeId = m_guiHelper->registerGraphicsShape(&glmesh->m_vertices->at(0).xyzw[0], 
																		glmesh->m_numvertices, 
																		&glmesh->m_indices->at(0), 
																		glmesh->m_numIndices,
																		B3_GL_TRIANGLES, -1);
		shape->setUserIndex(shapeId);
		int renderInstance = m_guiHelper->registerGraphicsInstance(shapeId,pos,orn,color,scaling);
		body->setUserIndex(renderInstance);
    }
   


   m_guiHelper->autogenerateGraphicsObjects(m_dynamicsWorld);


}

 CommonExampleInterface*    ImportObjCreateFunc(struct CommonExampleOptions& options)
 {
	 return new ImportObjSetup(options.m_guiHelper, options.m_fileName);
 }
