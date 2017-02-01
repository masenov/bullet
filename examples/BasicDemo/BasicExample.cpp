/*
  Bullet Continuous Collision Detection and Physics Library
  Copyright (c) 2015 Google Inc. http://bulletphysics.org

  This software is provided 'as-is', without any express or implied warranty.
  In no event will the authors be held liable for any damages arising from the use of this software.
  Permission is granted to anyone to use this software for any purpose, 
  including commercial applications, and to alter it and redistribute it freely, 
  subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
  3. This notice may not be removed or altered from any source distribution.
*/


#include "BasicExample.h"

#include "btBulletDynamicsCommon.h"
#define ARRAY_SIZE_Y 5
#define ARRAY_SIZE_X 5
#define ARRAY_SIZE_Z 5
#include "landscapeData.h"

#include "LinearMath/btVector3.h"
#include "LinearMath/btAlignedObjectArray.h"

#include "../CommonInterfaces/CommonRigidBodyBase.h"

static btScalar gTilt = 20.0f/180.0f*SIMD_PI; // tilt the ramp 20 degrees

static btScalar gRampFriction = 1; // set ramp friction to 1

static btScalar gRampRestitution = 0; // set ramp restitution to 0 (no restitution)

static btScalar gBoxFriction = 1; // set box friction to 1

static btScalar gBoxRestitution = 0; // set box restitution to 0

static btScalar gSphereFriction = 1; // set sphere friction to 1

static btScalar gSphereRollingFriction = 1; // set sphere rolling friction to 1

static btScalar gSphereRestitution = 0; // set sphere restitution to 0

static btRigidBody* ramp = NULL;
static btRigidBody* gSphere = NULL;



struct BasicExample : public CommonRigidBodyBase
{
	BasicExample(struct GUIHelperInterface* helper)
		:CommonRigidBodyBase(helper)
	{
	}
  void createLargeMeshBody();
	virtual ~BasicExample(){}
	virtual void initPhysics();
	virtual void renderScene();
	void resetCamera()
	{
		float dist = 4;
		float pitch = 52;
		float yaw = 35;
		float targetPos[3]={-6,6,-6};
		m_guiHelper->resetCamera(dist,pitch,yaw,targetPos[0],targetPos[1],targetPos[2]);
	}
};

