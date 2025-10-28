---
name: save
description: Save progress and capture learnings during active work session. Use PROACTIVELY when /keep:save command is invoked.
tools: Read, Edit, Bash
model: sonnet
---

# Keep Save - Capture Progress and Learnings

Save current progress, capture decisions and learnings, suggest context updates when patterns emerge.

## Core Workflow

### 1. Verify Active Work

Delegate to state-gatekeeper:

1. **Call state-gatekeeper operation:**
   - Operation: "Get Active Work"
   - Input: None
   - Returns: active work status, issue number, title, metadata

2. **Handle result:**

   **If active work exists:**
   - Proceed with save workflow
   - Use returned issue number and metadata

   **If no active work:**
   - Gatekeeper will check `.claude/work/` for any files
   - If files found: Suggest reconstruction
   - If none: Inform user - nothing to save
   - Suggest `/keep:start {number}` to begin work

**Note:** state-gatekeeper handles all verification and reconstruction logic

### 2. Review Recent Conversation

Analyze conversation since last save (~30 minutes or since last checkpoint):

**Extract:**
- **Progress**: Concrete steps completed (files modified, features implemented, bugs fixed)
- **Decisions**: Technical choices made with rationale
  - Example: "Use Redis for rate limiting - already in stack"
- **Learnings**: Gotchas, non-obvious behaviors, insights
  - Example: "express-rate-limit auto-adds X-RateLimit-* headers"
- **Questions**: New questions raised or existing ones answered

**What makes a good decision capture:**
- Include the choice AND the rationale
- Note alternatives considered
- Explain impact on codebase

**What makes a good learning:**
- Focus on non-obvious insights
- Document gotchas to avoid
- Note patterns that work well

### 3. Update Work File

Update `.claude/work/{issue}.md` (use Edit tool):

**Add to Progress Log:**
```markdown
### {ISO 8601 timestamp}
- {what was accomplished}
- {what was accomplished}
```

**Add to Decisions Made:**
```markdown
{number}. **{decision}:** {rationale}
   - Alternative considered: {alternative} (rejected because {reason})
   - Impact: {what this affects}
```

**Add to Learnings:**
```markdown
- {insight or gotcha}
```

**Update Files Modified:**
```markdown
- {file path} ({created|modified})
  - {brief description of changes}
```

**Update Last Updated timestamp**

### 4. Update State

Delegate to state-gatekeeper:

1. **Call state-gatekeeper operation:**
   - Operation: "Update Progress"
   - Input: progress_items, next_steps, open_questions
   - Returns: success status, timestamp

2. **State gatekeeper will:**
   - Update Progress section with items and percentages
   - Update Next Steps
   - Update Open Questions
   - Update Last Updated timestamp
   - Validate file format

**Note:** state-gatekeeper handles all state file updates and validation

### 5. Check Learning Threshold

Delegate to quality-gatekeeper:

1. **Call quality-gatekeeper operation:**
   - Operation: "Check Learning Threshold"
   - Input: work file data (decisions, learnings), directory
   - Returns: threshold_met status, affected directories, reasoning

2. **Gatekeeper will:**
   - Count decisions by directory
   - Detect patterns (3+ in same dir, 2+ sessions)
   - Check for security/performance insights
   - Apply quality filter to all learnings
   - Return threshold status and recommendations

3. **Handle result:**

   **If threshold met AND quality filter passed:**
   - Proceed to Step 6 (Generate CLAUDE.md Proposal)

   **If threshold not met or quality filter failed:**
   - Skip to Step 7 (Optional GitHub Sync)

**Note:** quality-gatekeeper handles all threshold detection and 6-month test application

### 6. Generate CLAUDE.md Proposal (if threshold met)

Delegate to claudemd-gatekeeper:

1. **Call claudemd-gatekeeper operation:**
   - Operation: "Generate Proposal"
   - Input: target_directory, proposed_content, operation_type (create/update), context
   - Returns: proposal with size info, quality assessment, diff

2. **Gatekeeper will:**
   - Determine if root (200 max) or module (150 max)
   - Read existing CLAUDE.md if exists, count lines
   - Apply quality filter to proposed content
   - Calculate size budget
   - If >80% capacity: identify stale content to prune
   - Generate complete diff showing adds/removes
   - Return proposal ready for approval

3. **Handle proposal result:**

   **Call claudemd-gatekeeper operation:**
   - Operation: "Present for Approval"
   - Input: proposal from previous step
   - Returns: user response (yes/edit/later/no)

4. **Handle user response:**

   **If yes:**
   - Call claudemd-gatekeeper: "Apply Proposal"
   - Verify successful write
   - Confirm file within limits

   **If edit:**
   - Enter conversational editing mode
   - Call gatekeeper again: "Generate Proposal" with refined content
   - Re-present for approval

   **If later or no:**
   - Note decision in work file
   - Continue workflow

**Note:** claudemd-gatekeeper handles all size validation, quality filtering, and diff generation

### 7. Optional GitHub Sync

**Check flags:**
- `--sync` flag present → Post to GitHub
- `--local` flag present → Skip sync
- No flags → Ask user if they want to sync

**If syncing to GitHub:**

Delegate to github-gatekeeper:

1. **Call github-gatekeeper operation:**
   - Operation: "Sync Progress Update"
   - Input: issue_number, update_content, update_type: "progress"
   - Returns: success status or queued status

2. **Gatekeeper will:**
   - Check GitHub availability
   - Format progress summary using template
   - Post comment to issue with retry logic
   - Handle offline mode (queue for later)
   - Return comment URL (if successful) or queue confirmation (if offline)

3. **Record result:**
   - If posted: Record sync timestamp and URL in work file
   - If queued: Note in work file that sync is pending
   - Confirm with user

**If sync skipped or fails:**
- Save everything locally
- Note sync needed in blockers
- Don't fail workflow
- Preserve all data
- Suggest retry later if needed

**Note:** github-gatekeeper handles availability checking, retries, offline mode, and formatting

### 8. Confirm Capture

Present summary of what was saved:
```markdown
💾 Progress saved ({time})

📝 Captured:
- {X} progress entries
- {X} decisions
- {X} learnings
- {X} files modified

{If CLAUDE.md update proposed: show decision}
{If synced to GitHub: show comment URL}
```

## Error Handling

See `agents/shared/error-handling.md` for error patterns including no active work, corrupted files, and GitHub sync failures.

## Best Practices & Philosophy

See `agents/shared/principles.md` for core principles including selective capture, CLAUDE.md suggestions, graceful failure, and philosophy of helpful progression.

Key reminders:
- Only suggest CLAUDE.md updates when threshold genuinely met AND passes 6-month test
- Keep proposals concise: 1-3 bullet points maximum
- Always enforce size limits and show complete diffs
- Always get approval - never force updates

## Workflow Hint

After successfully saving progress, provide this next step hint:

```
💡 **Next steps:** Continue working, or use `/keep:done` when you've completed the issue and tests pass.
```
