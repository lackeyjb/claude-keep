---
description: Complete work on current issue and sync to GitHub
---

# Keep: Complete Work

Load the Keep skill to complete work on the current issue.

## Task

Invoke the Keep skill by loading `.claude/skills/keep/SKILL.md` to complete the current issue.

## Instructions

1. Load the Keep skill
2. Follow the "Completing Work" workflow from the skill
3. Ensure active work file exists (`.claude/work/{issue}.md`)

## Expected Outcome

The Keep skill should:
- Read complete work file
- Aggregate all progress, decisions, learnings
- Generate comprehensive summary:
  - What was accomplished (outcomes)
  - Why decisions were made (rationale)
  - What was learned (insights)
  - What was tested (status)
  - What follow-up needed (if any)
- Check for context updates:
  - Review all learnings
  - Identify which CLAUDE.md files should be updated
  - Generate proposals
  - Get approval
- Sync to GitHub:
  - Post completion summary as issue comment
  - Ask about closing issue
  - If confirmed: close issue with `gh issue close {number}`
- Archive work file:
  - Move `.claude/work/{issue}.md` to `.claude/archive/`
  - Preserve all content
- Update state:
  - Clear active issue
  - Add to recent work
  - Update context (hot areas)
- Recommend next work:
  - Fetch open issues from GitHub
  - Score using algorithm (continuity + priority + freshness + dependencies)
  - Present top 3-5 recommendations
  - Offer to start immediately

## Flags

- `--close` - Close the GitHub issue without asking
- `--no-close` - Leave issue open without asking
- `--no-sync` - Skip GitHub sync (local only)
- `--no-recommend` - Skip next work recommendations

## Error Handling

If no active work found:
- Check `.claude/state.md` for active issue
- If found but no work file, warn and offer to create from GitHub
- If not found, inform user - nothing to complete

If GitHub sync fails:
- Archive work file locally
- Note that sync needed
- Don't fail the workflow
- Preserve all captured data
- User can manually sync later

If next work recommendations fail:
- Continue with completion
- Note that recommendations unavailable
- User can run `/keep:next` manually

## GitHub Summary Format

The completion comment posted to GitHub should follow this format:

```markdown
## ✅ Work Complete - {date} {time}

### Summary
{1-2 paragraph summary of what was accomplished and why}

### Changes Made
- {file}: {what changed}
- {file}: {what changed}

### Key Decisions
1. **{decision}**: {rationale}
2. **{decision}**: {rationale}

### Testing
- ✅ {test type} passing
- ⏸️ {test type} needed

### Learnings
{key insights captured}

### Follow-up
- {follow-up item if any}
```

## Example Usage

```
/keep:done
```

Completes work, posts summary to GitHub, asks about closing, recommends next.

```
/keep:done --close
```

Completes work, posts summary, closes issue, recommends next.

```
/keep:done --no-sync
```

Completes work locally only, no GitHub interaction.

```
/keep:done --no-recommend
```

Completes work and syncs but skips next work recommendations.
