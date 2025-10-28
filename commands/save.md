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

## Pre-Flight Checks

Before delegating to the save sub-agent:

1. **Verify active work exists**
   - Check `.claude/state.md` for active issue
   - If no active work: inform user, suggest `/keep:start` first

2. **Verify work file exists**
   - Check `.claude/work/{issue}.md`
   - If missing but state says active: offer to recover from state

3. **Check for content to save**
   - If very new session: note that there may be minimal content to save

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
