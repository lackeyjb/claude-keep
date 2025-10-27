---
description: Save progress and capture learnings from current work
---

# Keep: Save Progress

Delegate to the save sub-agent to capture progress and learnings.

## Flags

{{#if args}}
Flags: {{args}}
{{else}}
No flags provided.
{{/if}}

Supported flags:
- `--sync` - Force sync to GitHub
- `--local` - Skip GitHub sync

## Delegation

Use the Task tool to invoke the save sub-agent:

**Sub-agent:** save
**Task:** Save current progress{{#if args}} with flags: {{args}}{{/if}}

The save sub-agent will:
1. Review recent conversation
2. Extract progress, decisions, learnings
3. Update `.claude/work/{issue}.md`
4. Update `.claude/state.md`
5. Check learning threshold and suggest CLAUDE.md updates if needed
6. Optionally sync to GitHub (based on flags)

## Expected Behavior

The sub-agent operates in its own context window with focused tools (Read, Edit, Bash) and will confirm what was captured.