void BasicExample::initPhysics()
{
	m_guiHelper->setUpAxis(1);

	createEmptyDynamicsWorld();
	//m_dynamicsWorld->setGravity(btVector3(0,0,0));
	m_guiHelper->createPhysicsDebugDrawer(m_dynamicsWorld);

	if (m_dynamicsWorld->getDebugDrawer())
		m_dynamicsWorld->getDebugDrawer()->setDebugMode(btIDebugDraw::DBG_DrawWireframe+btIDebugDraw::DBG_DrawContactPoints);

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

  { //create a static inclined plane
		btBoxShape* inclinedPlaneShape = createBoxShape(btVector3(btScalar(20.),btScalar(1.),btScalar(10.)));
		m_collisionShapes.push_back(inclinedPlaneShape);

		btTransform startTransform;
		startTransform.setIdentity();

		// position the inclined plane above ground
		startTransform.setOrigin(btVector3(
                                       btScalar(0),
                                       btScalar(0),
                                       btScalar(0)));

		btQuaternion incline;
		incline.setRotation(btVector3(0,0,1),gTilt);
		startTransform.setRotation(incline);

		btScalar mass(0.);
		ramp = createRigidBody(mass,startTransform,inclinedPlaneShape);
		ramp->setFriction(gRampFriction);
		ramp->setRestitution(gRampRestitution);
	}
  { //create a sphere above the inclined plane
    btSphereShape* sphereShape = new btSphereShape(btScalar(1));

		m_collisionShapes.push_back(sphereShape);

		btTransform startTransform;
		startTransform.setIdentity();

		btScalar sphereMass(1.f);

		startTransform.setOrigin(
                             btVector3(btScalar(0), btScalar(20), btScalar(4)));

		gSphere = createRigidBody(sphereMass, startTransform, sphereShape);
		gSphere->forceActivationState(DISABLE_DEACTIVATION); // to prevent the sphere on the ramp from disabling
		gSphere->setFriction(gSphereFriction);
		gSphere->setRestitution(gSphereRestitution);
		gSphere->setRollingFriction(gSphereRollingFriction);
	}
	{
		//create a few dynamic rigidbodies
		// Re-using the same collision is better for memory usage and performance

		btBoxShape* colShape = createBoxShape(btVector3(.1,.1,.1));

		//btCollisionShape* colShape = new btSphereShape(btScalar(1.));
		m_collisionShapes.push_back(colShape);

		/// Create Dynamic Objects
		btTransform startTransform;
		startTransform.setIdentity();

		btScalar	mass(1.f);

		//rigidbody is dynamic if and only if mass is non zero, otherwise static
		bool isDynamic = (mass != 0.f);

		btVector3 localInertia(0,0,0);
		if (isDynamic)
			colShape->calculateLocalInertia(mass,localInertia);


		for (int k=0;k<ARRAY_SIZE_Y;k++)
      {
        for (int i=0;i<ARRAY_SIZE_X;i++)
          {
            for(int j = 0;j<ARRAY_SIZE_Z;j++)
              {
                startTransform.setOrigin(btVector3(
                                                   btScalar(0.2*i),
                                                   btScalar(2+.2*k),
                                                   btScalar(0.2*j)));

                createRigidBody(mass,startTransform,colShape);

              }
          }
      }
	}

	
  ///////////////////////////////////////////////////////////////////////////////
  // LargeMesh

  int LandscapeVtxCount[] = {
    LandscapemyVtxCount,
  };

  int LandscapeIdxCount[] = {
    LandscapemyIdxCount,
  };

  btScalar *LandscapeVtx[] = {
    LandscapemyVtx,
  };

  btScalar *LandscapeNml[] = {
    LandscapemyNml,
  };

  btScalar* LandscapeTex[] = {
    LandscapemyTex,
  };

  unsigned short  *LandscapeIdx[] = {
    LandscapemyIdx,
  };

	btTransform trans;
	trans.setIdentity();

	for(int i=0;i<8;i++) {

		btTriangleIndexVertexArray* meshInterface = new btTriangleIndexVertexArray();
		btIndexedMesh part;

		part.m_vertexBase = (const unsigned char*)LandscapeVtx[i];
		part.m_vertexStride = sizeof(btScalar) * 3;
		part.m_numVertices = LandscapeVtxCount[i];
		part.m_triangleIndexBase = (const unsigned char*)LandscapeIdx[i];
		part.m_triangleIndexStride = sizeof( short) * 3;
		part.m_numTriangles = LandscapeIdxCount[i]/3;
		part.m_indexType = PHY_SHORT;

		meshInterface->addIndexedMesh(part,PHY_SHORT);

		bool	useQuantizedAabbCompression = true;
		btBvhTriangleMeshShape* trimeshShape = new btBvhTriangleMeshShape(meshInterface,useQuantizedAabbCompression);
		btVector3 localInertia(0,0,0);
		trans.setOrigin(btVector3(0,-25,0));

		btRigidBody* body = createRigidBody(0,trans,trimeshShape);
		body->setFriction (btScalar(0.9));
	}

	m_guiHelper->autogenerateGraphicsObjects(m_dynamicsWorld);
}


void BasicExample::renderScene()
{
	CommonRigidBodyBase::renderScene();
	
}







CommonExampleInterface*    BasicExampleCreateFunc(CommonExampleOptions& options)
{
	return new BasicExample(options.m_guiHelper);

}


B3_STANDALONE_EXAMPLE(BasicExampleCreateFunc)



