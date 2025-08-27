---
description: Execute the documented plan strictly without extras
allowed-tools: Read, Write, MultiEdit, Edit, Bash, Grep, Glob, LS
---

Execute the plan documented in objectives.md, plan.md, and proposed_changes.md:

**IMPORTANT**: ultrathink ++ on staying strictly within the bounds of proposed_changes.md - no extras!

1. **Commit current state**:
   - Check git status for uncommitted files
   - Commit objectives.md, plan.md, proposed_changes.md with message:
     "Checkpoint: plan : {brief summary of plan}". Don't use claude branding for commit message.
   - For other uncommitted files (excluding test files and test outputs):
     * List them and ask user whether to commit each one
     * Commit approved files in the same commit

2. **Read all plan files**:
   - Read objectives.md to understand the goals
   - Read plan.md to understand the plan
   - Read proposed_changes.md to see exact changes needed
   - Store checksums of all three files to verify they remain unchanged

3. **Execute the plan**:
   - Follow plan.md step by step
   - ultrathink ++ before each change to ensure it's explicitly in proposed_changes.md
   - Make ONLY the changes listed in proposed_changes.md
   - NO performance improvements
   - NO code cleanup beyond what's specified
   - NO additional features
   - NO changes to objectives.md, plan.md, or proposed_changes.md

4. **Verify plan files unchanged**:
   - Check that objectives.md, plan.md, and proposed_changes.md have not been modified
   - If modified, notify the user of what changes were made and wait for further instructions.

5. **Deep review all changes**:
   - Use git diff to review every change made
   - Compare each change against proposed_changes.md
   - Identify any changes NOT listed in proposed_changes.md

6. **If extra changes found**:
   - List all extra changes detected
   - Revert the extra changes and course-correct to match proposed_changes.md
   - ultrathink ++ on how you can be even more careful and stick to the plan strictly.
   - Repeat until no extra changes are found.

7. **Final verification**:
   - Confirm all changes match proposed_changes.md exactly
   - Confirm no extra changes were made
   - Confirm plan files remain unchanged
   - Report successful completion only when plan is followed exactly

Do not commit the changes yet.