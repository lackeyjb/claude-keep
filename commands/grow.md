---
description: Create or update CLAUDE.md files for project context. Use --update to update existing, --condense to prune bloated files.
---

# Keep: Grow Context

Delegate to the grow sub-agent to analyze a directory and create/update CLAUDE.md.

## Target Directory & Flags

{{#if args}}
Arguments: {{args}}

Parse flags from args:
- --update: Update existing CLAUDE.md
- --condense: Prune bloated CLAUDE.md to fit size limits
- --force: Create even if patterns unclear

Target directory: First non-flag argument (or current directory if none)
{{else}}
No directory specified. The grow sub-agent will default to current working directory or project root.
{{/if}}

## Delegation

Use the Task tool to invoke the grow sub-agent:

**Sub-agent:** grow
**Task:** Analyze {{#if args}}{{args}}{{else}}project directory{{/if}} and create or update CLAUDE.md

The grow sub-agent will:
1. Analyze directory for patterns
2. Assess if CLAUDE.md would be valuable (6-month test)
3. Check existing size if updating
4. Generate proposal with size validation
5. Present for approval (showing line counts)
6. Create or update CLAUDE.md (if approved and within limits)

## Expected Behavior

The sub-agent operates in its own context window with focused tools (Read, Glob, Grep, Write, Edit) and will only create CLAUDE.md when patterns are clear and valuable.
