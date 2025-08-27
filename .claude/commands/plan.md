---
description: Generate a broad implementation plan for requested features
allowed-tools: Glob, Grep, WebSearch, Read, Write, LS
---

# Broad Implementation Plan Generator

Please create a comprehensive broad-level implementation plan for the requested task. Follow these steps:

## 1. Codebase Analysis
- Use Glob and Grep tools to scan the existing codebase for relevant:
  - Classes and their key methods
  - Functions and their purposes  
  - Modules and their relationships
  - Design patterns already in use
- Focus on components that relate to the requested task
- Summarize the current architecture and how the new feature would fit

## 2. Research Best Practices
- Use WebSearch to find:
  - Latest best practices for the relevant technologies
  - Current package versions and their documentation
  - Common implementation patterns for similar features
  - Performance considerations and optimization strategies
  - Security best practices if applicable

## 3. Plan Creation
Create a broad-level plan that includes:

### Primary Implementation Approach
- High-level architecture decisions
- Key components and their responsibilities
- Data flow and interactions between components
- Technology stack recommendations
- Integration points with existing code

### Alternative Approaches (Optional)
- Present alternative strategies only if significantly different
- Focus on practical trade-offs for immediate implementation
- Skip if the primary approach is clearly optimal

### Design Considerations
- Essential error handling only
- Minimal viable testing strategy
- Critical production considerations
- Skip future extensibility unless explicitly needed

**IMPORTANT**: This plan should be optimized for immediate implementation, not phased rollout over weeks/months. Backward compatibility is NOT required unless explicitly mentioned by the user. Focus on the simplest, most direct solution that meets the requirements.

## 4. Output Format
Write the complete plan to a markdown file. If no file path is provided, ask: "Where should I write the implementation plan? Please provide a file path (e.g., plan.md or docs/feature-plan.md)"

**IMPORTANT**: If the specified file already exists and contains a previous broad plan, OVERWRITE it completely with the new plan. Do not append or merge with existing content.

Remember: This is a BROAD plan - no actual code implementation, just architectural decisions and design outlines.