---
description: Add a coding constraint to avoid bugs in this repository
allowed-tools: ["Read", "Write", "Edit", "Bash"]
argument-hint: "constraint description"
---

Add a new coding constraint to `.claude/constraints.yaml`:

1. **Parse and polish description**:
   - Extract constraint description from: `$ARGUMENTS`
   - Polish the description: fix typos, improve clarity, make it precise
   - Preserve the original meaning and technical requirements
   - Use consistent technical terminology
   - Validate it's not empty or too generic

2. **Extract scope**:
   - Look for mentions of files, classes, methods in the description
   - Auto-extract scope when clear (format: `"type name [location]"`)
   - If ambiguous, ask user for clarification

3. **Check for duplicates**:
   - Read `.claude/constraints.yaml` (create if doesn't exist)
   - Check if any existing constraint describes the same requirement
   - If duplicate/overlap found:
     - Show both constraints
     - Ask: replace old, keep both, or combine?

4. **Add constraint**:
   - Structure:
     ```yaml
     - description: "constraint text"
       tags: [tag1, tag2]  # Optional: auto-suggest based on content
       scope:
         - "type name [location]"
     ```
   - Auto-suggest tags based on keywords in description
   - Append to constraints list
   - Report what was added and total count

## Constraint format

```yaml
constraints:
  - description: "In haystack async components run and run_async methods need to have same signature"
    tags: [async, haystack, consistency]
    scope:
      - "class AsyncComponent [haystack-ai]"
      - "method run [src/pipelines/base.py]"
      - "method run_async [src/pipelines/base.py]"

  - description: "Output schemas submitted to google cannot have 'additionalProperties'"
    tags: [schema, google-api, validation]
    scope:
      - "function prepare_google_schema [src/llm/schema_utils.py]"
      - "function validate_schema [src/llm/validators.py]"

  - description: "Always use type hints for function parameters"
    tags: [type-hints, code-style, python]
```

## Examples

```
# Clear scope - automatically extracted
/constrain "In haystack async components run and run_async methods need to have same signature"
# Creates:
# - description: "In haystack async components run and run_async methods need to have same signature"
#   tags: [async, haystack, consistency]
#   scope:
#     - "class AsyncComponent [haystack-ai]"
#     - "method run [src/pipelines/base.py]"
#     - "method run_async [src/pipelines/base.py]"

# Function constraint
/constrain "prepare_google_schema function must strip all additionalProperties from schemas"
# Creates:
# - description: "prepare_google_schema function must strip all additionalProperties from schemas"
#   tags: [schema, google-api, validation]
#   scope:
#     - "function prepare_google_schema [src/llm/schema_utils.py]"

# Ambiguous - asks for clarification
/constrain "PDF processing must handle both single and multi-page documents"
# Asks: "I found references to PDF processing. Which specific files/classes/methods does this apply to?"

# No specific scope
/constrain "Always use type hints for function parameters"
# Creates:
# - description: "Always use type hints for function parameters"
#   tags: [type-hints, code-style, python]
```

## Scope types
Common scope types include:
- `module [path]` - single file (e.g., src/utils/helpers.py, src/components/Button.tsx)
- `package [path]` - directory/folder (e.g., src/pipelines, src/components)
- `package [package-name]` - external package (e.g., haystack-ai, numpy, react, next)
- `file [path]` - any file
- `component [file]` - React/Vue/Angular component
- `class [file/package]` - class definition
- `method [file]` - method in a class
- `function [file]` - standalone function
- `hook [file]` - React hook (useEffect, useState, custom hooks)
- `route [path]` - API route or page route
- `constant [file]` - constant/variable
- `variable [file]` - variable definition

The scope format is flexible: `"type name [location]"` where type can be any code element (decorator, property, protocol, enum, etc.)

## Important notes
- Create `.claude/constraints.yaml` if it doesn't exist
- Use natural language understanding to detect duplicate/overlapping constraints
- Auto-extract scope when clear from description
- Only ask for clarification when scope is ambiguous
- Scope format: `"type name [location]"` where location is in square brackets
- Multiple scopes can apply to a single constraint
- Constraints without scope apply globally