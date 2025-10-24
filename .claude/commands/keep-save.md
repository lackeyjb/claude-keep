---
description: Save progress and capture learnings from current work
---

# Keep: Save Progress

Load the Keep skill to save current progress and capture learnings.

## Task

Invoke the Keep skill by loading `.claude/skills/keep/SKILL.md` to save progress on the current issue.

## Instructions

1. Load the Keep skill
2. Follow the "Saving Progress" workflow from the skill
3. Ensure active work file exists (`.claude/work/{issue}.md`)

## Expected Outcome

The Keep skill should:
- Review recent conversation since last save
- Extract:
  - Concrete progress made
  - Decisions with rationale
  - Learnings and gotchas discovered
  - Questions raised or answered
- Update `.claude/work/{issue}.md`:
  - Add timestamped progress log entry
  - Document decisions in Decisions Made section
  - Capture learnings in Learnings section
  - Update files modified list
- Update `.claude/state.md`:
  - Update progress indicators
  - Update next steps
  - Note any new questions
- Check learning threshold:
  - Count decisions by directory
  - If threshold met (3+ decisions), suggest CLAUDE.md update
  - Generate proposal and get approval
- If `--sync` flag or user confirms:
  - Generate progress summary
  - Post to GitHub as issue comment
  - Record sync timestamp
- Confirm what was captured

## Flags

- `--sync` - Force sync to GitHub (even if auto-sync disabled)
- `--local` - Skip GitHub sync confirmation, save locally only

## Error Handling

If no active work found:
- Check `.claude/state.md` for active issue
- If found, recreate work file from GitHub issue
- If not found, inform user and suggest `/keep-start`

If GitHub sync fails:
- Save progress locally
- Note that sync needed
- Don't fail the workflow
- Preserve all captured data

## Context Update Approval

When suggesting CLAUDE.md updates:
- Show complete proposed change
- Present as diff or addition
- Explain benefit to future work
- Offer options:
  - yes: Apply update immediately
  - edit: Enter conversational editing mode
  - later: Save suggestion for later
  - no: Don't apply this update
- Respect user choice
- Never force updates

## Example Usage

```
/keep-save
```

Saves progress locally, suggests context updates if threshold met.

```
/keep-save --sync
```

Saves progress and posts update to GitHub issue.

```
/keep-save --local
```

Saves progress locally without GitHub sync prompt.
