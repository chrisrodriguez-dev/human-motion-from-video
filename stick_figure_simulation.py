import json
import pybullet as p
import pybullet_data
import time
import numpy as np

# Load pose data
with open('upright_stick_figure_walk_cycle.json', 'r') as f:
    data = json.load(f)
frames = [frame['j3d'] for frame in data]

# Connect to PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)
p.resetDebugVisualizerCamera(cameraDistance=2, cameraYaw=60, cameraPitch=-30, cameraTargetPosition=[0.5, 0.5, 1])

# Define bone connections
bone_pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (6, 7), (2, 8), (8, 9), (9, 10), (0, 11), (11, 12), (12, 13), (0, 14), (14, 15), (15, 16)]

def create_cylinder_link(start, end, color=[1, 0, 0, 1]):
    start = np.array(start)
    end = np.array(end)
    center = (start + end) / 2
    height = np.linalg.norm(end - start)
    direction = (end - start) / height
    axis = np.cross([0, 0, 1], direction)
    angle = np.arccos(np.clip(np.dot([0, 0, 1], direction), -1.0, 1.0))
    if np.linalg.norm(axis) < 1e-6:
        orn = [0, 0, 0, 1]
    else:
        axis = axis / np.linalg.norm(axis)
        orn = p.getQuaternionFromAxisAngle(axis.tolist(), angle)
    visual_id = p.createVisualShape(p.GEOM_CYLINDER, radius=0.015, length=height, rgbaColor=color)
    return p.createMultiBody(baseMass=0, baseCollisionShapeIndex=-1, baseVisualShapeIndex=visual_id, basePosition=center.tolist(), baseOrientation=orn)

# Create joint spheres
joint_radius = 0.03
joint_ids = []
for pos in frames[0]:
    shape_id = p.createVisualShape(p.GEOM_SPHERE, radius=joint_radius, rgbaColor=[1, 1, 0, 1])
    body_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=-1, baseVisualShapeIndex=shape_id, basePosition=pos)
    joint_ids.append(body_id)

# Animate
for frame in frames:
    for i, pos in enumerate(frame):
        p.resetBasePositionAndOrientation(joint_ids[i], pos, [0, 0, 0, 1])
    # Remove all previous bones
    p.removeAllUserDebugItems()
    # Draw bones as cylinders
    for i, j in bone_pairs:
        if i < len(frame) and j < len(frame):
            create_cylinder_link(frame[i], frame[j], color=[1, 0, 0, 1])
    p.stepSimulation()
    time.sleep(1 / 30)