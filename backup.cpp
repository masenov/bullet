#include "BasicExample.h"
#include "btBulletDynamicsCommon.h"
#define ARRAY_SIZE_Y 5
#define ARRAY_SIZE_X 5
#define ARRAY_SIZE_Z 5
#include "LinearMath/btVector3.h"
#include "LinearMath/btAlignedObjectArray.h"
#include "../CommonInterfaces/CommonRigidBodyBase.h"
#include <fstream>
//using namespace std;
static btRigidBody* ramp = NULL;
static btRigidBody* gSphere = NULL;
static btScalar gTilt = 40.0f/180.0f*SIMD_PI; // tilt the ramp 20 degrees
static btScalar gRampFriction = 0.474; // set ramp friction to 1
static btScalar gRampRestitution = 1.2; // set ramp restitution to 0 (no restitution)
static btScalar gBoxFriction = 1.3; // set box friction to 1
static btScalar gBoxRestitution = 1; // set box restitution to 0
static btScalar gSphereFriction = 1; // set sphere friction to 1
static btScalar gSphereRollingFriction =0.368; // set sphere rolling friction to 1
static btScalar gSphereRestitution = 1.5; // set sphere restitution to 0

struct BasicExample : public CommonRigidBodyBase
{
	BasicExample(struct GUIHelperInterface* helper)
		:CommonRigidBodyBase(helper)
	{
	}
	virtual ~BasicExample(){}
	virtual void initPhysics();
	virtual void renderScene();
	virtual void stepSimulation(float deltaTime);

  void resetCamera()
	{
		float dist = 4;
		float pitch = 52;
		float yaw = 35;
		float targetPos[3]={-6,6,-6};
		m_guiHelper->resetCamera(dist,pitch,yaw,targetPos[0],targetPos[1],targetPos[2]);
	}
};

void BasicExample::stepSimulation(float deltaTime)
{
  std::ofstream myfile;
  myfile.open ("example.txt",std::ios::app);
  //myfile << "Writing this to a file.\n";
  m_dynamicsWorld->stepSimulation(4./240,0);
  std::string s = std::to_string(gSphere->getCenterOfMassPosition()[0]) + ", " + std::to_string(gSphere->getCenterOfMassPosition()[1]) + ", " + std::to_string(gSphere->getCenterOfMassPosition()[2]) + "\n";
  myfile << s;
  myfile.close();
    //       b3Printf("Velocity = %f,%f,%f,%f,%f,%f\n",gSphere->getAngularVelocity()[0],
    //                gSphere->getAngularVelocity()[1],
    //                gSphere->getAngularVelocity()[2],
    //                gSphere->getCenterOfMassPosition()[0],
    //                gSphere->getCenterOfMassPosition()[1],
    //                gSphere->getCenterOfMassPosition()[2]);

    // //CommonRigidBodyBase::stepSimulation(deltaTime);
}

void BasicExample::initPhysics()
{
  std::ofstream myfile;
  myfile.open("example.txt");
  myfile.close();

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
                             btVector3(btScalar(8), btScalar(10), btScalar(4)));

		gSphere = createRigidBody(sphereMass, startTransform, sphereShape);
		gSphere->forceActivationState(DISABLE_DEACTIVATION); // to prevent the sphere on the ramp from disabling
		gSphere->setFriction(gSphereFriction);
		gSphere->setRestitution(gSphereRestitution);
		gSphere->setRollingFriction(gSphereRollingFriction);
    //gSphere->setContactStiffnessAndDamping(100,1);
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

		btScalar	mass(1);

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




