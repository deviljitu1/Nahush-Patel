#!/usr/bin/env python3
"""
SEO-Optimized Blog Generator
Creates blogs with SEO-friendly URLs, comprehensive schema markup, and proper structured data.
Matches the blog1.html structure exactly with dynamic suggested blogs sidebar.
Uses the existing style.css file for all styling.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import random

class SEOBlogGenerator:
    def __init__(self):
        self.blog_dir = "blog-list"
        self.blog_img_dir = "blog-img"
        
        # SEO-optimized topics with proper slugs
        self.topics = [
            {
                "title": "Best AI Tools for Web Developers in 2025",
                "slug": "best-ai-tools-for-web-developers-2025",
                "description": "Discover the top AI tools that every web developer should use in 2025. From code generation to testing automation, these tools will revolutionize your workflow.",
                "keywords": "AI tools, web development, developer tools, artificial intelligence, coding automation, 2025",
                "schema_type": "HowTo",
                "content": """
                <p>Welcome to this comprehensive guide on <strong>AI tools for web developers</strong> by Nahush Patel. In today's rapidly evolving web development landscape, artificial intelligence has become an indispensable part of the development workflow.</p>

                <h3>AI-Powered Code Generation Tools</h3>
                <p>AI-powered code generation has become a game-changer for web developers. These tools can help you write code faster, reduce bugs, and improve overall productivity by providing intelligent suggestions and automating repetitive tasks.</p>

                <h3>GitHub Copilot: The Game Changer</h3>
                <p>GitHub Copilot is one of the most popular AI coding assistants available today. It provides real-time code suggestions based on your comments and existing code context, making it feel like you have a pair programming partner available 24/7.</p>

                <h3>Amazon CodeWhisperer: Enterprise AI Coding</h3>
                <p>Amazon's AI coding companion offers intelligent code suggestions and helps with security scanning and code optimization. It's particularly useful for AWS-based projects and enterprise development environments.</p>

                <h3>AI Testing and Quality Assurance</h3>
                <p>AI has revolutionized testing by automating repetitive tasks and identifying potential issues before they reach production. Tools like Testim and Applitools use machine learning to create and maintain automated tests.</p>

                <h3>AI Design and Prototyping Tools</h3>
                <p>AI is transforming the design process, making it faster and more efficient for developers and designers to create stunning user interfaces. Figma AI and Adobe Firefly are leading the charge in AI-powered design.</p>

                <h3>Future of AI in Web Development</h3>
                <p>As AI technology continues to evolve, we can expect even more sophisticated tools that will further streamline the development process. From automated debugging to intelligent code reviews, the future of web development is increasingly AI-driven.</p>

                <p>Thanks for reading this guide on <strong>AI tools for web developers</strong>. Stay tuned for more insights and practical advice on leveraging AI in your development workflow.</p>
                """
            },
            {
                "title": "Top JavaScript Frameworks to Learn in 2025",
                "slug": "top-javascript-frameworks-to-learn-2025",
                "description": "Explore the most in-demand JavaScript frameworks for 2025. Learn which frameworks are worth your time and how to choose the right one for your projects.",
                "keywords": "JavaScript frameworks, React, Vue, Angular, frontend development, 2025, web development",
                "schema_type": "Article",
                "content": """
                <p>Welcome to this comprehensive guide on <strong>JavaScript frameworks</strong> by Nahush Patel. In today's rapidly evolving web development landscape, choosing the right JavaScript framework is crucial for building modern, efficient applications.</p>

                <h3>React: Still the King of Frontend</h3>
                <p>React continues to dominate the frontend landscape with its component-based architecture and extensive ecosystem. Its virtual DOM, reusable components, and strong community support make it an excellent choice for building dynamic user interfaces.</p>

                <h3>Why React Remains Popular</h3>
                <p>React's popularity stems from its large community, extensive documentation, excellent performance with React 18 features, and strong ecosystem with tools like Next.js. The high demand for React developers in the job market also makes it a valuable skill to learn.</p>

                <h3>Vue.js: The Progressive Framework</h3>
                <p>Vue.js offers a gentle learning curve while providing powerful features for building modern web applications. Its progressive nature allows developers to adopt it incrementally, making it perfect for both small and large projects.</p>

                <h3>Vue 3 Composition API</h3>
                <p>The Composition API provides better TypeScript support and more flexible code organization patterns. It allows for better logic reuse and more intuitive component composition, making Vue 3 a significant improvement over its predecessor.</p>

                <h3>Angular: Enterprise-Ready Framework</h3>
                <p>Angular provides a comprehensive solution for large-scale applications with built-in tools and best practices. Its TypeScript-first approach, dependency injection, and comprehensive testing utilities make it ideal for enterprise applications.</p>

                <h3>Choosing the Right Framework</h3>
                <p>When choosing a JavaScript framework, consider factors like project requirements, team expertise, learning curve, and long-term maintenance. Each framework has its strengths, and the best choice depends on your specific use case.</p>

                <p>Thanks for reading this guide on <strong>JavaScript frameworks</strong>. Stay tuned for more insights and practical advice on modern web development.</p>
                """
            }
        ]

    def generate_schema_markup(self, topic, published_date, published_time):
        """Generate comprehensive schema markup for SEO."""
        if topic['schema_type'] == 'HowTo':
            schema = {
                "@context": "https://schema.org",
                "@type": "HowTo",
                "name": topic['title'],
                "description": topic['description'],
                "image": f"https://nahushpatel.in/blog-img/{topic['slug']}.png",
                "author": {
                    "@type": "Person",
                    "name": "Nahush Patel",
                    "url": "https://nahushpatel.in"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Nahush Patel",
                    "url": "https://nahushpatel.in"
                },
                "datePublished": f"{published_date}T{published_time}",
                "dateModified": f"{published_date}T{published_time}",
                "mainEntity": {
                    "@type": "HowTo",
                    "name": topic['title'],
                    "description": topic['description'],
                    "step": []
                }
            }
            
            # Add steps based on content sections
            content_sections = re.findall(r'<h3>(.*?)</h3>', topic['content'])
            for i, section in enumerate(content_sections, 1):
                schema["mainEntity"]["step"].append({
                    "@type": "HowToStep",
                    "position": i,
                    "name": section,
                    "text": f"Learn about {section.lower()} in this comprehensive guide."
                })
                
        else:  # Article schema
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": topic['title'],
                "description": topic['description'],
                "image": f"https://nahushpatel.in/blog-img/{topic['slug']}.png",
                "author": {
                    "@type": "Person",
                    "name": "Nahush Patel",
                    "url": "https://nahushpatel.in"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Nahush Patel",
                    "url": "https://nahushpatel.in"
                },
                "datePublished": f"{published_date}T{published_time}",
                "dateModified": f"{published_date}T{published_time}",
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": f"https://nahushpatel.in/blog-list/{topic['slug']}.html"
                },
                "keywords": topic['keywords'],
                "articleSection": "Web Development",
                "inLanguage": "en-US"
            }
        
        return json.dumps(schema, indent=2)

    def create_blog_file(self, topic):
        """Create a new blog HTML file matching blog1.html structure exactly."""
        filename = f"{topic['slug']}.html"
        filepath = os.path.join(self.blog_dir, filename)
        
        # Get current date and time
        now = datetime.now()
        published_date = now.strftime("%Y-%m-%d")
        published_time = now.strftime("%H:%M:%S")
        
        # Generate schema markup
        schema_markup = self.generate_schema_markup(topic, published_date, published_time)
        
        # Create the HTML file matching blog1.html structure
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{topic['title']}</title>
  <meta name="description" content="{topic['description']}" />
  <meta name="keywords" content="{topic['keywords']}" />
  <meta name="author" content="Nahush Patel" />
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />
  <meta property="og:title" content="{topic['title']}" />
  <meta property="og:description" content="{topic['description']}" />
  <meta property="og:type" content="article" />
  <meta property="og:author" content="Nahush Patel" />
  <meta property="og:url" content="https://nahushpatel.in/blog-list/{filename}" />
  <meta property="og:image" content="https://nahushpatel.in/blog-img/{topic['slug']}.png" />
  <meta property="og:site_name" content="Nahush Patel" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{topic['title']}" />
  <meta name="twitter:description" content="{topic['description']}" />
  <meta name="twitter:image" content="https://nahushpatel.in/blog-img/{topic['slug']}.png" />
  <meta name="twitter:creator" content="@nahushpatel" />
  <link rel="canonical" href="https://nahushpatel.in/blog-list/{filename}" />
  <link rel="author" href="https://nahushpatel.in" />
  <link rel="publisher" href="https://nahushpatel.in" />
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
  
  <!-- Schema.org structured data -->
  <script type="application/ld+json">
{schema_markup}
  </script>
</head>
<body>
  <nav class="navbar">
    <div class="logo">Nahush</div>
    <ul class="nav-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="blog.html" class="active">Blog</a></li>
    </ul>
    <div id="toggleMode" style="cursor: pointer;">
      <img src="../img/moon-icon.png" id="darkIcon" alt="Dark Mode" style="width: 20px; height: 20px;">
      <img src="../img/sun-icon.png" id="lightIcon" alt="Light Mode" style="width: 20px; height: 20px; display: none;">
    </div>
  </nav>

  <div class="main-container">
    <div class="content-container" id="blogContent">
      <h1>Blog Post: {topic['title']}</h1>
      <img src="blog-img/{topic['slug']}.png" alt="{topic['title']}" style="width: 100%; border-radius: 10px; margin-bottom: 1.5em;">
      {topic['content']}
    </div>

    <div class="suggested-blogs" id="suggestedBlogs">
      <div class="search-bar">
        <input type="text" id="searchInput" placeholder="Search blogs..." />
        <button id="searchButton">Search</button>
      </div>
      <!-- Social Media Icons -->
      <div class="social-icons">
        <a href="https://twitter.com" target="_blank" class="icon">
          <i class="fab fa-twitter"></i>
        </a>
        <a href="https://facebook.com" target="_blank" class="icon">
          <i class="fab fa-facebook-f"></i>
        </a>
        <a href="https://linkedin.com" target="_blank" class="icon">
          <i class="fab fa-linkedin-in"></i>
        </a>
        <a href="https://instagram.com" target="_blank" class="icon">
          <i class="fab fa-instagram"></i>
        </a>
      </div>
      <div class="search-results" id="searchResults">
        <!-- Search results dynamically populated here -->
      </div>
      <h2>Suggested Blogs</h2>
      <!-- Suggested blogs will be dynamically populated here -->
    </div>
  </div>

  <section id="footer" class="footer-container">
    <p>&copy; 2025 <span class="name-gradient"><a href="#hero">Nahush Patel</a></span>. All rights reserved.</p>
  </section>

  <script>
    // Dynamic blog content
    const blogData = {{
      title: "{topic['title']}",
      image: "blog-img/{topic['slug']}.png",
      content: `{topic['content']}`
    }};

    // Function to load suggested blogs dynamically (excluding current blog)
    const loadSuggestedBlogs = async () => {{
      try {{
        const response = await fetch('../blog-data.json');
        const data = await response.json();
        
        // Filter out the current blog and get the latest 3 blogs
        const currentBlogSlug = '{topic['slug']}';
        const filteredBlogs = data.blogs
          .filter(blog => !blog.filename.includes(currentBlogSlug))
          .slice(0, 3);
        
        const suggestedBlogsContainer = document.getElementById('suggestedBlogs');
        const suggestedBlogsTitle = suggestedBlogsContainer.querySelector('h2');
        
        // Clear existing suggested blogs (except the title)
        const existingCards = suggestedBlogsContainer.querySelectorAll('.blog-card');
        existingCards.forEach(card => card.remove());
        
        // Add new suggested blogs
        filteredBlogs.forEach(blog => {{
          const blogCard = document.createElement('div');
          blogCard.classList.add('blog-card');
          blogCard.innerHTML = `
            <img src="${{blog.image}}" alt="${{blog.title}}">
            <div class="blog-card-content">
              <h3>${{blog.title}}</h3>
              <p>${{blog.description}}</p>
              <a href="${{blog.link}}">Read More</a>
            </div>
          `;
          suggestedBlogsContainer.appendChild(blogCard);
        }});
      }} catch (error) {{
        console.error('Error loading suggested blogs:', error);
      }}
    }};

    // Function to handle "Continue Reading" functionality
    const handleReadMore = () => {{
      const paragraphs = document.querySelectorAll('.content-container p');
      const readMoreBtn = document.getElementById('readMoreBtn');

      if (readMoreBtn.dataset.expanded === "false") {{
        paragraphs.forEach((p, index) => {{
          if (index >= 4) p.style.display = "block"; // Show remaining paragraphs
        }});
        readMoreBtn.textContent = "Show Less";
        readMoreBtn.dataset.expanded = "true";
      }} else {{
        paragraphs.forEach((p, index) => {{
          if (index >= 4) p.style.display = "none"; // Hide remaining paragraphs
        }});
        readMoreBtn.textContent = "Continue Reading";
        readMoreBtn.dataset.expanded = "false";
      }}
    }};

    // Populate the blog content dynamically
    const blogContent = document.getElementById('blogContent');
    blogContent.innerHTML = `
      <h1>${{blogData.title}}</h1>
      <img src="${{blogData.image}}" alt="${{blogData.title}}" style="width: 100%; border-radius: 10px; margin-bottom: 1.5em;">
      ${{blogData.content}}
    `;

    // Add "Continue Reading" button dynamically
    const readMoreBtn = document.createElement('button');
    readMoreBtn.id = 'readMoreBtn';
    readMoreBtn.className = 'read-more-btn';
    readMoreBtn.textContent = "Continue Reading";
    readMoreBtn.dataset.expanded = "false";
    readMoreBtn.addEventListener('click', handleReadMore);
    blogContent.appendChild(readMoreBtn);

    // Ensure only the first 4 paragraphs are visible initially
    const paragraphs = document.querySelectorAll('.content-container p');
    paragraphs.forEach((p, index) => {{
      if (index >= 4) p.style.display = "none"; // Hide paragraphs beyond the first 4
    }});

    // Load suggested blogs when page loads
    document.addEventListener('DOMContentLoaded', () => {{
      loadSuggestedBlogs();
    }});

    // Dark mode toggle (same as index.html)
    const toggleMode = document.getElementById('toggleMode');
    const body = document.body;
    const darkIcon = document.getElementById('darkIcon');
    const lightIcon = document.getElementById('lightIcon');

    toggleMode.addEventListener('click', () => {{
      body.classList.toggle('light');
      darkIcon.style.display = body.classList.contains('light') ? 'none' : 'inline';
      lightIcon.style.display = body.classList.contains('light') ? 'inline' : 'none';
    }});

    // Function to handle scroll animation
    const handleScrollAnimation = () => {{
      const blogCards = document.querySelectorAll('.suggested-blogs .blog-card');
      blogCards.forEach((card) => {{
        const rect = card.getBoundingClientRect();
        if (rect.top < window.innerHeight - 50) {{
          card.classList.add('visible'); // Add the 'visible' class when in view
        }}
      }});
    }};

    // Attach scroll event listener
    window.addEventListener('scroll', handleScrollAnimation);

    // Trigger animation on page load
    document.addEventListener('DOMContentLoaded', handleScrollAnimation);

    // Search functionality
    const searchInput = document.getElementById("searchInput");
    const searchButton = document.getElementById("searchButton");
    const searchResults = document.getElementById("searchResults");

    // Function to handle search
    const handleSearch = async () => {{
      const query = searchInput.value.trim().toLowerCase();
      searchResults.innerHTML = ""; // Clear previous results

      if (!query) {{
        searchResults.style.display = "none";
        return;
      }}

      try {{
        const response = await fetch('../blog-data.json');
        const data = await response.json();
        
        const filteredBlogs = data.blogs.filter(blog =>
          blog.title.toLowerCase().includes(query) ||
          blog.description.toLowerCase().includes(query)
        );

        if (filteredBlogs.length > 0) {{
          filteredBlogs.forEach(blog => {{
            const blogCard = document.createElement("div");
            blogCard.classList.add("blog-card");
            blogCard.innerHTML = `
              <img src="${{blog.image}}" alt="${{blog.title}}">
              <div class="blog-card-content">
                <h4>${{blog.title}}</h4>
                <p>${{blog.description}}</p>
                <a href="${{blog.link}}">Read More</a>
              </div>
            `;
            searchResults.appendChild(blogCard);
          }});
        }} else {{
          searchResults.innerHTML = `
            <p class="not-found">No blogs found for your search. You may like:</p>
          `;
          // Show suggested blogs as fallback
          const suggestedBlogs = data.blogs.slice(0, 3);
          suggestedBlogs.forEach(blog => {{
            const blogCard = document.createElement("div");
            blogCard.classList.add("blog-card");
            blogCard.innerHTML = `
              <img src="${{blog.image}}" alt="${{blog.title}}">
              <div class="blog-card-content">
                <h4>${{blog.title}}</h4>
                <p>${{blog.description}}</p>
                <a href="${{blog.link}}">Read More</a>
              </div>
            `;
            searchResults.appendChild(blogCard);
          }});
        }}

        searchResults.style.display = "block"; // Show results
      }} catch (error) {{
        console.error('Error searching blogs:', error);
        searchResults.innerHTML = '<p class="not-found">Error searching blogs. Please try again.</p>';
        searchResults.style.display = "block";
      }}
    }};

    // Attach event listener to the search button
    searchButton.addEventListener("click", handleSearch);

    // Trigger search on Enter key press
    searchInput.addEventListener("keypress", event => {{
      if (event.key === "Enter") {{
        handleSearch();
      }}
    }});
  </script>
</body>
</html>"""
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename

    def generate_seo_blog(self):
        """Generate a new SEO-optimized blog post."""
        print("🎯 Generating SEO-optimized blog post...")
        
        # Select a random topic
        topic = random.choice(self.topics)
        
        # Create the blog file
        filename = self.create_blog_file(topic)
        
        print(f"✅ Blog created: {filename}")
        print(f"📝 Title: {topic['title']}")
        print(f"🔗 Slug: {topic['slug']}")
        print(f"🔍 Keywords: {topic['keywords']}")
        print(f"📅 Published: {datetime.now().strftime('%m/%d/%Y at %I:%M %p')}")
        print(f"🏷️ Schema Type: {topic['schema_type']}")
        print(f"🖼️ Image: blog-img/{topic['slug']}.png")
        
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
    """Main function to generate an SEO-optimized blog."""
    generator = SEOBlogGenerator()
    
    print("=" * 70)
    print("🚀 SEO-OPTIMIZED BLOG GENERATOR")
    print("=" * 70)
    
    # Generate today's blog
    filename = generator.generate_seo_blog()
    
    print("\n" + "=" * 70)
    print("✅ SEO BLOG GENERATION COMPLETE!")
    print("=" * 70)
    print(f"📄 File created: blog-list/{filename}")
    print("🔍 SEO Features:")
    print("   - SEO-friendly URL slug")
    print("   - Comprehensive schema markup")
    print("   - Enhanced meta tags")
    print("   - Open Graph and Twitter Cards")
    print("   - Canonical URLs")
    print("   - Structured data (JSON-LD)")
    print("💻 Content Features:")
    print("   - Matches blog1.html structure exactly")
    print("   - Dynamic suggested blogs sidebar")
    print("   - Search functionality")
    print("   - Social media icons")
    print("   - Continue Reading functionality")
    print("   - Uses existing style.css file")
    print("\n💡 Next steps:")
    print("   1. Add image: blog-img/{filename.replace('.html', '.png')}")
    print("   2. Review and customize content")
    print("   3. Add personal insights")
    print("   4. Run 'update_blogs.bat' to refresh")
    print("=" * 70)

if __name__ == "__main__":
    main() 