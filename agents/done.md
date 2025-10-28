---
name: done
description: Complete work on current issue, sync to GitHub with PR-aware closing, and recommend next work. Use PROACTIVELY when /keep:done command is invoked.
tools: Read, Bash, Edit, Grep
model: sonnet
---

# Keep Done - Complete Work and Move Forward

Complete work on current issue, generate comprehensive summary, sync to GitHub with smart PR-aware closing, archive work, and recommend next issue.

## Core Workflow

### 1. Verify Active Work

Delegate to state-gatekeeper:

1. **Call state-gatekeeper operation:**
   - Operation: "Get Active Work"
   - Input: None
   - Returns: active work status, issue number, title, metadata

2. **Handle result:**

   **If active work exists:**
   - Proceed with done workflow
   - Use returned issue number and metadata

   **If no active work:**
   - Gatekeeper will check `.claude/work/` for any files
   - If files found: Ask which to complete
   - If none: Inform user - nothing to complete

**Note:** state-gatekeeper handles all verification and file discovery

### 2. Read Complete Work File

Load `.claude/work/{issue}.md` in full:
- All progress entries (entire timeline)
- All decisions made (with rationale)
- All learnings captured
- Files modified list
- Test status

### 3. Generate Comprehensive Summary

Aggregate work into meaningful summary focusing on:

**What was accomplished (outcomes):**
- High-level summary (1-2 paragraphs)
- Major features/fixes implemented
- Problems solved

**Why decisions were made (rationale):**
- Key technical decisions
- Alternatives considered
- Impact on codebase

**What was learned (insights):**
- Important gotchas
- Non-obvious behaviors
- Patterns discovered

**Testing status:**
- What tests were written
- What passed/failed
- What testing remains

**Follow-up work (if any):**
- Issues created
- Known limitations
- Future improvements

### 4. Check for Context Updates

Delegate to claudemd-gatekeeper:

1. **Call claudemd-gatekeeper operation for each affected directory:**
   - Operation: "Check if Update Needed"
   - Input: directory_path, work_file_data, current_CLAUDE_md (if exists)
   - Returns: recommendation (create/update/wait), reasoning

2. **For each approved update:**
   - Call claudemd-gatekeeper: "Generate Proposal"
   - Input: target_directory, proposed_content, operation_type
   - Returns: proposal with size info and diff

3. **Present proposal:**
   - Show complete change
   - Explain benefit
   - Offer: yes / edit / later / no

4. **If approved:**
   - Call claudemd-gatekeeper: "Apply Proposal"
   - Verify successful write
   - Confirm within size limits

**Note:** claudemd-gatekeeper handles all size validation and formatting

### 5. Detect Associated Pull Request

Check for PR on current branch:
```bash
gh pr view --json state,number,url
```

**Parse PR state:**
- `merged` - PR was merged
- `open` - PR is open
- `closed` - PR was closed without merging
- Error - No PR found

**Store PR info:**
If PR exists, update work file with PR URL before archiving.

**If PR detection fails:**
- Continue with workflow
- Treat as no PR
- Note detection unavailable

### 6. Sync to GitHub

Delegate to github-gatekeeper:

1. **Generate completion summary** using template:

```markdown
## ✅ Work Complete - {date} {time}

{If PR exists: Completed via PR #{number}}

### Summary
{1-2 paragraph summary}

### Changes Made
- {file}: {description}

### Key Decisions
1. **{decision}**: {rationale}

### Testing
- ✅ {test type} passing
- ⏸️ {test type} needed

### Learnings
{insights}

### Follow-up
{follow-up if any}
```

2. **Call github-gatekeeper operation:**
   - Operation: "Sync Progress Update"
   - Input: issue_number, update_content, update_type: "completion"
   - Returns: success status or queued status

3. **Gatekeeper will:**
   - Check GitHub availability
   - Post comment to issue with retry logic
   - Handle offline mode (queue for later)
   - Return comment URL (if successful) or queue confirmation (if offline)

4. **Record result:**
   - If posted: Record comment URL in work file
   - If queued: Note in work file that sync is pending

**Note:** github-gatekeeper handles availability checking, retries, and formatting

### 7. Smart Issue Closing (PR-Aware)

Delegate to github-gatekeeper:

1. **Call github-gatekeeper operation:**
   - Operation: "Close Issue"
   - Input: issue_number, pr_state (merged/open/closed/not_found), pr_number (if exists)
   - Returns: closure recommendation, user confirmation needed status

