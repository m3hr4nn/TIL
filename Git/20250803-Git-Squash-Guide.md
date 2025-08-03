---
title: "Git Squash Guide"
date: "2025-08-03"
tags: ["git", "basics", "syntax"]
---

# Git Squash Guide

## What is Git Squash?

Git squash is a technique used to combine multiple commits into a single commit. This helps create a cleaner, more organized commit history by condensing related changes into logical units.

## How to Use Git Squash

### Interactive Rebase (Most Common Method)

```bash
# Squash the last 3 commits
git rebase -i HEAD~3

# Squash commits up to a specific commit
git rebase -i <commit-hash>
```

In the interactive editor that opens:
1. Keep the first commit as `pick`
2. Change subsequent commits from `pick` to `squash` (or `s`)
3. Save and close the editor
4. Edit the commit message in the next editor that opens

**Example:**
```
pick 1234567 Add user authentication
squash 2345678 Fix authentication bug
squash 3456789 Update auth tests
```

### Merge with Squash

```bash
# Squash all commits from feature branch when merging
git merge --squash feature-branch
git commit -m "Add complete user authentication feature"
```

### Reset and Recommit

```bash
# Soft reset to combine commits manually
git reset --soft HEAD~3
git commit -m "Combined commit message"
```

## When to Use Git Squash

### ✅ Good Use Cases

- **Before merging feature branches**: Clean up work-in-progress commits
- **Fixing typos and small bugs**: Combine fix commits with original feature commits
- **Related commits**: Group commits that implement a single logical feature
- **Cleaning up experimentation**: Remove "trying this" and "trying that" commits
- **Code review preparation**: Present clean history to reviewers

### ❌ Avoid Squashing When

- **Commits are already pushed** to shared branches (rewrites history)
- **Different logical changes**: Don't combine unrelated features
- **Important debugging info**: Keep commits that help understand the development process
- **Working on main/master**: Never rewrite history on shared branches
- **Commits have different authors**: Preserve attribution

## Best Practices

### Before Squashing
- Ensure you're on a feature branch, not main/master
- Make sure no one else is working on the same branch
- Back up your branch: `git branch backup-branch-name`

### Commit Message Guidelines
- Write clear, descriptive commit messages after squashing
- Follow your team's commit message conventions
- Include ticket numbers or issue references if applicable

### Example Workflow
```bash
# 1. Create and work on feature branch
git checkout -b feature/user-auth
# ... make several commits ...

# 2. Before merging, squash commits
git rebase -i HEAD~5

# 3. Push the squashed branch
git push --force-with-lease origin feature/user-auth

# 4. Create pull request with clean history
```

## Common Commands Summary

| Command | Purpose |
|---------|---------|
| `git rebase -i HEAD~n` | Interactive rebase for last n commits |
| `git merge --squash branch` | Squash merge from another branch |
| `git reset --soft HEAD~n` | Soft reset to combine commits manually |
| `git push --force-with-lease` | Safely force push after rewriting history |

## Tips and Warnings

### 🔧 Tips
- Use `--force-with-lease` instead of `--force` when pushing rewritten history
- Practice squashing on test branches first
- Use descriptive commit messages after squashing
- Consider using `git log --oneline` to visualize commit history

### ⚠️ Warnings
- **Never squash commits on shared branches** (main, master, develop)
- **Always communicate** with team members before rewriting shared history
- **Test thoroughly** after squashing to ensure nothing was lost
- **Be careful with merge conflicts** during interactive rebase

## Alternative: Squash and Merge via GitHub/GitLab

Most Git hosting platforms offer "Squash and Merge" options in their web interface, which automatically squashes all commits from a pull request into a single commit when merging. This is often safer than manual squashing for teams.
