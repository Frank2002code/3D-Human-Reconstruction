#!/bin/bash
# This script is used to generate multiview images using SDXL

IMAGE_PATH="assets/demo/i2mv/A_decorative_figurine_of_a_young_anime-style_girl.png"
TEXT="A decorative figurine of a young anime-style girl"
OUTPUT_DIR="../result/test_i2mv_sdxl/test.png"

cd ../MV-Generation
python -m scripts.inference_i2mv_sdxl \
--image "$IMAGE_PATH" \
--text "$TEXT" \
--seed 21  \
--output "$OUTPUT_DIR" --remove_bg