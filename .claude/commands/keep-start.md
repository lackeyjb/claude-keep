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
No issue number provided. Keep will help you discover starter work:

**The Zero-Issues Workflow:**

1. **Discover** - Search for planning docs (ROADMAP.md, TODO.md) and code signals (TODO/FIXME comments, missing tests) using native Glob/Grep tools

2. **Synthesize** - Prioritize findings into 3-5 actionable issue suggestions with source attribution

3. **Create** - User selects which issues to create, Keep generates natural issue bodies and creates them via GitHub

4. **Start** - User picks which issue to work on, Keep loads context and begins normal workflow

This uses Claude's native capabilities to analyze your project intelligently. See SKILL.md Section 8 for detailed workflow.
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
/keep-start 1234
```

Starts work on issue #1234 with full context loading.

```
/keep-start
```

Prompts for issue number or offers to recommend next work.
