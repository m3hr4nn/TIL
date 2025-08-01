import os
import json
from datetime import datetime
from collections import Counter
import base64
from io import BytesIO

# Try to import wordcloud, fallback to manual generation if not available
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    WORDCLOUD_AVAILABLE = True
except ImportError:
    WORDCLOUD_AVAILABLE = False
    print("WordCloud library not available. Install with: pip install wordcloud matplotlib")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_REPO_URL = "https://github.com/m3hr4nn/TIL/blob/main"

def scan_posts():
    posts = []
    categories = []
    
    for category in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category)
        if os.path.isdir(category_path) and not category.startswith('.'):
            if category == ".github":
                continue
            
            # Count posts in this category for weighting
            post_count = 0
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
            
            # Add category with weight based on post count
            for _ in range(post_count):
                categories.append(category)
    
    # Sort posts by latest modified time
    posts.sort(key=lambda x: x['updated'], reverse=True)
    
    # Convert timestamps to ISO 8601
    for post in posts:
        post['updated'] = datetime.fromtimestamp(post['updated']).isoformat()
    
    return posts, categories

def generate_wordcloud_image(categories):
    """Generate word cloud image and return as base64 string"""
    if not WORDCLOUD_AVAILABLE or not categories:
        return None
    
    try:
        # Create word frequency dictionary
        word_freq = Counter(categories)
        
        # Generate word cloud
        wordcloud = WordCloud(
            width=800, 
            height=200, 
            background_color='transparent',
            colormap='viridis',
            max_words=50,
            relative_scaling=0.5,
            min_font_size=12
        ).generate_from_frequencies(word_freq)
        
        # Save to BytesIO
        img_buffer = BytesIO()
        plt.figure(figsize=(10, 2.5), facecolor='none')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(img_buffer, format='PNG', transparent=True, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        # Convert to base64
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        img_buffer.close()
        
        return img_base64
        
    except Exception as e:
        print(f"Error generating word cloud: {e}")
        return None

def generate_css_wordcloud(categories):
    """Generate CSS-based word cloud as fallback"""
    if not categories:
        return ""
    
    word_freq = Counter(categories)
    max_count = max(word_freq.values())
    
    css_words = []
    for word, count in word_freq.items():
        # Scale font size based on frequency (12px to 32px)
        font_size = 12 + (count / max_count) * 20
        css_words.append(f'<span style="font-size: {font_size}px; margin: 0 8px; opacity: {0.6 + (count / max_count) * 0.4};">{word}</span>')
    
    return ' '.join(css_words)

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

def generate_index_html(posts, categories, wordcloud_base64):
    posts_list_html = "\n".join(
        [f"                <li><a href='{p['path']}'>{p['category']} - {p['title']}</a></li>"
         for p in posts]
    )
    
    # Generate word cloud HTML
    if wordcloud_base64:
        wordcloud_html = f'<div class="wordcloud"><img src="data:image/png;base64,{wordcloud_base64}" alt="Categories Word Cloud" /></div>'
    else:
        # Fallback to CSS word cloud
        css_wordcloud = generate_css_wordcloud(categories)
        wordcloud_html = f'<div class="wordcloud css-wordcloud">{css_wordcloud}</div>' if css_wordcloud else ""

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
        <p class="tagline">Small notes, big impact.</p>
        {wordcloud_html}
    </header>
    <main>
        <section class="posts">
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

def main():
    posts, categories = scan_posts()
    
    # Generate word cloud image
    wordcloud_base64 = generate_wordcloud_image(categories)
    
    # Generate files
    generate_posts_json(posts)
    generate_categories_json(categories)
    generate_index_html(posts, categories, wordcloud_base64)
    
    print("CMS updated: index.html, posts.json, and categories.json")
    if wordcloud_base64:
        print("Word cloud generated successfully!")
    else:
        print("Using CSS fallback for word cloud")

if __name__ == "__main__":
    main()
