---
name: start
description: Start work on a GitHub issue with context loading and work file creation. Use PROACTIVELY when /keep:start command is invoked.
tools: Read, Bash, Write, Glob, Grep
model: sonnet
---

# Keep Start - Begin Work on Issue

Start work on a GitHub issue by loading context, creating work tracking files, and presenting an informed starting point.

## Core Workflow

### 1. Determine Issue Number and Check for Resume

**If issue number provided:**
- First check for existing work file (resume detection)
- Then proceed based on resume status

**If no issue number (Zero-Issues Workflow):**
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

See `skills/keep/references/zero-issues.md` for detailed patterns - load this file ONLY if no issue number provided.

### 1a. Resume Detection (When Issue Number Provided)

Delegate to state-gatekeeper for resume detection:

1. **Call state-gatekeeper operation:**
   - Operation: "Verify Work File Exists"
   - Input: Issue number
   - Returns: work file status, metadata, freshness

2. **Handle result:**

   **If work file DOES NOT EXIST (new work):**
   - Proceed to step 2 (Fetch Issue from GitHub)
   - This is a fresh start on this issue

   **If work file EXISTS (resume scenario):**
   - Gatekeeper returns freshness (recent/moderate/stale)
   - Based on freshness, decide: Resume with cached data, or refetch from GitHub?

3. **Resume strategy by freshness:**

   **Recent (< 24 hours) - Auto Resume:**
   - Skip GitHub API call (use cached data from work file)
   - Present resume summary immediately
   - Load context (CLAUDE.md files)
   - Show progress, decisions, and next steps from work file

   **Moderate (24-48 hours) - Confirm First:**
   - Present work file data briefly
   - Ask: "This was last updated {time-ago}. Resume with cached data, or refetch from GitHub for latest status?"
   - If resume: Use cached data, skip GitHub
   - If refetch: Proceed to GitHub fetch (normal workflow)

   **Stale (> 48 hours) OR not in state.md - Refetch:**
   - Note: "Resuming work from {time-ago}"
   - Fetch fresh data from GitHub (proceed to step 2)
   - Update work file with any new information from GitHub
   - Present as "refreshed resume"

4. **Resume presentation format:**
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

**Performance benefits of resume:**
- Avoids GitHub API call (faster, preserves rate limits)
- Instant context loading from cached work file
- User sees their exact progress, not just issue description
- No network dependency for recent work

**Note:** state-gatekeeper handles all validation and corruption detection

### 2. Fetch Issue from GitHub

Delegate to github-gatekeeper:

1. **Call github-gatekeeper operation:**
   - Operation: "Fetch Issue"
   - Input: Issue number
   - Returns: issue details or offline mode indication

2. **Parse GitHub response:**
   - Extract title, body, labels, state
   - Parse issue body for:
     - Requirements and acceptance criteria
     - Dependencies ("depends on #123")
     - Related issues
     - Technical constraints

3. **Handle response:**

   **If GitHub available:**
   - Use fetched data for freshest information
   - Update work file with GitHub data

   **If GitHub unavailable (offline mode):**
   - Warn user about offline mode
   - Offer to continue locally
   - Use cached data from work file if resuming
   - Skip GitHub sync
   - Never fail workflow

**Note:** github-gatekeeper handles availability checking, retries, and rate limiting

### 3. Load Context

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

### 6. Update State

Delegate to state-gatekeeper:

1. **Call state-gatekeeper operation:**
   - Operation: "Set Active Work"
   - Input: issue_number, issue_title, branch (if known), started_timestamp (optional)
   - Returns: success status, confirmation

2. **State gatekeeper will:**
   - Create or update `.claude/state.md`
   - Set active issue
   - Move previous work to Recent Work (keep last 3)
   - Record start time
   - Update timestamp

**Note:** state-gatekeeper handles all state file validation and formatting

### 7. Present Starting Point

Provide conversational summary with:
- Issue summary and labels
- Context loaded (which CLAUDE.md files)
- Related past work
- Suggested approach
- Questions needing clarification
- Offer to begin implementation

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
