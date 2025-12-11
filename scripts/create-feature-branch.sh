#!/bin/bash
#
# Helper script to create a feature branch following the naming convention
# Usage: ./scripts/create-feature-branch.sh <type> <description>
# Example: ./scripts/create-feature-branch.sh feature add-metric-tracking
#
# Types: feature, bugfix, hotfix, docs, refactor, test, chore

set -e

TYPE=$1
DESCRIPTION=$2

if [ -z "$TYPE" ] || [ -z "$DESCRIPTION" ]; then
    echo "Usage: $0 <type> <description>"
    echo ""
    echo "Types: feature, bugfix, hotfix, docs, refactor, test, chore"
    echo "Example: $0 feature add-metric-tracking"
    exit 1
fi

# Validate branch type
VALID_TYPES=("feature" "bugfix" "hotfix" "docs" "refactor" "test" "chore")
if [[ ! " ${VALID_TYPES[@]} " =~ " ${TYPE} " ]]; then
    echo "Error: Invalid type '$TYPE'"
    echo "Valid types: ${VALID_TYPES[*]}"
    exit 1
fi

# Ensure we're on main/master and it's up to date
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ] && [ "$CURRENT_BRANCH" != "master" ]; then
    echo "Warning: You're not on main/master branch. Current branch: $CURRENT_BRANCH"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create branch name
BRANCH_NAME="${TYPE}/${DESCRIPTION}"

# Check if branch already exists
if git show-ref --verify --quiet refs/heads/"$BRANCH_NAME"; then
    echo "Error: Branch '$BRANCH_NAME' already exists"
    exit 1
fi

# Create and checkout new branch
git checkout -b "$BRANCH_NAME"
echo "Created and switched to branch: $BRANCH_NAME"
echo ""
echo "Next steps:"
echo "  1. Make your changes"
echo "  2. Commit with: git commit (will use template)"
echo "  3. Push: git push -u origin $BRANCH_NAME"
echo "  4. Create a Pull Request"

