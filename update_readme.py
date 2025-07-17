#!/usr/bin/env python3


import os
import re
import json
from datetime import datetime
from pathlib import Path
import frontmatter

def extract_title_and_content(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            post = frontmatter.loads(content)
            title = post.metadata.get('title', '')
            body = post.content
            date = post.metadata.get('date', '')
        except:
            body = content
            title = ''
            date = ''

        if not title:
            title_match = re.search(r'^#\s+(.+)', body, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else Path(filepath).stem.replace('-', ' ').title()

        lines = body.split('\n')
        content_lines = []
        skip_title = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#') and not skip_title:
                skip_title = True
                continue
            if line and not line.startswith('#'):
                content_lines.append(line)
                if len(content_lines) >= 3:
                    break
        preview = ' '.join(content_lines[:3])
        preview = preview[:147] + '...' if len(preview) > 150 else preview

        if not date:
            mtime = os.path.getmtime(filepath)
            date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

        return title, preview, date
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None, None, None

def get_all_md_files():
    md_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        if root == '.':
            continue
        for file in files:
            if file.endswith('.md') and file.lower() != 'readme.md':
                md_files.append(os.path.join(root, file))
    return md_files

def generate_readme_and_json():
    md_files = get_all_md_files()
    entries = []

    for filepath in md_files:
        title, preview, date = extract_title_and_content(filepath)
        if title and preview:
            clean_path = filepath.replace(os.sep, '/').lstrip('./')
            folder = clean_path.split('/')[0]
            github_url = f"https://github.com/m3hr4nn/TIL/blob/main/{clean_path}"

            entries.append({
                'title': title,
                'preview': preview,
                'date': date,
                'folder': folder,
                'url': github_url,
                'filepath': clean_path
            })

    entries.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M'), reverse=True)

    # Build README content
    readme_content = """# Today I Learned (TIL)

> A collection of things I learn every day across a variety of languages and technologies.

## Recent Entries

"""
    for entry in entries:
        readme_content += f"### {entry['date']} - {entry['title']}\n\n"
        readme_content += f"{entry['preview']}\n\n"
        readme_content += f"[**See more...**]({entry['url']})\n\n"
        readme_content += "---\n\n"

    readme_content += f"""## Stats

- **Total entries:** {len(entries)}
- **Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

_This README is automatically generated from the markdown files in this repository._
"""

    # Write README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)

    # Write posts.json
    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2)

    print("✅ README.md and posts.json generated successfully.")

if __name__ == "__main__":
    generate_readme_and_json()
