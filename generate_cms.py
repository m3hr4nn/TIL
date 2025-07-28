import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_REPO_URL = "https://github.com/m3hr4nn/TIL/blob/main"

def scan_posts():
    posts = []
    for category in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category)
        if os.path.isdir(category_path) and not category.startswith('.'):
            if category == ".github":
                continue
            for file in os.listdir(category_path):
                if file.endswith('.md'):
                    file_path = os.path.join(category_path, file)
                    posts.append({
                        "category": category,
                        "title": os.path.splitext(file)[0],
                        "path": f"{GITHUB_REPO_URL}/{category}/{file}",
                        "updated": os.path.getmtime(file_path)
                    })
    # Sort posts by latest modified time
    posts.sort(key=lambda x: x['updated'], reverse=True)
    # Convert timestamps to ISO 8601
    for post in posts:
        post['updated'] = datetime.fromtimestamp(post['updated']).isoformat()
    return posts

def generate_posts_json(posts):
    with open(os.path.join(BASE_DIR, 'posts.json'), 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

def generate_index_html(posts):
    posts_list_html = "\n".join(
        [f"                <li><a href='{p['path']}'>{p['category']} - {p['title']}</a></li>"
         for p in posts]
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

def main():
    posts = scan_posts()
    generate_posts_json(posts)
    generate_index_html(posts)
    print("CMS updated: index.html and posts.json")

if __name__ == "__main__":
    main()
