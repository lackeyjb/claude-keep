---
description: Create or update CLAUDE.md files for project context
---

# Keep: Grow Context

Delegate to the grow sub-agent to analyze a directory and create/update CLAUDE.md.

## Target Directory

{{#if args}}
Target directory: {{args}}
{{else}}
No directory specified. The grow sub-agent will default to current working directory or project root.
{{/if}}

## Delegation

Use the Task tool to invoke the grow sub-agent:

**Sub-agent:** grow
**Task:** Analyze {{#if args}}{{args}}{{else}}project directory{{/if}} and create or update CLAUDE.md

The grow sub-agent will:
1. Analyze directory for patterns
2. Assess if CLAUDE.md would be valuable
3. Generate proposal (if valuable)
4. Present for approval
5. Create or update CLAUDE.md (if approved)

## Expected Behavior

The sub-agent operates in its own context window with focused tools (Read, Glob, Grep, Write, Edit) and will only create CLAUDE.md when patterns are clear and valuable.
