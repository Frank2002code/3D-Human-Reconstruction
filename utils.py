import warnings
warnings.filterwarnings("ignore")

from PIL import Image
from pathlib import Path
import torch as T
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import os
import open3d as o3d

def path_to_image(
    dir_path: str,
) -> list[Image.Image]:
    images = []
    for img_path in Path(dir_path).glob("*.png"):
        # print(img_path)
        images.append(Image.open(img_path))
    return images

def remove_bg(
    image: Image.Image,
    transform: transforms.Compose,
    net: AutoModelForImageSegmentation,
    device: T.device,
) -> Image.Image:
    image_size = image.size
    input_image = transform(image).unsqueeze(0).to(device)  # add a batch dimension
    with T.no_grad():
        preds = net(input_image)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(image_size)
    image.putalpha(mask)  # turn the image into RGBA (透明度)
    return image

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

if __name__ == "__main__":
    import sys
    model_path = "model/tsai_video_nobg_model.ply"
    show_ply_file(model_path)
    input("Input any key to exit.")
    sys.exit(0)
    # Prepare transform & model
    image_transform = transforms.Compose(
        [
            transforms.Resize((1024, 1024)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    device = T.device("cuda") if T.cuda.is_available() else T.device("mps")
    birefnet = AutoModelForImageSegmentation.from_pretrained(
            "ZhengPeng7/BiRefNet", trust_remote_code=True
    ).to(device)
    # Load 
    image_dir_path = "data/tsai_video/images"
    images = path_to_image(image_dir_path)
    
    # Remove background
    images = list(map(lambda x: remove_bg(x, image_transform, birefnet, T.device("mps")), images))
    
    # Save images
    output_dir_path = "data/tsai_video_nobg/images"
    os.makedirs(output_dir_path, exist_ok=True)
    for idx, img in enumerate(images):
        file_path = os.path.join(output_dir_path, f"frame_{idx:04d}.png")
        img.save(fp=file_path)
    print(f"Images saved to {output_dir_path}")