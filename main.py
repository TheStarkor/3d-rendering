import os
import numpy as np
import trimesh
import pyrender
import matplotlib.pyplot as plt

dir_names = [
    # 'CBCT_2018_stl_100',
    # 'CBCT_2019_stl_99',
    'CBCT_2020_stl_100'
]

camera_pose_set = {
    'CBCT_2018_stl_100': [
        np.array([
            [1.0, 0.0, 0.0, 100.0],
            [0.0, np.cos(np.pi/1.2), -np.sin(np.pi/1.2), -130.0],
            [0.0, np.sin(np.pi/1.2), np.cos(np.pi/1.2), -250.0],
            [0.0,  0.0,           0.0,          1.0]
        ]),
        np.array([
            [np.cos(np.pi/2.0), -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), np.sin(np.pi/2.0) * np.sin(np.pi/2.0), 300.0],
            [np.sin(np.pi/2.0), np.cos(np.pi/2.0) * np.cos(np.pi/2.0),  -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), 150.0],
            [0.0, np.sin(np.pi/2.0), np.cos(np.pi/2.0), -150.0],
            [0.0, 0.0, 0.0, 1.0]
        ]),
        np.array([
            [np.cos(np.pi/2.0), -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), np.sin(np.pi/2.0) * np.sin(np.pi/2.0), 200.0],
            [np.sin(np.pi/2.0), np.cos(np.pi/2.0) * np.cos(np.pi/2.0),  -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), 50.0],
            [0.0, np.sin(np.pi/2.0), np.cos(np.pi/2.0), -100.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    ],
    'CBCT_2019_stl_99': [
        np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, np.cos(np.pi/1.2), -np.sin(np.pi/1.2), -300.0],
            [0.0, np.sin(np.pi/1.2), np.cos(np.pi/1.2), -100.0],
            [0.0,  0.0,           0.0,          1.0]
        ]),
        np.array([
            [np.cos(np.pi/2.0), -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), np.sin(np.pi/2.0) * np.sin(np.pi/2.0), 150.0],
            [np.sin(np.pi/2.0), np.cos(np.pi/2.0) * np.cos(np.pi/2.0),  -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), 20.0],
            [0.0, np.sin(np.pi/2.0), np.cos(np.pi/2.0), 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]),
        np.array([
            [np.cos(np.pi/2.0), -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), np.sin(np.pi/2.0) * np.sin(np.pi/2.0), 100.0],
            [np.sin(np.pi/2.0), np.cos(np.pi/2.0) * np.cos(np.pi/2.0),  -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), -90.0],
            [0.0, np.sin(np.pi/2.0), np.cos(np.pi/2.0), 70.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    ],
    'CBCT_2020_stl_100': [
        np.array([
            [1.0, 0.0, 0.0, 0.0],
            [0.0, np.cos(np.pi/1.2), -np.sin(np.pi/1.2), -300.0],
            [0.0, np.sin(np.pi/1.2), np.cos(np.pi/1.2), -100.0],
            [0.0,  0.0,           0.0,          1.0]
        ]),
        np.array([
            [np.cos(np.pi/2.0), -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), np.sin(np.pi/2.0) * np.sin(np.pi/2.0), 150.0],
            [np.sin(np.pi/2.0), np.cos(np.pi/2.0) * np.cos(np.pi/2.0),  -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), 20.0],
            [0.0, np.sin(np.pi/2.0), np.cos(np.pi/2.0), 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ]),
        np.array([
            [np.cos(np.pi/2.0), -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), np.sin(np.pi/2.0) * np.sin(np.pi/2.0), 100.0],
            [np.sin(np.pi/2.0), np.cos(np.pi/2.0) * np.cos(np.pi/2.0),  -np.sin(np.pi/2.0) * np.cos(np.pi/2.0), -90.0],
            [0.0, np.sin(np.pi/2.0), np.cos(np.pi/2.0), 70.0],
            [0.0, 0.0, 0.0, 1.0]
        ])
    ]
}

for dir_name in dir_names:
    dir_path = f'./datasets/{dir_name}'
    for (root, directories, files) in os.walk(dir_path):

        for file in files:
            file_path = os.path.join(root, file)

            if 'CR' in file_path:
                camera_poses = camera_pose_set[dir_name]
                for i, camera_pose in enumerate(camera_poses):
                    fuze_trimesh = trimesh.load(file_path)

                    mesh = pyrender.Mesh.from_trimesh(fuze_trimesh)
                    scene = pyrender.Scene()
                    scene.add(mesh)
                    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0, aspectRatio=1.0)

                    scene.add(camera, pose=camera_pose)

                    direc_l = pyrender.DirectionalLight(color=np.ones(3), intensity=1.0)
                    spot_l = pyrender.SpotLight(color=np.ones(3), intensity=20.0,
                                        innerConeAngle=np.pi/16, outerConeAngle=np.pi/6)

                    direc_l_node = scene.add(direc_l, pose=camera_pose)
                    spot_l_node = scene.add(spot_l, pose=camera_pose)

                    r = pyrender.OffscreenRenderer(800, 800)
                    color, depth = r.render(scene)

                    os.makedirs(f'./results/{dir_name}/{root.strip(dir_path)}', exist_ok=True)
                    plt.imsave(f'./results/{dir_name}/{root.strip(dir_path)}/000{i}.png', color)

                    print(f"./results/{dir_name}/{root.strip(dir_path)}/000{i}.png saved!")