#include "BasicExample.h"
#include "btBulletDynamicsCommon.h"
#define ARRAY_SIZE_Y 5
#define ARRAY_SIZE_X 5
#define ARRAY_SIZE_Z 5
#include "LinearMath/btVector3.h"
#include "LinearMath/btAlignedObjectArray.h"
#include "../CommonInterfaces/CommonRigidBodyBase.h"
#include <fstream>
#include <stdlib.h>     /* srand, rand */
#include <time.h>

//using namespace std;
static btRigidBody* ramp = NULL;
static btRigidBody* gSphere = NULL;
static btScalar gTilt = 0.0f/180.0f*SIMD_PI; // tilt the ramp 20 degrees
static btScalar gRampFriction = 0.9; // set ramp friction to 1
static btScalar gRampRestitution = 0.9; // set ramp restitution to 0 (no restitution)
static btScalar gSphereFriction = 0.9; // set sphere friction to 1
static btScalar gSphereRollingFriction =0.368; // set sphere rolling friction to 1
static btScalar gSphereRestitution = 0.9; // set sphere restitution to 0
static btScalar sphereMass = 0.0f;
static std::string filename = "experiments3/data_rest0.9fric_0.9tilt0.0mass0.0exp99.txt";

float rnd (int seed) {
  srand ( (unsigned) time(0) + seed );
  return (((double)rand()) / RAND_MAX) * 40 - 20;
    };

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
		float dist = 2;
		float pitch = 52;
		float yaw = 35;
		float targetPos[3]={-6,6,-6};
		m_guiHelper->resetCamera(dist,pitch,yaw,targetPos[0],targetPos[1],targetPos[2]);
	}
};



void BasicExample::stepSimulation(float deltaTime)
{
  std::ofstream myfile;
  myfile.open (filename,std::ios::app);
  std::string s = std::to_string(gSphere->getCenterOfMassPosition()[0]) + ", " + std::to_string(gSphere->getCenterOfMassPosition()[1]) + ", " + std::to_string(gSphere->getCenterOfMassPosition()[2]) + ", " + std::to_string(gSphere->getLinearVelocity()[0]) + ", " + std::to_string(gSphere->getLinearVelocity()[1]) + ", " + std::to_string(gSphere->getLinearVelocity()[2]) + ", ";
  m_dynamicsWorld->stepSimulation(4./240,0);
  s +=  std::to_string(gTilt) + ", "  + std::to_string(sphereMass) + ", " + std::to_string(gSphereFriction) + ", " + std::to_string(gRampRestitution) + "," + std::to_string(gSphere->getCenterOfMassPosition()[0]) + ", " + std::to_string(gSphere->getCenterOfMassPosition()[1]) + ", " + std::to_string(gSphere->getCenterOfMassPosition()[2]) + ", " + std::to_string(gSphere->getLinearVelocity()[0]) + ", " + std::to_string(gSphere->getLinearVelocity()[1]) + ", " + std::to_string(gSphere->getLinearVelocity()[2]) + "\n";
  myfile << s;
  myfile.close();
  //    b3Printf("Velocity = %f,%f,%f,%f,%f,%f\n",gSphere->getAngularVelocity()[0],
    //                gSphere->getAngularVelocity()[1],
    //                gSphere->getAngularVelocity()[2],
    //                gSphere->getCenterOfMassPosition()[0],
    //                gSphere->getCenterOfMassPosition()[1],
    //                gSphere->getCenterOfMassPosition()[2]);

    // //CommonRigidBodyBase::stepSimulation(deltaTime);
  //printf ("Velocity = %f,%f,%f,%f,%f,%f\n",gSphere->getLinearVelocity()[0], gSphere->getLinearVelocity()[1], gSphere->getLinearVelocity()[2], gSphere->getCenterOfMassPosition()[0], gSphere->getCenterOfMassPosition()[1], gSphere->getCenterOfMassPosition()[2]);
  // printf ("%f\n", rnd());
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
  /*
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
 
  */
  { //create a static inclined plane
    static btRigidBody* ramp2 = NULL;
		btBoxShape* inclinedPlaneShape2 = createBoxShape(btVector3(btScalar(380.),btScalar(1.),btScalar(380.)));
		m_collisionShapes.push_back(inclinedPlaneShape2);

		btTransform startTransform2;
		startTransform2.setIdentity();

		// position the inclined plane above ground
		startTransform2.setOrigin(btVector3(
                                       btScalar(40),
                                       btScalar(0),
                                       btScalar(0)));

		btQuaternion incline2;
		incline2.setRotation(btVector3(0,0,1),0);
		startTransform2.setRotation(incline2);

		btScalar mass2(0.);
		ramp2 = createRigidBody(mass2,startTransform2,inclinedPlaneShape2);
		ramp2->setFriction(gRampFriction);
		ramp2->setRestitution(gRampRestitution);
	}
  { //create a sphere above the inclined plane
    btSphereShape* sphereShape = new btSphereShape(btScalar(1));

		m_collisionShapes.push_back(sphereShape);

		btTransform startTransform;
		startTransform.setIdentity();

		btScalar sphereMass(.1f);

		startTransform.setOrigin(btVector3(btScalar(18), btScalar(15), btScalar(14)));

		gSphere = createRigidBody(sphereMass, startTransform, sphereShape);
		gSphere->forceActivationState(DISABLE_DEACTIVATION); // to prevent the sphere on the ramp from disabling
		gSphere->setFriction(gSphereFriction);
		gSphere->setRestitution(gSphereRestitution);
		gSphere->setRollingFriction(gSphereRollingFriction);
    gSphere->setLinearVelocity(btVector3(rnd(0), rnd(1), rnd(2)));
    printf ("Velocity = %f,%f,%f,%f,%f,%f\n",gSphere->getLinearVelocity()[0], gSphere->getLinearVelocity()[1], gSphere->getLinearVelocity()[2], gSphere->getCenterOfMassPosition()[0], gSphere->getCenterOfMassPosition()[1], gSphere->getCenterOfMassPosition()[2]);

    //gSphere->setContactStiffnessAndDamping(100,1);
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



