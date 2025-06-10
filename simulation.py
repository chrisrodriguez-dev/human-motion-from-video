import json
import pybullet as p
import pybullet_data
import time

with open("stick_figure_walk_cycle.json", "r") as f:
    data = json.load(f)

frames = [frame["j3d"] for frame in data]

p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.8)

bone_pairs = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (1, 5), (5, 6), (6, 7),
    (1, 8), (8, 9), (9, 10),
    (1, 11), (11, 12), (12, 13),
    (0, 14), (0, 15), (14, 16), (15, 17)
]  # adjust based on your joint order!


def draw_bones(joints):
    p.removeAllUserDebugItems()  # Clear old lines
    for i, j in bone_pairs:
        if i < len(joints) and j < len(joints):
            p.addUserDebugLine(joints[i], joints[j], [1, 0, 0], 2.0)
    

# creating skeleton
joint_ids = []
radius = 0.05

for joint in frames[0]:
    visual_shape_id = p.createVisualShape(p.GEOM_SPHERE, radius=radius)
    joint_id = p.createMultiBody(baseMass=0,
                                 baseCollisionShapeIndex=-1,
                                 baseVisualShapeIndex=visual_shape_id,
                                 basePosition=joint)
    joint_ids.append(joint_id)

for frame in frames:
    for i, pos in enumerate(frame):
        p.resetBasePositionAndOrientation(joint_ids[i], pos, [0,0,0,1])
    draw_bones(frame)
    p.stepSimulation()
    time.sleep(1/30)