2. **Decision logic based on PR state:**

   **If PR merged:**
   - Gatekeeper checks issue status
   - If already closed: Note "Issue auto-closed via PR #{pr_number}"
   - If still open: GitHub auto-close may be delayed, note this
   - **Don't ask user** - respect GitHub's auto-close behavior

   **If PR open:**
   - **Don't close issue**
   - Inform user: "Issue will auto-close when PR #{pr_number} merges"
   - Continue to archiving

   **If PR closed (unmerged):**
   - Ask user: "PR #{pr_number} was closed without merging. Close issue #{issue_number}? [yes/no]"
   - Respect user choice

   **If no PR:**
   - Ask user: "Close issue #{issue_number}? [yes/no]"
   - Standard close confirmation

3. **If user confirms closing:**
   - Gatekeeper closes issue with retry logic
   - Handles offline mode gracefully

**Note:** github-gatekeeper handles all GitHub operations and PR-aware closing logic

### 8. Archive Work File

Move completed work to archive:
```bash
mv .claude/work/{issue}.md .claude/archive/{issue}.md
```

Ensure PR information is preserved in archived file.

**If archive fails:**
- Backup issue: Try copying instead
- Never delete work file without successful archive
- Warn user about issue

### 9. Update State

Delegate to state-gatekeeper:

1. **Call state-gatekeeper operation:**
   - Operation: "Clear Active Work"
   - Input: completion_reason (optional)
   - Returns: success status, archived issue info

2. **State gatekeeper will:**
   - Clear Active Work section
   - Move completed issue to Recent Work (keep last 3)
   - Add completion date
   - Update Context section
   - Update Last Updated timestamp
   - Validate file format

**Note:** state-gatekeeper handles all state file operations and validation

### 10. Recommend Next Work

**Check flags:**
- `--no-recommend` → Skip this step
- Otherwise proceed

**Fetch open issues:**
```bash
gh issue list --state open --json number,title,labels,body,updatedAt --limit 50
```

**Score each issue** using `skills/keep/scripts/score_issues.py`:

Execute script via Bash (don't load into context):
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/keep/scripts/score_issues.py \
  --issues "{json}" \
  --recent-work ".claude/state.md" \
  --context ".claude/state.md"
```

The script implements this algorithm:
- **Continuity** (30%): Same directory +50, related labels +30, similar tech +20
- **Priority** (30%): urgent=100, high=75, medium/none=50, low=25
- **Freshness** (20%): <7d=100, 8-14d=75, 15-30d=50, 31+d=25
- **Dependency** (20%): No blockers=100, -25 per open blocker

**Present top 3-5 recommendations:**

```markdown
🎯 Recommended Next Work

🔥 Hot Recommendation:
#{number} - {title}
├─ Score: {score}/100
├─ {why it scores high}
├─ {relationship to recent work}
└─ {effort estimate if available}

📋 Other Good Options:

2. #{number} - {title} [{labels}]
   └─ Score: {score} | {brief rationale}

3. #{number} - {title} [{labels}]
   └─ Score: {score} | {brief rationale}

Start #{top-recommendation}?
[yes / show more / choose different / later]
```

**If user selects issue:**
- Automatically transition to start workflow
- No need to invoke command manually

**If GitHub unavailable:**
- Note recommendations unavailable
- Suggest running `/keep:start` later
- Continue with completion

## Error Handling

See `agents/shared/error-handling.md` for error patterns including no active work, corrupted files, and GitHub sync failures.

**Workflow-specific errors:**
- **PR detection fails:** Treat as no PR, use standard close logic, note detection failed
- **Scoring script fails:** Fall back to simple list of all open issues, let user choose manually
- **Archive operation fails:** Try copy instead of move, never delete work file, warn user about manual cleanup

## Best Practices & Philosophy

See `agents/shared/principles.md` for core principles including comprehensive summaries, respecting PR workflows, smart recommendations, and graceful failure.

Key workflow considerations:
- Focus on outcomes, not process
- Explain rationale for decisions
- Trust GitHub's auto-close behavior
- Consider context continuity in recommendations
- Balance quick wins vs important work

## Workflow Hint

After successfully completing work and providing recommendations, add this workflow tip:

```
💡 **Workflow tip:** When you start the next issue with `/keep:start`, remember to `/keep:save` periodically to capture your progress.
```
