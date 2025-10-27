---
description: Start work on a GitHub issue with full context loading
---

# Keep: Start Work

Delegate to the keep-start sub-agent to begin work on a GitHub issue.

## Issue Number

{{#if args}}
Issue number: {{args}}
{{else}}
No issue number provided. The keep-start sub-agent will help you discover starter work using the Zero-Issues Workflow.
{{/if}}

## Delegation

Use the Task tool to invoke the keep-start sub-agent:

**Sub-agent:** keep-start
**Task:** Start work on {{#if args}}issue #{{args}}{{else}}a new issue (zero-issues discovery if no issues exist){{/if}}

The keep-start sub-agent will:
1. {{#if args}}Fetch issue #{{args}} from GitHub{{else}}Discover starter work or fetch specified issue{{/if}}
2. Load relevant context (CLAUDE.md files, state, archive)
3. Create `.claude/work/{{#if args}}{{args}}{{else}}{issue-number}{{/if}}.md`
4. Update `.claude/state.md`
5. Present comprehensive starting point

## Expected Behavior

The sub-agent operates in its own context window with focused tools (Read, Bash, Write, Glob, Grep) and will present an informed starting point for the work.
