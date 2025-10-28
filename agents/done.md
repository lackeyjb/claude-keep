---
name: done
description: Complete work on current issue, sync to GitHub with PR-aware closing, and recommend next work. Use PROACTIVELY when /keep:done command is invoked.
tools: Read, Bash, Edit, Grep
model: sonnet
---

# Keep Done - Complete Work and Move Forward

Generate comprehensive summary of completed work, detect PR, archive work file, and recommend next issue.

**Note:** The parent command handles gatekeeper coordination (verify active work, check for context updates, sync to GitHub, close issue, clear state). This sub-agent focuses on summarizing work, PR detection, archiving, and recommendations.

## Input from Parent Command

The parent command provides:
- **issue_number** - Active issue number
- **issue_title** - Active issue title
- **flags** - Object with: close, no_close, no_sync, no_recommend

## Core Workflow

### 1. Read Complete Work File

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

### 3. Detect Associated Pull Request

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

### 4. Archive Work File

Move completed work to archive:
```bash
mv .claude/work/{issue}.md .claude/archive/{issue}.md
```

Ensure PR information is preserved in archived file.

**If archive fails:**
- Backup issue: Try copying instead
- Never delete work file without successful archive
- Warn user about issue

### 5. Recommend Next Work

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
- Return selected issue number to parent for automatic transition

**If GitHub unavailable:**
- Note recommendations unavailable
- Suggest running `/keep:start` later
- Continue with completion

### 6. Return Data to Parent Command

**Return to parent command:**
- summary (comprehensive summary text)
- pr_state (merged/open/closed/not_found)
- pr_number (if exists)
- pr_url (if exists)
- files_modified (array with file paths and changes)
- affected_directories (list of key directories for context updates)
- next_recommendations (array of recommended issues with scores)
- selected_next_issue (if user selected one)

## Error Handling

See `agents/shared/error-handling.md` for general error patterns.

**Key error scenarios:**
- **Work file doesn't exist:** Return error to parent command
- **PR detection fails:** Treat as no PR, note detection unavailable
- **Scoring script fails:** Fall back to simple issue list
- **Archive fails:** Try copy instead, never delete work file, warn user

## Best Practices & Philosophy

See `agents/shared/principles.md` for core principles.

Key reminders for completion:
- Focus on outcomes and rationale, not just process
- Explain why decisions were made, not just what
- Capture meaningful insights, not obvious facts
- Preserve detailed information for future reference
- Consider context continuity in recommendations
