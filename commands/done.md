---
description: Complete work on current issue and sync to GitHub
---

# Keep: Complete Work

Delegate to the done sub-agent to complete work on the current issue.

## Flags

{{#if args}}
Flags: {{args}}
{{else}}
No flags provided.
{{/if}}

Supported flags:
- `--close` - Close the GitHub issue without asking
- `--no-close` - Leave issue open without asking
- `--no-sync` - Skip GitHub sync (local only)
- `--no-recommend` - Skip next work recommendations

## Delegation

Use the Task tool to invoke the done sub-agent:

**Sub-agent:** done
**Task:** Complete work on current issue{{#if args}} with flags: {{args}}{{/if}}

The done sub-agent will:
1. Read complete work file
2. Generate comprehensive summary
3. Check for context updates
4. Detect associated PR (if exists)
5. Sync to GitHub with PR-aware closing
6. Archive work file to `.claude/archive/`
7. Update `.claude/state.md`
8. Recommend next work (unless --no-recommend)

## Expected Behavior

The sub-agent operates in its own context window with focused tools (Read, Bash, Edit, Grep) and will guide you through completion and recommend next work.
