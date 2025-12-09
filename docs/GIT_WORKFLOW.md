# Git Workflow Guide

This document provides a step-by-step guide for the Git workflow used in this ML project.

## Initial Setup

### 1. Configure Git (if not already done)
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Configure Commit Template
```bash
git config commit.template .gitmessage
```

### 3. Clone and Setup
```bash
git clone <repository-url>
cd ML_Services
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Daily Workflow

### Starting a New Feature

1. **Update your local main branch:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Create a feature branch:**
   ```bash
   # Using helper script (recommended)
   ./scripts/create-feature-branch.sh feature my-new-feature
   
   # Or manually
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes:**
   - Write code
   - Add tests
   - Update documentation

4. **Stage and commit:**
   ```bash
   git add .
   git commit  # This will open the template
   # Or with message:
   git commit -m "feat(scope): your commit message"
   ```

5. **Push your branch:**
   ```bash
   git push -u origin feature/my-new-feature
   ```

6. **Create a Pull Request:**
   - Go to GitHub/GitLab
   - Click "New Pull Request"
   - Fill out the PR template
   - Request reviewers
   - Wait for approval and CI checks

### Keeping Your Branch Updated

While working on your feature, keep it synced with main:

```bash
# Fetch latest changes
git fetch origin

# Option 1: Rebase (cleaner history)
git checkout feature/my-branch
git rebase origin/main

# Option 2: Merge (simpler)
git checkout feature/my-branch
git merge origin/main
```

**Resolve conflicts if any, then:**
```bash
git push origin feature/my-branch
# If you rebased, you may need:
git push --force-with-lease origin feature/my-branch
```

### Making Changes After Review

1. **Address review comments:**
   ```bash
   git checkout feature/my-branch
   # Make changes
   git add .
   git commit -m "fix: address review feedback"
   git push origin feature/my-branch
   ```

2. **The PR will automatically update**

### After PR Approval

1. **Merge via GitHub/GitLab UI:**
   - Use "Squash and merge" for cleaner history
   - Delete the branch after merging

2. **Update your local main:**
   ```bash
   git checkout main
   git pull origin main
   ```

## Common Scenarios

### Fixing a Bug

```bash
git checkout main
git pull origin main
git checkout -b bugfix/fix-bug-description
# Make fixes
git add .
git commit -m "fix(scope): description of bug fix"
git push -u origin bugfix/fix-bug-description
# Create PR
```

### Updating Documentation

```bash
git checkout main
git pull origin main
git checkout -b docs/update-readme
# Update docs
git add .
git commit -m "docs: update README with new instructions"
git push -u origin docs/update-readme
# Create PR
```

### Hotfix (Critical Production Issue)

```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix
# Make urgent fix
git add .
git commit -m "hotfix(scope): critical production fix"
git push -u origin hotfix/critical-fix
# Create PR, request urgent review
# After merge, tag release if needed
```

### Amending the Last Commit

```bash
# Make changes
git add .
git commit --amend
# Update the commit message if needed
git push --force-with-lease origin feature/my-branch
```

### Squashing Commits

Before merging, you might want to squash commits:

```bash
# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# In the editor, change 'pick' to 'squash' for commits to combine
# Save and close, then edit the combined commit message
```

## Branch Protection Rules

The `main` branch is protected with the following rules:
- No direct pushes allowed
- All changes must go through PRs
- At least one approval required
- All CI checks must pass
- No force pushes allowed

## Troubleshooting

### Accidentally Committed Large Files

```bash
# Remove from history (use with caution)
git rm --cached large-file.pkl
git commit --amend
git push --force-with-lease origin feature/my-branch
```

### Undo Last Commit (Keep Changes)

```bash
git reset --soft HEAD~1
```

### Undo Last Commit (Discard Changes)

```bash
git reset --hard HEAD~1
```

### View Commit History

```bash
git log --oneline --graph --decorate
```

### Check What Files Changed

```bash
git status
git diff
git diff --staged
```

## Best Practices

1. **Commit Often**: Small, focused commits are easier to review
2. **Write Good Messages**: Use the template, be descriptive
3. **Keep Branches Short-Lived**: Merge within a few days
4. **Test Before Committing**: Run tests locally
5. **Review Your Own PR**: Check the diff before requesting review
6. **Keep PRs Focused**: One feature/fix per PR
7. **Update Documentation**: Keep docs in sync with code
8. **Respect the .gitignore**: Don't commit ignored files

## Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Git Best Practices](https://github.com/git/git/blob/master/Documentation/SubmittingPatches)
