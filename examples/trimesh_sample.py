import trimesh

trimesh.util.attach_to_log()

# mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]],
#                        faces=[[0, 1, 2]])

# mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]],
#                        faces=[[0, 1, 2]],
#                        process=False)

# mesh = trimesh.load('./models/cube.STL')

mesh = trimesh.load('./models/CR.stl')

mesh.is_watertight

mesh.euler_number

print(mesh.volume / mesh.convex_hull.volume)

# mesh.vertices -= mesh.center_mass

mesh.moment_inertia

# mesh.split()

# for facet in mesh.facets:
#     mesh.visual.face_colors[facet] = trimesh.visual.random_color()

# preview mesh in an opengl window if you installed pyglet and scipy with pip
mesh.show()