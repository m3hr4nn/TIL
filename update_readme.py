#!/usr/bin/env python3

import os
import re
import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Remove frontmatter dependency for now - let's test without it
# import frontmatter

def parse_date_flexible(date_string):
    """Parse date string with flexible format support"""
    if not date_string:
        return datetime.now()
    
    try:
        return datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        except ValueError:
            try:
                return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                print(f"Warning: Could not parse date '{date_string}', using current date")
                return datetime.now()

def extract_title_and_content(filepath):
    """Extract title, content preview, and metadata from markdown file"""
    print(f"📝 Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"   📄 File size: {len(content)} characters")

        # Initialize defaults
        title = ''
        date = ''
        tags = []
        body = content

        # Simple frontmatter parsing (without library)
        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_text = parts[1]
                    body = parts[2].strip()
                    
                    # Parse YAML-like frontmatter
                    for line in frontmatter_text.strip().split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            
                            if key == 'title':
                                title = value
                            elif key == 'date':
                                date = value
                            elif key == 'tags':
                                # Simple tag parsing
                                tags = [t.strip().strip('"\'') for t in value.strip('[]').split(',')]
                    
                    print(f"   ✅ Found frontmatter - title: {title}, date: {date}")
            except Exception as e:
                print(f"   ⚠️  Frontmatter parsing failed: {e}")

        # Extract title from markdown if not in frontmatter
        if not title:
            title_match = re.search(r'^#\s+(.+)', body, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                print(f"   📌 Extracted title from markdown: {title}")
            else:
                # Use filename as fallback
                title = Path(filepath).stem.replace('-', ' ').replace('_', ' ').title()
                print(f"   📂 Using filename as title: {title}")

        # Extract content preview
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
            
            # Collect content lines
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

        print(f"   📖 Preview: {preview[:50]}...")

        # Use file modification time if no date
        if not date:
            mtime = os.path.getmtime(filepath)
            date = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
            print(f"   📅 Using file mtime: {date}")

        result = {
            'title': title,
            'preview': preview,
            'date': date,
            'tags': [tag for tag in tags if tag] if isinstance(tags, list) else []
        }
        
        print(f"   ✅ Successfully processed: {title}")
        return result

    except Exception as e:
        print(f"   ❌ Error processing {filepath}: {e}")
        return None

def get_all_md_files():
    """Get all markdown files organized by category (folder)"""
    print("🔍 Scanning for markdown files...")
    md_files = []
    
    # Show current directory structure
    print(f"📁 Current directory: {os.getcwd()}")
    print("📁 Directory contents:")
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(f"   📂 {item}/")
        else:
            print(f"   📄 {item}")
    
    # Walk through all directories
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        if root == '.':
            continue
            
        print(f"📂 Checking directory: {root}")
        
        for file in files:
            if file.endswith('.md') and file.lower() != 'readme.md':
                filepath = os.path.join(root, file)
                md_files.append(filepath)
                print(f"   ✅ Found: {filepath}")
    
    print(f"📊 Total markdown files found: {len(md_files)}")
    return md_files

def generate_readme_and_json():
    """Generate README.md and posts.json with categorized content"""
    print("🚀 Starting README and JSON generation...")
    
    md_files = get_all_md_files()
    
    if not md_files:
        print("⚠️  No markdown files found!")
        # Create empty files anyway
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write("# Today I Learned (TIL)\n\n> No entries yet. Add some .md files in category folders!\n")
        
        with open('posts.json', 'w', encoding='utf-8') as f:
            json.dump({
                'posts': [],
                'categories': {},
                'stats': {
                    'total_posts': 0,
                    'total_categories': 0,
                    'last_updated': datetime.now().isoformat(),
                    'category_counts': {}
                }
            }, f, indent=2)
        
        print("✅ Created empty README.md and posts.json")
        return

    entries = []
    categories = defaultdict(list)

    print(f"📝 Processing {len(md_files)} files...")
    
    for filepath in md_files:
        result = extract_title_and_content(filepath)
        if result and result['title']:
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
            print(f"✅ Added: {category} -> {result['title']}")
        else:
            print(f"❌ Skipped: {filepath} (no title or content)")

    if not entries:
        print("⚠️  No valid entries found!")
        return

    print(f"📊 Found {len(entries)} valid entries in {len(categories)} categories")

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

---

_This README is automatically generated from the markdown files in this repository._
"""

    # Write README.md
    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ README.md written successfully")
    except Exception as e:
        print(f"❌ Error writing README.md: {e}")
        return

    # Prepare data for posts.json
    posts_data = {
        'posts': entries,
        'categories': {cat: [entry for entry in cat_entries] for cat, cat_entries in categories.items()},
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
        print("✅ posts.json written successfully")
        
        # Show a preview of the JSON
        print(f"📄 posts.json preview:")
        print(f"   📊 Posts: {len(posts_data['posts'])}")
        print(f"   📂 Categories: {list(posts_data['categories'].keys())}")
        print(f"   📅 Last updated: {posts_data['stats']['last_updated']}")
        
    except Exception as e:
        print(f"❌ Error writing posts.json: {e}")
        return

    print(f"🎉 Successfully generated content!")
    print(f"   📝 {len(entries)} entries")
    print(f"   📂 {len(categories)} categories: {list(categories.keys())}")

if __name__ == "__main__":
    generate_readme_and_json()
