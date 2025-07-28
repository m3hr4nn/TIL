import os
import json
from datetime import datetime
import markdown

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STYLES_CSS = """/* Auto-generated styles.css */
body {
    background-color: #1e1e1e;
    color: #f1f1f1;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    margin: 0;
    padding: 0;
}
header {
    text-align: center;
    padding: 2rem 1rem;
    background-color: #2b2b2b;
    border-bottom: 2px solid #8b0000;
}
header h1 {
    margin: 0;
    font-size: 2.5rem;
}
.tagline {
    font-size: 1.2rem;
    color: #ccc;
    margin-top: 0.5rem;
}
main {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}
.posts ul {
    list-style: none;
    padding: 0;
}
.posts li {
    margin: 0.75rem 0;
    font-size: 1.2rem;
}
.posts a {
    color: #b22222;
    text-decoration: none;
    transition: color 0.2s ease-in-out;
}
.posts a:hover {
    color: #ff4040;
    text-decoration: underline;
}
footer {
    text-align: center;
    padding: 1.5rem;
    background-color: #2b2b2b;
    color: #aaa;
    font-size: 0.9rem;
    border-top: 2px solid #8b0000;
}
footer a {
    color: #b22222;
    text-decoration: none;
}
footer a:hover {
    text-decoration: underline;
}
"""

def scan_posts():
    posts = []
    for category in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category)
        if os.path.isdir(category_path) and not category.startswith('.'):
            for file in os.listdir(category_path):
                if file.endswith('.md'):
                    file_path = os.path.join(category_path, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        posts.append({
                            "category": category,
                            "title": os.path.splitext(file)[0],
                            "path": f"{category}/{file}",
                            "updated": datetime.fromtimestamp(
                                os.path.getmtime(file_path)
                            ).isoformat()
                        })
    return posts

def generate_posts_json(posts):
    with open(os.path.join(BASE_DIR, 'posts.json'), 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

def generate_index_html(posts):
    posts_list_html = "\n".join(
        [f"                <li><a href='{p['path']}'>{p['category']} - {p['title']}</a></li>"
         for p in sorted(posts, key=lambda x: (x['category'], x['title']))]
    )

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

def ensure_styles_css():
    css_path = os.path.join(BASE_DIR, 'styles.css')
    if not os.path.exists(css_path):
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(STYLES_CSS)

def main():
    posts = scan_posts()
    generate_posts_json(posts)
    generate_index_html(posts)
    ensure_styles_css()
    print("CMS updated: index.html, posts.json, and styles.css")

if __name__ == "__main__":
    main()
