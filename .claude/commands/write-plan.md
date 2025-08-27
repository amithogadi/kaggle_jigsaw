---
description: Document the current plan and proposed changes in three separate files
allowed-tools: Bash, Write, Read, Glob, Grep, LS
---

!`rm -f objectives.md plan.md proposed_changes.md constraints.md bugs.md`

Document the plan that was just presented to the user:

1. **Create objectives.md** in the project root:
    - Clearly state the main objectives of this plan
    - List each objective as a clear, measurable goal
    - These objectives will be used to validate the plan and changes
    - Keep it concise - focus only on what needs to be achieved

2. **Create plan.md** in the project root:
    - Write the exact plan that was shown to the user
    - Include high-level description of the problem/issue
    - Include proposed solution approach
    - Include order of tasks to be done
    - Explain how this plan achieves the objectives in objectives.md
    - NO code snippets, only descriptions

3. **Create proposed_changes.md** in the project root:
    - Investigate all files that are relevant to the plan and ultrathink ++ on what minimal changes are needed.
    - List all files that need to be changed. Use relative paths to the project root.
    - For each file, specify exactly what changes are needed (do not write code, describe in simple english)
        - "Delete file":
        - "Rewrite the file"
        - "Move file to [location]"
        - "Modify method [name] to [description]"
        - "Add method [name] that [description]"
        - "Remove [component]"
        - Explicitly mention important parts of the file which are not to be touched for extra clarity.
    - Only include the minimal changes required to execute plan.md
    - NO extra improvements
    - NO performance optimizations unless explicitly in the plan
    - NO backward compatibility unless explicitly requested
    - NO additional features beyond what was planned

4. **Review all three files** to ensure:
    - ultrathink ++ on whether any unnecessary changes have crept in
    - objectives.md contains clear, measurable goals
    - plan.md directly addresses all objectives
    - proposed_changes.md contains only changes needed to implement plan.md
    - No unnecessary changes are included
    - No extra features beyond what was asked for
    - The proposed_changes.md exactly matches plan.md requirements
    - Nothing more, nothing less than what was planned

If any extra changes are found during review, remove them and update the files and review again.

## IMPORTANT CODE PREFERENCES

* Prefer surgical edits (`Edit`) over blanket rewrites.
* Avoid using hasattr getattr when the type of the object is known. 
* Avoid one line functions if they are going to be used only once.
* Avoid one line obvious comments like "saving the file", "initializing the counter", etc.