import os
import argparse
from PIL import Image
from peft import PeftModel
from torchvision import transforms
from diffusers import StableDiffusionImg2ImgPipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pretrained_path', type=str, required=True)
    parser.add_argument('--lora_path', type=str, required=True)
    parser.add_argument('--folder_path', type=str, required=True)
    parser.add_argument('--strength', type=float, required=True)
    parser.add_argument('--save_path', type=str, default='styled_image.jpg')
    args = vars(parser.parse_args())

    # Load pretrained model
    pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(args['pretrained_path'])
    pipeline.to("cuda")

    # Load LoRA
    pipeline.unet = PeftModel.from_pretrained(pipeline.unet, args['lora_path'])

    # Inference through the entire folder
    folder_path = args['folder_path']
    image_names = os.listdir(folder_path)

    for image_name in image_names:
        image_path = os.path.join(folder_path, image_name)
        # Load content image
        im = Image.open(image_path)
        image_transforms = transforms.Compose(
            [
                transforms.Resize(256, interpolation=transforms.InterpolationMode.BILINEAR),
                transforms.CenterCrop(256),
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
            ]
        )
        im = image_transforms(im)

        # Inference
        style_image = pipeline(prompt="Monet style", image=im, strength=args['strength'], num_inference_steps=100).images[0]

        # Save generated image
        save_path = os.path.join(args['save_path'], image_name)
        style_image.save(save_path)

if __name__ == "__main__":
    main()

