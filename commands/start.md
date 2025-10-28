---
description: Start work on a GitHub issue with full context loading
---

# Keep: Start Work

Delegate to the start sub-agent to begin work on a GitHub issue.

## Issue Number

{{#if args}}
Issue number: {{args}}
{{else}}
No issue number provided. The start sub-agent will help you discover starter work using the Zero-Issues Workflow.
{{/if}}

## Pre-Flight Checks

Before delegating to the start sub-agent:

1. **Verify `.claude/` directory exists**
   - If missing: create it
   - Create `.claude/work/` and `.claude/archive/` subdirectories

2. **Verify `.claude/state.md` format**
   - If missing: will be created by sub-agent
   - If exists but malformed: warn user, offer to repair

3. **Check for active work**
   - If active work exists and recent: suggest resuming with `/keep:start {issue}`
   - If active work exists but old: suggest refreshing

## Delegation

Use the Task tool to invoke the start sub-agent:

**Sub-agent:** start
**Task:** Start work on {{#if args}}issue #{{args}}{{else}}a new issue (zero-issues discovery if no issues exist){{/if}}

The start sub-agent will:
1. {{#if args}}Fetch issue #{{args}} from GitHub{{else}}Discover starter work or fetch specified issue{{/if}}
2. Load relevant context (CLAUDE.md files, state, archive)
3. Create `.claude/work/{{#if args}}{{args}}{{else}}{issue-number}{{/if}}.md`
4. Update `.claude/state.md`
5. Present comprehensive starting point

## Expected Behavior

The sub-agent operates in its own context window with focused tools (Read, Bash, Write, Glob, Grep) and will present an informed starting point for the work.
