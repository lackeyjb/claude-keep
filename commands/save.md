---
description: Save progress and capture learnings from current work
---

# Keep: Save Progress

Orchestrate progress saving by coordinating gatekeepers and the save sub-agent.

## Flags

{{#if args}}
Flags: {{args}}
{{else}}
No flags provided.
{{/if}}

Supported flags:
- `--sync` - Force sync to GitHub
- `--local` - Skip GitHub sync

## Workflow Orchestration

### Step 1: Verify Active Work

**Call state-gatekeeper to verify active work:**

Use Task tool with sub-agent `state-gatekeeper`:
- **Operation:** "Get Active Work"
- **Input:** None
- **Returns:** active_work_exists (boolean), issue_number, issue_title, metadata

**Handle result:**

- **If no active work:** Inform user, suggest `/keep:start` first, exit workflow
- **If active work exists:** Store issue_number and metadata for next steps

### Step 2: Extract Progress and Learnings

**Call save sub-agent to analyze conversation:**

Use Task tool with sub-agent `save`:
- **Input:** issue_number, issue_title
- **Task:** Review recent conversation and extract progress, decisions, learnings

**Sub-agent will:**
1. Review conversation since last save (~30 min or last checkpoint)
2. Extract progress items, decisions, learnings, questions
3. Update work file `.claude/work/{issue}.md`
4. Return: progress_items, decisions, learnings, next_steps, open_questions, files_modified

### Step 3: Update State

**Call state-gatekeeper to update state:**

Use Task tool with sub-agent `state-gatekeeper`:
- **Operation:** "Update Progress"
- **Input:** progress_items, next_steps, open_questions
- **Returns:** success status, timestamp

**State gatekeeper will:**
- Update Progress section with items
- Update Next Steps
- Update Open Questions
- Update Last Updated timestamp
- Validate file format

### Step 4: Check Learning Threshold

**Call quality-gatekeeper to assess if CLAUDE.md update is warranted:**

Use Task tool with sub-agent `quality-gatekeeper`:
- **Operation:** "Check Learning Threshold"
- **Input:** decisions, learnings, affected directories
- **Returns:** threshold_met (boolean), affected_directories, reasoning

**Gatekeeper will:**
- Count decisions by directory
- Detect patterns (3+ in same dir, 2+ sessions)
- Check for security/performance insights
- Apply quality filter (6-month test)
- Return threshold status

**If threshold NOT met:** Skip to Step 6 (GitHub Sync)

### Step 5: Generate and Apply CLAUDE.md Proposal (if threshold met)

**Call claudemd-gatekeeper to generate proposal:**

Use Task tool with sub-agent `claudemd-gatekeeper`:
- **Operation:** "Generate Proposal"
- **Input:** target_directory, proposed_content, operation_type (create/update), context
- **Returns:** proposal with size info, quality assessment, diff

**Gatekeeper will:**
- Determine size limits (root: 200, module: 150)
- Read existing CLAUDE.md, count lines
- Apply quality filter
- Calculate size budget
- If >80% capacity: identify stale content to prune
- Generate complete diff
- Return validated proposal

**Call claudemd-gatekeeper to present proposal:**

Use Task tool with sub-agent `claudemd-gatekeeper`:
- **Operation:** "Present for Approval"
- **Input:** proposal from previous step
- **Returns:** user_response (yes/edit/later/no)

**Handle user response:**

- **If yes:** Call claudemd-gatekeeper "Apply Proposal", verify write succeeded
- **If edit:** Enter conversational editing, regenerate proposal, re-present
- **If later/no:** Note decision, continue workflow

### Step 6: Optional GitHub Sync

**Check flags and user preference:**

{{#if args}}
- If `--sync` flag: Force sync to GitHub
- If `--local` flag: Skip sync
{{else}}
- No flags provided: Ask user if they want to sync
{{/if}}

**If syncing to GitHub:**

Use Task tool with sub-agent `github-gatekeeper`:
- **Operation:** "Sync Progress Update"
- **Input:** issue_number, update_content (progress items), update_type: "progress"
- **Returns:** success status, comment_url, or queued status

**Gatekeeper will:**
- Check GitHub availability
- Format progress summary
- Post comment to issue (with retry logic)
- Handle offline mode (queue for later)
- Return comment URL or queue confirmation

**Record result:**
- If posted: Record sync timestamp and URL in work file
- If queued: Note pending sync in work file
- If offline: Save locally, suggest retry later

### Step 7: Confirm Capture

Present summary of what was saved:
```markdown
💾 Progress saved ({time})

📝 Captured:
- {X} progress entries
- {X} decisions
- {X} learnings
- {X} files modified

{If CLAUDE.md proposed: show decision}
{If synced to GitHub: show comment URL}
```

**Workflow hint:**
```
💡 **Next steps:** Continue working, or use `/keep:done` when you've completed the issue and tests pass.
```

## Error Handling

- **No active work:** Inform user, suggest `/keep:start` first
- **Work file missing:** Offer reconstruction from state
- **State file corrupted:** state-gatekeeper handles recovery
- **GitHub unavailable:** Queue for later, don't fail workflow
- **Minimal content:** Warn user but allow save

## Architecture

This command orchestrates four sub-agents:
1. **state-gatekeeper** - Verify active work and update state
2. **save** - Extract progress and learnings from conversation
3. **quality-gatekeeper** - Assess learning threshold
4. **claudemd-gatekeeper** - Generate and apply CLAUDE.md proposals
5. **github-gatekeeper** - Sync progress to GitHub

Each operates in its own context window with focused tools.
