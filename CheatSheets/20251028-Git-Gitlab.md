# Git/GitLab Interview Cheat Sheet

## Git Basics

### Configuration
```bash
# Set user info
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Set default editor
git config --global core.editor "vim"

# View configuration
git config --list
git config user.name

# Config levels: --system, --global, --local
```

### Repository Setup
```bash
# Initialize repository
git init

# Clone repository
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git custom-name

# Clone specific branch
git clone -b branch-name https://github.com/user/repo.git
```

## Basic Commands

### Status and Information
```bash
# Check status
git status
git status -s  # Short format

# View commit history
git log
git log --oneline
git log --graph --all --decorate
git log --author="John"
git log --since="2 weeks ago"
git log -p  # Show diff
git log --stat  # Show stats

# Show specific commit
git show COMMIT_HASH
git show HEAD~2  # 2 commits back

# View differences
git diff  # Unstaged changes
git diff --staged  # Staged changes
git diff branch1..branch2  # Between branches
```

### Staging and Committing
```bash
# Add files to staging
git add file.txt
git add .  # Add all files
git add *.js  # Add pattern
git add -p  # Interactive staging

# Remove from staging
git reset HEAD file.txt
git restore --staged file.txt

# Commit changes
git commit -m "Commit message"
git commit -am "Add and commit"  # Tracked files only

# Amend last commit
git commit --amend
git commit --amend --no-edit
git commit --amend --author="Name <email>"
```

## Branches

### Branch Management
```bash
# List branches
git branch  # Local branches
git branch -r  # Remote branches
git branch -a  # All branches

# Create branch
git branch feature-branch
git checkout -b feature-branch  # Create and switch
git switch -c feature-branch  # Modern syntax

# Switch branches
git checkout branch-name
git switch branch-name

# Rename branch
git branch -m old-name new-name
git branch -m new-name  # Rename current

# Delete branch
git branch -d branch-name  # Safe delete
git branch -D branch-name  # Force delete

# Delete remote branch
git push origin --delete branch-name
```

### Merging
```bash
# Merge branch into current
git merge feature-branch

# Merge with no fast-forward
git merge --no-ff feature-branch

# Abort merge
git merge --abort

# Resolve conflicts manually, then:
git add resolved-file.txt
git commit
```

### Rebasing
```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Interactive rebase commands:
# pick - use commit
# reword - edit commit message
# edit - stop to amend commit
# squash - combine with previous
# fixup - like squash, discard message
# drop - remove commit

# Continue after resolving conflicts
git rebase --continue

# Abort rebase
git rebase --abort

# Skip current commit
git rebase --skip
```

## Remote Operations

### Remote Management
```bash
# List remotes
git remote
git remote -v

# Add remote
git remote add origin https://github.com/user/repo.git

# Change remote URL
git remote set-url origin https://github.com/user/new-repo.git

# Remove remote
git remote remove origin

# Rename remote
git remote rename origin upstream
```

### Push and Pull
```bash
# Push to remote
git push origin main
git push -u origin main  # Set upstream

# Push all branches
git push --all origin

# Push tags
git push --tags

# Force push (dangerous)
git push --force
git push --force-with-lease  # Safer

# Pull from remote
git pull origin main
git pull --rebase origin main

# Fetch without merging
git fetch origin
git fetch --all
```

## Stashing

```bash
# Stash changes
git stash
git stash save "Work in progress"

# List stashes
git stash list

# Apply stash
git stash apply  # Keep stash
git stash pop  # Apply and remove

# Apply specific stash
git stash apply stash@{2}

# Drop stash
git stash drop stash@{0}

# Clear all stashes
git stash clear

# Create branch from stash
git stash branch new-branch stash@{0}
```

## Undoing Changes

### Discard Changes
```bash
# Discard working directory changes
git checkout -- file.txt
git restore file.txt

# Discard all changes
git checkout .
git restore .
```

### Reset
```bash
# Soft reset (keep changes staged)
git reset --soft HEAD~1

# Mixed reset (keep changes unstaged) - default
git reset HEAD~1
git reset --mixed HEAD~1

# Hard reset (discard changes) - DANGEROUS
git reset --hard HEAD~1
git reset --hard origin/main
```

### Revert
```bash
# Create new commit that undoes changes
git revert COMMIT_HASH

# Revert without committing
git revert -n COMMIT_HASH
```

## Tags

```bash
# List tags
git tag
git tag -l "v1.*"

# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Version 1.0.0"

# Tag specific commit
git tag v1.0.0 COMMIT_HASH

# Push tags
git push origin v1.0.0
git push origin --tags

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0

# Checkout tag
git checkout v1.0.0
```

## Advanced Git

### Cherry-pick
```bash
# Apply specific commit to current branch
git cherry-pick COMMIT_HASH

# Cherry-pick without committing
git cherry-pick -n COMMIT_HASH

# Cherry-pick range
git cherry-pick COMMIT1..COMMIT2
```

### Bisect (Find bug)
```bash
# Start bisect
git bisect start

# Mark current as bad
git bisect bad

# Mark known good commit
git bisect good COMMIT_HASH

# Git will checkout commits for testing
# Mark each as good or bad
git bisect good
git bisect bad

# Finish bisect
git bisect reset
```

### Reflog
```bash
# View reference logs (all changes to HEAD)
git reflog

# Recover lost commit
git checkout COMMIT_HASH
git checkout -b recovery-branch
```

### Worktrees
```bash
# Create worktree
git worktree add ../feature-worktree feature-branch

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../feature-worktree
```

