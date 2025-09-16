import pybullet as p
import pybullet_data
import time
import numpy as np

# Connect to simulator (GUI for visualization)
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# add floor plane
plane = p.loadURDF("plane.urdf")

# add table
table_pos = [0.5, 0, 0]  # x, y, z
table_orientation = p.getQuaternionFromEuler([0, 0, 0])
table = p.loadURDF("table/table.urdf", basePosition=table_pos, baseOrientation=table_orientation)

# mount robot on wall
wall_orientation = p.getQuaternionFromEuler([0, 1.57, 0])
leftArm =  p.loadURDF("franka_panda/panda.urdf", basePosition=[0, -0.25, 1.0], baseOrientation=wall_orientation, useFixedBase=True)
rightArm = p.loadURDF("franka_panda/panda.urdf", basePosition=[0, 0.25, 1.0], baseOrientation=wall_orientation, useFixedBase=True)

# move robot
num_joints = p.getNumJoints(leftArm)
for step in range(10000):
    for i in range(1):
        p.setJointMotorControl2(
            bodyIndex=leftArm,
            jointIndex=i,
            controlMode=p.POSITION_CONTROL,
            targetPosition=0.5 * (step / 100)  # simple motion
        )
    p.stepSimulation()
    time.sleep(1./240.)