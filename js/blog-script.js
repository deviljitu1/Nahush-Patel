// blog-script.js

// Blog Data - Add all your blogs here
const allBlogs = [
    {
      id: "blog4",
      title: "The Future of Web Development",
      image: "../blog-img/blog1-thumbnail.jpg",
      link: "../blog-list/blog4.html",
      description: "Exploring emerging trends in web development technologies.",
      date: "April 10, 2025",
      tags: ["web development", "trends"]
    },
    {
        id: "blog5",
        title: "How AI is Revolutionizing Web Development",
        image: "../blog-img/ai-webdev.jpg",
        link: "../blog-list/blog5.html",
        description: "Discover how AI tools are transforming modern web development workflows.",
        date: "June 10, 2025",
        tags: ["AI", "web development", "productivity"]
      }
    // Add other blogs here...
  ];
  
  // Current blog should be defined in each HTML file before loading this script
  // Example: 
  // <script>const currentBlog = { id: "blog1", ... };</script>
  // <script src="js/blog-script.js"></script>
  
  // Functions
  function renderCurrentBlog() {
    if (!window.currentBlog) return;
    
    const blogContent = document.getElementById('blogContent');
    if (!blogContent) return;
    
    blogContent.innerHTML = `
      <h1>${currentBlog.title}</h1>
      <img src="${currentBlog.image}" alt="${currentBlog.alt || currentBlog.title}">
      <div class="blog-meta">
        <span><i class="fas fa-calendar-alt"></i> ${currentBlog.date}</span>
        <span><i class="fas fa-user"></i> ${currentBlog.author}</span>
      </div>
      ${currentBlog.content}
      <div class="read-more-section">
        <button class="read-more-btn" id="showSuggestionsBtn">Show Related Articles</button>
      </div>
    `;
  }
  
  function getRelatedBlogs() {
    if (!window.currentBlog || !allBlogs.length) return [];
    
    const availableBlogs = allBlogs.filter(blog => blog.id !== currentBlog.id);
    
    if (currentBlog.tags?.length) {
      const related = availableBlogs.filter(blog => 
        blog.tags?.some(tag => currentBlog.tags.includes(tag))
      );
      if (related.length >= 3) return related.slice(0, 3);
    }
    
    return availableBlogs
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .slice(0, 3);
  }
  
  function renderSuggestedBlogs(blogs) {
    const container = document.getElementById('suggestedBlogs');
    if (!container) return;
    
    container.innerHTML = `
      <h2>You Might Also Like</h2>
      ${blogs.map(blog => `
        <div class="blog-card">
          <img src="${blog.image}" alt="${blog.title}">
          <div class="blog-card-content">
            <h3>${blog.title}</h3>
            <p>${blog.description}</p>
            <span class="blog-date"><i class="fas fa-calendar-alt"></i> ${blog.date}</span>
            <a href="${blog.link}">Read More <i class="fas fa-arrow-right"></i></a>
          </div>
        </div>
      `).join('')}
      <div class="view-all-blogs">
        <button class="view-all-btn" id="viewAllBtn">View All Blogs</button>
      </div>
    `;
  }
  
  function setupDarkModeToggle() {
    const toggleMode = document.getElementById('toggleMode');
    const body = document.body;
    const darkIcon = document.getElementById('darkIcon');
    const lightIcon = document.getElementById('lightIcon');
  
    if (!toggleMode || !darkIcon || !lightIcon) return;
  
    const savedMode = localStorage.getItem('darkMode');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedMode === 'light' || (!savedMode && !systemPrefersDark)) {
      body.classList.add('light');
      darkIcon.style.display = 'none';
      lightIcon.style.display = 'inline';
    }
  
    toggleMode.addEventListener('click', () => {
      body.classList.toggle('light');
      const isLight = body.classList.contains('light');
      
      darkIcon.style.display = isLight ? 'none' : 'inline';
      lightIcon.style.display = isLight ? 'inline' : 'none';
      localStorage.setItem('darkMode', isLight ? 'light' : 'dark');
    });
  }
  
  function setupScrollAnimation() {
    const handleScroll = () => {
      document.querySelectorAll('.blog-card').forEach(card => {
        const rect = card.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100) {
          card.classList.add('visible');
        }
      });
    };
  
    window.addEventListener('scroll', handleScroll);
    handleScroll();
  }
  
  // Initialize
  document.addEventListener('DOMContentLoaded', () => {
    renderCurrentBlog();
    setupDarkModeToggle();
    setupScrollAnimation();
    
    // Event Delegation for dynamic buttons
    document.addEventListener('click', (e) => {
      if (e.target?.id === 'showSuggestionsBtn') {
        renderSuggestedBlogs(getRelatedBlogs());
        e.target.textContent = "More Suggestions";
        document.getElementById('suggestedBlogs')?.scrollIntoView({ behavior: 'smooth' });
      }
      else if (e.target?.id === 'viewAllBtn') {
        window.location.href = "../blog-list/all-blogs.html";
      }
    });
  
    // Initial suggestions
    setTimeout(() => {
      renderSuggestedBlogs(
        allBlogs
          .filter(blog => blog.id !== currentBlog?.id)
          .sort((a, b) => new Date(b.date) - new Date(a.date))
          .slice(0, 3)
      );
    }, 500);
  });