---
description: Review PlannedChanges – verify implementation matches proposed_changes.md
allowed-tools: Read, LS, Task, Write, Bash
---

# Review Changes Workflow

**IMPORTANT**: This workflow should be delegated to code-reviewer agent.

**Purpose**

Compare the _actual_ uncommitted modifications in the working tree against `proposed_changes.md` to ensure the codebase reflects the planned **minimal** edits—no more, no less.

ultrathink ++ on identifying deviations from the plan.

**IMPORTANT**: This workflow has TWO phases:
1. If proposed_changes.md does not exist, exit and inform the user that this workflow is not applicable.
2. First, check for constraint compliance using the existing `constraints.md` file
3. Then, proceed with the code change review

---

## Phase 1: Constraint Compliance Check

### Step 1: Check for existing constraints.md
1. Use the LS tool to check if `constraints.md` exists in the root directory
2. **If constraints.md EXISTS**:
   - Read the file using the Read tool
   - Check the "## Constraint Violations" section
   - If it says "No violations found.", proceed to Phase 2
   - If violations are listed, report them to the user and ask: "Constraint violations found in constraints.md. Would you like to continue with the code review anyway? (yes/no)"
3. **If constraints.md DOES NOT EXIST**:
   - Inform the user: "No constraints.md file found. Running constraint checker..."
   - Use the Task tool with subagent_type="constraint-checker" to check proposed_changes.md and plan.md
   - Create constraints.md with the constraint-checker's output using the format below
   - Follow the same violation checking logic as above

### constraints.md Format (if creating new):
```markdown
# Constraint Analysis for Current Plan

## Relevant Constraints
List all constraints from .claude/constraints.yaml that are relevant to the current plan:
- [Constraint 1]: [Brief description]
- [Constraint 2]: [Brief description]
- ...

## Constraint Violations
[If violations exist, list each with description and suggested fixes]
### Violation 1: [Constraint Name]
**Description**: [What the violation is]
**Suggested Fix**: [How to resolve this violation]

[If no violations exist, write:]
No violations found.
```

---

## Phase 2: Code Change Review

**Proceed to this phase if either:**
- No constraint violations were found, OR
- Violations were found but the user responded "yes" to continue

### Core Review Questions
1. **Coverage** – Have _all_ changes listed in `proposed_changes.md` been implemented?
2. **Over-scope** – Have any files or lines been altered that were **not** part of the proposal?

These two concerns should be addressed; ignore style-only edits such as formatting changes, removal of unused imports, or comment-only modifications. Test quality and other refactors are out of scope.

### Steps

1. **Parse Objectives and Planned Edits**  
   • Read `objectives.md` to understand the overarching goals.  
   • Read `proposed_changes.md`.  
   • Extract the file names, functions, or line ranges slated for modification.

2. **Collect Actual Edits**  
   • Run `git status --porcelain` to list modified / added / deleted files.  
   • Run `git diff` for each file to capture the exact hunks.  
   (If the repo is initialised but has no commits yet, diff against the empty tree.)

3. **Analyse Coverage**  
   • ultrathink ++ on whether all planned changes are actually implemented
   • For every planned edit, confirm a corresponding change exists in the diff.  
   • Flag anything missing.
   • Verify changes align with objectives from objectives.md.

4. **Detect Extra Work**  
   • ultrathink ++ on spotting unauthorized additions or scope creep
   • For each modified file/hunk, check whether it appears in the proposal list.  
   • Flag all modifications that were **not** proposed.

### Conciseness Rules
• Keep the entire report ≤ 100 words.  
• Use bullet lines only, no paragraphs.  

### Output  
   Produce exactly two bullet lines (each ≤ 12 words):  
   • Planned changes made? (Yes/No — list missing)  
   • Extra changes made? (Yes/No — list extras)

   Print the review in chat.

**Must not** modify any code or configuration files during this workflow.

---

## Helper Tips

* Use `Bash` to execute `git status` and `git diff`.  
  Example:
  ```
  git status --porcelain
  ```
* Treat renamed files (`R `) as both deletion and addition when matching.
* Ignore whitespace-only changes (`git diff -w`).
* Ignore diffs that exclusively remove unused imports, reformat code, or edit comments.