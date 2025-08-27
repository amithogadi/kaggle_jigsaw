---
description: Commit all changes, push, and create a pull request
allowed-tools: Bash, Read, Grep
---

# Initial cleanup 
!`rm -f objectives.md plan.md proposed_changes.md constraints.md bugs.md`

Create a pull request with all uncommitted changes:

1. **Check current branch and changes**:
   - Get current branch name
   - Run git status to see all changes
   - Run git diff to understand what's being committed

2. **Commit all changes**:
   - If there are uncommitted changes:
     - Review all changes for sensitive or temporary files:
       - Check for API keys, tokens, passwords, or other secrets
       - Check for temporary files (test outputs, build artifacts, etc.)
       - If any sensitive or temporary files found, ask user for instructions before proceeding
     - Stage all changes with git add
     - Create a descriptive commit message based on the changes
     - NO Claude Code branding or attribution
     - Use format: "feat/fix/refactor: clear description of changes"
   - If changes are already committed, proceed to next step

3. **Push to remote**:
   - Push current branch to origin
   - Use -u flag if branch doesn't exist on remote

4. **Create pull request**:
   - Use gh pr create
   - Title format: "[branch-name] Description of changes"
   - Body should include:
     - Summary of changes
     - Any relevant context
     - Testing notes if applicable
   - NO Claude Code branding in PR description

5. **Return PR URL** so user can review it

Important:
- If no changes to commit and no local commits to push, inform user and stop
- If on main/master branch, ask user to create a feature branch first
- Handle any push conflicts gracefully