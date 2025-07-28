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
