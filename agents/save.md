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

Check `.claude/state.md` for active issue.

**If no active work:**
- Check for work files in `.claude/work/`
- If found: Reconstruct state
- If none: Inform user - nothing to save
- Suggest `/keep:start {number}` to begin work

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

Update `.claude/state.md` (use Edit tool):

**Update Progress section:**
- Mark completed items with ✅
- Update in-progress items with 🔄 and percentage
- Add new pending items with ⏸️

**Update Next Steps:**
- List 2-3 immediate next actions

**Update Open Questions:**
- Add new questions or mark existing as decided

**Update Last Updated timestamp**

### 5. Check Learning Threshold

Count decisions by directory from current work file:

**Threshold detection:**
- **3+ decisions** in same directory → Suggest CLAUDE.md update
- **2+ sessions** in same directory → Consider new CLAUDE.md
- **Recurring patterns** → Document in relevant CLAUDE.md
- **Security/performance insights** → Always capture

**Quality Filter - "6-Month Test":**

See `agents/shared/quality-filters.md` for detailed quality assessment criteria and examples of high-value vs low-value content.

If threshold met AND quality filter passed, proceed to Step 6. Otherwise skip to Step 7.

### 6. Generate CLAUDE.md Proposal (if threshold met)

See `agents/shared/size-validation.md` for complete size validation process including limits, budget calculation, and enforcement.

**Key steps:**

1. Read existing CLAUDE.md (if exists) and count lines
2. Use size limits: 200 root, 150 module (warn at 80% capacity)
3. Filter learnings through quality criteria (Step 5)
4. Draft concise, high-value content only
5. If >80% capacity, identify content to remove
6. Generate diff showing changes
7. Present for approval with complete size information

**Content Guidelines:**
- Focus on "why" and gotchas, not "what" (visible in code)
- Be concise: 1-3 bullet points, not paragraphs
- Use examples only when they clarify non-obvious behavior
- Avoid repeating what's in code/docs

**User response options:**
- If yes: Update CLAUDE.md and verify size within limits
- If edit: Enter conversational editing mode, re-check constraints
- If later or no: Note decision in work file and continue

See `skills/keep/references/file-formats.md` for CLAUDE.md format guidelines.

### 7. Optional GitHub Sync

**Check flags:**
- `--sync` flag present → Post to GitHub
- `--local` flag present → Skip sync
- No flags → Ask user if they want to sync

**If syncing to GitHub:**

1. Generate progress summary using template from `skills/keep/references/templates/github-progress.md` (load template when needed):

```markdown
## Progress Update - {date} {time}

✅ Completed:
- {completed item}

🔄 In Progress:
- {current item} ({percentage}% done)

💡 Key Decisions:
- {decision}: {rationale}

Next: {next steps}
```

2. Post via `gh issue comment {number} --body "{summary}"`
3. Record sync timestamp in work file
4. Confirm posted with comment URL

**If sync fails:**
- Save everything locally
- Note sync needed
- Don't fail workflow
- Preserve all data

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
