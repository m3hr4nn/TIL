import os
import json
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GITHUB_REPO_URL = "https://github.com/m3hr4nn/TIL/blob/main"

def extract_date_from_filename(filename):
    """Extract date from filename if it starts with YYYYMMDD format"""
    date_pattern = r'^(\d{8})'
    match = re.match(date_pattern, filename)
    if match:
        date_str = match.group(1)
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            timestamp = date_obj.timestamp()
            return timestamp
        except ValueError:
            pass
    return None

def scan_posts():
    posts = []
    debug_info = []
    
    for category in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category)
        if os.path.isdir(category_path) and not category.startswith('.'):
            if category == ".github":
                continue
            
            for file in os.listdir(category_path):
                if file.endswith('.md'):
                    file_path = os.path.join(category_path, file)
                    filename_without_ext = os.path.splitext(file)[0]
                    
                    # Debug: Log what we're processing
                    debug_info.append(f"Processing: {category}/{file}")
                    debug_info.append(f"  Filename without ext: '{filename_without_ext}'")
                    
                    # Extract date from filename (YYYYMMDD format)
                    file_date = extract_date_from_filename(filename_without_ext)
                    if file_date is None:
                        # Fallback to file modification time if no date in filename
                        file_date = os.path.getmtime(file_path)
                        debug_info.append(f"  No date found, using file mtime: {datetime.fromtimestamp(file_date)}")
                    else:
                        debug_info.append(f"  Found date: {datetime.fromtimestamp(file_date)}")
                    
                    posts.append({
                        "category": category,
                        "title": filename_without_ext,
                        "path": f"{GITHUB_REPO_URL}/{category}/{file}",
                        "updated": file_date
                    })
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['updated'], reverse=True)
    
    # Convert timestamps to ISO 8601
    for post in posts:
        post['updated'] = datetime.fromtimestamp(post['updated']).isoformat()
    
    # Write debug info to a file
    with open(os.path.join(BASE_DIR, 'debug.txt'), 'w', encoding='utf-8') as f:
        f.write("=== DEBUG INFO ===\n")
        f.write(f"Total posts found: {len(posts)}\n\n")
        for info in debug_info:
            f.write(info + "\n")
        f.write("\n=== FINAL SORT ORDER ===\n")
        for i, post in enumerate(posts):
            f.write(f"{i+1}. {post['category']}/{post['title']} - {post['updated']}\n")
    
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
    try:
        posts = scan_posts()
        generate_posts_json(posts)
        generate_index_html(posts)
        print("CMS updated: index.html, posts.json, and debug.txt")
    except Exception as e:
        # Write error to debug file
        with open(os.path.join(BASE_DIR, 'debug.txt'), 'w', encoding='utf-8') as f:
            f.write(f"ERROR: {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())
        print(f"Error occurred: {e}")
        raise

if __name__ == "__main__":
    main()
