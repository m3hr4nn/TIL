## Example TIL Entries

### AI/prompt-engineering-tips.md
```markdown
# Effective Prompt Engineering for LLMs

## Context
Learning how to write better prompts for large language models to get more accurate and useful responses.

## Key Techniques

### 1. Be Specific and Clear
Instead of: "Help me with Python"
Use: "Show me how to read a CSV file in Python using pandas and handle missing values"

### 2. Provide Context
```python
# Instead of asking "Fix this code"
# Provide context like:
# "This Python function should calculate fibonacci numbers but returns wrong results"
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
