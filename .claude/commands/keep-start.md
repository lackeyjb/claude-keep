---
description: Start work on a GitHub issue with full context loading
---

# Keep: Start Work

Load the Keep skill and begin work on a GitHub issue.

## Task

Invoke the Keep skill by loading `.claude/skills/keep/SKILL.md` to start work on an issue.

## Issue Number

{{#if args}}
Issue number: {{args}}
{{else}}
No issue number provided. The Keep skill should either:
1. Ask the user for an issue number
2. Offer to recommend next work using the scoring algorithm
3. Allow the user to work without issue tracking (local-only)
{{/if}}

## Instructions

1. Load the Keep skill
2. Follow the "Starting Work" workflow from the skill
3. Ensure proper directory structure exists:
   - Create `.claude/work/` if needed
   - Create `.claude/archive/` if needed
   - Create `.claude/state.md` if needed

## Expected Outcome

The Keep skill should:
- Fetch the issue from GitHub (if issue number provided)
- Load relevant context (CLAUDE.md files, state, archive)
- Parse the issue into structured approach
- Create `.claude/work/{issue-number}.md`
- Update `.claude/state.md`
- Present a comprehensive starting point with:
  - Issue summary
  - Context loaded
  - Suggested approach
  - Questions if requirements unclear

## Flags

- `--offline` - Skip GitHub, work locally only
- `--no-fetch` - Use existing work file if present (resume)

## Error Handling

If GitHub unavailable:
- Warn user
- Offer local-only mode
- Continue workflow without GitHub integration
- Note that sync will be needed later

If issue not found:
- Suggest verifying issue number
- Offer to create issue or work without one
- Don't fail the workflow

## Example Usage

```
/keep:start 1234
```

Starts work on issue #1234 with full context loading.

```
/keep:start
```

Prompts for issue number or offers to recommend next work.
