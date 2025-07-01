import os
from urllib.parse import quote

SITE_URL = "https://jiitufolio.com"
OUTPUT_FILE = "sitemap.xml"
INCLUDE_DIRS = [".", "blog-list"]


def get_html_files():
    html_files = []
    for directory in INCLUDE_DIRS:
        for root, dirs, files in os.walk(directory):
            # Exclude hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.endswith('.html') and not file.startswith('.'):
                    rel_dir = os.path.relpath(root, '.')
                    rel_file = os.path.join(rel_dir, file) if rel_dir != '.' else file
                    html_files.append(rel_file.replace('\\', '/'))
    return html_files

def make_url(path):
    # Remove leading './' if present
    if path.startswith('./'):
        path = path[2:]
    return f"{SITE_URL}/{quote(path)}"

def generate_sitemap():
    html_files = get_html_files()
    urls = [make_url(f) for f in html_files]
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for url in urls:
            f.write('  <url>\n')
            f.write(f'    <loc>{url}</loc>\n')
            f.write('  </url>\n')
        f.write('</urlset>\n')
    print(f"Sitemap generated with {len(urls)} URLs: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_sitemap() 