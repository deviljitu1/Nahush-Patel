#!/usr/bin/env python3
"""
Blog Scanner Script
Scans the blog-list directory and extracts metadata from HTML files
to generate a JSON file for dynamic blog display.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import html

def extract_metadata_from_html(file_path):
    """Extract metadata from an HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1) if title_match else Path(file_path).stem
        
        # Extract meta description
        desc_match = re.search(r'<meta name="description" content="(.*?)"', content, re.IGNORECASE)
        description = desc_match.group(1) if desc_match else ""
        
        # Extract image from content - look for img tags with src
        img_matches = re.findall(r'<img[^>]+src="([^"]+)"[^>]*>', content)
        image = ""
        
        # Look for blog images first
        for img_src in img_matches:
            if 'blog-img' in img_src or 'blog' in img_src.lower():
                image = img_src
                break
        
        # If no blog image found, use the first image
        if not image and img_matches:
            image = img_matches[0]
        
        # Clean up image path (remove ../ if present)
        if image.startswith('../'):
            image = image[3:]
        
        # Get file modification time for sorting and date
        mtime = os.path.getmtime(file_path)
        date_obj = datetime.fromtimestamp(mtime)
        date_str = date_obj.strftime("%m/%d/%Y")
        
        # Extract first paragraph as excerpt - look for content paragraphs
        p_matches = re.findall(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
        excerpt = ""
        
        for p_content in p_matches:
            clean_content = re.sub(r'<[^>]+>', '', p_content).strip()
            clean_content = html.unescape(clean_content)
            
            # Skip if it's just copyright or navigation content
            if (len(clean_content) > 20 and 
                'copyright' not in clean_content.lower() and 
                '©' not in clean_content and
                'all rights reserved' not in clean_content.lower()):
                excerpt = clean_content
                break
        
        # Limit excerpt length
        if len(excerpt) > 200:
            excerpt = excerpt[:200] + "..."
        
        # If no good excerpt found, use description
        if not excerpt and description:
            excerpt = description[:200] + "..." if len(description) > 200 else description
        
        return {
            "title": html.unescape(title),
            "description": html.unescape(description),
            "excerpt": excerpt,
            "image": image,
            "date": date_str,
            "filename": Path(file_path).stem,
            "link": f"blog-list/{Path(file_path).stem}.html",
            "modified_time": mtime  # Add modification time for sorting
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def scan_blog_directory(blog_dir="blog-list"):
    """Scan the blog directory and extract metadata from all HTML files."""
    blogs = []
    
    if not os.path.exists(blog_dir):
        print(f"Blog directory '{blog_dir}' not found!")
        return blogs
    
    # Get all HTML files in the blog directory
    html_files = [f for f in os.listdir(blog_dir) if f.endswith('.html') and f != 'all-blogs.html']
    
    for html_file in html_files:
        file_path = os.path.join(blog_dir, html_file)
        metadata = extract_metadata_from_html(file_path)
        
        if metadata:
            blogs.append(metadata)
            print(f"Processed: {html_file} (Modified: {metadata['date']})")
    
    # Sort by modification time (newest first)
    blogs.sort(key=lambda x: x['modified_time'], reverse=True)
    
    # Remove the modification_time from final output
    for blog in blogs:
        del blog['modified_time']
    
    return blogs

def generate_blog_json(blogs, output_file="blog-data.json"):
    """Generate JSON file with blog metadata."""
    blog_data = {
        "last_updated": datetime.now().isoformat(),
        "total_blogs": len(blogs),
        "blogs": blogs
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(blog_data, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {output_file} with {len(blogs)} blogs")
    print("Blogs sorted by modification date (newest first):")
    for i, blog in enumerate(blogs, 1):
        print(f"  {i}. {blog['title']} - {blog['date']}")

def main():
    """Main function to scan blogs and generate JSON."""
    print("Scanning blog directory...")
    blogs = scan_blog_directory()
    
    if blogs:
        generate_blog_json(blogs)
        print(f"Successfully processed {len(blogs)} blog files")
    else:
        print("No blog files found!")

if __name__ == "__main__":
    main() 