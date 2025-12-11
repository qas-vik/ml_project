# Contributing Guide

This guide outlines our Git workflow, branching strategy, commit conventions, and code review process to ensure clean collaboration and reproducible work.

## Branching Strategy

### Main Branch Protection
- `main` is always deployable and protected. Direct commits are disallowed.
- All changes must come through feature branches and pull requests.
- Keep `main` in a stable, working state at all times.

### Branch Naming Convention
Create feature branches from `main` using the pattern: `<type>/<short-description>`

**Branch Types:**
- `feature/` - New features or enhancements
- `bugfix/` - Bug fixes
- `hotfix/` - Critical production fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks

**Examples:**
- `feature/add-metric-tracking`
- `bugfix/fix-data-validation`
- `docs/update-api-documentation`
- `refactor/simplify-preprocessing`

### Creating Branches

**Option 1: Use the helper script (Recommended)**
```bash
# Bash (Linux/Mac)
./scripts/create-feature-branch.sh feature add-metric-tracking

# PowerShell (Windows)
.\scripts\create-feature-branch.ps1 -Type feature -Description add-metric-tracking
```

**Option 2: Manual creation**
```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### Branch Workflow
1. Create a feature branch from `main`
2. Make your changes and commit frequently
3. Keep your branch up-to-date with `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-branch
   git rebase main  # or git merge main
   ```
4. Push your branch and create a Pull Request
5. After PR approval, merge via GitHub (squash merge recommended)

## Commit Messages

### Format
Use the **Conventional Commits** style:
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without changing functionality
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Changes to build process, dependencies, or auxiliary tools
- `ci`: Changes to CI configuration

### Scope (Optional)
The scope indicates the area of the codebase affected:
- `api` - API endpoints
- `training` - Training scripts/pipelines
- `data` - Data processing/preprocessing
- `model` - Model architecture
- `eval` - Evaluation/metrics
- `deploy` - Deployment scripts

### Examples

**Simple commit:**
```
feat(api): add batch inference endpoint
```

**Detailed commit:**
```
fix(training): guard against empty datasets

Previously, the training pipeline would crash when encountering
empty datasets. This fix adds validation to check dataset size
before training begins and provides a clear error message.

Fixes #123
```

**Breaking change:**
```
feat(api): change response format for predictions

BREAKING CHANGE: The prediction endpoint now returns results in
a nested structure instead of a flat array. Clients need to
update their parsing logic.

Migration guide: docs/migration-v2.md
```

### Commit Message Guidelines
- **Subject line**: Imperative mood, lowercase, no period, max 72 characters
- **Body**: Explain *what* and *why*, wrap at 72 characters
- **Footer**: Reference issues, breaking changes, or related PRs
- Use the commit message template (configured via `.gitmessage`)
- Squash fixup commits before merging

### Using the Commit Template
The repository includes a commit message template. When you run `git commit` without `-m`, your editor will open with the template. Configure it globally:
```bash
git config commit.template .gitmessage
```

## Pull Requests & Reviews

### PR Checklist
Before opening a PR, ensure:
- [ ] Branch is up-to-date with `main`
- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated if needed
- [ ] Commit messages follow conventions
- [ ] No large files (data, models, logs) are included

### PR Description Template
Use the following structure for PR descriptions:

```markdown
## Problem
Brief description of the problem or feature request.

## Solution
What changes were made and how they solve the problem.

## Changes
- List of key changes
- Files modified
- New features added

## Testing
How was this tested?
- Unit tests
- Integration tests
- Manual testing steps
- Experiment results/metrics

## Validation
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No breaking changes (or migration guide provided)

## Related Issues
Closes #123
```

### Code Review Process
1. **Request Review**: Assign at least one peer reviewer
2. **Review Focus Areas**:
   - Code correctness and logic
   - Reproducibility (can others run this?)
   - Model ethics and safety implications
   - Performance considerations
   - Documentation clarity
3. **Addressing Feedback**:
   - Make changes in follow-up commits
   - Avoid force-pushing after review starts (coordinate if needed)
   - Respond to all comments
4. **Merge Requirements**:
   - At least one approval
   - All CI checks passing
   - No merge conflicts
   - Use "Squash and merge" for cleaner history

### Review Guidelines for Reviewers
- Be constructive and respectful
- Focus on code quality, not personal preferences
- Check for:
  - Edge cases and error handling
  - Security implications
  - Performance bottlenecks
  - Test coverage
  - Documentation completeness
  - ML-specific concerns (data leakage, model bias, etc.)

## Collaboration Tips

### Documentation
- Document modeling decisions in `docs/` (design notes or ADRs)
- Keep README files updated
- Add docstrings to functions and classes
- Include examples in documentation

### Large Artifacts
- **Never commit**: data files, model checkpoints, logs, large outputs
- Store large artifacts in:
  - Object storage (S3, GCS, Azure Blob)
  - Artifact trackers (MLflow, Weights & Biases)
  - Shared network drives
- Document where artifacts are stored in README or docs

### Environment Setup
- Automate environment setup in `scripts/`
- Use `requirements.txt` or `environment.yml` for dependencies
- Document any manual setup steps
- Use virtual environments (`.venv/` is gitignored)

### Best Practices
- Commit frequently with meaningful messages
- Keep branches focused (one feature/fix per branch)
- Rebase before opening PRs to keep history clean
- Write tests for new features
- Update documentation alongside code changes
- Communicate breaking changes clearly

## Getting Help

If you're unsure about the workflow:
1. Check this guide first
2. Look at recent PRs for examples
3. Ask in team chat or create a discussion
4. Review the main README.md for project-specific guidelines