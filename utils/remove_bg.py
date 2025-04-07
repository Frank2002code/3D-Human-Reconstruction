import warnings
warnings.filterwarnings("ignore")

from PIL import Image
import torch as T
from torchvision import transforms
from transformers import AutoModelForImageSegmentation
import os

def path_to_image(
    images_folder_path: str,
    image_exten: tuple[str] | None = None,
) -> list[Image.Image]:
    if not os.path.exists(images_folder_path):
        raise FileNotFoundError(f"Image folder not found: {images_folder_path}")
    if image_exten is None:
        image_exten = (".png", ".jpg", ".jpeg", ".webp")
    images = []
    for filename in os.listdir(images_folder_path):
        if filename.lower().endswith(image_exten):
            image_path = os.path.join(images_folder_path, filename)
            image = Image.open(fp=image_path)
            images.append(image)
    return images

def remove_images_bg(
    images_folder_path: str,
    output_folder_path: str,
    image_exten: tuple[str] | None = None,
    device: T.device | None = None,
    net: AutoModelForImageSegmentation | None = None,
    transform: transforms.Compose | None = None,
) -> list[Image.Image]:
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    ## Prepare images
    if image_exten is None:
        image_exten = (".png", ".jpg", ".jpeg", ".webp")
    image_size = (1024, 1024)
    images = path_to_image(
        images_folder_path=images_folder_path,
        image_exten=image_exten,
    )
    image_size = images[0].size
    print(f"Image size: {image_size}")

    ## Prepare model & transform
    if device is None:
        device = T.device("cuda") if T.cuda.is_available() else T.device("mps")
    if net is None:
        net = AutoModelForImageSegmentation.from_pretrained(
            "ZhengPeng7/BiRefNet", trust_remote_code=True
        ).to(device).eval()  # half precision
    if transform is None:
        transform = transforms.Compose(
            [
                transforms.Resize(image_size),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )
    print(f"Load model {type(net).__name__} successfully.")
    
    ## Deal with single image
    def remove_image_bg(
        image: Image.Image,
    ) -> Image.Image:
        input_images = transform(image).unsqueeze(0).to(device)  # add a batch dimension and half precision
        with T.no_grad():
            preds = net(input_images)[-1].sigmoid().cpu()
        pred = preds[0].squeeze()
        pred_pil = transforms.ToPILImage()(pred)
        mask = pred_pil.resize(image_size)
        image.putalpha(mask)  # turn the image into RGBA (透明度)
        return image
    
    # for idx, filename in enumerate(os.listdir(images_folder_path)):
    #     if idx == 0:
    #         print(f"Start removing background from {len(os.listdir(images_folder_path))} images.")
    #     if filename.lower().endswith(image_exten):
    #         image_path = os.path.join(images_folder_path, filename)
    #         image = Image.open(fp=image_path)
    #         image = remove_image_bg(
    #             image=image,
    #         )
    #         output_path = os.path.join(output_folder_path, f"viewpoint_{idx:04d}.png")
    #         image.save(fp=output_path)
    #         print(f"Image {idx + 1} saved to {output_path}")
    for idx, image in enumerate(images):
        if idx == 0:
            print(f"Start removing background from {len(images)} images.")
        image = remove_image_bg(
            image=image,
        )
        output_path = os.path.join(output_folder_path, f"viewpoint_{idx:04d}.png")
        image.save(fp=output_path)
        print(f"Image {idx + 1} saved to {output_path}")

if __name__ == "__main__":
    ## Convert the PLY file to RGB
    # model_path = "result/3Dmodel/tsai_video_nobg.ply"
    # convert2rgb(model_path)
    
    ## Remove background
    # images = list(
    #     map(
    #         lambda x: remove_image_bg(
    #             image=x,
    #             transform=image_transform,
    #             net=birefnet,
    #             device=T.device("mps")),
    #         images
    #     )
    # )
    images_folder_path = f"../data/creeper"
    output_folder_path = f"../result/creeper_nobg"
    
    remove_images_bg(
        images_folder_path=images_folder_path,
        output_folder_path=output_folder_path,
    )
    