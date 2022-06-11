import os
import numpy as np
import trimesh
import pyrender
import matplotlib.pyplot as plt

dir_names = [
    'CBCT_2018_stl_100',
    'CBCT_2019_stl_99',
    # 'CBCT_2020_stl_100'
]

degrees = [
    1.60, 1.63, 1.66, 1.69,
    1.70, 1.73, 1.76, 1.79,
    1.80, 1.83, 1.86, 1.89,
    1.90, 1.93, 1.96, 1.99,
    2.00, 2.03, 2.06, 2.09,
    2.10, 2.13, 2.16, 2.19,
    2.20, 2.23, 2.26, 2.29,
]

def get_camera_pose (name, degree = 2.0):
    if (name == 'CBCT_2018_stl_100'):
        return np.array([
            [np.cos(np.pi/degree), -np.sin(np.pi/degree) * np.cos(np.pi/degree), np.sin(np.pi/degree) * np.sin(np.pi/degree), 700.0],
            [np.sin(np.pi/degree), np.cos(np.pi/degree) * np.cos(np.pi/degree),  -np.sin(np.pi/degree) * np.cos(np.pi/degree), 200.0],
            [0.0, np.sin(np.pi/degree), np.cos(np.pi/degree), -150.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

    else:
        return np.array([
            [np.cos(np.pi/degree), -np.sin(np.pi/degree) * np.cos(np.pi/degree), np.sin(np.pi/degree) * np.sin(np.pi/degree), 700.0],
            [np.sin(np.pi/degree), np.cos(np.pi/degree) * np.cos(np.pi/degree),  -np.sin(np.pi/degree) * np.cos(np.pi/degree), 150.0],
            [0.0, np.sin(np.pi/degree), np.cos(np.pi/degree), -80.0],
            [0.0, 0.0, 0.0, 1.0]
        ])

for dir_name in dir_names:
    dir_path = f'./datasets/{dir_name}'
    for (root, directories, files) in os.walk(dir_path):

        for file in files:
            file_path = os.path.join(root, file)

            if 'CR' in file_path:
                if (os.path.isdir(f'./results/{dir_name}_side/{root.strip(dir_path)}')):
                    print('Exist!!')
                    continue
                
                for i, degree in enumerate(degrees):
                    try:
                        print(i, degree)
                        os.makedirs(f'./results/{dir_name}_side/{root.strip(dir_path)}', exist_ok=True)

                        camera_pose = get_camera_pose(dir_name, degree)
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

                        os.makedirs(f'./results/{dir_name}_side/{root.strip(dir_path)}', exist_ok=True)
                        plt.imsave(f'./results/{dir_name}_side/{root.strip(dir_path)}/000{i}.png', color)

                        print(f"./results/{dir_name}_side/{root.strip(dir_path)}/000{i}.png saved!")
                    except Exception as e:
                        print(f'error {e}')
                        continue
                    finally:
                        continue