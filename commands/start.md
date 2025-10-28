---
description: Start work on a GitHub issue with full context loading
---

# Keep: Start Work

Orchestrate work startup by coordinating gatekeepers and the start sub-agent.

## Issue Number

{{#if args}}
Issue number: {{args}}
{{else}}
No issue number provided. The start sub-agent will help you discover starter work using the Zero-Issues Workflow.
{{/if}}

## Pre-Flight Checks

Before workflow execution:

1. **Verify `.claude/` directory exists**
   - If missing: create it with subdirectories
   ```bash
   mkdir -p .claude/work .claude/archive
   ```

2. **Verify `.claude/state.md` format**
   - If missing: will be created during workflow
   - If exists but malformed: warn user, offer to repair

## Workflow Orchestration

### Step 1: Resume Detection (If Issue Number Provided)

{{#if args}}
**Call state-gatekeeper for resume detection:**

Use Task tool with sub-agent `state-gatekeeper`:
- **Operation:** "Verify Work File Exists"
- **Input:** Issue number {{args}}
- **Returns:** work_file_exists (boolean), work_file_path, metadata, freshness

**Handle result:**

- **If work file DOES NOT exist:** Continue to Step 2 (fresh start)
- **If work file EXISTS:** Check freshness:
  - **Recent (< 24h):** Resume with cached data, skip GitHub fetch
  - **Moderate (24-48h):** Ask user: resume cached or refetch from GitHub?
  - **Stale (> 48h):** Proceed to refetch from GitHub

If resuming with cached data, skip to Step 4 (delegate to start sub-agent with resume=true).
{{/if}}

### Step 2: Fetch Issue from GitHub

{{#if args}}
**Call github-gatekeeper to fetch issue:**

Use Task tool with sub-agent `github-gatekeeper`:
- **Operation:** "Fetch Issue"
- **Input:** Issue number {{args}}
- **Returns:** issue_data (title, body, labels, state, url) or offline_mode indication

**Handle result:**

- **If GitHub available:** Store issue_data for sub-agent
- **If offline mode:** Warn user, proceed with cached data if available, or fail gracefully

Collect issue metadata: title, body, labels, state, url
{{else}}
No issue number provided - sub-agent will handle zero-issues discovery workflow.
{{/if}}

### Step 3: Delegate to Start Sub-Agent

Use Task tool with sub-agent `start`:

**Pass to sub-agent:**
{{#if args}}
- Issue number: {{args}}
- Issue data: (title, body, labels, state, url from Step 2)
- Resume mode: (true/false from Step 1)
- Work file data: (if resuming with cached data)
{{else}}
- Zero-issues mode: true
{{/if}}

**Sub-agent will:**
1. Load context (CLAUDE.md files, state, archive)
2. {{#if args}}Present issue overview and suggest approach{{else}}Discover starter work and create issues{{/if}}
3. Create work file `.claude/work/{issue-number}.md`
4. Return: issue_number, issue_title, work_file_created

### Step 4: Update State

**Call state-gatekeeper to set active work:**

Use Task tool with sub-agent `state-gatekeeper`:
- **Operation:** "Set Active Work"
- **Input:** issue_number, issue_title, started_timestamp (ISO 8601)
- **Returns:** success status

**State gatekeeper will:**
- Update `.claude/state.md` with active work
- Move previous work to Recent Work
- Record start timestamp

### Step 5: Present Starting Point

Inform user that work has begun:
- Issue is now active in state.md
- Work file created
- Ready to proceed

**Workflow hint:**
```
💡 **Next steps:** As you work, use `/keep:save` to checkpoint progress and capture decisions. Run it at natural breakpoints (after implementing features, making key decisions, or every 30-45 min).
```

## Error Handling

- **GitHub unavailable:** Continue in offline mode, skip sync operations
- **State file corrupted:** state-gatekeeper handles recovery
- **Work file exists:** Handle resume vs refetch based on freshness
- **No issues found (zero-issues):** Guide user through issue creation

## Architecture

This command orchestrates three sub-agents:
1. **state-gatekeeper** - Resume detection and state updates
2. **github-gatekeeper** - Issue fetching with retry logic
3. **start** - Context loading, work file creation, presentation

Each operates in its own context window with focused tools.
