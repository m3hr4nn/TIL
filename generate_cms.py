import os
import json
from datetime import datetime
import markdown

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
                        html_content = markdown.markdown(content)
                        posts.append({
                            "category": category,
                            "title": os.path.splitext(file)[0],
                            "path": f"{category}/{file}",
                            "html": html_content,
                            "updated": datetime.fromtimestamp(
                                os.path.getmtime(file_path)
                            ).isoformat()
                        })
    return posts

def generate_posts_json(posts):
    with open(os.path.join(BASE_DIR, 'posts.json'), 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

def generate_index_html(posts):
    html = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='UTF-8' />",
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0' />",
        "  <title>Today I Learned</title>",
        "  <style>body{font-family:sans-serif;margin:2rem;}a{text-decoration:none;color:#0070f3;}li{margin:0.5rem 0;}</style>",
        "</head>",
        "<body>",
        "  <h1>Today I Learned (TIL)</h1>",
        "  <ul>"
    ]
    for post in sorted(posts, key=lambda x: (x['category'], x['title'])):
        html.append(f"    <li><a href='{post['path']}'>{post['category']} - {post['title']}</a></li>")
    html += ["  </ul>", "</body>", "</html>"]

    with open(os.path.join(BASE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write("\n".join(html))

def main():
    posts = scan_posts()
    generate_posts_json(posts)
    generate_index_html(posts)
    print("CMS files generated: index.html and posts.json")

if __name__ == "__main__":
    main()
