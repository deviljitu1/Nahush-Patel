#!/usr/bin/env python3
"""
Automated Blog Generator
Creates SEO-friendly blog posts with proper metadata and structure.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import random

class BlogGenerator:
    def __init__(self):
        self.blog_dir = "blog-list"
        self.blog_img_dir = "blog-img"
        self.blog_counter = self.get_next_blog_number()
        
        # SEO-friendly topics for web development
        self.topics = [
            {
                "title": "10 Essential JavaScript Tips Every Developer Should Know",
                "description": "Master these crucial JavaScript techniques to write cleaner, more efficient code and improve your web development skills.",
                "keywords": "JavaScript tips, web development, coding best practices, JS optimization",
                "content_sections": [
                    "Understanding JavaScript Fundamentals",
                    "Modern ES6+ Features You Should Use",
                    "Performance Optimization Techniques",
                    "Common Pitfalls to Avoid",
                    "Best Practices for Clean Code"
                ]
            },
            {
                "title": "Complete Guide to CSS Grid Layout in 2025",
                "description": "Learn how to create responsive, flexible layouts using CSS Grid. Master modern web design techniques for better user experiences.",
                "keywords": "CSS Grid, responsive design, web layout, modern CSS, frontend development",
                "content_sections": [
                    "Understanding CSS Grid Basics",
                    "Creating Responsive Grid Layouts",
                    "Grid vs Flexbox: When to Use Each",
                    "Advanced Grid Techniques",
                    "Real-World Examples and Use Cases"
                ]
            },
            {
                "title": "React Performance Optimization: A Developer's Guide",
                "description": "Discover proven techniques to optimize React applications for better performance, faster loading times, and improved user experience.",
                "keywords": "React optimization, performance, frontend development, React hooks, web performance",
                "content_sections": [
                    "Understanding React Rendering",
                    "Optimizing Component Re-renders",
                    "Code Splitting and Lazy Loading",
                    "Memory Management Best Practices",
                    "Performance Monitoring Tools"
                ]
            },
            {
                "title": "SEO Best Practices for Web Developers in 2025",
                "description": "Learn essential SEO techniques that every web developer should implement to improve website visibility and search engine rankings.",
                "keywords": "SEO, search engine optimization, web development, technical SEO, on-page SEO",
                "content_sections": [
                    "Technical SEO Fundamentals",
                    "On-Page Optimization Techniques",
                    "Mobile-First Indexing",
                    "Core Web Vitals Optimization",
                    "Structured Data Implementation"
                ]
            },
            {
                "title": "Building Scalable Web Applications with Node.js",
                "description": "Explore advanced Node.js patterns and architectures for building scalable, maintainable web applications that can handle high traffic.",
                "keywords": "Node.js, backend development, scalable applications, server architecture, web development",
                "content_sections": [
                    "Node.js Architecture Patterns",
                    "Database Design and Optimization",
                    "API Design Best Practices",
                    "Security Implementation",
                    "Deployment and Monitoring"
                ]
            }
        ]

    def get_next_blog_number(self):
        """Get the next available blog number."""
        if not os.path.exists(self.blog_dir):
            return 1
        
        existing_files = [f for f in os.listdir(self.blog_dir) if f.startswith('blog') and f.endswith('.html')]
        if not existing_files:
            return 1
        
        numbers = []
        for file in existing_files:
            match = re.search(r'blog(\d+)\.html', file)
            if match:
                numbers.append(int(match.group(1)))
        
        return max(numbers) + 1 if numbers else 1

    def generate_blog_content(self, topic):
        """Generate comprehensive blog content based on the topic."""
        content = f"""
        <p>Welcome to this comprehensive guide on <strong>{topic['title'].split(':')[0]}</strong> by Nahush Patel. In today's rapidly evolving web development landscape, staying updated with the latest techniques and best practices is crucial for building modern, efficient applications.</p>
        
        <p>This guide will walk you through essential concepts, practical examples, and real-world applications that will help you enhance your development skills and create better web experiences.</p>
        """
        
        for i, section in enumerate(topic['content_sections'], 1):
            content += f"""
            <h3>{section}</h3>
            <p>This section covers the fundamental aspects of {section.lower()}. Understanding these concepts is essential for any developer looking to improve their skills in this area.</p>
            
            <p>Let's dive deep into the practical implementation and explore various approaches that can help you master these techniques. We'll also look at common challenges and how to overcome them effectively.</p>
            """
            
            # Add some variety to content
            if i % 2 == 0:
                content += """
                <p>Remember, the key to mastering these concepts is consistent practice and real-world application. Don't just read about these techniques—implement them in your projects to truly understand their value.</p>
                """
        
        content += f"""
        <h3>Conclusion</h3>
        <p>We've covered a lot of ground in this comprehensive guide on {topic['title'].split(':')[0]}. These techniques and best practices will help you become a more proficient developer and create better web applications.</p>
        
        <p>Remember that web development is a continuous learning journey. Stay curious, keep experimenting, and always be open to new approaches and technologies. The skills you've learned here will serve as a solid foundation for your future projects.</p>
        
        <p>Thank you for reading this guide. If you found it helpful, consider sharing it with fellow developers who might benefit from these insights. Stay tuned for more in-depth tutorials and practical guides on web development.</p>
        """
        
        return content

    def create_blog_file(self, topic):
        """Create a new blog HTML file with the given topic."""
        filename = f"blog{self.blog_counter}.html"
        filepath = os.path.join(self.blog_dir, filename)
        
        # Generate content
        content = self.generate_blog_content(topic)
        
        # Create the HTML file
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{topic['title']} | Nahush Patel</title>
  <meta name="description" content="{topic['description']}" />
  <meta name="keywords" content="{topic['keywords']}" />
  <meta name="author" content="Nahush Patel" />
  <meta property="og:title" content="{topic['title']}" />
  <meta property="og:description" content="{topic['description']}" />
  <meta property="og:type" content="article" />
  <meta property="og:author" content="Nahush Patel" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{topic['title']}" />
  <meta name="twitter:description" content="{topic['description']}" />
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="../css/blog.css">
</head>
<body>
  <nav class="navbar">
    <div class="logo">Nahush</div>
    <ul class="nav-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../blog.html" class="active">Blog</a></li>
    </ul>
    <div id="toggleMode" style="cursor: pointer;">
      <img src="../img/moon-icon.png" id="darkIcon" alt="Dark Mode" style="width: 20px; height: 20px;">
      <img src="../img/sun-icon.png" id="lightIcon" alt="Light Mode" style="width: 20px; height: 20px; display: none;">
    </div>
  </nav>

  <div class="content-container" id="blogContent">
    <h1>{topic['title']}</h1>
    <img src="../blog-img/blog{self.blog_counter}-image.png" alt="{topic['title']}" style="width: 100%; border-radius: 10px; margin-bottom: 1.5em;">
    
    {content}
  </div>

  <div class="suggested-blogs" id="suggestedBlogs">
    <h2>Suggested Blogs</h2>
    <!-- Suggested blogs will be dynamically populated here -->
  </div>

  <section id="footer" class="footer-container">
    <p>&copy; 2025 <span class="name-gradient"><a href="#hero">Nahush Patel</a></span>. All rights reserved.</p>
  </section>

  <script src="../js/darkmode.js"></script>
  <script src="../js/blog.js"></script>
</body>
</html>"""
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename

    def generate_daily_blog(self):
        """Generate a new blog post for today."""
        print("🎯 Generating today's SEO-friendly blog post...")
        
        # Select a random topic
        topic = random.choice(self.topics)
        
        # Create the blog file
        filename = self.create_blog_file(topic)
        
        print(f"✅ Blog created: {filename}")
        print(f"📝 Title: {topic['title']}")
        print(f"🔍 Keywords: {topic['keywords']}")
        print(f"📅 Published: {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}")
        
        # Update the blog data
        self.update_blog_data()
        
        return filename

    def update_blog_data(self):
        """Update the blog-data.json file."""
        try:
            # Run the blog scanner to update the JSON
            os.system("python scripts/blog_scanner.py")
            print("🔄 Blog data updated successfully!")
        except Exception as e:
            print(f"❌ Error updating blog data: {e}")

def main():
    """Main function to generate a daily blog."""
    generator = BlogGenerator()
    
    print("=" * 60)
    print("🚀 AUTOMATED BLOG GENERATOR")
    print("=" * 60)
    
    # Generate today's blog
    filename = generator.generate_daily_blog()
    
    print("\n" + "=" * 60)
    print("✅ BLOG GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📄 File created: blog-list/{filename}")
    print("🔍 SEO optimized with proper metadata")
    print("📱 Mobile-friendly and responsive")
    print("🎨 Styled with your existing theme")
    print("\n💡 Next steps:")
    print("   1. Review the generated content")
    print("   2. Add your personal insights")
    print("   3. Update images if needed")
    print("   4. Run 'update_blogs.bat' to refresh")
    print("=" * 60)

if __name__ == "__main__":
    main() 