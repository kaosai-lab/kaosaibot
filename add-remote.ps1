# Run this script after installing Git to connect this project to GitHub.
# Install Git: https://git-scm.com/download/win

$repo = "https://github.com/kaosai-lab/kaosaibot.git"
$projectRoot = if ($PSScriptRoot) { $PSScriptRoot } else { "c:\Users\kevin\OneDrive\Desktop\kaosaibot" }
Set-Location $projectRoot

if (-not (Test-Path ".git")) {
    git init
    Write-Host "Initialized git repository."
}
git remote remove origin 2>$null
git remote add origin $repo
Write-Host "Remote 'origin' set to: $repo"
git remote -v
