import os
from pathlib import Path
from datetime import datetime

REPO_URL = "https://github.com/m3hr4nn/TIL/blob/main"

def get_note_info(md_path):
    # Get date from file modification time
    date = datetime.fromtimestamp(md_path.stat().st_mtime).strftime('%Y-%m-%d')
    # Title: filename without extension
    title = md_path.parent.name + '/' + md_path.stem
    # Read first 2-3 non-empty lines
    with md_path.open(encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    preview = '\n'.join(lines[:3])
    # Build GitHub link
    rel_path = md_path.relative_to(Path.cwd())
    link = f"{REPO_URL}/{rel_path.as_posix()}"
    return f"- **{date} – {title}**  \n{preview}  \n[see more...]({link})\n"

def main():
    notes = []
    for md_path in Path('.').rglob('*.md'):
        if md_path.name == 'README.md':
            continue
        notes.append(get_note_info(md_path))
    notes.sort(reverse=True)  # Optional: newest first
    with open('../README.md', 'w', encoding='utf-8') as f:
        f.write("## Today I Learned\n\n")
        f.write('\n'.join(notes))

if __name__ == "__main__":
    main()
