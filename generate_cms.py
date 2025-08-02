import os
import json
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_REPO_URL = "https://github.com/m3hr4nn/TIL/blob/main"

def extract_date_from_filename(filename):
    """Extract date from filename if it starts with YYYYMMDD format"""
    print(f"[DEBUG] Checking filename: '{filename}'")
    date_pattern = r'^(\d{8})'
    match = re.match(date_pattern, filename)
    if match:
        date_str = match.group(1)
        print(f"[DEBUG] Found date string: {date_str}")
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            timestamp = date_obj.timestamp()
            print(f"[DEBUG] Converted to: {date_obj} (timestamp: {timestamp})")
            return timestamp
        except ValueError as e:
            print(f"[DEBUG] Error parsing date: {e}")
    else:
        print(f"[DEBUG] No date found in filename")
    return None

def scan_posts():
    posts = []
    
    print("[DEBUG] Starting to scan posts...")
    for category in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category)
        if os.path.isdir(category_path) and not category.startswith('.'):
            if category == ".github":
                continue
            
            print(f"[DEBUG] Scanning category: {category}")
            for file in os.listdir(category_path):
                if file.endswith('.md'):
                    print(f"[DEBUG] Processing file: {file}")
                    file_path = os.path.join(category_path, file)
                    filename_without_ext = os.path.splitext(file)[0]
                    print(f"[DEBUG] Filename without extension: '{filename_without_ext}'")
                    
                    # Extract date from filename (YYYYMMDD format)
                    file_date = extract_date_from_filename(filename_without_ext)
                    if file_date is None:
                        # Fallback to file modification time if no date in filename
                        file_date = os.path.getmtime(file_path)
                        print(f"[DEBUG] Using file mtime: {datetime.fromtimestamp(file_date)}")
                    
                    posts.append({
                        "category": category,
                        "title": filename_without_ext,
                        "path": f"{GITHUB_REPO_URL}/{category}/{file}",
                        "updated": file_date
                    })
    
    print(f"[DEBUG] Found {len(posts)} posts before sorting")
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['updated'], reverse=True)
    
    print("[DEBUG] Posts after sorting:")
    for i, post in enumerate(posts):
        print(f"[DEBUG] {i+1}. {post['category']}/{post['title']} - {datetime.fromtimestamp(post['updated'])}")
    
    # Convert timestamps to ISO 8601
    for post in posts:
        post['updated'] = datetime.fromtimestamp(post['updated']).isoformat()
    
    return posts

def generate_posts_json(posts):
    # Add debug comment to the JSON
    debug_comment = {
        "_debug": f"Generated at {datetime.now().isoformat()}, found {len(posts)} posts"
    }
    output_data = [debug_comment] + posts
    
    with open(os.path.join(BASE_DIR, 'posts.json'), 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)

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
    <!-- Debug: Generated at {datetime.now().isoformat()}, found {len(posts)} posts -->
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
    print("[DEBUG] Starting CMS generation...")
    posts = scan_posts()
    generate_posts_json(posts)
    generate_index_html(posts)
    print("[DEBUG] CMS updated: index.html and posts.json")

if __name__ == "__main__":
    main()
