  // Dynamic blog content
    const blogData = {
  title: "Web Development Best Practices: A Guide for Modern Developers",
  image: "../../blog-img/Web Development Best Practices.png",
  link: "../blog-list/blog2.html",
  content: `
    <p>Staying up to date with modern <strong>web development best practices</strong> is essential for building fast, accessible, and maintainable websites. In this guide, we explore proven strategies that every front-end and back-end developer should know to stay competitive in the ever-evolving tech landscape.</p>

    <h3>Use Semantic HTML for Better Accessibility and SEO</h3>
    <p>Semantic HTML improves the structure and meaning of your content. Tags like <code>&lt;header&gt;</code>, <code>&lt;main&gt;</code>, <code>&lt;nav&gt;</code>, and <code>&lt;footer&gt;</code> help search engines and assistive technologies understand your site, boosting both <strong>SEO</strong> and <strong>accessibility</strong>.</p>

    <h3>Implement a Mobile-First, Responsive Design</h3>
    <p>With most users browsing on mobile devices, a mobile-first approach is a must. Use CSS media queries, fluid grids, and flexible layouts to ensure your website looks great on all screen sizes. Tools like Flexbox and CSS Grid make this easier and more consistent.</p>

    <h3>Optimize Website Performance</h3>
    <p>Fast-loading websites reduce bounce rates and improve SEO rankings. Minify CSS and JavaScript, compress images, and use lazy loading where possible. Implement <strong>browser caching</strong> and leverage a <strong>Content Delivery Network (CDN)</strong> to deliver static files efficiently.</p>

    <h3>Write Clean, Modular, and Reusable Code</h3>
    <p>Keep your codebase organized and easy to maintain by following DRY (Don't Repeat Yourself) principles. Use component-based architecture when working with frameworks like React or Vue. Write utility functions for repeated logic and separate concerns clearly across files.</p>

    <h3>Use Modern JavaScript (ES6+)</h3>
    <p>Embrace features like <code>let</code>/<code>const</code>, arrow functions, template literals, and async/await. These features improve readability, performance, and reduce bugs. Modularize your JavaScript code with ES Modules and use bundlers like Vite or Webpack for scalable builds.</p>

    <h3>Adopt Scalable CSS Practices</h3>
    <p>Maintain a clean and scalable stylesheet by using methodologies like BEM (Block Element Modifier), SMACSS, or utility-first frameworks like Tailwind CSS. Use variables and custom properties to manage themes, spacing, and colors efficiently.</p>

    <h3>Make Accessibility (a11y) a Priority</h3>
    <p>Ensure your website is usable by people with disabilities. Provide meaningful alt text for images, use correct HTML roles and ARIA labels, and ensure keyboard navigation works. Test your site with screen readers and tools like Lighthouse and Axe.</p>

    <h3>Secure Your Web Application</h3>
    <p>Web security should never be an afterthought. Sanitize user input, escape output to prevent XSS attacks, and protect against CSRF. Use HTTPS, set secure headers, and update dependencies regularly to close known vulnerabilities.</p>

    <h3>Use Git and Practice Version Control</h3>
    <p>Track your code changes using Git and platforms like GitHub or GitLab. Branch your features, write clear commit messages, and create pull requests for collaborative code review. This ensures better team collaboration and project history tracking.</p>

    <h3>Test Early and Often</h3>
    <p>Catch bugs before they hit production by writing unit, integration, and end-to-end tests. Use frameworks like Jest, Mocha, or Cypress to ensure your code works as expected. CI/CD tools like GitHub Actions and Netlify can automate testing and deployment.</p>

    <h3>Document Your Code and Project Structure</h3>
    <p>Good documentation accelerates onboarding, collaboration, and maintenance. Include README files, inline comments, and clear instructions for setup and contribution. Well-documented APIs and components improve usability for teams and third-party developers.</p>

    <h3>Stay Updated with Evolving Standards</h3>
    <p>The web is constantly evolving. Subscribe to tech blogs, read the official documentation, join developer communities, and explore open-source projects. Staying informed helps you adopt new technologies and best practices early.</p>

    <p>In summary, following modern web development best practices leads to better user experiences, higher rankings, fewer bugs, and long-term scalability. By investing in quality, performance, and maintainability, you're laying the foundation for successful, future-ready web applications.</p>
  `
};

    const suggestedBlogs = [
    
      {
        title: "Mastering JavaScript Frameworks",
        image: "../../blog-img/Mastering JavaScript Frameworks.png",
        link: "../blog-list/blog3.html",
        description: "Dive into popular JavaScript frameworks, including React, Vue, and Angular, and discover their ideal use cases for building dynamic web applications."
      },
      {
        title: "Blog Post 4",
        image: "../blog-img/blog4-thumbnail.jpg",
        link: "../blog-list/blog4.html",
        description: "Understand the basics of SEO for better website visibility."
      },
      {
        title: "Blog Post 5",
        image: "../blog-img/blog5-thumbnail.jpg",
        link: "../blog-list/blog5.html",
        description: "Learn about responsive design and its importance."
      }
    ];

    // Function to handle "Continue Reading" functionality
    const handleReadMore = () => {
      const paragraphs = document.querySelectorAll('.content-container p');
      const readMoreBtn = document.getElementById('readMoreBtn');

      if (readMoreBtn.dataset.expanded === "false") {
        paragraphs.forEach((p, index) => {
          if (index >= 4) p.style.display = "block"; // Show remaining paragraphs
        });
        readMoreBtn.textContent = "Show Less";
        readMoreBtn.dataset.expanded = "true";
      } else {
        paragraphs.forEach((p, index) => {
          if (index >= 4) p.style.display = "none"; // Hide remaining paragraphs
        });
        readMoreBtn.textContent = "Continue Reading";
        readMoreBtn.dataset.expanded = "false";
      }
    };

    // Populate the blog content dynamically
    const blogContent = document.getElementById('blogContent');
    blogContent.innerHTML = `
      <h1>${blogData.title}</h1>
      <img src="${blogData.image}" alt="${blogData.title}" style="width: 100%; border-radius: 10px; margin-bottom: 1.5em;">
      ${blogData.content}
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
    paragraphs.forEach((p, index) => {
      if (index >= 4) p.style.display = "none"; // Hide paragraphs beyond the first 4
    });

    // Populate suggested blogs dynamically
    const suggestedBlogsContainer = document.getElementById('suggestedBlogs');
    suggestedBlogs.forEach(blog => {
      const blogCard = document.createElement('div');
      blogCard.classList.add('blog-card');
      blogCard.innerHTML = `
        <img src="${blog.image}" alt="${blog.title}">
        <div class="blog-card-content">
          <h3>${blog.title}</h3>
          <p>${blog.description}</p>
          <a href="${blog.link}">Read More</a>
        </div>
      `;
      suggestedBlogsContainer.appendChild(blogCard);
    });

    // Dark mode toggle (same as index.html)
    const toggleMode = document.getElementById('toggleMode');
    const body = document.body;
    const darkIcon = document.getElementById('darkIcon');
    const lightIcon = document.getElementById('lightIcon');

    toggleMode.addEventListener('click', () => {
      body.classList.toggle('light');
      darkIcon.style.display = body.classList.contains('light') ? 'none' : 'inline';
      lightIcon.style.display = body.classList.contains('light') ? 'inline' : 'none';
    });

    // Function to handle scroll animation
    const handleScrollAnimation = () => {
      const blogCards = document.querySelectorAll('.suggested-blogs .blog-card');
      blogCards.forEach((card) => {
        const rect = card.getBoundingClientRect();
        if (rect.top < window.innerHeight - 50) {
          card.classList.add('visible'); // Add the 'visible' class when in view
        }
      });
    };

    // Attach scroll event listener
    window.addEventListener('scroll', handleScrollAnimation);

    // Trigger animation on page load
    document.addEventListener('DOMContentLoaded', handleScrollAnimation);