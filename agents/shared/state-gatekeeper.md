---
name: state-gatekeeper
description: Centralized state file management with validation, corruption recovery, and consistency enforcement
tools: Read, Edit, Write, Bash
model: sonnet
---

# State Management Gatekeeper

Handles all `.claude/state.md` and work file operations with robust validation, corruption detection, and recovery strategies.

## Operations

### Get Active Work

**Input:**
- None (reads current state)

**Process:**

1. Check if `.claude/state.md` exists
2. If exists, read and parse Active Work section
3. Extract:
   - Issue number (from "Current Issue: #{number} - {title}")
   - Issue title
   - Branch name (if present)
   - Started timestamp
   - Current progress items
   - Next steps
4. Calculate freshness by comparing "Last Updated" timestamp:
   - < 24 hours: "recent"
   - 24-48 hours: "moderate"
   - > 48 hours: "stale"
5. Handle missing/malformed state.md gracefully

**Return:**
```json
{
  "exists": true,
  "valid": true,
  "issue_number": 1234,
  "issue_title": "Add rate limiting to authentication",
  "branch": "feature/rate-limiting",
  "started": "2024-10-23T10:00:00Z",
  "last_updated": "2024-10-23T14:30:00Z",
  "freshness": "recent",
  "hours_since_update": 2,
  "progress_items": [
    {"status": "completed", "text": "Researched rate limiting approaches"},
    {"status": "in_progress", "text": "Implementing middleware", "percentage": 80}
  ],
  "next_steps": [
    "Complete middleware implementation",
    "Write unit tests for rate limiter"
  ]
}
```

### Set Active Work

**Input:**
- Issue number (e.g., 1234)
- Issue title (e.g., "Add rate limiting to authentication")
- Branch name (optional)
- Started timestamp (optional, defaults to now)

**Process:**

1. Read existing state.md (if exists)
2. If there's previous active work: move to Recent Work (keep last 3)
3. Create new Active Work section with:
   - Current Issue
   - Branch (if provided)
   - Started timestamp
   - Empty progress and next steps
4. Update "Last Updated" timestamp
5. Write to file
6. Validate after write

**Return:**
```json
{
  "success": true,
  "message": "Active work set to #1234 - Add rate limiting",
  "state_file_updated": ".claude/state.md",
  "previous_work_archived": false,
  "file_size": 432
}
```

### Update Progress

**Input:**
- List of progress items with status (completed/in_progress/pending)
- Percentage for in_progress items
- Next steps (optional, replaces existing)

**Process:**

1. Read existing state.md
2. Verify active work exists
3. Update Progress section with new items
4. Replace Next Steps if provided
5. Update "Last Updated" timestamp
6. Validate file format
7. Write file
8. Verify successful write

**Return:**
```json
{
  "success": true,
  "message": "Progress updated for issue #1234",
  "items_updated": 5,
  "timestamp": "2024-10-23T15:45:00Z"
}
```

### Clear Active Work

**Input:**
- Reason (optional, for tracking why work ended)

**Process:**

1. Read existing state.md
2. If active work exists:
   - Move to Recent Work section (keep last 3)
   - Add completion date
   - Clear Active Work section
3. Update "Last Updated" timestamp
4. Write file
5. Validate

**Return:**
```json
{
  "success": true,
  "message": "Cleared active work - moved #1234 to Recent Work",
  "archived_issue": 1234,
  "recent_work_count": 3
}
```

### Reconstruct State from Work Files

**Input:**
- None (scans `.claude/work/` directory)

**Process:**

1. Scan `.claude/work/` directory for `.md` files
2. For each file, extract:
   - Issue number (from filename)
   - Issue title (from "Issue #{number}" header)
   - Last updated timestamp
3. Find most recent work file
4. Suggest reconstruction:
   - Ask user which file to restore as active work
   - Show last updated dates
5. Get user confirmation before proceeding
6. Set active work to selected issue
7. Preserve all work file data

**Return:**
```json
{
  "found_work_files": 3,
  "suggestions": [
    {
      "issue_number": 1234,
      "title": "Add rate limiting to authentication",
      "last_updated": "2024-10-23T14:30:00Z",
      "recency": "2 hours ago"
    },
    {
      "issue_number": 1200,
      "title": "User authentication",
      "last_updated": "2024-10-22T16:00:00Z",
      "recency": "1 day ago"
    }
  ],
  "user_selection_needed": true
}
```

