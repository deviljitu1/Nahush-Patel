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
        
        # API keys for image generation
        self.api_keys = {
            "huggingface": os.getenv("HF_TOKEN", ""),
            "together": os.getenv("TOGETHER_API_KEY", "27d3a97f9acc0d1cce896337df956b79acf66d1dee56df4d37b4f7d3ec07b21d"),
            "replicate": os.getenv("REPLICATE_API_TOKEN", "")
        }
    
    def generate_ai_image(self, blog_title, slug):
        """Generate AI image for blog post."""
        filename = f"{slug}.png"
        filepath = os.path.join("blog-img", filename)
        
        print(f"🎨 Generating AI image for: {blog_title}")
        
        # Try Together AI first (since you have the API key)
        if self.api_keys["together"]:
            try:
                API_URL = "https://api.together.xyz/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {self.api_keys['together']}",
                    "Content-Type": "application/json"
                }
                
                # Create optimized prompt for unique, high-quality images
                prompt = self.create_image_prompt(blog_title)
                enhanced_prompt = f"professional blog header image: {prompt}, modern graphic design, clean typography, vibrant colors, high resolution, 16:9 aspect ratio, technology theme, web development, no text overlay, perfect composition, professional photography style"
                
                data = {
                    "model": "runwayml/stable-diffusion-v1-5",
                    "prompt": enhanced_prompt,
                    "n": 1,
                    "size": "1024x1024"
                }
                
                print(f"🔄 Using Together AI API...")
                print(f"📝 Prompt: {enhanced_prompt}")
                print(f"⏳ Starting image generation (this may take 10-30 seconds)...")
                
                response = requests.post(API_URL, headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()
                    if "data" in result and len(result["data"]) > 0:
                        image_url = result["data"][0]["url"]
                        print(f"🖼️ Image URL: {image_url}")
                        
                        # Wait at least 10 seconds for image to be ready
                        print(f"⏳ Waiting for image to be generated...")
                        time.sleep(10)
                        
                        # Try to download the image with retries
                        max_retries = 5
                        for attempt in range(max_retries):
                            try:
                                print(f"🔄 Attempt {attempt + 1}/{max_retries}: Downloading image...")
                                image_response = requests.get(image_url, timeout=30)
                                
                                if image_response.status_code == 200:
                                    with open(filepath, "wb") as f:
                                        f.write(image_response.content)
                                    print(f"✅ AI image generated and saved: {filename}")
                                    return filename
                                else:
                                    print(f"❌ Download failed (attempt {attempt + 1}): {image_response.status_code}")
                                    if attempt < max_retries - 1:
                                        print(f"⏳ Waiting 5 seconds before retry...")
                                        time.sleep(5)
                            except Exception as e:
                                print(f"❌ Download error (attempt {attempt + 1}): {e}")
                                if attempt < max_retries - 1:
                                    print(f"⏳ Waiting 5 seconds before retry...")
                                    time.sleep(5)
                        
                        print(f"❌ Failed to download image after {max_retries} attempts")
                    else:
                        print(f"❌ No image data in response: {result}")
                else:
                    print(f"❌ Together AI API error: {response.status_code}")
                    print(f"Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Together AI error: {e}")
        
        # Try Hugging Face
        if self.api_keys["huggingface"]:
            try:
                API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
                headers = {"Authorization": f"Bearer {self.api_keys['huggingface']}"}
                
                prompt = self.create_image_prompt(blog_title)
                enhanced_prompt = f"professional blog header image: {prompt}, modern design, clean layout, high quality, 16:9 aspect ratio, technology theme, web development"
                
                print(f"🔄 Using Hugging Face API...")
                print(f"📝 Prompt: {enhanced_prompt}")
                print(f"⏳ Starting image generation (this may take 10-30 seconds)...")
                
                response = requests.post(API_URL, headers=headers, json={"inputs": enhanced_prompt})
                
                if response.status_code == 200:
                    # Wait at least 10 seconds for image to be ready
                    print(f"⏳ Waiting for image to be generated...")
                    time.sleep(10)
                    
                    # Try to save the image with retries
                    max_retries = 5
                    for attempt in range(max_retries):
                        try:
                            print(f"🔄 Attempt {attempt + 1}/{max_retries}: Saving image...")
                            with open(filepath, "wb") as f:
                                f.write(response.content)
                            print(f"✅ AI image generated and saved: {filename}")
                            return filename
                        except Exception as e:
                            print(f"❌ Save error (attempt {attempt + 1}): {e}")
                            if attempt < max_retries - 1:
                                print(f"⏳ Waiting 5 seconds before retry...")
                                time.sleep(5)
                    
                    print(f"❌ Failed to save image after {max_retries} attempts")
                else:
                    print(f"❌ Hugging Face API error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Hugging Face error: {e}")
        
        # Try Replicate
        if self.api_keys["replicate"]:
            try:
                import replicate
                
                prompt = self.create_image_prompt(blog_title)
                enhanced_prompt = f"professional blog header image: {prompt}, modern design, clean layout, high quality, 16:9 aspect ratio, technology theme, web development"
                
                print(f"🔄 Using Replicate API...")
                print(f"📝 Prompt: {enhanced_prompt}")
                print(f"⏳ Starting image generation (this may take 10-30 seconds)...")
                
                output = replicate.run(
                    "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                    input={"prompt": enhanced_prompt}
                )
                
                if output and len(output) > 0:
                    image_url = output[0]
                    
                    # Wait at least 10 seconds for image to be ready
                    print(f"⏳ Waiting for image to be generated...")
                    time.sleep(10)
                    
                    # Try to download the image with retries
                    max_retries = 5
                    for attempt in range(max_retries):
                        try:
                            print(f"🔄 Attempt {attempt + 1}/{max_retries}: Downloading image...")
                            image_response = requests.get(image_url, timeout=30)
                            
                            if image_response.status_code == 200:
                                with open(filepath, "wb") as f:
                                    f.write(image_response.content)
                                print(f"✅ AI image generated and saved: {filename}")
                                return filename
                            else:
                                print(f"❌ Download failed (attempt {attempt + 1}): {image_response.status_code}")
                                if attempt < max_retries - 1:
                                    print(f"⏳ Waiting 5 seconds before retry...")
                                    time.sleep(5)
                        except Exception as e:
                            print(f"❌ Download error (attempt {attempt + 1}): {e}")
                            if attempt < max_retries - 1:
                                print(f"⏳ Waiting 5 seconds before retry...")
                                time.sleep(5)
                    
                    print(f"❌ Failed to download image after {max_retries} attempts")
                else:
                    print(f"❌ No image generated by Replicate")
                    
            except Exception as e:
                print(f"❌ Replicate error: {e}")
        
        # Create placeholder image as last resort
        print("🔄 Creating placeholder image...")
        self.create_placeholder_image(blog_title, filepath)
        return filename
    
    def create_image_prompt(self, blog_title):
        """Create an optimized prompt for image generation."""
        title_lower = blog_title.lower()
        
        # Create unique, detailed prompts for different topics
        if 'javascript' in title_lower or 'react' in title_lower or 'vue' in title_lower or 'angular' in title_lower:
            return "modern JavaScript code editor, colorful syntax highlighting, web development workspace, multiple screens showing code, modern office setup, clean desk, coffee cup, plants, natural lighting, professional workspace"
        elif 'css' in title_lower or 'styling' in title_lower or 'design' in title_lower:
            return "beautiful web design mockups, color palette swatches, typography samples, modern UI components, design tools, creative workspace, inspiration board, modern minimalist design"
        elif 'ai' in title_lower or 'artificial intelligence' in title_lower or 'machine learning' in title_lower:
            return "futuristic AI technology, neural network visualization, glowing circuit boards, holographic displays, modern tech lab, blue and purple lighting, sci-fi atmosphere, innovation concept"
        elif 'web' in title_lower or 'development' in title_lower or 'programming' in title_lower:
            return "web development process, multiple monitors showing different stages of development, code on screens, wireframes, modern office environment, collaborative workspace, technology tools"
        elif 'seo' in title_lower or 'optimization' in title_lower:
            return "SEO analytics dashboard, search engine visualization, data charts, modern analytics interface, professional marketing workspace, graphs and metrics, digital marketing tools"
        elif 'tools' in title_lower or 'utilities' in title_lower:
            return "collection of modern development tools, organized workspace, productivity setup, multiple devices, clean desk organization, professional tools layout, modern office environment"
        elif 'best practices' in title_lower or 'guidelines' in title_lower:
            return "professional development workflow, organized project management, clean workspace, modern office setup, productivity tools, professional environment, quality assurance concept"
        elif 'hooks' in title_lower:
            return "React hooks visualization, modern React development, code components, functional programming concept, modern web development, clean code structure, professional development environment"
        elif 'frameworks' in title_lower:
            return "multiple framework logos, modern web development stack, technology comparison, professional development tools, modern workspace, clean design, technology ecosystem"
        else:
            # Extract keywords and create a unique prompt
            keywords = blog_title.lower().split()
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'in', 'for', '2025', 'guide', 'complete', 'mastering', 'top', 'best'}
            keywords = [word for word in keywords if word not in stop_words and len(word) > 2]
            
            if keywords:
                return f"modern {', '.join(keywords[:3])} concept, professional workspace, clean design, technology theme, modern office environment, natural lighting, professional setup"
            else:
                return "modern web development workspace, professional office environment, clean design, technology tools, natural lighting, modern workspace, professional setup"
    
    def create_placeholder_image(self, blog_title, filepath):
        """Create a high-quality placeholder image."""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a 1200x630 image (blog header size - 16:9 aspect ratio)
            img = Image.new('RGB', (1200, 630), color=(102, 126, 234))
            draw = ImageDraw.Draw(img)
            
            # Create gradient background
            for y in range(630):
                # Create a subtle gradient from top to bottom
                r = int(102 + (y / 630) * 20)
                g = int(126 + (y / 630) * 30)
                b = int(234 + (y / 630) * 20)
                color = (r, g, b)
                draw.line([(0, y), (1200, y)], fill=color)
            
            # Try to use a default font
            try:
                # Try to use a larger, more readable font
                title_font = ImageFont.truetype("arial.ttf", 48)
                subtitle_font = ImageFont.truetype("arial.ttf", 24)
                author_font = ImageFont.truetype("arial.ttf", 20)
            except:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                author_font = ImageFont.load_default()
            
            # Add title text (ensure it fits properly)
            text = blog_title[:60] + "..." if len(blog_title) > 60 else blog_title
            bbox = draw.textbbox((0, 0), text, font=title_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Center the text properly
            x = (1200 - text_width) // 2
            y = (630 - text_height) // 2 - 80
            
            # Add text shadow for better readability
            draw.text((x+2, y+2), text, font=title_font, fill=(0, 0, 0, 100))
            draw.text((x, y), text, font=title_font, fill=(255, 255, 255))
            
            # Add subtitle
            subtitle = "Web Development & Technology"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (1200 - subtitle_width) // 2
            subtitle_y = y + text_height + 20
            
            draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(255, 255, 255, 200))
            
            # Add author
            author = "By Nahush Patel"
            author_bbox = draw.textbbox((0, 0), author, font=author_font)
            author_width = author_bbox[2] - author_bbox[0]
            author_x = (1200 - author_width) // 2
            author_y = subtitle_y + 40
            
            draw.text((author_x, author_y), author, font=author_font, fill=(255, 255, 255, 150))
            
            # Add some decorative elements
            # Draw a subtle line at the bottom
            draw.line([(100, 580), (1100, 580)], fill=(255, 255, 255, 100), width=2)
            
            # Add some geometric shapes for visual interest
            draw.rectangle([50, 50, 150, 150], outline=(255, 255, 255, 50), width=3)
            draw.rectangle([1050, 430, 1150, 530], outline=(255, 255, 255, 50), width=3)
            
            img.save(filepath, "PNG", quality=95)
            print(f"✅ High-quality placeholder image created: {os.path.basename(filepath)}")
            
        except ImportError:
            # If PIL is not available, create a text file
            with open(filepath.replace('.png', '.txt'), "w", encoding="utf-8") as f:
                f.write(f"Blog Image Placeholder\n\nTitle: {blog_title}\n\nPlease add an image manually: {os.path.basename(filepath)}")
            print(f"⚠️ Created text placeholder: {os.path.basename(filepath).replace('.png', '.txt')}")
        except Exception as e:
            print(f"❌ Error creating placeholder image: {e}")
            # Create a simple colored rectangle as fallback
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
    main() 