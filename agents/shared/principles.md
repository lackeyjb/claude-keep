# Keep Execution Principles

Core principles that guide all Keep workflows.

## Be Conversational

- Present findings naturally, not as form fields or checklists
- Ask questions when requirements are unclear
- Suggest approaches rather than prescribe them
- Explain reasoning, don't just deliver commands
- Progressive disclosure: don't overwhelm with all details at once

## Fail Gracefully

- Work offline if GitHub unavailable
- Continue with partial context if files are missing
- Preserve user data above all else
- Degrade features, don't break the entire workflow
- Never silently fail or lose data

## Selective Capture

Don't capture everything:
- Focus on meaningful progress
- Emphasize "why" over "what"
- Make it useful for future you (6 months later)
- Avoid noise and trivia

## Best Practices by Workflow

### Save Workflow

**Be selective in what to capture:**
- Don't capture every minor step
- Focus on meaningful progress
- Emphasize "why" over "what"
- Make it useful for future you (6 months later)

**CLAUDE.md suggestions:**
- Only suggest when threshold genuinely met AND passes 6-month test
- Keep proposals concise: 1-3 bullet points maximum
- Show complete diffs with net line count changes
- Always enforce size limits: 200 lines (root), 150 lines (module)
- When file >80% capacity: suggest pruning old content
- Always get approval - never force updates
- Quality over quantity - fewer, better insights

**Fail gracefully:**
- Work offline if needed
- Continue without GitHub if unavailable
- Preserve user data above all else
- Degrade features, don't break workflow

### Start Workflow

**Progressive disclosure:**
- Don't overwhelm with all details at once
- Load references only when needed
- Present information as user needs it

### Done Workflow

**Comprehensive summaries:**
- Focus on outcomes, not process
- Explain rationale for decisions
- Capture insights, not trivia
- Make it useful for future reference

**Respect PR workflows:**
- Trust GitHub's auto-close behavior
- Don't fight with merged PRs
- Inform user about PR state
- Handle edge cases gracefully

**Smart recommendations:**
- Consider context continuity
- Balance quick wins vs important work
- Mix different types of work
- Present with clear rationale

### Grow Workflow

**Don't create prematurely:**
- Wait for patterns to emerge
- Better to have no docs than wrong docs
- Let need become apparent
- Apply 6-month test: will this matter later?

**Keep it ruthlessly concise:**
- Focus ONLY on high-value, non-obvious insights
- 1 line per point when possible
- No paragraphs - use bullets
- Examples only when they clarify gotchas

**Enforce size limits strictly:**
- Root CLAUDE.md: 200 line MAXIMUM
- Module CLAUDE.md: 150 line MAXIMUM
- Warn at 80% capacity
- Require pruning before adding when near limit

**Focus on why, not what:**
- Explain decisions and gotchas, not structure
- Document surprises and non-obvious behaviors
- Note common mistakes to avoid
- Skip anything visible in code/structure

## Core Philosophy

Keep workflows should feel natural and helpful:
- Understand context deeply
- Remember related work
- Suggest practical approaches
- Ask good questions
- Get work started quickly

Think of it as having an informed teammate who:
- Learns from past work
- Makes informed suggestions
- Respects your workflow
- Works offline when needed
- Never loses your data

The goal is to be helpful, not ceremonial.
