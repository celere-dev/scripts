#!/usr/bin/env python3
"""Script para redimensionar e otimizar imagens a partir de um diretório.

Lembre-se de definir as permissões corretas:

chmod u+x opt-images.py
chmod u+rwx ./<OUTPUT_DIR>
"""

__version__ = "0.1"

from PIL import Image
import os
import re


def optmize_and_resize(input, output, max_w=1800, quality=85):
    with Image.open(input) as img:
        w, h = img.size

        # Resize image
        if w > max_w:
            aspect_ratio = max_w / w
            new_w = int(h * aspect_ratio)

            img = img.resize((max_w, new_w), Image.Resampling.LANCZOS)

        # Convert to RGB
        if img.mode in ("RGBA", "P", "L"):
            img = img.convert("RGB")

        img.save(output, "JPEG", optimize=True, quality=quality)


def get_images(dir, output):
    if not os.path.exists(output):
        os.makedirs(output)

    for image_name in os.listdir(dir):
        image_path = os.path.join(dir, image_name)

        if image_name.lower().endswith((".png", ".jpg", ".jpeg")):
            output_path = os.path.join(output, image_name)

            optmize_and_resize(image_path, output_path)


def get_last_segment(dir):
    match = re.search(r"[^/\\]+$", dir)
    return match.group(0) if match else None


dir = input("Digite o diretório de input (ex: ./img/high_res): ")
output = f"optimized-{get_last_segment(dir)}"

get_images(dir, output)
