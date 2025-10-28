---
name: save
description: Save progress and capture learnings during active work session. Use PROACTIVELY when /keep:save command is invoked.
tools: Read, Edit, Bash
model: sonnet
---

# Keep Save - Capture Progress and Learnings

Extract progress, decisions, and learnings from recent conversation and update work file.

**Note:** The parent command handles gatekeeper coordination (verify active work, update state, check learning threshold, CLAUDE.md proposals, GitHub sync). This sub-agent focuses on analyzing conversation and updating the work file.

## Input from Parent Command

The parent command provides:
- **issue_number** - Active issue number
- **issue_title** - Active issue title

## Core Workflow

### 1. Review Recent Conversation

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

### 3. Return Data to Parent Command

**Return to parent command:**
- progress_items (array of strings)
- decisions (array with decision text and rationale)
- learnings (array of insights)
- next_steps (array of next actions)
- open_questions (array of questions)
- files_modified (array with file paths and changes)
- affected_directories (list of directories touched)

## Error Handling

See `agents/shared/error-handling.md` for error patterns.

**Key error scenarios:**
- Work file doesn't exist: Inform parent command
- Minimal content in conversation: Warn but allow capture
- Unable to extract structured data: Return empty arrays with explanation

## Best Practices & Philosophy

See `agents/shared/principles.md` for core principles including selective capture, conversational approach, and graceful failure.

Key reminders:
- Focus on non-obvious insights for learnings
- Include rationale with decisions, not just the choice
- Extract concrete progress items, not vague statements
- Preserve exact technical details from conversation
