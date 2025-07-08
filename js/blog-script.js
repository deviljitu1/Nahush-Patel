// blog-script.js

// Utility to get current blog slug from URL
function getCurrentBlogSlug() {
  const path = window.location.pathname.split('/').pop();
  return path.replace('.html', '');
}

let blogsData = [];
let currentBlog = null;

// Fetch all blogs and set current blog
async function loadAllBlogs() {
  try {
    const response = await fetch('../blog-data.json');
    if (!response.ok) throw new Error('Failed to load blog data');
    const data = await response.json();
    blogsData = data.blogs.sort((a, b) => {
      const dateA = new Date(`${a.published_date} ${a.published_time}`);
      const dateB = new Date(`${b.published_date} ${b.published_time}`);
      return dateB - dateA;
    });
    const currentSlug = getCurrentBlogSlug();
    currentBlog = blogsData.find(blog => blog.filename === currentSlug);
    renderCurrentBlog();
    renderSuggestedBlogs(getRelatedBlogs());
  } catch (error) {
    document.getElementById('blogContent').innerHTML = '<h2>Error loading blog. Please try again later.</h2>';
    document.getElementById('suggestedBlogs').innerHTML = '';
  }
}

function renderCurrentBlog() {
  if (!currentBlog) return;
  const blogContent = document.getElementById('blogContent');
  if (!blogContent) return;
  blogContent.innerHTML = `
    <h1>${currentBlog.title}</h1>
    <img src="${currentBlog.image}" alt="${currentBlog.title}">
    <div class="blog-meta">
      <span><i class="fas fa-calendar-alt"></i> ${currentBlog.published_date} ${currentBlog.published_time}</span>
      <span><i class="fas fa-user"></i> Nahush Patel</span>
    </div>
    <p>${currentBlog.excerpt || currentBlog.description}</p>
    <div class="read-more-section">
      <button class="read-more-btn" id="showSuggestionsBtn">Show Related Articles</button>
    </div>
  `;
}

function getRelatedBlogs() {
  if (!currentBlog || !blogsData.length) return [];
  return blogsData.filter(blog => blog.filename !== currentBlog.filename).slice(0, 3);
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
          <span class="blog-date"><i class="fas fa-calendar-alt"></i> ${blog.published_date} ${blog.published_time}</span>
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
  loadAllBlogs();
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
});