import open3d as o3d
from plyfile import PlyData, PlyElement
import numpy as np
import os

def show_ply_file(
    file_path: str,
) -> None:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Create a visualizer
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    
    pcd = o3d.io.read_point_cloud(file_path)
    mesh = o3d.io.read_triangle_mesh(file_path)
    if len(mesh.triangles) > 0:
        print("This is a mesh file.")
        del pcd
        # Visualize the mesh
        # o3d.visualization.draw_geometries([mesh])
        vis.add_geometry(mesh)
        vis.run()
        vis.destroy_window()
    elif len(pcd.points) > 0:
        print("This is a point cloud file.")
        del mesh
        # Visualize the point cloud
        # o3d.visualization.draw_geometries([pcd])
        vis.add_geometry(pcd)
        vis.run()
        vis.destroy_window()
    else:
        print("This is not a valid point cloud or mesh file.")
    return

def convert2rgb(input_ply_path: str) -> None:
    if not os.path.exists(input_ply_path):
        raise FileNotFoundError(f"File not found: {input_ply_path}")
    plydata = PlyData.read(stream=input_ply_path)

    # coordinates of the vertices
    x = np.array(plydata['vertex']['x'])
    y = np.array(plydata['vertex']['y'])
    z = np.array(plydata['vertex']['z'])
    
    print(f"coordinates shape: {x.shape}, {y.shape}, {z.shape}")

    # colors of the vertices
    try:
        r = np.clip(np.array(plydata['vertex']['f_dc_0']) * 255, 0, 255).astype(np.uint8)
        g = np.clip(np.array(plydata['vertex']['f_dc_1']) * 255, 0, 255).astype(np.uint8)
        b = np.clip(np.array(plydata['vertex']['f_dc_2']) * 255, 0, 255).astype(np.uint8)
        
        # 其他屬性：scale, opacity, rotation
        scale_0 = plydata['vertex']['scale_0']
        scale_1 = plydata['vertex']['scale_1']
        scale_2 = plydata['vertex']['scale_2']
        opacity  = plydata['vertex']['opacity']
        rot_0 = plydata['vertex']['rot_0']
        rot_1 = plydata['vertex']['rot_1']
        rot_2 = plydata['vertex']['rot_2']
        rot_3 = plydata['vertex']['rot_3']
    except KeyError as e:
        raise RuntimeError("The input PLY file does not contain RGB color and other information.") from e

    # Create a new PLY file with the same vertices but with color information
    vertex_data = np.array(
        list(zip(x, y, z, r, g, b, scale_0, scale_1, scale_2, opacity, rot_0, rot_1, rot_2, rot_3)),
        dtype=[
            ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
            ('red', 'u1'), ('green', 'u1'), ('blue', 'u1'),
            ('scale_0', 'f4'), ('scale_1', 'f4'), ('scale_2', 'f4'),
            ('opacity', 'f4'),
            ('rot_0', 'f4'), ('rot_1', 'f4'), ('rot_2', 'f4'), ('rot_3', 'f4'),
        ]
    )

    # === 建立新 PLY 結構並儲存為 ASCII（方便 Blender 載入）===
    output_ply_path = "model/tsai_video_nobg_colored.ply"
    vertex_element = PlyElement.describe(vertex_data, 'vertex')
    PlyData([vertex_element], text=True).write(output_ply_path)

    print(f"✅New PLY file saved to {output_ply_path}")