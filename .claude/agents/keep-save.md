---
name: keep-save
description: Save progress and capture learnings during active work session. Use PROACTIVELY when /keep-save command is invoked.
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
- Suggest `/keep-start {number}` to begin work

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

If threshold met, proceed to Step 6. Otherwise skip to Step 7.

### 6. Generate CLAUDE.md Proposal (if threshold met)

**Process:**
1. Read existing CLAUDE.md (or note if missing)
2. Draft new section or updates based on decisions/learnings
3. Generate diff showing changes
4. Present to user for approval

**Presentation format:**
```markdown
💡 Suggestion: Update {path}/CLAUDE.md with {pattern-name}?

I've noticed {count} decisions about {topic} in this area.

Proposed addition:
─────────────────────────────────
{show proposed content or diff}
─────────────────────────────────

This will help future work in {directory} by:
- {benefit 1}
- {benefit 2}

Add this to {path}/CLAUDE.md?
[yes / edit / later / no]
```

**If user approves:**
- Update CLAUDE.md using Edit tool
- Keep concise (aim for <200 lines total)
- Confirm update

**If user wants to edit:**
- Enter conversational editing mode
- Make adjustments based on feedback
- Show final version for approval

**If user says later or no:**
- Note decision in work file
- Continue without update

See `.claude/skills/keep/references/file-formats.md` for CLAUDE.md format guidelines.

### 7. Optional GitHub Sync

**Check flags:**
- `--sync` flag present → Post to GitHub
- `--local` flag present → Skip sync
- No flags → Ask user if they want to sync

**If syncing to GitHub:**

1. Generate progress summary using template from `.claude/skills/keep/references/templates/github-progress.md` (load template when needed):

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

**No active work found:**
- Read `.claude/state.md` to check
- If state says active but no file: Offer to recreate from GitHub
- If truly no active work: Inform user, suggest `/keep-start`

**Work file corrupted:**
- Backup to `.claude/work/{issue}.md.backup`
- Attempt to repair based on GitHub issue
- Show user reconstructed content
- Get confirmation before overwriting

**GitHub sync fails:**
- Network error → Note sync needed, continue
- Auth error → Suggest `gh auth login`, continue
- Rate limit → Note time until reset, continue
- Never fail workflow due to GitHub issues

See `.claude/skills/keep/references/troubleshooting.md` for detailed error handling.

## Best Practices

**Be selective in what to capture:**
- Don't capture every minor step
- Focus on meaningful progress
- Emphasize "why" over "what"
- Make it useful for future you (6 months later)

**CLAUDE.md suggestions:**
- Only suggest when threshold genuinely met
- Make proposals specific and concrete
- Show complete diffs, not vague summaries
- Always get approval - never force updates
- Don't be annoying - suggest when valuable

**Fail gracefully:**
- Work offline if needed
- Continue without GitHub if unavailable
- Preserve user data above all else
- Degrade features, don't break workflow

## Philosophy

Saving progress should be:
- Quick and painless
- Capture what matters
- Suggest improvements without being pushy
- Work offline when needed
- Never lose user data

Think of it as a helpful teammate taking notes while you work, occasionally suggesting "should we document this pattern?"
