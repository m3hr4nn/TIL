import os
import json
from datetime import datetime
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_REPO_URL = "https://github.com/m3hr4nn/TIL/blob/main"

def scan_posts():
    posts = []
    categories = []
    
    print("Scanning for posts and categories...")
    
    for category in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category)
        if os.path.isdir(category_path) and not category.startswith('.'):
            if category == ".github":
                continue
            
            print(f"Found category: {category}")
            post_count = 0
            
            try:
                for file in os.listdir(category_path):
                    if file.endswith('.md'):
                        file_path = os.path.join(category_path, file)
                        posts.append({
                            "category": category,
                            "title": os.path.splitext(file)[0],
                            "path": f"{GITHUB_REPO_URL}/{category}/{file}",
                            "updated": os.path.getmtime(file_path)
                        })
                        post_count += 1
                        print(f"  - Found post: {file}")
                
                # Add category multiple times based on post count for weighting
                for _ in range(max(1, post_count)):  # At least 1, even if no posts
                    categories.append(category)
                    
            except Exception as e:
                print(f"Error processing {category}: {e}")
                # Still add the category even if we can't read posts
                categories.append(category)
    
    # Sort posts by latest modified time
    posts.sort(key=lambda x: x['updated'], reverse=True)
    
    # Convert timestamps to ISO 8601
    for post in posts:
        post['updated'] = datetime.fromtimestamp(post['updated']).isoformat()
    
    print(f"Found {len(posts)} posts in {len(set(categories))} categories")
    print(f"Categories: {list(set(categories))}")
    
    return posts, categories

def generate_css_wordcloud_html(categories):
    """Generate HTML for CSS-based word cloud - GUARANTEED to work"""
    if not categories:
        # Fallback with some default categories if none found
        categories = ['Python', 'JavaScript', 'Linux', 'AI', 'Programming']
        print("No categories found, using defaults")
    
    word_freq = Counter(categories)
    max_count = max(word_freq.values()) if word_freq else 1
    
    print(f"Word frequencies: {dict(word_freq)}")
    
    css_words = []
    for word, count in word_freq.items():
        # Scale font size based on frequency (16px to 32px)
        font_size = 16 + (count / max_count) * 16
        opacity = 0.8 + (count / max_count) * 0.2
        css_words.append(
            f'<span class="cloud-word" style="font-size: {font_size}px; opacity: {opacity};">{word}</span>'
        )
    
    # Shuffle for better visual distribution
    import random
    random.shuffle(css_words)
    
    html = f'''
        <div class="wordcloud css-wordcloud">
            <div class="cloud-container">
                {' '.join(css_words)}
            </div>
        </div>'''
    
    print("Generated word cloud HTML")
    return html

def generate_posts_json(posts):
    with open(os.path.join(BASE_DIR, 'posts.json'), 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

def generate_categories_json(categories):
    """Generate categories.json with frequency data"""
    word_freq = Counter(categories)
    categories_data = [{"name": word, "count": count} for word, count in word_freq.items()]
    categories_data.sort(key=lambda x: x['count'], reverse=True)
    
    with open(os.path.join(BASE_DIR, 'categories.json'), 'w', encoding='utf-8') as f:
        json.dump(categories_data, f, indent=4, ensure_ascii=False)

def generate_index_html(posts, categories):
    posts_list_html = "\n".join(
        [f"                <li><a href='{p['path']}'><span class='category'>{p['category']}</span> - {p['title']}</a></li>"
         for p in posts]
    )
    
    # Generate word cloud HTML - ALWAYS generate something
    wordcloud_html = generate_css_wordcloud_html(categories)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Today I Learned</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Today I Learned (TIL)</h1>
        <p class="tagline">Small notes, big impact.</p>{wordcloud_html}
    </header>
    <main>
        <section class="posts">
            <h2>Recent Posts ({len(posts)})</h2>
            <ul>
{posts_list_html}
            </ul>
        </section>
    </main>
    <footer>
        <p>&copy; 2025 <a href="https://m3hr4n.com">Mehran Naderizadeh</a> - Built with ♥</p>
    </footer>
</body>
</html>
"""
    
    with open(os.path.join(BASE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Generated index.html with word cloud")

def main():
    print("Starting CMS generation...")
    posts, categories = scan_posts()
    
    # Generate files
    generate_posts_json(posts)
    generate_categories_json(categories)
    generate_index_html(posts, categories)
    
    print("✅ CMS updated: index.html, posts.json, and categories.json")
    print("✅ Word cloud generated and embedded!")

if __name__ == "__main__":
    main()
