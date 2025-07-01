#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from PIL import Image, ImageDraw, ImageFont
import io
import os
import sys
import textwrap

def crop_center_16_9(image):
    # Calculate the largest 16:9 crop from the center
    width, height = image.size
    target_ratio = 16 / 9
    new_width = width
    new_height = int(width / target_ratio)
    if new_height > height:
        new_height = height
        new_width = int(height * target_ratio)
    left = (width - new_width) // 2
    top = (height - new_height) // 2
    right = left + new_width
    bottom = top + new_height
    return image.crop((left, top, right, bottom))

# Step 1: Generate a dark image
api_key = "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"
prompt = "A dark, minimalistic background, suitable for a blog header, 16:9 aspect ratio, no text, no watermark, no border."
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {api_key}"}
payload = {"inputs": prompt}

response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    # Step 2: Crop to 16:9 aspect ratio
    image = Image.open(io.BytesIO(response.content)).convert("RGBA")
    image = crop_center_16_9(image)
    draw = ImageDraw.Draw(image)
    # You can use a TTF font file you have, or use the default
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    text = "Nahush Patel"
    # Calculate text size (compatibility for different Pillow versions)
    try:
        textwidth, textheight = font.getsize(text)
    except AttributeError:
        bbox = draw.textbbox((0, 0), text, font=font)
        textwidth = bbox[2] - bbox[0]
        textheight = bbox[3] - bbox[1]
    # Position: bottom right with some padding
    x = image.width - textwidth - 40
    y = image.height - textheight - 40
    # Draw text with a white color and slight shadow for contrast
    draw.text((x+2, y+2), text, font=font, fill=(0,0,0,180))  # shadow
    draw.text((x, y), text, font=font, fill=(255,255,255,255))  # main text

    os.makedirs("blog-img", exist_ok=True)
    image_path = os.path.join("blog-img", "dark-header-with-name.png")
    image.save(image_path)
    print(f"[HF+Pillow] Image with text overlay saved as {image_path}")
else:
    print("[HF] Failed:", response.status_code)
    print("[HF] Error:", response.text)

if len(sys.argv) < 2:
    print("Usage: python image_generator.py 'Title' [output_filename]")
    sys.exit(1)

title = sys.argv[1]
output_name = sys.argv[2] if len(sys.argv) > 2 else title

# Always use the provided diver image as the base
base_image_path = os.path.join("blog-img", "diver-base.jpeg")
if not os.path.exists(base_image_path):
    print(f"Base image not found: {base_image_path}")
    sys.exit(1)

image = Image.open(base_image_path).convert("RGBA")
draw = ImageDraw.Draw(image)
try:
    font_title = ImageFont.truetype("arial.ttf", 54)
    font_by = ImageFont.truetype("arial.ttf", 36)
except:
    font_title = ImageFont.load_default()
    font_by = ImageFont.load_default()

def get_text_size(draw, text, font):
    try:
        return font.getsize(text)
    except AttributeError:
        bbox = draw.textbbox((0, 0), text, font=font)
        return (bbox[2] - bbox[0], bbox[3] - bbox[1])

def wrap_text(text, font, max_width, draw):
    lines = []
    for paragraph in text.split('\n'):
        line = []
        for word in paragraph.split():
            test_line = ' '.join(line + [word])
            w, _ = get_text_size(draw, test_line, font)
            if w <= max_width or not line:
                line.append(word)
            else:
                lines.append(' '.join(line))
                line = [word]
        if line:
            lines.append(' '.join(line))
    return lines

# Wrap the title to fit the image width with padding
padding = 60
max_text_width = image.width - 2 * padding
title_lines = wrap_text(title, font_title, max_text_width, draw)

# Calculate total height of the title block
line_height = get_text_size(draw, 'Ay', font_title)[1]
title_block_height = line_height * len(title_lines)

# Center the title block vertically (upper half)
title_y = image.height // 3 - title_block_height // 2

# Draw each line of the title
for i, line in enumerate(title_lines):
    tw, th = get_text_size(draw, line, font_title)
    title_x = (image.width - tw) // 2
    y = title_y + i * line_height
    draw.text((title_x+2, y+2), line, font=font_title, fill=(0,0,0,180))
    draw.text((title_x, y), line, font=font_title, fill=(255,255,255,255))

# Draw 'by Nahush Patel' (centered, below title block)
by_text = "by Nahush Patel"
by_tw, by_th = get_text_size(draw, by_text, font_by)
by_x = (image.width - by_tw) // 2
by_y = title_y + title_block_height + 20
draw.text((by_x+2, by_y+2), by_text, font=font_by, fill=(0,0,0,180))
draw.text((by_x, by_y), by_text, font=font_by, fill=(255,255,255,255))

# Save as new image with filename based on blog title
os.makedirs("blog-img", exist_ok=True)
filename = output_name.lower().replace(" ", "-").replace(":", "").replace(",", "")
filename = "".join(c for c in filename if c.isalnum() or c == "-")
filename = filename[:50]
image_path = os.path.join("blog-img", f"{filename}-hf.png")
image.save(image_path)
print(f"[Pillow] Blog image with overlay saved as {image_path}")
print(f"[DEBUG] Full image path: {os.path.abspath(image_path)}") 