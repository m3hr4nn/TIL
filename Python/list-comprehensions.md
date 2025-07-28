---
title: "Python List Comprehensions"
date: "2025-07-28"
tags: ["python", "basics"]
---

# Python List Comprehensions

List comprehensions provide a concise way to create lists in Python.

Basic syntax: `[expression for item in iterable]`

Examples:
- `squares = [x**2 for x in range(10)]`
- `evens = [x for x in range(20) if x % 2 == 0]`

## JavaScript/async-await.md
---
title: "JavaScript Async/Await"
date: "2025-07-27"
tags: ["javascript", "async"]
---

# JavaScript Async/Await

Async/await makes working with promises much easier and more readable.

```javascript
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

## Linux/vim-commands.md
---
title: "Essential Vim Commands"
date: "2025-07-26"
tags: ["vim", "linux", "editor"]
---

# Essential Vim Commands

Basic navigation and editing commands in Vim.

## Navigation
- `h, j, k, l` - left, down, up, right
- `w` - next word
- `b` - previous word
- `0` - beginning of line
- `$` - end of line

## Editing
- `i` - insert mode
- `a` - append mode
- `o` - new line below
- `dd` - delete line