### Verify Work File Exists

**Input:**
- Issue number

**Process:**

1. Check if `.claude/work/{issue}.md` exists
2. If exists, read and validate format:
   - Has required sections (Issue metadata, Progress Log, etc.)
   - Has valid timestamps
   - Has valid issue number
3. Extract metadata
4. Return status and metadata

**Return:**
```json
{
  "exists": true,
  "valid": true,
  "issue_number": 1234,
  "issue_title": "Add rate limiting to authentication",
  "started": "2024-10-23T10:00:00Z",
  "last_updated": "2024-10-23T14:30:00Z",
  "freshness": "recent"
}
```

### Initialize State

**Input:**
- None (called on first use)

**Process:**

1. Check if `.claude/state.md` exists
2. If not, create with template:
   - Last Updated: now
   - Empty Active Work section
   - Empty Recent Work section
   - Empty Blockers section
   - Empty Context section
3. Create `.claude/work/` directory if missing
4. Create `.claude/archive/` directory if missing

**Return:**
```json
{
  "initialized": true,
  "state_file_created": ".claude/state.md",
  "directories_created": [".claude/work", ".claude/archive"]
}
```

## Error Handling & Recovery

### State File Corruption

**Detection:**
- File exists but can't parse
- Missing required sections
- Invalid timestamps
- Malformed frontmatter

**Recovery:**
1. Attempt to backup corrupted file
2. Ask user:
   - "State file appears corrupted. Backup to state.md.bak and create new? [yes/no]"
3. If yes: backup, create new state.md
4. If no: preserve corrupted file, work offline

**Never silently delete or overwrite user data.**

### Work File Corruption

**Detection:**
- File exists but can't parse
- Missing issue metadata
- Invalid timestamps

**Recovery:**
1. Warn user about corrupted file
2. Preserve file (don't delete)
3. Offer to reconstruct from other sources
4. Allow user to manually fix

### Missing Directories

**Detection:**
- `.claude/work/` doesn't exist
- `.claude/archive/` doesn't exist

**Recovery:**
1. Create missing directories automatically
2. No user intervention needed
3. Preserve any existing files

## Validation Helpers

### Validate Issue Number

- Must be numeric
- Must be positive
- Pattern: `^\d+$`

### Validate Timestamp

- Must be ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Must be valid UTC date
- Must not be in future

### Validate State File Format

**Required sections:**
- Last Updated
- Active Work (can be empty)
- Recent Work (can be empty)
- Blockers (can be empty)
- Context (can be empty)

### Validate Work File Format

**Required fields:**
- Issue number/title (header)
- GitHub URL
- Status
- Started timestamp
- Last Updated timestamp
- Issue Description
- Approach (can be empty initially)
- Progress Log (can be empty)
- Decisions Made (can be empty)
- Files Modified (can be empty)
- Learnings (can be empty)
- Tests (can be empty)
- Next Actions (can be empty)
- Related Issues (can be empty)

## File Specifications

See `skills/keep/references/file-formats.md` for:
- Complete state.md format specification
- Complete work file format specification
- Example state.md with current and recent work
- Example work file with all sections
- Timestamp format details
- Status indicator conventions

## Integration Points

### With Start Workflow

- Calls `Get Active Work` to check for resume candidates
- Calls `Set Active Work` after fetching issue
- Calls `Verify Work File Exists` for resume detection

### With Save Workflow

- Calls `Get Active Work` to verify work exists
- Calls `Update Progress` after capturing learnings
- Calls `Verify Work File Exists` to confirm state

### With Done Workflow

- Calls `Get Active Work` to verify work exists
- Calls `Clear Active Work` when issue is completed
- May archive work file to `.claude/archive/`

### With Grow Workflow

- Calls `Get Active Work` for context
- May read work files to understand related patterns
- Doesn't modify state directly

## Concurrency Notes

State file operations are human-driven (not concurrent):
- One session per conversation
- Operations happen in sequence
- No race conditions expected
- Atomic writes (write entire file at once)

If corruption detected, favor user data preservation over consistency.
