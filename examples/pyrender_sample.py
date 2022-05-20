import os
import numpy as np
import trimesh

from pyrender import PerspectiveCamera,\
                     DirectionalLight, SpotLight, PointLight,\
                     MetallicRoughnessMaterial,\
                     Primitive, Mesh, Node, Scene,\
                     OffscreenRenderer

trimesh.util.attach_to_log()

model_trimesh = trimesh.load('./models/CR.stl')
model_mesh = Mesh.from_trimesh(model_trimesh)

#==============================================================================
# Light creation
#==============================================================================

direc_l = DirectionalLight(color=np.ones(3), intensity=1.0)
spot_l = SpotLight(color=np.ones(3), intensity=10.0,
                   innerConeAngle=np.pi/16, outerConeAngle=np.pi/6)
point_l = PointLight(color=np.ones(3), intensity=10.0)

#==============================================================================
# Camera creation
#==============================================================================

cam = PerspectiveCamera(yfov=(np.pi / 3.0))
cam_pose = np.array([
    [0.0,  -np.sqrt(2)/2, np.sqrt(2)/2, 0.5],
    [1.0, 0.0,           0.0,           0.0],
    [0.0,  np.sqrt(2)/2,  np.sqrt(2)/2, 0.4],
    [0.0,  0.0,           0.0,          1.0]
])

#==============================================================================
# Scene creation
#==============================================================================

scene = Scene(ambient_light=np.array([0.02, 0.02, 0.02, 1.0]))

#------------------------------------------------------------------------------
# By manually creating nodes
#------------------------------------------------------------------------------
model_node = Node(mesh=model_mesh, translation=np.array([0.1, 0.15, 0.05]))
scene.add_node(model_node)

#==============================================================================
# Rendering offscreen from that camera
#==============================================================================

cam_node = scene.add(cam, pose=cam_pose)
r = OffscreenRenderer(viewport_width=640*2, viewport_height=480*2)
color, depth = r.render(scene)
r.delete()

import matplotlib.pyplot as plt
plt.figure(figsize=(20,20))
plt.imshow(color)
plt.show()