### Submodules
```bash
# Add submodule
git submodule add https://github.com/user/repo.git path/to/submodule

# Initialize submodules
git submodule init
git submodule update

# Clone with submodules
git clone --recurse-submodules https://github.com/user/repo.git

# Update submodules
git submodule update --remote
```

## GitLab Specific

### GitLab CI/CD (.gitlab-ci.yml)
```yaml
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: myapp:latest

before_script:
  - echo "Setting up environment"

build_job:
  stage: build
  script:
    - echo "Building application"
    - docker build -t $DOCKER_IMAGE .
  artifacts:
    paths:
      - build/
    expire_in: 1 week
  only:
    - main
    - merge_requests

test_job:
  stage: test
  script:
    - echo "Running tests"
    - npm test
  coverage: '/Coverage: \d+\.\d+%/'
  dependencies:
    - build_job

deploy_production:
  stage: deploy
  script:
    - echo "Deploying to production"
    - kubectl apply -f k8s/
  environment:
    name: production
    url: https://app.example.com
  only:
    - main
  when: manual
```

### GitLab Runner
```bash
# Register runner
gitlab-runner register \
  --url https://gitlab.com/ \
  --registration-token TOKEN \
  --executor docker \
  --docker-image alpine:latest

# Start runner
gitlab-runner start

# List runners
gitlab-runner list
```

### Merge Request via CLI
```bash
# Create merge request
git push -o merge_request.create \
  -o merge_request.target=main \
  -o merge_request.title="Feature X"

# Set assignee and reviewer
git push -o merge_request.create \
  -o merge_request.assign="@username" \
  -o merge_request.reviewer="@reviewer"
```

### GitLab API
```bash
# Get projects
curl --header "PRIVATE-TOKEN: your-token" \
  "https://gitlab.com/api/v4/projects"

# Create issue
curl --request POST \
  --header "PRIVATE-TOKEN: your-token" \
  --data "title=Bug in feature&description=Details here" \
  "https://gitlab.com/api/v4/projects/PROJECT_ID/issues"

# Trigger pipeline
curl --request POST \
  --form token=TOKEN \
  --form ref=main \
  "https://gitlab.com/api/v4/projects/PROJECT_ID/trigger/pipeline"
```

## Git Flow

### Main Branches
- **main/master**: Production-ready code
- **develop**: Integration branch

### Supporting Branches
- **feature/***: New features
- **release/***: Release preparation
- **hotfix/***: Emergency production fixes

### Workflow
```bash
# Start feature
git checkout -b feature/new-feature develop

# Finish feature
git checkout develop
git merge --no-ff feature/new-feature
git branch -d feature/new-feature
git push origin develop

# Start release
git checkout -b release/1.0.0 develop

# Finish release
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0
git checkout develop
git merge --no-ff release/1.0.0
git branch -d release/1.0.0

# Hotfix
git checkout -b hotfix/1.0.1 main
# Fix bug
git checkout main
git merge --no-ff hotfix/1.0.1
git tag -a v1.0.1
git checkout develop
git merge --no-ff hotfix/1.0.1
git branch -d hotfix/1.0.1
```

## .gitignore

```bash
# Example .gitignore
*.log
*.tmp
node_modules/
.env
.DS_Store
build/
dist/
*.class

# Ignore all except
!important.log

# Ignore directory
temp/

# Remove tracked file from git
git rm --cached file.txt
git rm -r --cached directory/
```

## Common Interview Questions

**Q: Difference between git merge and git rebase?**
- Merge: Creates merge commit, preserves history
- Rebase: Rewrites history, linear timeline
- Use merge for shared branches, rebase for local cleanup

**Q: What is git stash?**
- Temporarily saves changes without committing
- Useful for switching branches with uncommitted work
- Can apply stash later with `git stash pop`

**Q: Explain git reset --soft, --mixed, --hard**
- soft: Move HEAD, keep changes staged
- mixed: Move HEAD, unstage changes (default)
- hard: Move HEAD, discard all changes (DANGEROUS)

**Q: How to undo last commit?**
- `git reset --soft HEAD~1`: Undo commit, keep changes
- `git revert HEAD`: Create new commit undoing changes
- `git commit --amend`: Modify last commit

**Q: What is a detached HEAD?**
- HEAD points to specific commit, not a branch
- Happens with `git checkout COMMIT_HASH`
- Create branch to save work: `git checkout -b new-branch`

**Q: Difference between origin and upstream?**
- origin: Your fork/repo
- upstream: Original repo you forked from
- Convention, not enforced by Git

**Q: How to resolve merge conflicts?**
- Edit conflicted files manually
- Remove conflict markers (<<<<, ====, >>>>)
- `git add` resolved files
- `git commit` to complete merge

**Q: What is git cherry-pick?**
- Apply specific commit from another branch
- Creates new commit with same changes
- Useful for hotfixes

**Q: Explain fast-forward merge**
- Linear history, no merge commit
- Happens when target branch hasn't diverged
- Use `--no-ff` to force merge commit

**Q: What is GitLab CI/CD?**
- Continuous Integration/Deployment
- Defined in .gitlab-ci.yml
- Automated testing and deployment
- Runners execute jobs

**Q: How to protect branches in GitLab?**
- Settings → Repository → Protected Branches
- Restrict push/merge access
- Require approvals for merges
- Prevent force push

**Q: What are GitLab runners?**
- Execute CI/CD jobs
- Can be shared or project-specific
- Various executors: Docker, Shell, Kubernetes
- Self-hosted or GitLab-managed

**Q: Explain merge request workflow**
- Create feature branch
- Push changes
- Open merge request
- Code review and approval
- Merge to target branch
