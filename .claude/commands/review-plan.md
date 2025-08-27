---
description: Review Plan – minimal change analysis with optional output file
allowed-tools: Bash(rm -f constraints.md), Task, Glob, Grep, LS, Read, Write
---

# Initial cleanup

!`rm -f constraints.md`

# Your Task

## Review Plan Workflow

**IMPORTANT**: This is a two-step process. First check constraints, then proceed to code review only if no violations
are found.

ultrathink ++ on detecting unnecessary changes and scope creep.

**Objective**

Ensure the repository evolves toward the objectives laid out in `objectives.md` and implemented via `plan.md` *only* via
the smallest, least-invasive set of
edits that still comply with all repository constraints.  
Major design flaws or missing steps **must** be highlighted; minor stylistic enhancements, new feature additions, and
backward-compatibility considerations **should be ignored** unless explicitly required by `plan.md` or `objectives.md`.

**IMPORTANT**: Repository constraints (as identified by the constraint-checker agent in step 1 below) override
minimality considerations. If a constraint requires additional changes beyond the minimal approach, those changes are
mandatory.

### Core Review Objectives

1. **Extra Work Detection** – Flag any change that exceeds the minimal requirement (e.g. rewriting an entire file
   instead of adding a single function).
2. **Dependency Gaps** – Identify required dependency updates that are missing from `proposed_changes.md`.
3. **Re-inventing the Wheel** – Detect cases where existing functionality could be reused but is instead being
   rewritten.

---

## High-Level Steps

### Step 1: Check Constraints First

!`rm -f constraints.md`

1. **Remove existing constraints.md if present**
    - Constraints.md has been removed by the bash command above

2. **Run constraint check**
   Use the Task tool with subagent_type="constraint-checker" to check proposed_changes.md and plan.md and verify the
   plan against repository constraints
    - Report which constraints are respected
    - Flag any potential violations

3. **Create constraints.md documentation**
   After receiving the constraint-checker's output, create a new `constraints.md` file in the root directory with the
   following structure:

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

### Violation 2: [Constraint Name]

**Description**: [What the violation is]
**Suggested Fix**: [How to resolve this violation]

[If no violations exist, write:]
No violations found.
```

**IMPORTANT**: If the constraint-checker finds violations, report them immediately and ask the user: "Constraint
violations found. Would you like to continue with the code review anyway? (yes/no)"

### Step 2: Proceed with Code Review (if appropriate)

**Proceed to this step if either:**

- Step 1 reports no violations, OR
- Step 1 found violations but the user responded "yes" to continue

When delegating to the code-reviewer agent, include the constraint-checker's findings in the prompt. Use the Task tool
with subagent_type="code-reviewer" and pass the following context:

```
ultrathink ++ on minimality while respecting constraints.

CONSTRAINT CHECK RESULTS:
[Include the full output from the constraint-checker agent here]

IMPORTANT: The constraints identified above override minimality considerations. Any changes required by constraints are mandatory, even if they exceed the minimal implementation approach.

Now proceed with the code review following these instructions:
```

1. **Understand the Objectives and Plan**  
   Read `objectives.md` to understand the goals, then read `plan.md` and verify it addresses all objectives.

2. **Draft Minimal Implementation Strategy**  
   • Identify the files / modules that must change.  
   • Describe the exact scope of each change (add, edit, delete).  
   • State why each change is *required* for the objective.  
   • Explicitly note anything that **must not** be touched (e.g. public APIs, data contracts, critical configs).

3. **Compare With Proposed Changes**  
   Read `proposed_changes.md` and list where its approach diverges from the minimal strategy drafted in step 2.

4. **Validate Coverage & Necessity**  
   • Confirm every truly required change is present in either plan.  
   • Flag any change that is not required (over-engineering / scope-creep).

**In addition:**
• *Do not propose new feature additions.*
• *Ignore backward-compatibility work unless `plan.md` explicitly demands it.*

5. **Apply Conciseness Rules**
   • The entire review must fit in ≤ 150 words (≈10–12 lines).  
   • Bullet-list only – one idea per line, no paragraphs.  
   • Omit all compliments/soft language; state problems only.  
   • If no blockers exist, output exactly: "No blockers found."

6. **Output**  
   Produce the review in this order (each line ≤ 12 words):  
   • Minimal changes required  
   • Delta vs proposed_changes.md  
   • Plan minimal? (Yes/No)
   • Unhandled breakages? (Yes/No)  
   • DRY violations? (Yes/No — list)

   Print the review in chat as usual.

**Must not** modify any code or configuration files during this workflow. The only permissible file write is the
markdown file designated to contain the review.

---

## Helper Tips and Preferences

* Use `Grep` or `Glob` to discover affected code quickly.
* Prefer surgical edits (`Edit`) over blanket rewrites.
* Avoid using hasattr etc. especially when the type of the object is known.
* Avoid one line obvious comments like "saving the file", "initializing the counter", etc.