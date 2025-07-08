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
  // Parse the HTML content into a DOM fragment
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = currentBlog.content || `<p>${currentBlog.excerpt || currentBlog.description}</p>`;
  const paragraphs = tempDiv.querySelectorAll('p, h3, h2, ul, ol, pre, img');
  // Responsive teaser count
  let teaserCount = 4;
  if (window.innerWidth <= 600) teaserCount = 2;
  else if (window.innerWidth <= 1023) teaserCount = 3;
  if (paragraphs.length > teaserCount) {
    // Teaser: first N elements
    const teaser = document.createElement('div');
    teaser.className = 'teaser-content';
    for (let i = 0; i < teaserCount; i++) {
      if (paragraphs[i]) teaser.appendChild(paragraphs[i].cloneNode(true));
    }
    // Fade overlay
    const fade = document.createElement('div');
    fade.className = 'content-fade';
    // Read more button
    const readMoreBtn = document.createElement('button');
    readMoreBtn.id = 'readMoreBtn';
    readMoreBtn.className = 'read-more-btn';
    readMoreBtn.textContent = 'Continue Reading';
    fade.appendChild(readMoreBtn);
    // Container for teaser + fade
    const teaserContainer = document.createElement('div');
    teaserContainer.className = 'teaser-container';
    teaserContainer.appendChild(teaser);
    teaserContainer.appendChild(fade);
    blogContent.innerHTML = '';
    blogContent.appendChild(teaserContainer);
    readMoreBtn.addEventListener('click', () => {
      // Show full content
      blogContent.innerHTML = tempDiv.innerHTML;
    });
  } else {
    blogContent.innerHTML = tempDiv.innerHTML;
  }
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

// --- Search Bar Logic ---
function setupSearchBar() {
  const searchInput = document.getElementById('searchInput');
  const searchButton = document.getElementById('searchButton');
  const searchResults = document.getElementById('searchResults');
  if (!searchInput || !searchButton || !searchResults) return;

  const handleSearch = () => {
    const query = searchInput.value.trim().toLowerCase();
    searchResults.innerHTML = '';
    if (!query) {
      searchResults.style.display = 'none';
      return;
    }
    const filteredBlogs = blogsData.filter(blog =>
      blog.title.toLowerCase().includes(query) ||
      blog.description.toLowerCase().includes(query)
    );
    if (filteredBlogs.length > 0) {
      filteredBlogs.forEach(blog => {
        const blogCard = document.createElement('div');
        blogCard.classList.add('blog-card');
        blogCard.innerHTML = `
          <img src="${blog.image}" alt="${blog.title}">
          <div class="blog-card-content">
            <h4>${blog.title}</h4>
            <p>${blog.description}</p>
            <a href="${blog.link}">Read More</a>
          </div>
        `;
        searchResults.appendChild(blogCard);
      });
    } else {
      searchResults.innerHTML = `<p class="not-found">No blogs found for your search. You may like:</p>`;
      renderSuggestedBlogs(getRelatedBlogs());
    }
    searchResults.style.display = 'block';
  };
  searchButton.addEventListener('click', handleSearch);
  searchInput.addEventListener('keypress', event => {
    if (event.key === 'Enter') handleSearch();
  });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadAllBlogs();
  setupDarkModeToggle();
  setupScrollAnimation();
  setupSearchBar();
  // Event Delegation for dynamic buttons
  document.addEventListener('click', (e) => {
    if (e.target?.id === 'showSuggestionsBtn') {
      renderSuggestedBlogs(getRelatedBlogs());
      e.target.textContent = "More Suggestions";
      document.getElementById('suggestedBlogs')?.scrollIntoView({ behavior: 'smooth' });
    }
  });
});