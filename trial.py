import pybullet as p
import pybullet_data
import time

p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane_id = p.loadURDF("plane.urdf")

robot_id = p.loadURDF("r2d2.urdf", basePosition=[0,0,1])

p.setGravity(0,0,-9.8)

for step in range(1000):
    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()

