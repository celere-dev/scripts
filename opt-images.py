#!/usr/bin/env python3
"""Script para redimensionar e otimizar imagens a partir de um diretório.

Lembre-se de definir as permissões corretas:

chmod u+x opt-images.py
chmod u+rwx ./<OUTPUT_DIR>
"""

__version__ = "0.2"

from PIL import Image, UnidentifiedImageError
import os
import re


def get_metadata_without_dpi(img):
    metadata_dict = {}

    for key, value in img.info.items():
        if key != "dpi":
            metadata_dict[key] = value

    return metadata_dict


def optmize_and_resize(input, output, max_w=1800, quality=85):
    with Image.open(input) as img:
        w, h = img.size

        # Resize image
        if w > max_w:
            aspect_ratio = max_w / w
            new_w = int(h * aspect_ratio)

            img = img.resize((max_w, new_w), Image.Resampling.LANCZOS)

        # Get metadata
        metadata = get_metadata_without_dpi(img)

        # Get/Set DPI
        opt_dpi = (300, 300)
        dpi = img.info.get("dpi", opt_dpi)

        if dpi[0] > 300:
            dpi = opt_dpi

        img.save(
            output,
            img.format,
            optimize=True,
            quality=quality,
            dpi=dpi,
            **metadata,
        )


def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except (IOError, UnidentifiedImageError):
        return False


def get_images(dir, output):
    if not os.path.exists(output):
        os.makedirs(output)

    for image_name in os.listdir(dir):
        image_path = os.path.join(dir, image_name)
        output_path = os.path.join(output, image_name)

        if is_valid_image(image_path):
            optmize_and_resize(image_path, output_path)

            continue

        with open(image_path, "rb") as original, open(output_path, "wb") as copy:
            copy.write(original.read())

            print(f"Arquivo não otimizado: {image_name}")


def get_last_segment(dir):
    match = re.search(r"[^/\\]+$", dir)
    return match.group(0) if match else None


dir = input("Digite o diretório de input (ex: /img/high_res): ")
output = f"optimized-{get_last_segment(dir)}"

get_images(dir, output)
