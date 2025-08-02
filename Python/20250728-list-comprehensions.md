---
title: "Python List Comprehensions"
date: "2025-07-28"
tags: ["python", "basics", "syntax"]
---

# Python List Comprehensions

List comprehensions provide a concise way to create lists in Python.

## Basic Syntax

```python
[expression for item in iterable]
```

## Examples

### Simple list creation
```python
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### With conditions
```python
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

### Nested comprehensions
```python
matrix = [[i*j for j in range(3)] for i in range(3)]
# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]
```

List comprehensions are faster and more readable than traditional for loops for simple operations.
