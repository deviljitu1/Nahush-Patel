#!/usr/bin/env python3
"""
Unified Blog Automation Script
Generates a new blog (random type), creates a local image, updates blog-data.json, updates sitemap, and prints a summary.
"""
import os
import sys
import random
import subprocess
from datetime import datetime

# Import blog generators
from advanced_blog_generator import AdvancedBlogGenerator
from seo_blog_generator import SEOBlogGenerator
from blog_generator import BlogGenerator

# Local image generation (from image_generator.py, only PIL logic)
from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_placeholder_image(title, slug):
    os.makedirs("blog-img", exist_ok=True)
    filepath = os.path.join("blog-img", f"{slug}.png")
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), color=(102, 126, 234))
    draw = ImageDraw.Draw(img)
    # Gradient background
    for y in range(height):
        r = int(102 + (y / height) * 20)
        g = int(126 + (y / height) * 30)
        b = int(234 + (y / height) * 20)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    # Fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 24)
        author_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        author_font = ImageFont.load_default()
    # Wrap title
    max_width = 1100
    lines = []
    for line in textwrap.wrap(title, width=40):
        while draw.textlength(line, font=title_font) > max_width and len(line) > 0:
            line = line[:-1]
        lines.append(line)
    line_height = title_font.getbbox('A')[3] + 8
    total_text_height = line_height * len(lines)
    y = (height - total_text_height) // 2 - 80
    for line in lines:
        text_width = draw.textlength(line, font=title_font)
        x = (width - text_width) // 2
        draw.text((x+2, y+2), line, font=title_font, fill=(0, 0, 0, 100))
        draw.text((x, y), line, font=title_font, fill=(255, 255, 255))
        y += line_height
    # Subtitle
    subtitle = "Web Development & Technology"
    subtitle_width = draw.textlength(subtitle, font=subtitle_font)
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = y + 10
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(255, 255, 255, 200))
    # Author
    author = "By Nahush Patel"
    author_width = draw.textlength(author, font=author_font)
    author_x = (width - author_width) // 2
    author_y = subtitle_y + 40
    draw.text((author_x, author_y), author, font=author_font, fill=(255, 255, 255, 150))
    # Decorative elements
    draw.line([(100, 580), (1100, 580)], fill=(255, 255, 255, 100), width=2)
    draw.rectangle([50, 50, 150, 150], outline=(255, 255, 255, 50), width=3)
    draw.rectangle([1050, 430, 1150, 530], outline=(255, 255, 255, 50), width=3)
    img.save(filepath, "PNG", quality=95)
    print(f"✅ Placeholder image created: {filepath}")
    return filepath

def update_blog_data():
    print("🔄 Updating blog-data.json...")
    subprocess.run([sys.executable, "scripts/blog_scanner.py"])

def update_sitemap():
    print("🔄 Updating sitemap.xml...")
    subprocess.run([sys.executable, "scripts/generate_sitemap.py"])

def main():
    print("="*80)
    print("🤖 UNIFIED BLOG AUTOMATION")
    print("="*80)
    # Randomly pick blog type
    blog_type = random.choice(["advanced", "seo", "basic"])
    print(f"📝 Generating a {blog_type} blog post...")
    if blog_type == "advanced":
        generator = AdvancedBlogGenerator()
        topic = random.choice(generator.topics)
        filename = generator.create_blog_file(topic)
        blog_title = topic['title']
        slug = topic['slug']
    elif blog_type == "seo":
        generator = SEOBlogGenerator()
        topic = random.choice(generator.topics)
        filename = generator.create_blog_file(topic)
        blog_title = topic['title']
        slug = topic['slug']
    else:
        generator = BlogGenerator()
        filename = generator.generate_daily_blog()
        # Extract title from generated file
        with open(os.path.join("blog-list", filename), 'r', encoding='utf-8') as f:
            import re
            content = f.read()
            title_match = re.search(r'<title>(.*?)</title>', content)
            blog_title = title_match.group(1) if title_match else "Web Development Blog"
            slug = filename.replace('.html', '')
    # Generate local image
    generate_placeholder_image(blog_title, slug)
    # Update blog-data.json
    update_blog_data()
    # Update sitemap
    update_sitemap()
    print("="*80)
    print(f"✅ Blog generated: blog-list/{filename}")
    print(f"🖼️ Image: blog-img/{slug}.png")
    print(f"🔗 Slug: {slug}")
    print("🔄 blog-data.json and sitemap.xml updated!")
    print("="*80)

if __name__ == "__main__":
    main() 