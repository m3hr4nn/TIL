#!/usr/bin/env python3

import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import hashlib

def extract_frontmatter_and_content(content):
    """Extract frontmatter and content from markdown"""
    if not content.startswith('---'):
        return {}, content
    
    try:
        parts = content.split('---', 2)
        if len(parts) < 3:
            return {}, content
        
        frontmatter_text = parts[1].strip()
        body_content = parts[2].strip()
        
        metadata = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                if key == 'tags':
                    # Parse tags array
                    if value.startswith('[') and value.endswith(']'):
                        value = value[1:-1]
                    metadata[key] = [tag.strip().strip('"\'') for tag in value.split(',') if tag.strip()]
                else:
                    metadata[key] = value
        
        return metadata, body_content
    except Exception as e:
        print(f"Warning: Failed to parse frontmatter: {e}")
        return {}, content

def markdown_to_html(markdown_text):
    """Convert basic markdown to HTML"""
    html = markdown_text
    
    # Headers
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Inline code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank">\1</a>', html)
    
    # Line breaks
    html = html.replace('\n\n', '</p><p>')
    html = f'<p>{html}</p>'
    html = html.replace('<p></p>', '')
    
    return html

def process_markdown_file(filepath):
    """Process a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        metadata, body = extract_frontmatter_and_content(content)
        
        # Extract title
        title = metadata.get('title', '')
        if not title:
            title_match = re.search(r'^#\s+(.+)', body, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else Path(filepath).stem.replace('-', ' ').title()
        
        # Extract date
        date = metadata.get('date', '')
        if not date:
            mtime = os.path.getmtime(filepath)
            date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        
        # Extract tags
        tags = metadata.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        # Create preview (first few sentences)
        preview_text = re.sub(r'^#.*$', '', body, flags=re.MULTILINE)  # Remove headers
        preview_text = re.sub(r'```.*?```', '', preview_text, flags=re.DOTALL)  # Remove code blocks
        preview_text = re.sub(r'[*_`]', '', preview_text)  # Remove markdown syntax
        preview_lines = [line.strip() for line in preview_text.split('\n') if line.strip()]
        preview = ' '.join(preview_lines[:3])[:200]
        if len(preview) >= 200:
            preview += '...'
        
        # Convert full content to HTML
        html_content = markdown_to_html(body)
        
        # Create clean path
        clean_path = filepath.replace('\\', '/').lstrip('./')
        category = clean_path.split('/')[0].title()
        
        # Create slug
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', title.lower()).strip('-')
        
        return {
            'title': title,
            'slug': slug,
            'date': date,
            'category': category,
            'tags': tags,
            'preview': preview,
            'content': html_content,
            'filepath': clean_path,
            'id': hashlib.md5(clean_path.encode()).hexdigest()[:8]
        }
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def find_markdown_files():
    """Find all markdown files in the repository"""
    md_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and git directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        if root == '.':
            continue
        
        for file in files:
            if file.endswith('.md') and file.lower() != 'readme.md':
                filepath = os.path.join(root, file)
                md_files.append(filepath)
    
    return md_files

def generate_posts_json(posts):
    """Generate posts.json for the website"""
    categories = defaultdict(list)
    tags_count = defaultdict(int)
    
    for post in posts:
        categories[post['category']].append(post)
        for tag in post['tags']:
            tags_count[tag] += 1
    
    # Sort posts by date
    sorted_posts = sorted(posts, key=lambda x: x['date'], reverse=True)
    
    # Sort categories
    for category in categories:
        categories[category].sort(key=lambda x: x['date'], reverse=True)
    
    data = {
        'posts': sorted_posts,
        'categories': dict(categories),
        'stats': {
            'total_posts': len(posts),
            'total_categories': len(categories),
            'last_updated': datetime.now().isoformat(),
            'category_counts': {cat: len(posts) for cat, posts in categories.items()},
            'popular_tags': dict(sorted(tags_count.items(), key=lambda x: x[1], reverse=True)[:10])
        }
    }
    
    return data

def generate_index_html(posts_data):
    """Generate the main index.html file"""
    stats = posts_data['stats']
    recent_posts = posts_data['posts'][:6]  # Show 6 recent posts
    categories = posts_data['categories']
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Mehran's TIL - Today I Learned</title>
    <meta name="description" content="A collection of things I learn every day across various technologies">
    
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --text-muted: #656d76;
            --accent: #58a6ff;
            --accent-secondary: #f78166;
            --border: #30363d;
            --success: #238636;
            --shadow: rgba(0, 0, 0, 0.3);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}

        /* Header */
        .header {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            padding: 4rem 0 3rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="%23ffffff" stroke-width="0.5" opacity="0.05"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.1;
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .header h1 {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--accent), var(--accent-secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(88, 166, 255, 0.3);
        }}

        .header p {{
            font-size: 1.25rem;
            color: var(--text-secondary);
            margin-bottom: 2rem;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}

        .stat-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }}

        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 40px var(--shadow);
            border-color: var(--accent);
        }}

        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--accent);
            display: block;
        }}

        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* Navigation */
        .nav {{
            background: var(--bg-secondary);
            padding: 1rem 0;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(10px);
        }}

        .nav-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .search-container {{
            flex: 1;
            max-width: 400px;
            position: relative;
        }}

        .search-input {{
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 25px;
            color: var(--text-primary);
            font-size: 0.875rem;
            transition: all 0.3s ease;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.1);
        }}

        .search-icon {{
            position: absolute;
            left: 0.75rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }}

        .filter-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .filter-tag {{
            padding: 0.5rem 1rem;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 20px;
            color: var(--text-secondary);
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
        }}

        .filter-tag:hover,
        .filter-tag.active {{
            background: var(--accent);
            color: white;
            border-color: var(--accent);
        }}

        /* Main Content */
        .main {{
            padding: 3rem 0;
        }}

        .section-title {{
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 2rem;
            text-align: center;
        }}

        .posts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
        }}

        .post-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .post-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent), var(--accent-secondary));
        }}

        .post-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 20px 40px var(--shadow);
            border-color: var(--accent);
        }}

        .post-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1rem;
        }}

        .post-category {{
            background: var(--accent);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .post-date {{
            color: var(--text-muted);
            font-size: 0.875rem;
        }}

        .post-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            line-height: 1.3;
        }}

        .post-preview {{
            color: var(--text-secondary);
            margin-bottom: 1rem;
            line-height: 1.5;
        }}

        .post-tags {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }}

        .tag {{
            background: var(--bg-primary);
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            color: var(--text-muted);
            border: 1px solid var(--border);
        }}

        .read-more {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 500;
            font-size: 0.875rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            transition: opacity 0.2s ease;
        }}

        .read-more:hover {{
            opacity: 0.8;
        }}

        /* Categories Section */
        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }}

        .category-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }}

        .category-card:hover {{
            transform: translateY(-4px);
            border-color: var(--accent);
        }}

        .category-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .category-name {{
            font-size: 1.125rem;
            font-weight: 600;
        }}

        .category-count {{
            background: var(--bg-primary);
            color: var(--text-secondary);
            padding: 0.25rem 0.5rem;
            border-radius: 12px;
            font-size: 0.75rem;
        }}

        .category-posts {{
            list-style: none;
        }}

        .category-posts li {{
            padding: 0.5rem 0;
            border-bottom: 1px solid var(--border);
        }}

        .category-posts li:last-child {{
            border-bottom: none;
        }}

        .category-posts a {{
            color: var(--text-secondary);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        .category-posts a:hover {{
            color: var(--accent);
        }}

        /* Footer */
        .footer {{
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            padding: 2rem 0;
            text-align: center;
            color: var(--text-muted);
        }}

        /* Loading states */
        .loading {{
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
        }}

        .error {{
            background: #f85149;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            margin: 2rem 0;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2.5rem;
            }}
            
            .nav-content {{
                flex-direction: column;
            }}
            
            .search-container {{
                max-width: none;
            }}
            
            .posts-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="header-content">
                <h1>📚 Today I Learned</h1>
                <p>A collection of things I learn every day across various technologies</p>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <span class="stat-number">{stats['total_posts']}</span>
                        <span class="stat-label">Total Posts</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{stats['total_categories']}</span>
                        <span class="stat-label">Categories</span>
                    </div>
                    <div class="stat-card">
                        <span class="stat-number">{datetime.fromisoformat(stats['last_updated']).strftime('%b %d')}</span>
                        <span class="stat-label">Last Updated</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <nav class="nav">
        <div class="container">
            <div class="nav-content">
                <div class="search-container">
                    <span class="search-icon">🔍</span>
                    <input type="text" class="search-input" placeholder="Search posts..." id="searchInput">
                </div>
                
                <div class="filter-tags">
                    <span class="filter-tag active" data-category="all">All</span>'''
    
    # Add category filters
    for category, count in stats['category_counts'].items():
        html += f'''
                    <span class="filter-tag" data-category="{category}">{category} ({count})</span>'''
    
    html += f'''
                </div>
            </div>
        </div>
    </nav>

    <main class="main">
        <div class="container">
            <h2 class="section-title">🔥 Recent Posts</h2>
            
            <div class="posts-grid" id="postsGrid">'''
    
    # Add recent posts
    for post in recent_posts:
        tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in post['tags']])
        html += f'''
                <article class="post-card" data-category="{post['category']}" data-tags="{','.join(post['tags']).lower()}">
                    <div class="post-header">
                        <span class="post-category">{post['category']}</span>
                        <span class="post-date">{post['date']}</span>
                    </div>
                    <h3 class="post-title">{post['title']}</h3>
                    <p class="post-preview">{post['preview']}</p>
                    {f'<div class="post-tags">{tags_html}</div>' if post['tags'] else ''}
                    <a href="#" class="read-more" onclick="showPost('{post['id']}')">
                        Read more →
                    </a>
                </article>'''
    
    html += f'''
            </div>

            <h2 class="section-title">📚 Categories</h2>
            
            <div class="categories-grid">'''
    
    # Add categories
    for category, posts in categories.items():
        html += f'''
                <div class="category-card">
                    <div class="category-header">
                        <h3 class="category-name">{category}</h3>
                        <span class="category-count">{len(posts)} posts</span>
                    </div>
                    <ul class="category-posts">'''
        
        for post in posts[:5]:  # Show top 5 posts per category
            html += f'''
                        <li><a href="#" onclick="showPost('{post['id']}')">{post['title']}</a></li>'''
        
        if len(posts) > 5:
            html += f'''
                        <li><em>... and {len(posts) - 5} more</em></li>'''
        
        html += '''
                    </ul>
                </div>'''
    
    html += '''
            </div>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>Made with ❤️ by Mehran • Updated automatically via GitHub Actions</p>
        </div>
    </footer>

    <!-- Post Modal (for future enhancement) -->
    <div id="postModal" style="display: none;">
        <div id="postContent"></div>
    </div>

    <script>
        let allPosts = [];
        let currentFilter = 'all';

        // Load posts data
        async function loadPosts() {
            try {
                const response = await fetch('./posts.json');
                const data = await response.json();
                allPosts = data.posts;
                console.log('Loaded', allPosts.length, 'posts');
            } catch (error) {
                console.error('Failed to load posts:', error);
            }
        }

        // Search functionality
        function filterPosts() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.post-card');
            
            cards.forEach(card => {
                const title = card.querySelector('.post-title').textContent.toLowerCase();
                const preview = card.querySelector('.post-preview').textContent.toLowerCase();
                const category = card.dataset.category.toLowerCase();
                const tags = card.dataset.tags;
                
                const matchesSearch = !searchTerm || 
                    title.includes(searchTerm) || 
                    preview.includes(searchTerm) || 
                    category.includes(searchTerm) || 
                    tags.includes(searchTerm);
                
                const matchesCategory = currentFilter === 'all' || card.dataset.category === currentFilter;
                
                card.style.display = matchesSearch && matchesCategory ? 'block' : 'none';
            });
        }

        // Category filter
        function setFilter(category) {
            currentFilter = category;
            
            // Update active filter
            document.querySelectorAll('.filter-tag').forEach(tag => {
                tag.classList.toggle('active', tag.dataset.category === category);
            });
            
            filterPosts();
        }

        // Show individual post (placeholder for future modal/page)
        function showPost(postId) {
            const post = allPosts.find(p => p.id === postId);
            if (post) {
                // For now, just log to console
                console.log('Showing post:', post);
                // TODO: Implement modal or separate page
                alert(`Post: ${post.title}\\n\\nThis will open in a modal or separate page in the future!`);
            }
        }

        // Event listeners
        document.addEventListener('DOMContentLoaded', () => {
            loadPosts();
            
            // Search input
            document.getElementById('searchInput').addEventListener('input', filterPosts);
            
            // Category filters
            document.querySelectorAll('.filter-tag').forEach(tag => {
                tag.addEventListener('click', (e) => {
                    setFilter(e.target.dataset.category);
                });
            });
        });
    </script>
</body>
</html>'''
    
    return html

def main():
    """Main function to generate the CMS"""
    print("🚀 Starting TIL CMS generation...")
    
    # Find all markdown files
    md_files = find_markdown_files()
    print(f"📁 Found {len(md_files)} markdown files")
    
    if not md_files:
        print("⚠️  No markdown files found!")
        return
    
    # Process all files
    posts = []
    for filepath in md_files:
        post = process_markdown_file(filepath)
        if post:
            posts.append(post)
            print(f"✅ {post['category']}: {post['title']}")
    
    if not posts:
        print("❌ No valid posts found!")
        return
    
    print(f"📊 Processed {len(posts)} posts successfully")
    
    # Generate posts.json
    posts_data = generate_posts_json(posts)
    
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, indent=2, ensure_ascii=False)
    print("✅ Generated posts.json")
    
    # Generate index.html
    html_content = generate_index_html(posts_data)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✅ Generated index.html")
    
    print(f"🎉 CMS generated successfully!")
    print(f"   📝 {len(posts)} posts")
    print(f"   📂 {posts_data['stats']['total_categories']} categories")
    print(f"   🏷️  {len(posts_data['stats']['popular_tags'])} unique tags")

if __name__ == "__main__":
    main()
