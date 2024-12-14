#!/bin/bash

export PYTHONPATH="$PYTHONPATH:$pwd"

python inference/transfer_style.py \
--pretrained_path "/home/trapoom555/data/hf_models/stable-diffusion-2-1" \
--lora_path "/home/trapoom555/code/Diffusion-LoRA-Style-Transfer/lora_ckpt/monet_all_bs_32" \
--image_path "/home/trapoom555/data/monet_data/photo_jpg/4bf1292d69.jpg" \
--strength 0.3 \
--save_path "styled_image.jpg"