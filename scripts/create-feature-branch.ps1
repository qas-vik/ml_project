# PowerShell script to create a feature branch following the naming convention
# Usage: .\scripts\create-feature-branch.ps1 -Type <type> -Description <description>
# Example: .\scripts\create-feature-branch.ps1 -Type feature -Description add-metric-tracking
#
# Types: feature, bugfix, hotfix, docs, refactor, test, chore

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("feature", "bugfix", "hotfix", "docs", "refactor", "test", "chore")]
    [string]$Type,
    
    [Parameter(Mandatory=$true)]
    [string]$Description
)

# Create branch name
$BranchName = "$Type/$Description"

# Check current branch
$CurrentBranch = git rev-parse --abbrev-ref HEAD
if ($CurrentBranch -ne "main" -and $CurrentBranch -ne "master") {
    $response = Read-Host "Warning: You're not on main/master branch. Current branch: $CurrentBranch. Continue anyway? (y/n)"
    if ($response -ne "y" -and $response -ne "Y") {
        exit 1
    }
}

# Check if branch already exists
$branchExists = git show-ref --verify --quiet "refs/heads/$BranchName"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Error: Branch '$BranchName' already exists" -ForegroundColor Red
    exit 1
}

# Create and checkout new branch
git checkout -b $BranchName
if ($LASTEXITCODE -eq 0) {
    Write-Host "Created and switched to branch: $BranchName" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Make your changes"
    Write-Host "  2. Commit with: git commit (will use template)"
    Write-Host "  3. Push: git push -u origin $BranchName"
    Write-Host "  4. Create a Pull Request"
} else {
    Write-Host "Error: Failed to create branch" -ForegroundColor Red
    exit 1
}
