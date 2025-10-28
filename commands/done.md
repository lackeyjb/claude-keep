---
description: Complete work on current issue and sync to GitHub
---

# Keep: Complete Work

Orchestrate work completion by coordinating gatekeepers and the done sub-agent.

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

### Step 2: Generate Summary and Detect PR

**Call done sub-agent to analyze completed work:**

Use Task tool with sub-agent `done`:
- **Input:** issue_number, issue_title, flags
- **Task:** Read work file, generate comprehensive summary, detect PR

**Sub-agent will:**
1. Read complete work file (progress, decisions, learnings, files modified)
2. Generate comprehensive summary (outcomes, rationale, insights, testing)
3. Detect associated PR (if exists) via `gh pr view`
4. Return: summary, pr_state (merged/open/closed/not_found), pr_number, pr_url, files_modified, affected_directories

### Step 3: Check for Context Updates

**Call claudemd-gatekeeper for each affected directory:**

Use Task tool with sub-agent `claudemd-gatekeeper`:
- **Operation:** "Check if Update Needed"
- **Input:** directory_path, work_file_data, current_CLAUDE_md (if exists)
- **Returns:** recommendation (create/update/wait), reasoning

**For each directory needing update:**

1. **Generate proposal:**
   - Call claudemd-gatekeeper: "Generate Proposal"
   - Input: target_directory, proposed_content, operation_type
   - Returns: proposal with size info and diff

2. **Present proposal:**
   - Call claudemd-gatekeeper: "Present for Approval"
   - Returns: user_response (yes/edit/later/no)

3. **If approved:**
   - Call claudemd-gatekeeper: "Apply Proposal"
   - Verify successful write

### Step 4: Sync Completion to GitHub

{{#unless no-sync}}
**Call github-gatekeeper to post completion summary:**

Use Task tool with sub-agent `github-gatekeeper`:
- **Operation:** "Sync Progress Update"
- **Input:** issue_number, update_content (comprehensive summary), update_type: "completion"
- **Returns:** success status, comment_url, or queued status

**Gatekeeper will:**
- Check GitHub availability
- Format completion summary with template
- Post comment to issue (with retry logic)
- Handle offline mode (queue for later)
- Return comment URL or queue confirmation

**Record result:**
- If posted: Record comment URL in work file
- If queued: Note pending sync in work file
{{/unless}}

### Step 5: Smart Issue Closing (PR-Aware)

{{#unless no-close}}
**Call github-gatekeeper for PR-aware closing:**

Use Task tool with sub-agent `github-gatekeeper`:
- **Operation:** "Close Issue"
- **Input:** issue_number, pr_state (from Step 2), pr_number (if exists)
- **Returns:** closure recommendation, user confirmation needed status

**Decision logic based on PR state:**

- **If PR merged:** Don't ask - respect GitHub's auto-close behavior
- **If PR open:** Don't close - inform "Issue will auto-close when PR merges"
- **If PR closed (unmerged):** Ask user to confirm closing
- **If no PR:** Ask user to confirm closing (unless --close flag)

**If user confirms closing:**
- Gatekeeper closes issue with retry logic
- Handles offline mode gracefully
{{/unless}}

### Step 6: Archive Work File

Archive completed work:
```bash
mv .claude/work/{issue}.md .claude/archive/{issue}.md
```

Ensure PR information is preserved in archived file.

**If archive fails:**
- Try copying instead
- Never delete work file without successful archive
- Warn user about manual cleanup needed

### Step 7: Update State

**Call state-gatekeeper to clear active work:**

Use Task tool with sub-agent `state-gatekeeper`:
- **Operation:** "Clear Active Work"
- **Input:** completion_reason (optional)
- **Returns:** success status, archived_issue_info

**State gatekeeper will:**
- Clear Active Work section
- Move completed issue to Recent Work (keep last 3)
- Add completion date
- Update Context section
- Update Last Updated timestamp
- Validate file format

### Step 8: Recommend Next Work

{{#unless no-recommend}}
**Fetch open issues and provide recommendations:**

1. Fetch open issues via `gh issue list`
2. Score each issue using scoring algorithm:
   - Continuity (30%): Same directory, related labels, similar tech
   - Priority (30%): urgent=100, high=75, medium=50, low=25
   - Freshness (20%): Recent issues score higher
   - Dependency (20%): Issues without blockers score higher

3. Present top 3-5 recommendations:
   ```markdown
   🎯 Recommended Next Work

   🔥 Hot Recommendation:
   #{number} - {title}
   ├─ Score: {score}/100
   ├─ {why it scores high}
   ├─ {relationship to recent work}
   └─ {effort estimate if available}

   📋 Other Good Options:
   2. #{number} - {title}
   3. #{number} - {title}

   Start #{top-recommendation}? [yes / show more / choose different / later]
   ```

4. If user selects issue: Automatically transition to start workflow

**If GitHub unavailable:**
- Note recommendations unavailable
- Suggest running `/keep:start` later
{{/unless}}

### Step 9: Confirm Completion

Present confirmation to user:
```markdown
✅ Work complete on issue #{issue_number}

📝 Summary posted to GitHub
{{#if closed}}🔒 Issue closed{{/if}}
📁 Work file archived to .claude/archive/{issue}.md
{{#if next_recommendation}}🎯 Recommended next: #{next_issue}{{/if}}
```

**Workflow hint:**
```
💡 **Workflow tip:** When you start the next issue with `/keep:start`, remember to `/keep:save` periodically to capture your progress.
```

## Error Handling

- **No active work:** Inform user, suggest `/keep:start` first
- **Work file missing:** Inform user, exit workflow
- **GitHub unavailable:** Queue sync operations, continue with local completion
- **PR detection fails:** Treat as no PR, use standard close logic
- **Archive fails:** Try copy, never delete work file, warn user
- **Scoring script fails:** Fall back to simple issue list

## Architecture

This command orchestrates four sub-agents:
1. **state-gatekeeper** - Verify active work and clear state
2. **done** - Generate summary and detect PR
3. **claudemd-gatekeeper** - Check for and apply context updates
4. **github-gatekeeper** - Sync completion and close issue (PR-aware)

Each operates in its own context window with focused tools.
