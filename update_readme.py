#!/usr/bin/env python3

import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import frontmatter

def parse_date_flexible(date_string):
    """Parse date string with flexible format support"""
    if not date_string:
        return datetime.now()
    
    try:
        # Try parsing with time first
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                # Fallback to date only
                return datetime.strptime(date_string, '%Y-%m-%d')
            except ValueError:
                # If parsing fails, use file modification time
                print(f"Warning: Could not parse date '{date_string}', using current date")
                return datetime.now()

def extract_title_and_content(filepath):
    """Extract title, content preview, and metadata from markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Initialize defaults
        title = ''
        date = ''
        tags = []
        body = content

        # Try to parse frontmatter
        try:
            post = frontmatter.loads(content)
            title = post.metadata.get('title', '')
            date = post.metadata.get('date', '')
            tags = post.metadata.get('tags', [])
            body = post.content
        except Exception as e:
            print(f"No frontmatter in {filepath}: {e}")

        # Extract title from markdown if not in frontmatter
        if not title:
            title_match = re.search(r'^#\s+(.+)', body, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                # Use filename as fallback
                title = Path(filepath).stem.replace('-', ' ').replace('_', ' ').title()

        # Extract content preview (skip title, get meaningful content)
        lines = body.split('\n')
        content_lines = []
        found_title = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip the first markdown title
            if line.startswith('#') and not found_title:
                found_title = True
                continue
            
            # Collect non-header, non-empty lines for preview
            if line and not line.startswith('#') and not line.startswith('---'):
                # Clean up markdown syntax for preview
                clean_line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)  # Remove links
                clean_line = re.sub(r'[*_`]', '', clean_line)  # Remove emphasis
                clean_line = clean_line.strip()
                
                if clean_line:
                    content_lines.append(clean_line)
                    if len(content_lines) >= 3:
                        break

        preview = ' '.join(content_lines)
        if len(preview) > 200:
            preview = preview[:197] + '...'

        # Use file modification time if no date in frontmatter
        if not date:
            mtime = os.path.getmtime(filepath)
            date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

        return {
            'title': title,
            'preview': preview,
            'date': date,
            'tags': tags if isinstance(tags, list) else [tags] if tags else []
        }

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def get_all_md_files():
    """Get all markdown files organized by category (folder)"""
    md_files = []
    
    # Walk through all directories
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and root
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        if root == '.':
            continue
            
        for file in files:
            if file.endswith('.md') and file.lower() != 'readme.md':
                filepath = os.path.join(root, file)
                md_files.append(filepath)
    
    return md_files

def generate_readme_and_json():
    """Generate README.md and posts.json with categorized content"""
    print("🔍 Scanning for markdown files...")
    md_files = get_all_md_files()
    
    if not md_files:
        print("⚠️  No markdown files found!")
        return

    entries = []
    categories = defaultdict(list)

    print(f"📝 Processing {len(md_files)} files...")
    
    for filepath in md_files:
        result = extract_title_and_content(filepath)
        if result and result['title'] and result['preview']:
            # Clean path for URLs
            clean_path = filepath.replace('\\', '/').lstrip('./')
            category = clean_path.split('/')[0].title()
            
            # Create GitHub URL
            github_url = f"https://github.com/m3hr4nn/TIL/blob/main/{clean_path}"
            
            entry = {
                'title': result['title'],
                'preview': result['preview'],
                'date': result['date'],
                'category': category,
                'tags': result['tags'],
                'url': github_url,
                'filepath': clean_path,
                'slug': Path(filepath).stem
            }
            
            entries.append(entry)
            categories[category].append(entry)
            print(f"✅ {category}: {result['title']}")

    if not entries:
        print("⚠️  No valid entries found!")
        return

    # Sort entries by date (newest first)
    entries.sort(key=lambda x: parse_date_flexible(x['date']), reverse=True)
    
    # Sort entries within each category
    for category in categories:
        categories[category].sort(key=lambda x: parse_date_flexible(x['date']), reverse=True)

    # Generate README content
    readme_content = f"""# Today I Learned (TIL)

> A collection of things I learn every day across a variety of languages and technologies.

## 📊 Stats

- **Total entries:** {len(entries)}
- **Categories:** {len(categories)}
- **Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🔥 Recent Entries

"""

    # Show recent entries (top 5)
    for entry in entries[:5]:
        readme_content += f"### {entry['date']} - {entry['title']}\n"
        readme_content += f"**Category:** {entry['category']}\n\n"
        readme_content += f"{entry['preview']}\n\n"
        if entry['tags']:
            tags_str = ' '.join([f"`{tag}`" for tag in entry['tags']])
            readme_content += f"**Tags:** {tags_str}\n\n"
        readme_content += f"[**Read more →**]({entry['url']})\n\n"
        readme_content += "---\n\n"

    # Add categories section
    readme_content += "## 📚 Categories\n\n"
    
    for category, cat_entries in sorted(categories.items()):
        readme_content += f"### {category} ({len(cat_entries)} entries)\n\n"
        
        for entry in cat_entries[:3]:  # Show top 3 in each category
            readme_content += f"- **[{entry['title']}]({entry['url']})** _{entry['date']}_\n"
        
        if len(cat_entries) > 3:
            readme_content += f"- ... and {len(cat_entries) - 3} more\n"
        
        readme_content += "\n"

    readme_content += f"""## 🌐 Website

Visit the interactive website at: **[https://m3hr4nn.github.io/TIL/](https://m3hr4nn.github.io/TIL/)**

## 🏗️ Structure

```
TIL/
├── Category1/
│   ├── topic1.md
│   └── topic2.md
├── Category2/
│   ├── topic3.md
│   └── topic4.md
└── README.md (auto-generated)
```

---

_This README is automatically generated from the markdown files in this repository. Add your `.md` files in category folders and they'll appear here automatically!_
"""

    # Write README.md
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ README.md generated successfully")
    except Exception as e:
        print(f"❌ Error writing README.md: {e}")
        return

    # Prepare data for posts.json (for the website)
    posts_data = {
        'posts': entries,
        'categories': dict(categories),
        'stats': {
            'total_posts': len(entries),
            'total_categories': len(categories),
            'last_updated': datetime.now().isoformat(),
            'category_counts': {cat: len(entries) for cat, entries in categories.items()}
        }
    }

    # Write posts.json
    try:
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts_data, f, indent=2, ensure_ascii=False)
        print("✅ posts.json generated successfully")
    except Exception as e:
        print(f"❌ Error writing posts.json: {e}")
        return

    print(f"🎉 Generated {len(entries)} entries across {len(categories)} categories")
    print("Categories:", list(categories.keys()))

if __name__ == "__main__":
    generate_readme_and_json()
