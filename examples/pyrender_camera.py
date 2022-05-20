import numpy as np
import trimesh
import pyrender
import matplotlib.pyplot as plt
from pyrender import PerspectiveCamera,\
                     DirectionalLight, SpotLight, PointLight,\
                     MetallicRoughnessMaterial,\
                     Primitive, Mesh, Node, Scene,\
                     OffscreenRenderer

fuze_trimesh = trimesh.load('./models/CR.stl')

mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
scene = Scene()
scene.add(mesh)
camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)
s = np.sqrt(2)/2
camera_pose = np.array([
    [1.0, 0.0, 0.0, 100.0],
    [0.0, np.cos(np.pi/1.2), -np.sin(np.pi/1.2), -130.0],
    [0.0, np.sin(np.pi/1.2), np.cos(np.pi/1.2), -250.0],
    [0.0,  0.0,           0.0,          1.0]
])

scene.add(camera, pose=camera_pose)

direc_l = DirectionalLight(color=np.ones(3), intensity=1.0)
spot_l = SpotLight(color=np.ones(3), intensity=20.0,
                   innerConeAngle=np.pi/16, outerConeAngle=np.pi/6)

direc_l_node = scene.add(direc_l, pose=camera_pose)
spot_l_node = scene.add(spot_l, pose=camera_pose)

# pyrender.Viewer(scene, use_raymond_lighting=True)
r = pyrender.OffscreenRenderer(800, 800)
color, depth = r.render(scene)
plt.figure()
plt.axis('off')
plt.imshow(color)
plt.show()