#!/bin/bash
# This script is used to generate multiview images using SDXL

# IMAGE_PATH="assets/demo/i2mv/A_decorative_figurine_of_a_young_anime-style_girl.png"
# TEXT="A decorative figurine of a young anime-style girl"

IMAGE_PATH="../result/creeper_nobg/viewpoint_0009.png"
TEXT="A green creeper standing on a square burger"

N_VIEWS=2
OUTPUT_PATH="../result/creeper_i2mv/creeper_nobg"

cd ../MV_generation
python -m scripts.inference_i2mv_sdxl \
--image "$IMAGE_PATH" \
--text "$TEXT" \
--num_views $N_VIEWS \
--seed 21  \
--output_path "$OUTPUT_PATH" # --remove_bg