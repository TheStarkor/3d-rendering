import trimesh
import pyrender
import numpy as np

cr_trimesh = trimesh.load('./models/CR.stl')
mesh = pyrender.Mesh.from_trimesh(cr_trimesh)

scene = pyrender.Scene()
scene.add(mesh)

pyrender.Viewer(scene, use_raymond_lighting=True)