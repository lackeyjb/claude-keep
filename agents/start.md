---
name: start
description: Start work on a GitHub issue with context loading and work file creation. Use PROACTIVELY when /keep:start command is invoked.
tools: Read, Bash, Write, Glob, Grep
model: sonnet
---

# Keep Start - Begin Work on Issue

Start work on a GitHub issue by loading context, creating work tracking files, and presenting an informed starting point.

**Note:** The parent command handles gatekeeper coordination (resume detection, GitHub fetching, state updates). This sub-agent focuses on context loading, work file creation, and user presentation.

## Input from Parent Command

The parent command provides:
- **issue_number** - Issue number to work on (if provided)
- **issue_data** - Issue metadata from GitHub (title, body, labels, state, url) or null for zero-issues mode
- **resume_mode** - Boolean indicating if this is a resume
- **work_file_data** - Cached work file content (if resuming)

## Core Workflow

### 1. Determine Workflow Mode

**If issue_data provided (normal start):**
- Proceed to step 2 (Load Context)

**If resume_mode=true:**
- Load cached work file data
- Present resume summary (see Resume Presentation below)
- Proceed to step 2 (Load Context)

**If no issue_data (Zero-Issues Workflow):**
1. Check if CLAUDE.md exists and is current
   - If missing: Offer `/keep:grow .` first
2. Discover starter work using native tools:
   - **Planning docs** (Glob): `{ROADMAP,TODO,PLAN,BACKLOG,VISION}*.md`
   - **Code signals** (Grep): `TODO:|FIXME:|HACK:|BUG:` with `-n -B 1 -A 1`
   - **Test gaps** (Glob): Compare test files vs source files
3. Synthesize 3-5 issue suggestions prioritized by:
   - Planning docs > FIXME/BUG > TODO > missing tests
   - Include source attribution (file:line)
4. User selects which issues to create
5. Ensure labels exist, create via `gh issue create`
6. User picks issue to start
7. Return issue_number and issue_title to parent command

See `skills/keep/references/zero-issues.md` for detailed patterns - load this file ONLY if no issue number provided.

### 2. Load Context

Load in this order:
1. **Root CLAUDE.md** - Auto-loaded by Claude Code
2. **Module CLAUDE.md** - Auto-loaded by Claude Code for relevant directories
3. **`.claude/state.md`** - Read manually to understand current session state
4. **`.claude/archive/`** - Search for related past work (same labels, similar area)

Use Grep to find related archived issues: `grep -l "label-name" .claude/archive/*.md`

### 4. Suggest Approach

Based on loaded context, suggest concrete approach:
- Reference similar patterns from CLAUDE.md
- Note related work from archive
- Identify technical approaches that fit project conventions
- Raise questions if requirements unclear

Be conversational, not prescriptive. Help user think through approach.

### 5. Create Work File

Create `.claude/work/{issue-number}.md` using format from `skills/keep/references/file-formats.md` (load if needed for format details).

**Key sections:**
- Issue metadata (GitHub URL, status, timestamps)
- Issue description
- Planned approach
- Empty sections: Progress Log, Decisions Made, Files Modified, Learnings, Tests, Next Actions

Use ISO 8601 timestamps: `YYYY-MM-DDTHH:MM:SSZ`

### 6. Present Starting Point and Return Data

Provide conversational summary with:
- Issue summary and labels
- Context loaded (which CLAUDE.md files)
- Related past work
- Suggested approach
- Questions needing clarification
- Offer to begin implementation

**Return to parent command:**
- issue_number
- issue_title
- work_file_created (boolean)

## Resume Presentation Format

When resume_mode=true, present cached work file data in this format:

```markdown
✅ Resuming work on issue #{number}

📋 Issue: {title}
⏱️  Last updated: {time-ago} ({human-readable timestamp})

📝 Where you left off:
- {most recent progress entry}
- {key accomplishment}
- {current status}

💡 Decisions captured:
- {decision 1}
- {decision 2}

📂 Context loaded:
├─ CLAUDE.md (project overview)
└─ {module}/CLAUDE.md (if relevant)

🎯 Next steps (from last session):
1. {next action 1}
2. {next action 2}
3. {next action 3}

❓ Open questions:
- {question 1}
- {question 2}

Ready to continue?
```

## Error Handling

See `agents/shared/error-handling.md` for error patterns and recovery strategies.

## Directory Structure

Ensure these exist (create if missing):
```bash
mkdir -p .claude/work
mkdir -p .claude/archive
```

Create `.claude/state.md` if missing.

## Best Practices & Philosophy

See `agents/shared/principles.md` for core execution principles including conversational approach, graceful failure, and progressive disclosure.

## Workflow Hint

After successfully starting work, provide this next step hint to help users learn the cadence:

```
💡 **Next steps:** As you work, use `/keep:save` to checkpoint progress and capture decisions. Run it at natural breakpoints (after implementing features, making key decisions, or every 30-45 min).
```
