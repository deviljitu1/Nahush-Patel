#!/usr/bin/env python3
"""
Automated Blog System with AI Image Generation
Complete automation for generating blogs with AI-generated images.
Can be run manually or via GitHub Actions for automatic posting.
"""

import os
import sys
import random
import json
from datetime import datetime, timedelta
import requests
import time

# Import our existing generators
from seo_blog_generator import SEOBlogGenerator
from advanced_blog_generator import AdvancedBlogGenerator
from blog_generator import BlogGenerator

class AutomatedBlogSystem:
    def __init__(self):
        self.seo_generator = SEOBlogGenerator()
        self.advanced_generator = AdvancedBlogGenerator()
        self.basic_generator = BlogGenerator()
        
        # Blog generation schedule (3 times per week)
        self.schedule = {
            "monday": "advanced",      # Advanced blog with code examples
            "wednesday": "seo",        # SEO-optimized blog
            "friday": "basic"          # Simple daily blog
        }
    
    def generate_ai_image(self, blog_title, slug):
        """Generate placeholder image for blog post (no API)."""
        filename = f"{slug}.png"
        filepath = os.path.join("blog-img", filename)
        print(f"🎨 Generating placeholder image for: {blog_title}")
        self.create_placeholder_image(blog_title, filepath)
        return filename
    
    def create_placeholder_image(self, blog_title, filepath):
        """Create a high-quality placeholder image with wrapped title text."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import textwrap

            # Create a 1200x630 image (blog header size - 16:9 aspect ratio)
            img = Image.new('RGB', (1200, 630), color=(102, 126, 234))
            draw = ImageDraw.Draw(img)

            # Create gradient background
            for y in range(630):
                r = int(102 + (y / 630) * 20)
                g = int(126 + (y / 630) * 30)
                b = int(234 + (y / 630) * 20)
                color = (r, g, b)
                draw.line([(0, y), (1200, y)], fill=color)

            # Try to use a default font
            try:
                title_font = ImageFont.truetype("arial.ttf", 48)
                subtitle_font = ImageFont.truetype("arial.ttf", 24)
                author_font = ImageFont.truetype("arial.ttf", 20)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                author_font = ImageFont.load_default()

            # Wrap title text to fit within image width
            max_width = 1100
            lines = []
            if hasattr(draw, 'textlength'):
                # PIL >= 8.0.0
                for line in textwrap.wrap(blog_title, width=40):
                    while draw.textlength(line, font=title_font) > max_width and len(line) > 0:
                        line = line[:-1]
                    lines.append(line)
            else:
                # Fallback for older PIL
                for line in textwrap.wrap(blog_title, width=40):
                    while draw.textsize(line, font=title_font)[0] > max_width and len(line) > 0:
                        line = line[:-1]
                    lines.append(line)

            # Calculate total height of wrapped text
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), 'A', font=title_font)
                line_height = bbox[3] - bbox[1] + 8
            else:
                line_height = draw.textsize('A', font=title_font)[1] + 8
            total_text_height = line_height * len(lines)
            y = (630 - total_text_height) // 2 - 80

            # Draw each line of the title, centered
            for line in lines:
                if hasattr(draw, 'textlength'):
                    text_width = draw.textlength(line, font=title_font)
                else:
                    text_width = draw.textsize(line, font=title_font)[0]
                x = (1200 - text_width) // 2
                draw.text((x+2, y+2), line, font=title_font, fill=(0, 0, 0, 100))
                draw.text((x, y), line, font=title_font, fill=(255, 255, 255))
                y += line_height

            # Add subtitle
            subtitle = "Web Development & Technology"
            if hasattr(draw, 'textlength'):
                subtitle_width = draw.textlength(subtitle, font=subtitle_font)
            else:
                subtitle_width = draw.textsize(subtitle, font=subtitle_font)[0]
            subtitle_x = (1200 - subtitle_width) // 2
            subtitle_y = y + 10
            draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(255, 255, 255, 200))

            # Add author
            author = "By Nahush Patel"
            if hasattr(draw, 'textlength'):
                author_width = draw.textlength(author, font=author_font)
            else:
                author_width = draw.textsize(author, font=author_font)[0]
            author_x = (1200 - author_width) // 2
            author_y = subtitle_y + 40
            draw.text((author_x, author_y), author, font=author_font, fill=(255, 255, 255, 150))

            # Add some decorative elements
            draw.line([(100, 580), (1100, 580)], fill=(255, 255, 255, 100), width=2)
            draw.rectangle([50, 50, 150, 150], outline=(255, 255, 255, 50), width=3)
            draw.rectangle([1050, 430, 1150, 530], outline=(255, 255, 255, 50), width=3)

            img.save(filepath, "PNG", quality=95)
            print(f"✅ High-quality placeholder image created: {os.path.basename(filepath)}")

        except ImportError:
            with open(filepath.replace('.png', '.txt'), "w", encoding="utf-8") as f:
                f.write(f"Blog Image Placeholder\n\nTitle: {blog_title}\n\nPlease add an image manually: {os.path.basename(filepath)}")
            print(f"⚠️ Created text placeholder: {os.path.basename(filepath).replace('.png', '.txt')}")
        except Exception as e:
            print(f"❌ Error creating placeholder image: {e}")
            try:
                img = Image.new('RGB', (1200, 630), color=(102, 126, 234))
                img.save(filepath, "PNG")
                print(f"✅ Simple placeholder created: {os.path.basename(filepath)}")
            except:
                print(f"❌ Failed to create any placeholder image")
    
    def determine_blog_type(self):
        """Determine which type of blog to generate based on day of week."""
        today = datetime.now().strftime("%A").lower()
        
        if today in self.schedule:
            return self.schedule[today]
        else:
            # Default to basic blog for other days
            return "basic"
    
    def generate_blog_with_image(self, blog_type=None):
        """Generate a blog post with AI image."""
        if blog_type is None:
            blog_type = self.determine_blog_type()
        
        print(f"🚀 Generating {blog_type} blog post...")
        
        # Generate blog content
        if blog_type == "seo":
            generator = self.seo_generator
            topic = random.choice(generator.topics)
            filename = generator.create_blog_file(topic)
            blog_title = topic['title']
            slug = topic['slug']
            
        elif blog_type == "advanced":
            generator = self.advanced_generator
            topic = random.choice(generator.topics)
            filename = generator.create_blog_file(topic)
            blog_title = topic['title']
            slug = topic['slug']
            
        else:  # basic
            generator = self.basic_generator
            filename = generator.generate_daily_blog()
            # Extract title from generated file
            with open(os.path.join("blog-list", filename), 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract title from meta tag
                import re
                title_match = re.search(r'<title>(.*?)</title>', content)
                blog_title = title_match.group(1) if title_match else "Web Development Blog"
                slug = filename.replace('.html', '')
        
        # Generate AI image
        image_filename = self.generate_ai_image(blog_title, slug)
        
        # Update blog data
        try:
            os.system("python scripts/blog_scanner.py")
            print("🔄 Blog data updated successfully!")
        except Exception as e:
            print(f"❌ Error updating blog data: {e}")
        
        return {
            "filename": filename,
            "title": blog_title,
            "slug": slug,
            "image": image_filename,
            "type": blog_type
        }
    
    def run_automated_system(self):
        """Run the complete automated blog system."""
        print("=" * 80)
        print("🤖 AUTOMATED BLOG SYSTEM")
        print("=" * 80)
        
        # Check if we should generate a blog today
        today = datetime.now().strftime("%A").lower()
        
        if today in self.schedule:
            print(f"📅 Today is {today.capitalize()} - scheduled for {self.schedule[today]} blog")
            
            # Generate blog with image
            result = self.generate_blog_with_image()
            
            print("\n" + "=" * 80)
            print("✅ AUTOMATED BLOG GENERATION COMPLETE!")
            print("=" * 80)
            print(f"📄 Blog file: {result['filename']}")
            print(f"📝 Title: {result['title']}")
            print(f"🖼️ Image: {result['image']}")
            print(f"🏷️ Type: {result['type']}")
            print(f"📅 Generated: {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}")
            
            # Save result for GitHub Actions
            with open("blog_generation_result.json", "w") as f:
                json.dump(result, f, indent=2)
            
            return result
            
        else:
            print(f"📅 Today is {today.capitalize()} - no blog scheduled")
            print("📅 Scheduled days: Monday (Advanced), Wednesday (SEO), Friday (Basic)")
            return None

def main():
    """Main function for automated blog system."""
    system = AutomatedBlogSystem()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        blog_type = sys.argv[1]
        if blog_type in ["seo", "advanced", "basic"]:
            result = system.generate_blog_with_image(blog_type)
        else:
            print(f"❌ Invalid blog type: {blog_type}")
            print("Valid types: seo, advanced, basic")
            return
    else:
        # Run automated system
        result = system.run_automated_system()
    
    if result:
        print("\n🎉 Blog generation successful!")
        print("🚀 Your blog is now live and SEO-ready!")
    else:
        print("\n⏰ No blog scheduled for today.")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "generate_image":
        # Usage: python automated_blog_system.py generate_image "Blog Title" slug
        blog_title = sys.argv[2]
        slug = sys.argv[3] if len(sys.argv) > 3 else blog_title.lower().replace(' ', '-').replace(':', '').replace(',', '')
        system = AutomatedBlogSystem()
        system.generate_ai_image(blog_title, slug)
    else:
        main() 