# Keep - Project Specification

**Version:** 1.0
**Created:** 2024-10-23
**Purpose:** A lightweight, intelligent project memory and workflow system for Claude Code that uses GitHub Issues for persistence and nested CLAUDE.md files for context.

---

## Executive Summary

Keep is a drastically simplified alternative to complex project management systems. It leverages Claude Code's native features (nested CLAUDE.md files) and GitHub Issues to provide:

- **Persistent memory** across sessions
- **Intelligent context management** that grows with your project
- **Lightweight GitHub integration** without ceremony
- **Natural workflows** that enhance rather than constrain

**Key Metrics:**
- 1 Skill + 5 Commands (vs 50+ in alternatives)
- 90% fewer files to manage
- Zero custom context loaders (uses native Claude Code features)
- Works with or without GitHub

---

## Core Philosophy

### Design Principles

1. **Leverage Native Features** - Use Claude Code's built-in CLAUDE.md reading instead of custom loaders
2. **Intelligence Over Automation** - Skill suggests and learns rather than rigidly enforcing process
3. **Minimal Ceremony** - No multi-stage pipelines or complex file naming schemes
4. **Solo-First** - Optimized for individual developers, extensible for teams
5. **Fail Gracefully** - Works offline, works without GitHub, degrades elegantly

### Anti-Patterns We Avoid

❌ Complex multi-file frontmatter manipulation
❌ File renaming ceremonies (001.md → 1234.md)
❌ Rigid multi-stage pipelines (PRD → Epic → Tasks)
❌ 50+ bash scripts to maintain
❌ Git worktrees for every feature
❌ Static context that goes stale

---

## Architecture

### Directory Structure

```
project-root/
├── CLAUDE.md                           # Root project context (auto-loaded)
├── src/
│   ├── CLAUDE.md                       # Source code patterns
│   ├── auth/
│   │   └── CLAUDE.md                   # Domain-specific context
│   └── api/
│       └── CLAUDE.md                   # API-specific context
├── tests/
│   └── CLAUDE.md                       # Testing patterns
└── .claude/
    ├── work/
    │   ├── 1234.md                     # Active issue tracking
    │   └── 5678.md                     # Another active issue
    ├── archive/
    │   └── 1200.md                     # Completed issues (for reference)
    ├── state.md                        # Current session state
    └── skills/
        └── keep/                       # The Keep Skill
            ├── skill.json              # Skill configuration
            ├── README.md               # Skill documentation
            └── prompts/
                ├── start-work.md       # Work initiation prompt
                ├── capture-learning.md # Learning capture logic
                ├── suggest-context.md  # CLAUDE.md update suggestions
                ├── summarize-work.md   # GitHub summary generation
                └── analyze-next.md     # Next issue recommendation
```

### Component Overview

```
┌─────────────────────────────────────────────────────┐
│                    User                              │
└──────────────┬──────────────────────────────────────┘
               │
               │ Invokes commands
               ▼
┌─────────────────────────────────────────────────────┐
│              Slash Commands                          │
│  /keep:start  /keep:save  /keep:done               │
│  /keep:grow  /keep:next                            │
└──────────────┬──────────────────────────────────────┘
               │
               │ Delegates intelligence to
               ▼
┌─────────────────────────────────────────────────────┐
│              Keep Skill                              │
│  • Loads context (CLAUDE.md)                        │
│  • Captures learnings                               │
│  • Suggests updates                                 │
│  • Manages state                                    │
│  • Syncs with GitHub                                │
│  • Spawns parallel agents                           │
└──────────────┬──────────────────────────────────────┘
               │
               │ Reads/Writes
               ▼
┌─────────────────────────────────────────────────────┐
│              File System                             │
│  • Nested CLAUDE.md (context)                       │
│  • .claude/work/*.md (tracking)                     │
│  • .claude/state.md (current state)                 │
└─────────────────────────────────────────────────────┘
               │
               │ Syncs to
               ▼
┌─────────────────────────────────────────────────────┐
│              GitHub Issues                           │
│  • Source of truth                                  │
│  • Progress updates                                 │
│  • Team visibility                                  │
└─────────────────────────────────────────────────────┘
```

---

## File Specifications

### 1. Root `CLAUDE.md`

**Purpose:** Project-wide context that Claude Code automatically loads

**Location:** `{project-root}/CLAUDE.md`

**Structure:**
```markdown
# Project: {Project Name}

## Tech Stack
- Runtime/Language versions
- Major frameworks and libraries
- Database and infrastructure

## Architecture
- High-level architecture pattern (MVC, microservices, etc.)
- Key architectural decisions and rationale

## Project Structure
- Directory organization
- Module responsibilities
- Important file locations

## Development
- Setup instructions
- Common commands
- Environment variables

## Conventions
- Naming conventions
- Code style guidelines
- Testing approach

## Recent Changes (Last 3-6 months)
- Significant architectural changes
- New patterns adopted
- Deprecations
```

**Management:**
- Created manually or by `/init` command
- Updated by Keep Skill suggestions (with user approval)
- Kept concise (aim for < 200 lines)

---

### 2. Nested `CLAUDE.md` Files

**Purpose:** Domain-specific context for modules/directories

**Location:** `{project-root}/{directory}/CLAUDE.md`

**Structure:**
```markdown
# {Module Name}

## Purpose
What this module does and why it exists

## Key Patterns
- Specific patterns used in this module
- Important abstractions
- Design decisions

## API / Public Interface
- Key functions/classes
- How other modules interact with this

## Recent Learnings
- Gotchas discovered while working here
- Performance considerations
- Security considerations
- Common mistakes to avoid

## Dependencies
- External dependencies specific to this module
- Internal dependencies (other modules)

## Testing
- Testing approach for this module
- Key test files
```

**Management:**
- Created by Keep Skill when working in new area (with user approval)
- Updated as patterns emerge and learnings accumulate
- Skill suggests updates, user reviews and approves

**When to Create:**
- Working in a directory for 2nd+ time
- Patterns are emerging that should be documented
- Complex logic that benefits from explanation
- Don't create prematurely - let need emerge

---

### 3. `.claude/state.md`

**Purpose:** Current session state - what you're working on right now

**Location:** `.claude/state.md`

**Structure:**
```markdown
# Session State

**Last Updated:** 2024-10-23T14:30:00Z

## Active Work

**Current Issue:** #1234 - Add rate limiting to authentication
**Branch:** feature/rate-limiting
**Started:** 2024-10-23T10:00:00Z

### Progress
- ✅ Researched rate limiting approaches
- ✅ Installed express-rate-limit
- 🔄 Implementing middleware (80% done)
- ⏸️ Need to add tests
- ⏸️ Need to update API docs

### Next Steps
1. Complete middleware implementation
2. Write unit tests for rate limiter
3. Add integration tests
4. Update API documentation

### Open Questions
- Should rate limit be per IP or per user?
  → Decision: Per IP for unauthenticated, per user for authenticated
- What are the limits?
  → TBD: Need to discuss with team

## Recent Work

**Previous Issue:** #1200 - User authentication (Completed 2024-10-22)
**Previous Issue:** #1150 - Database migrations (Completed 2024-10-20)

## Blockers
None currently

## Context
- Working primarily in src/auth/
- Related to security improvements epic
- Builds on work from #1100 (JWT implementation)
```

**Management:**
- Updated by Keep Skill on `/keep:start`, `/keep:save`, `/keep:done`
- Auto-saved every 15 minutes during active work
- Human-readable markdown (Skill parses it)

---

### 4. `.claude/work/{issue-number}.md`

**Purpose:** Detailed tracking for a specific issue

**Location:** `.claude/work/{issue-number}.md`

**Structure:**
```markdown
# Issue #1234: Add rate limiting to authentication

**GitHub:** https://github.com/username/repo/issues/1234
**Status:** in_progress
**Started:** 2024-10-23T10:00:00Z
**Last Updated:** 2024-10-23T14:30:00Z

## Issue Description
Add rate limiting to prevent brute force attacks on authentication endpoints.

## Approach
Using express-rate-limit middleware with Redis store for distributed rate limiting.

## Progress Log

### 2024-10-23 14:30
- Implemented rate limiter middleware in src/auth/middleware/rateLimiter.ts
- Configured: 5 requests per 15 minutes for /login
- Configured: 3 requests per 15 minutes for /reset-password

### 2024-10-23 12:00
- Researched options: express-rate-limit vs rate-limiter-flexible
- Decided on express-rate-limit (simpler, sufficient for our needs)
- Installed dependencies

## Decisions Made
1. **Rate limit strategy:** Per-IP for unauthenticated routes
2. **Storage:** Redis (already in stack) for distributed limiting
3. **Limits:** Conservative (5/15min) - can adjust based on monitoring

## Files Modified
- src/auth/middleware/rateLimiter.ts (created)
- src/auth/routes.ts (modified)
- package.json (added express-rate-limit)

## Learnings
- express-rate-limit has excellent TypeScript support
- Need to exclude health check endpoints from rate limiting
- Rate limit headers (X-RateLimit-*) automatically added

## Tests
- [ ] Unit tests for rateLimiter middleware
- [ ] Integration test for login rate limiting
- [ ] Test rate limit header presence

## Next Actions
1. Write unit tests
2. Add integration tests
3. Update API documentation
4. Deploy to staging for testing

## Related Issues
- #1100 - JWT implementation (prerequisite)
- #1250 - Add monitoring for rate limit hits (follow-up)
```

**Management:**
- Created by `/keep:start` command
- Updated by Keep Skill during work (progress, decisions, learnings)
- Moved to `.claude/archive/` when issue completed
- Source for GitHub issue updates

---

### 5. Keep Skill Configuration

**Location:** `.claude/skills/keep/skill.json`

```json
{
  "name": "keep",
  "version": "1.0.0",
  "description": "Intelligent project memory and workflow management",
  "commands": {
    "start": "prompts/start-work.md",
    "save": "prompts/capture-learning.md",
    "done": "prompts/summarize-work.md",
    "grow": "prompts/suggest-context.md",
    "next": "prompts/analyze-next.md"
  },
  "auto_save_interval": 900,
  "github_sync": {
    "enabled": true,
    "auto_sync": false,
    "sync_on_done": true
  },
  "learning_threshold": {
    "suggest_context_update_after_decisions": 3,
    "suggest_new_claude_md_after_sessions": 2
  }
}
```

---

## Commands Specification

### Command 1: `/keep:start [issue-number]`

**Purpose:** Begin work on a GitHub issue with full context loading

**Behavior:**
1. **Fetch Issue** (if issue number provided)
   - Use `gh issue view {number} --json title,body,labels,state`
   - If no issue number: prompt user or offer `/keep:next` to recommend one

2. **Load Context**
   - Claude Code automatically loads relevant CLAUDE.md files
   - Keep Skill reads `.claude/state.md` for recent context
   - Look for related work in `.claude/archive/`

3. **Create Work File**
   - Create `.claude/work/{issue}.md` with structure above
   - Parse issue description into approach/tasks

4. **Update State**
   - Update `.claude/state.md` with active issue
   - Note start time, branch info

5. **Present Context**
   ```
   ✅ Ready to work on issue #1234

   📋 Issue: Add rate limiting to authentication
   🏷️  Labels: security, enhancement

   📚 Context loaded:
   ├─ CLAUDE.md (project overview)
   ├─ src/CLAUDE.md (code patterns)
   └─ src/auth/CLAUDE.md (auth patterns)

   🔗 Related work:
   └─ #1100 - JWT implementation (completed)

   💡 Suggested approach: [Skill analyzes and suggests]

   Where would you like to start?
   ```

**Parameters:**
- `issue-number` (optional) - GitHub issue number
- `--offline` flag - Skip GitHub, work locally only

**Error Handling:**
- No gh CLI: Warn, offer local-only mode
- Issue not found: Offer to create issue or work without one
- Network error: Fall back to local mode

**Files Modified:**
- Creates: `.claude/work/{issue}.md`
- Updates: `.claude/state.md`

---

### Command 2: `/keep:save`

**Purpose:** Save current progress, capture learnings, optionally sync to GitHub

**Behavior:**
1. **Update Work File**
   - Append progress log entry with timestamp
   - Update status indicators
   - Capture any decisions made

2. **Capture Learnings**
   - Skill analyzes recent work
   - Identifies patterns, gotchas, decisions
   - Stores in work file

3. **Suggest Context Updates**
   - If significant pattern emerged (3+ decisions in same area)
   - Suggest updating relevant CLAUDE.md
   - Show proposed changes, get approval

4. **Optional GitHub Sync**
   - If `--sync` flag or user confirms
   - Generate concise summary of progress
   - Post as issue comment
   - Use format:
     ```markdown
     ## Progress Update - 2024-10-23 14:30

     ✅ Completed:
     - Item 1
     - Item 2

     🔄 In Progress:
     - Item 3 (80% done)

     💡 Key Decisions:
     - Decision 1: Rationale

     Next: [Next steps]
     ```

5. **Confirmation**
   ```
   💾 Progress saved

   📝 Captured:
   - 2 progress entries
   - 1 key decision
   - 1 learning

   💡 Suggestion: Update src/auth/CLAUDE.md with rate-limiting pattern?
   [yes/no/later]
   ```

**Parameters:**
- `--sync` - Force sync to GitHub (even if auto-sync off)
- `--local` - Skip GitHub sync confirmation

**Auto-Save:**
- Runs automatically every 15 minutes (configurable)
- Auto-save doesn't sync to GitHub (too noisy)
- Auto-save just updates local files

**Files Modified:**
- Updates: `.claude/work/{issue}.md`
- Updates: `.claude/state.md`
- May update: relevant `CLAUDE.md` (with approval)

---

### Command 3: `/keep:done`

**Purpose:** Complete current issue, sync to GitHub, suggest next work

**Behavior:**
1. **Capture Final State**
   - Review all progress in `.claude/work/{issue}.md`
   - Capture final learnings and outcomes
   - List all files modified (from git)

2. **Generate Summary**
   - Comprehensive summary of work done
   - Key decisions and their rationale
   - Testing status
   - Any follow-up needed

3. **Sync to GitHub**
   - Post completion comment with full summary
   - Optionally close issue (ask user)
   - Format:
     ```markdown
     ## ✅ Work Complete - 2024-10-23 16:00

     ### Summary
     [Comprehensive summary]

     ### Changes Made
     - File 1: What changed
     - File 2: What changed

     ### Key Decisions
     1. Decision 1: Rationale
     2. Decision 2: Rationale

     ### Testing
     - ✅ Unit tests passing
     - ✅ Integration tests passing
     - ⏸️ Manual testing needed

     ### Learnings
     [Key learnings captured]

     ### Follow-up
     - Issue #1250: Add monitoring (created)
     ```

4. **Suggest Context Updates**
   - Review accumulated learnings
   - Suggest updating relevant CLAUDE.md files
   - Show diffs, get approval

5. **Archive Work**
   - Move `.claude/work/{issue}.md` to `.claude/archive/`
   - Update `.claude/state.md` to clear active issue

6. **Suggest Next Work**
   - Analyze GitHub issues
   - Recommend next issue based on:
     * Related to completed work
     * Same area of codebase (hot cache)
     * Priority labels
     * Dependencies (blockers cleared)
   ```
   🎉 Issue #1234 complete!

   📊 Summary:
   - 5 files modified
   - 3 key decisions documented
   - 2 learnings captured

   💡 Updated context:
   ✅ src/auth/CLAUDE.md (rate limiting pattern)

   🔗 Synced to: https://github.com/user/repo/issues/1234

   ⏭️  Recommended next:
   1. #1250 - Add monitoring (builds on this work)
   2. #1245 - Add OAuth (same area: auth)
   3. #1180 - Fix login bug (high priority)

   Start one now? [1/2/3/choose different]
   ```

**Parameters:**
- `--close` - Close the GitHub issue
- `--no-close` - Leave issue open
- `--no-sync` - Skip GitHub sync (local only)

**Files Modified:**
- Moves: `.claude/work/{issue}.md` → `.claude/archive/{issue}.md`
- Updates: `.claude/state.md`
- May update: relevant `CLAUDE.md` files (with approval)
- Interacts with: GitHub API (issue comment, close)

---

### Command 4: `/keep:grow [directory]`

**Purpose:** Create or expand CLAUDE.md files as project grows

**Behavior:**
1. **Analyze Directory**
   - Scan files in specified directory
   - Identify patterns, abstractions, key files
   - Detect if CLAUDE.md already exists

2. **Assess Need**
   - Is this a cohesive module?
   - Are there patterns worth documenting?
   - Will future work benefit from context here?

3. **Generate Proposal**
   - Draft CLAUDE.md content based on analysis
   - Show to user for review/editing
   ```
   📝 Proposed CLAUDE.md for src/payments/

   ─────────────────────────────────────
   # Payments Module

   ## Purpose
   Handles payment processing via Stripe API

   ## Key Patterns
   - Repository pattern for payment records
   - Webhook validation for Stripe events
   - Idempotency keys for retries

   [... full proposal ...]
   ─────────────────────────────────────

   Create this file? [yes/edit/no]
   ```

4. **Create or Update**
   - If approved: Create/update file
   - If edited: Apply user changes
   - If rejected: Skip

5. **Confirmation**
   ```
   ✅ Created src/payments/CLAUDE.md

   💡 This context will now auto-load when working in src/payments/

   Future work in this directory will benefit from this context!
   ```

**Parameters:**
- `directory` (required) - Directory to create CLAUDE.md in
- `--update` - Update existing CLAUDE.md (vs create new)

**When to Use:**
- Working in a directory for 2nd+ time
- Patterns are crystallizing
- Complex domain logic needs explanation
- Onboarding others (or future you)

**Files Modified:**
- Creates: `{directory}/CLAUDE.md`
- Or updates existing file

---

### Command 5: `/keep:next`

**Purpose:** Analyze GitHub issues and recommend what to work on next

**Behavior:**
1. **Fetch Open Issues**
   - Use `gh issue list --state open --json number,title,labels,createdAt`
   - Parse labels for priority, type, etc.

2. **Analyze Context**
   - What was just completed?
   - What area of codebase is "hot"?
   - What's the current branch?
   - Are there blockers cleared?

3. **Score Issues**
   - **Continuity** (30%): Same area as recent work
   - **Dependencies** (25%): Blockers cleared, prerequisites done
   - **Priority** (25%): Labels like "urgent", "high-priority"
   - **Context freshness** (20%): Recently discussed, activity

4. **Present Recommendations**
   ```
   🎯 Recommended Next Work

   🔥 Hot Recommendation:
   #1250 - Add monitoring for rate limiting
   ├─ Builds directly on #1234 (just completed)
   ├─ Same area: src/auth/
   ├─ Context is fresh in memory
   └─ Estimated: 2-3 hours

   📋 Other Good Options:

   2. #1245 - OAuth integration [high-priority]
      └─ Same area, but larger scope (1-2 days)

   3. #1180 - Fix login session bug [urgent]
      └─ Different area, but marked urgent

   4. #1300 - Add API documentation
      └─ Low priority, but unblocked now

   Start #1250? [yes/show more/choose different]
   ```

5. **Optional Start**
   - If user says yes, automatically run `/work-start {issue}`
   - If "show more", display more issues with details
   - If "choose different", let user specify

**Parameters:**
- `--filter {label}` - Only show issues with specific label
- `--area {directory}` - Only show issues related to directory
- `--all` - Show all issues, not just recommendations

**Scoring Algorithm:**
```javascript
score =
  (continuity_score * 0.30) +     // Same area as recent work
  (dependency_score * 0.25) +      // Prerequisites met
  (priority_score * 0.25) +        // Labels/urgency
  (context_freshness * 0.20)       // Recent activity

// Continuity: Same directory, related labels, similar scope
// Dependency: "depends on" cleared, no blockers
// Priority: Parse labels: urgent=100, high=75, medium=50, low=25
// Freshness: Recently commented/updated
```

**Files Read:**
- Reads: `.claude/state.md` (recent work context)
- Reads: `.claude/archive/*` (what's been done recently)
- Queries: GitHub API (open issues)

---

## Keep Skill Specification

### Skill Overview

**Name:** `keep`
**Type:** Conversational Skill with Tools
**Purpose:** Intelligent orchestration of project memory, context, and workflow

### Core Responsibilities

1. **Context Loading**
   - Identify relevant CLAUDE.md files for current work
   - Parse `.claude/state.md` for session context
   - Retrieve related work from archive

2. **Learning Capture**
   - Observe decisions during work
   - Identify patterns and gotchas
   - Extract key learnings from implementation

3. **Context Evolution**
   - Detect when new CLAUDE.md files would be valuable
   - Suggest updates to existing CLAUDE.md files
   - Keep context concise and current

4. **GitHub Integration**
   - Fetch issues and parse descriptions
   - Generate concise, valuable progress summaries
   - Post updates as issue comments
   - Handle rate limits and errors gracefully

5. **Workflow Intelligence**
   - Recommend next work based on context
   - Identify related issues and dependencies
   - Spawn parallel agents when beneficial
   - Consolidate results from multiple agents

---

### Skill Prompts

#### Prompt: `start-work.md`

**Invoked by:** `/keep:start [issue-number]`

**Context Provided:**
- Issue number (if provided)
- Current `.claude/state.md` content
- List of available CLAUDE.md files
- Recent work from archive

**Tasks:**
1. Fetch issue from GitHub (if issue provided)
2. Parse issue description into actionable structure
3. Identify relevant context (CLAUDE.md files, related issues)
4. Suggest initial approach based on project patterns
5. Create `.claude/work/{issue}.md`
6. Update `.claude/state.md`
7. Present comprehensive starting point to user

**Output:**
- Conversational presentation of issue and context
- Suggested approach
- Questions about unclear requirements
- Ready to start work

---

#### Prompt: `capture-learning.md`

**Invoked by:** `/keep:save`, auto-save interval

**Context Provided:**
- Current `.claude/work/{issue}.md` content
- Recent conversation/work (last 30 minutes)
- Relevant CLAUDE.md files

**Tasks:**
1. Analyze recent work for:
   - Progress made (concrete steps completed)
   - Decisions made (with rationale)
   - Learnings (gotchas, patterns, insights)
   - Questions raised or resolved

2. Update `.claude/work/{issue}.md`:
   - Add progress log entry with timestamp
   - Document decisions in Decisions section
   - Capture learnings in Learnings section
   - Update file list if new files modified

3. Assess if context updates needed:
   - Count significant decisions in same area
   - Check if new patterns emerged
   - Evaluate if CLAUDE.md update would help future work

4. If threshold met (e.g., 3 related decisions):
   - Generate proposed CLAUDE.md update
   - Show diff to user
   - Get approval before updating

5. If user chose `--sync` or confirmed:
   - Generate GitHub update (progress summary)
   - Post as issue comment
   - Record sync timestamp

**Output:**
- Confirmation of what was captured
- Optional suggestion for CLAUDE.md update
- Optional GitHub sync confirmation

---

#### Prompt: `suggest-context.md`

**Invoked by:** `/keep:grow [directory]`, or automatically when threshold met

**Context Provided:**
- Target directory path
- Files in that directory (ls, file types)
- Existing CLAUDE.md (if present)
- Recent work in that area (from archive)

**Tasks:**
1. **Analyze Directory:**
   - Scan file names and types
   - Read key files (main exports, interfaces)
   - Identify patterns (naming, structure, abstractions)
   - Detect frameworks/libraries in use

2. **Assess Value:**
   - Is this a cohesive module?
   - Are patterns clear enough to document?
   - Would future work benefit?
   - Is it too early to document?

3. **Generate Content:**
   If valuable, draft CLAUDE.md with:
   - Purpose: What this module does
   - Key Patterns: Important abstractions
   - API: How to interact with this module
   - Recent Learnings: Gotchas from recent work
   - Dependencies: What this relies on
   - Testing: How to test this

4. **Present Proposal:**
   - Show complete proposed CLAUDE.md
   - Highlight key sections
   - Ask: create/edit/skip
   - If edit: enter conversational editing mode

5. **Create/Update:**
   - Write file if approved
   - Confirm creation
   - Note that future work will auto-load this

**Output:**
- Analysis of whether CLAUDE.md would be valuable
- Complete proposed CLAUDE.md content
- Conversational editing if user wants changes
- Confirmation of creation

---

#### Prompt: `summarize-work.md`

**Invoked by:** `/keep:done`

**Context Provided:**
- Complete `.claude/work/{issue}.md` content
- Git diff or list of modified files
- Test results (if available)
- Related issues and context

**Tasks:**
1. **Generate Comprehensive Summary:**
   - What was accomplished
   - Why decisions were made this way
   - What was learned
   - What testing was done
   - What follow-up is needed

2. **Assess Context Updates:**
   - Review all learnings from work file
   - Identify which CLAUDE.md files should be updated
   - Generate proposed updates with diffs
   - Get user approval

3. **Create GitHub Summary:**
   - Professional, concise summary
   - Focus on outcomes, not process
   - Include key decisions with rationale
   - Note testing status
   - List follow-up items
   - Format for easy skimming

4. **Archive Work:**
   - Move work file to archive
   - Update state.md to clear active issue
   - Record completion timestamp

5. **Recommend Next:**
   - Invoke analyze-next logic
   - Present top 3 recommendations
   - Offer to start immediately

**Output:**
- Summary of work completed
- Context updates (with approval)
- GitHub issue updated/closed
- Recommendations for next work

---

#### Prompt: `analyze-next.md`

**Invoked by:** `/keep:next`, or after `/keep:done`

**Context Provided:**
- `.claude/state.md` (recent work history)
- `.claude/archive/*` (last 5 completed issues)
- GitHub open issues (via gh CLI)

**Tasks:**
1. **Fetch Open Issues:**
   ```bash
   gh issue list --state open --json number,title,labels,body,createdAt,updatedAt
   ```

2. **Load Context:**
   - What was just completed?
   - What area of codebase?
   - What's currently in progress (if any)?
   - What patterns/learnings are fresh?

3. **Score Each Issue:**
   - **Continuity (30%):** Same directory, related labels, similar tech
   - **Dependencies (25%):** Parse issue bodies for "depends on #", check if unblocked
   - **Priority (25%):** Parse labels: urgent=100, high-priority=75, medium=50, low=25
   - **Freshness (20%):** Recent comments/updates get higher score

4. **Rank and Select Top 3-5:**
   - Sort by score descending
   - Group by category (hot recommendation, other good options)
   - Prepare rationale for each recommendation

5. **Present Recommendations:**
   - Top recommendation with detailed rationale
   - Other good options with brief rationale
   - Allow filtering/searching
   - Offer to start immediately

**Scoring Pseudocode:**
```python
def score_issue(issue, recent_context):
    # Continuity: Same area as recent work
    continuity = 0
    if same_directory(issue, recent_context):
        continuity += 50
    if overlapping_labels(issue, recent_context):
        continuity += 30
    if similar_tech(issue, recent_context):
        continuity += 20

    # Dependencies: Are blockers cleared?
    dependency = 100  # Start assuming unblocked
    blockers = parse_depends_on(issue.body)
    for blocker in blockers:
        if not is_closed(blocker):
            dependency -= 50

    # Priority: Parse labels
    priority = 50  # Default medium
    if "urgent" in issue.labels:
        priority = 100
    elif "high-priority" in issue.labels:
        priority = 75
    elif "low-priority" in issue.labels:
        priority = 25

    # Freshness: Recent activity
    days_since_update = (now - issue.updatedAt).days
    freshness = max(0, 100 - (days_since_update * 5))

    # Weighted score
    return (
        continuity * 0.30 +
        dependency * 0.25 +
        priority * 0.25 +
        freshness * 0.20
    )
```

**Output:**
- Ranked list of recommended issues
- Rationale for each
- Option to start immediately
- Option to filter/search

---

### Skill Tools

The Keep Skill has access to these tools within its prompts:

1. **File System:**
   - Read: CLAUDE.md files, .claude/work/*, .claude/state.md
   - Write: .claude/work/*, .claude/state.md, CLAUDE.md (with approval)
   - Execute: Basic file operations

2. **Git:**
   - `git status` - Check current state
   - `git diff` - See changes
   - `git log --oneline -10` - Recent commits
   - `git branch --show-current` - Current branch

3. **GitHub CLI:**
   - `gh issue view {number}` - Fetch issue
   - `gh issue list` - List open issues
   - `gh issue comment {number}` - Post comment
   - `gh issue close {number}` - Close issue
   - `gh repo view` - Get repo info

4. **Subagents:**
   - Spawn parallel agents when beneficial
   - Pass clear file boundaries to each
   - Consolidate results

---

## Workflows

### Workflow 1: Start New Work

```
User: /keep:start 1234

Keep Skill:
1. Fetch issue #1234 from GitHub
   └─ gh issue view 1234 --json title,body,labels

2. Load relevant context
   ├─ Read CLAUDE.md (auto-loaded by Claude Code)
   ├─ Read src/auth/CLAUDE.md (auto-loaded)
   ├─ Read .claude/state.md
   └─ Check .claude/archive/ for related work

3. Parse issue into structure
   ├─ Extract requirements
   ├─ Identify affected areas
   └─ Note any dependencies

4. Create .claude/work/1234.md
   ├─ Issue metadata
   ├─ Approach section (suggested)
   ├─ Progress log (empty)
   └─ Decisions/learnings (empty)

5. Update .claude/state.md
   ├─ Set active issue: 1234
   ├─ Record start time
   └─ Move previous issue to "recent"

6. Present to user
   ├─ Issue summary
   ├─ Relevant context loaded
   ├─ Suggested approach
   └─ Ready to start

User sees:
┌────────────────────────────────────────┐
│ ✅ Ready to work on issue #1234        │
│                                         │
│ 📋 Issue: Add rate limiting to auth    │
│ 🏷️  Labels: security, enhancement      │
│                                         │
│ 📚 Context loaded:                     │
│ ├─ CLAUDE.md (project overview)        │
│ ├─ src/CLAUDE.md (code patterns)       │
│ └─ src/auth/CLAUDE.md (auth patterns)  │
│                                         │
│ 🔗 Related work:                       │
│ └─ #1100 - JWT implementation          │
│                                         │
│ 💡 Suggested approach:                 │
│ Based on existing auth patterns, I     │
│ suggest using express-rate-limit with  │
│ Redis store. This fits our current     │
│ architecture and JWT pattern.          │
│                                         │
│ Where would you like to start?         │
└────────────────────────────────────────┘
```

---

### Workflow 2: During Work (Auto-Save)

```
[15 minutes of active work]

Keep Skill (auto-save triggered):
1. Review recent conversation
   └─ Extract what was done, decisions made

2. Update .claude/work/1234.md
   ├─ Add progress log entry (timestamp)
   ├─ Document decisions in Decisions section
   ├─ Capture learnings in Learnings section
   └─ Update files modified

3. Check learning threshold
   └─ Count decisions: 2 related to rate limiting
   └─ Not yet at threshold (need 3)

4. Save state
   └─ Update .claude/state.md with latest progress

User sees:
┌────────────────────────────────────────┐
│ 💾 Auto-saved (14:30)                  │
│ Captured: 1 progress entry, 2 decisions│
└────────────────────────────────────────┘
```

---

### Workflow 3: Explicit Save with Context Update

```
User: /keep:save

Keep Skill:
1. Update .claude/work/1234.md
   ├─ Progress: Implemented middleware
   ├─ Decision: Use Redis for distributed rate limiting
   └─ Learning: express-rate-limit has great TS support

2. Check threshold
   └─ Count: 3 decisions about rate limiting
   └─ Threshold met!

3. Analyze for context update
   ├─ Working in src/auth/
   ├─ Rate limiting pattern is new
   └─ Should add to src/auth/CLAUDE.md

4. Generate proposed update
   ├─ Read current src/auth/CLAUDE.md
   ├─ Draft new section: "Rate Limiting"
   └─ Generate diff

5. Present to user

User sees:
┌────────────────────────────────────────┐
│ 💾 Progress saved                      │
│                                         │
│ 📝 Captured:                           │
│ - 2 progress entries                   │
│ - 3 decisions                          │
│ - 1 learning                           │
│                                         │
│ 💡 Suggestion: Update src/auth/        │
│    CLAUDE.md with rate-limiting        │
│    pattern?                            │
│                                         │
│ Proposed addition:                     │
│ ─────────────────────────────────      │
│ ## Rate Limiting                       │
│                                         │
│ - Use express-rate-limit middleware    │
│ - Redis store for distributed limiting │
│ - Limits: 5/15min for /login          │
│ - Exclude health checks                │
│ ─────────────────────────────────      │
│                                         │
│ Add this to src/auth/CLAUDE.md?        │
│ [yes / edit / later / no]              │
└────────────────────────────────────────┘

User: yes

Keep Skill:
6. Update src/auth/CLAUDE.md
   └─ Append new "Rate Limiting" section

7. Confirm

User sees:
┌────────────────────────────────────────┐
│ ✅ Updated src/auth/CLAUDE.md          │
│                                         │
│ Future work in auth/ will have this    │
│ rate limiting context!                 │
└────────────────────────────────────────┘
```

---

### Workflow 4: Complete Work

```
User: /keep:done

Keep Skill:
1. Read complete .claude/work/1234.md
   ├─ All progress entries
   ├─ All decisions made
   ├─ All learnings captured
   └─ Files modified list

2. Generate comprehensive summary
   ├─ What: Implemented rate limiting
   ├─ Why: Prevent brute force attacks
   ├─ How: express-rate-limit + Redis
   ├─ Decisions: Per-IP limiting, conservative limits
   ├─ Testing: Unit tests written, integration needed
   └─ Follow-up: Monitoring (#1250)

3. Check for context updates
   └─ Already updated src/auth/CLAUDE.md ✓

4. Generate GitHub summary

5. Post to GitHub
   └─ gh issue comment 1234 --body-file summary.md

6. Ask about closing

User sees:
┌────────────────────────────────────────┐
│ 🎉 Issue #1234 work complete!          │
│                                         │
│ 📊 Summary:                            │
│ - 4 files modified                     │
│ - 5 decisions documented               │
│ - 3 learnings captured                 │
│                                         │
│ 💡 Context updates:                    │
│ ✅ src/auth/CLAUDE.md (already done)   │
│                                         │
│ 🔗 Summary posted to issue             │
│                                         │
│ Close issue #1234? [yes / no / later]  │
└────────────────────────────────────────┘

User: yes

Keep Skill:
7. Close issue
   └─ gh issue close 1234

8. Archive work file
   └─ mv .claude/work/1234.md .claude/archive/

9. Update state
   ├─ Clear active issue
   └─ Move #1234 to recent work

10. Analyze next work
    └─ Invoke analyze-next logic

11. Present recommendations

User sees:
┌────────────────────────────────────────┐
│ ✅ Issue #1234 closed                  │
│                                         │
│ ⏭️  Recommended next work:             │
│                                         │
│ 🔥 Hot: #1250 - Add rate limit         │
│         monitoring                      │
│ ├─ Builds on #1234                     │
│ ├─ Same area: src/auth/                │
│ └─ Estimated: 2-3 hours                │
│                                         │
│ 📋 Other options:                      │
│ 2. #1245 - OAuth integration           │
│ 3. #1180 - Fix session bug             │
│                                         │
│ Start #1250? [yes / show more / other]│
└────────────────────────────────────────┘
```

---

### Workflow 5: Parallel Agent Execution

```
User: /keep:start 2000

Keep Skill analyzes issue #2000:
- Large scope: Database + API + UI changes
- Can be parallelized into streams

Keep Skill:
1. Identify work streams
   ├─ Stream A: Database schema/migrations
   ├─ Stream B: Repository layer
   ├─ Stream C: API endpoints
   └─ Stream D: Tests

2. Check for conflicts
   └─ Streams A-D touch different files ✓

3. Propose parallel execution

User sees:
┌────────────────────────────────────────┐
│ 📋 Issue #2000: Add product catalog    │
│                                         │
│ 💡 This can be parallelized!           │
│                                         │
│ Proposed streams:                      │
│ A. Database (schema, migrations)       │
│ B. Repository (product repository)     │
│ C. API (CRUD endpoints)                │
│ D. Tests (unit + integration)          │
│                                         │
│ Execute in parallel? [yes / no / edit] │
└────────────────────────────────────────┘

User: yes

Keep Skill:
4. Spawn parallel subagents
   ├─ Agent A: Database work
   │   └─ Files: src/db/*, migrations/*
   ├─ Agent B: Repository work
   │   └─ Files: src/repositories/product*
   ├─ Agent C: API work
   │   └─ Files: src/api/products*
   └─ Agent D: Test work
       └─ Files: tests/**/*product*

5. Monitor progress
   └─ Each agent reports back to Keep Skill

6. Consolidate results

User sees:
┌────────────────────────────────────────┐
│ ⚡ Running 4 parallel agents...        │
│                                         │
│ ✅ Agent A: Database complete (5 min)  │
│ ✅ Agent B: Repository complete (8 min)│
│ 🔄 Agent C: API in progress (60%)      │
│ 🔄 Agent D: Tests in progress (40%)    │
└────────────────────────────────────────┘

[After all complete]

┌────────────────────────────────────────┐
│ 🎉 All streams complete!               │
│                                         │
│ 📊 Summary:                            │
│ - 12 files created                     │
│ - 8 files modified                     │
│ - 15 tests added (all passing)         │
│                                         │
│ ⏱️  Total time: 12 minutes             │
│    (vs ~40 minutes sequential)         │
│                                         │
│ Continue with /work-save or           │
│ /work-done when ready.                 │
└────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: Foundation (Week 1)

**Goal:** Basic structure and core commands working locally (no GitHub)

**Tasks:**
1. Create directory structure
   ```
   .claude/
   ├── work/
   ├── archive/
   └── state.md
   ```

2. Implement `/keep:start` (local-only)
   - Create work file
   - Update state
   - No GitHub integration yet

3. Implement `/keep:save` (local-only)
   - Update work file with progress
   - Simple learning capture
   - No context suggestions yet

4. Implement `/keep:done` (local-only)
   - Archive work file
   - Update state
   - No GitHub sync yet

5. Create root CLAUDE.md template
   - Detect project type
   - Generate basic structure

**Deliverable:** Commands work locally, can track work without GitHub

---

### Phase 2: Keep Skill (Week 2)

**Goal:** Intelligent Skill that manages context and learning

**Tasks:**
1. Create Skill scaffold
   ```
   .claude/skills/keep/
   ├── skill.json
   └── prompts/
       ├── start-work.md
       ├── capture-learning.md
       └── summarize-work.md
   ```

2. Implement learning capture logic
   - Detect decisions during work
   - Identify patterns and gotchas
   - Store in work file

3. Implement context suggestion logic
   - Detect when CLAUDE.md update would help
   - Generate proposed updates
   - Present diffs for approval

4. Add auto-save functionality
   - Timer-based (15 min intervals)
   - Silent saves (no GitHub)
   - Update state and work file

**Deliverable:** Skill actively learns and suggests context updates

---

### Phase 3: GitHub Integration (Week 3)

**Goal:** Sync with GitHub Issues for persistence and visibility

**Tasks:**
1. Add GitHub fetching
   - Detect gh CLI availability
   - Fetch issue with `gh issue view`
   - Parse issue body and metadata
   - Graceful fallback if no gh

2. Add GitHub sync
   - Generate concise summaries
   - Post as issue comments
   - Handle rate limits
   - Record sync timestamps

3. Enhance `/keep:start` with GitHub
   - Fetch issue at start
   - Show labels, status
   - Parse related issues

4. Enhance `/keep:done` with GitHub
   - Post completion summary
   - Optional close issue
   - Handle errors gracefully

**Deliverable:** Full GitHub integration, issues as source of truth

---

### Phase 4: Next Work Intelligence (Week 4)

**Goal:** Recommend next work based on context and GitHub

**Tasks:**
1. Implement `/keep:next` command
   - Fetch open issues from GitHub
   - Parse labels and metadata
   - Basic scoring algorithm

2. Implement scoring logic
   - Continuity (same area)
   - Dependencies (blockers)
   - Priority (labels)
   - Freshness (recent activity)

3. Add recommendation presentation
   - Top 3 recommendations
   - Rationale for each
   - Option to start immediately

4. Add `analyze-next.md` Skill prompt
   - Intelligent analysis
   - Context-aware recommendations
   - Learning from past work

**Deliverable:** Smart recommendations for what to work on next

---

### Phase 5: Context Growth (Week 5)

**Goal:** Help project context evolve as codebase grows

**Tasks:**
1. Implement `/keep:grow` command
   - Analyze directory
   - Assess if CLAUDE.md would help
   - Generate proposal

2. Add directory analysis
   - Scan files and patterns
   - Detect key abstractions
   - Identify frameworks in use

3. Add CLAUDE.md generation
   - Template-based generation
   - Customized to detected patterns
   - Show proposal, get approval

4. Add `suggest-context.md` Skill prompt
   - Automatic detection of when to suggest
   - Threshold-based (3 decisions, 2 sessions)
   - Smart proposals

**Deliverable:** Context grows naturally as project evolves

---

### Phase 6: Parallel Agents (Week 6)

**Goal:** Spawn parallel agents for large issues

**Tasks:**
1. Add work stream analysis
   - Parse issue into potential streams
   - Identify file boundaries
   - Detect conflicts

2. Implement parallel spawning
   - Spawn multiple subagents
   - Pass clear file boundaries
   - Monitor progress

3. Add result consolidation
   - Collect results from agents
   - Merge into single summary
   - Update work file

4. Handle errors and conflicts
   - Detect file conflicts
   - Pause and request human intervention
   - Never auto-resolve conflicts

**Deliverable:** Large issues can be parallelized automatically

---

### Phase 7: Polish & Testing (Week 7)

**Goal:** Production-ready, well-tested, documented

**Tasks:**
1. Error handling
   - Graceful failures everywhere
   - Clear error messages
   - Recovery suggestions

2. Edge cases
   - No GitHub access
   - Corrupted state files
   - Network failures
   - Multiple issues active

3. Documentation
   - README for users
   - Examples and tutorials
   - Skill prompt documentation
   - Troubleshooting guide

4. Testing
   - Test with real projects
   - Various project types
   - With and without GitHub
   - Solo and team scenarios

**Deliverable:** Production-ready Claude Memory Manager

---

## Testing Strategy

### Unit Testing

**Skill Prompts:**
- Test with mock work files
- Test context suggestion logic
- Test GitHub summary generation
- Test scoring algorithm for /next

**Commands:**
- Test file creation/updates
- Test state management
- Test error handling
- Test parameter parsing

### Integration Testing

**Scenarios:**
1. **Fresh project start**
   - No existing .claude/ structure
   - Initialize and start first issue
   - Verify structure created correctly

2. **Complete workflow**
   - /keep:start → work → /keep:save → /keep:done
   - Verify all files updated correctly
   - Verify GitHub synced correctly

3. **Context evolution**
   - Work in new area
   - Trigger context suggestion
   - Verify CLAUDE.md created/updated

4. **Parallel execution**
   - Start large issue
   - Accept parallel execution
   - Verify agents run correctly
   - Verify consolidation works

5. **GitHub offline**
   - Disconnect from network
   - Verify graceful fallback
   - Verify local mode works

### Manual Testing

**Test Projects:**
- Node.js Express API
- React frontend
- Python Flask app
- Go microservice
- Rust CLI tool

**Test Scenarios:**
- Solo development (primary use case)
- Multiple issues in flight
- Long-running issues (multi-day)
- Context growth over time

---

## Future Enhancements

### Phase 8+: Beyond MVP

**Team Features:**
- Detect when multiple people working on same issue
- Coordinate through GitHub comments
- Share CLAUDE.md updates across team

**Advanced Intelligence:**
- Learn project-specific patterns over time
- Predict effort for issues
- Suggest issue breakdowns
- Detect technical debt

**Integrations:**
- Linear, Jira, other issue trackers
- Slack notifications
- CI/CD integration
- Code review integration

**UI/Visualization:**
- Web dashboard for project state
- Timeline visualization
- Context graph (what's connected)

**Analytics:**
- Velocity tracking
- Time spent per area
- Most valuable context files
- Pattern detection (common issues)

---

## Migration from CCPM

If transitioning from CCPM to Keep:

### Migration Steps

1. **Preserve GitHub Issues**
   - Already in GitHub ✓
   - No changes needed

2. **Convert Context**
   ```bash
   # Merge .claude/context/* into root CLAUDE.md
   cat .claude/context/project-overview.md >> CLAUDE.md
   cat .claude/context/tech-context.md >> CLAUDE.md
   # ... etc, manual curation
   ```

3. **Migrate Active Epics**
   ```bash
   # Active epics → work files
   for epic in .claude/epics/*/epic.md; do
     issue_num=$(extract_github_number $epic)
     cp $epic .claude/work/$issue_num.md
   done
   ```

4. **Clean Up**
   ```bash
   # Archive old structure
   mv .claude/epics .claude/epics.old
   mv .claude/context .claude/context.old
   ```

5. **Verify**
   - Run `/keep:start` on existing issue
   - Verify context loads
   - Verify GitHub sync works

### What You Gain

- 90% fewer files to manage
- No frontmatter manipulation
- No file renaming
- Simpler mental model
- Faster execution
- Same core benefits (memory, GitHub, agents)

### What You Lose

- Formal PRD → Epic → Task pipeline
- Git worktrees per epic
- Extensive bash scripts
- Predetermined directory structure

**Note:** If you need heavy structure, CCPM might still be better. Keep is for those who want lightweight intelligence over rigid process.

---

## Appendix

### A. Example Root CLAUDE.md

```markdown
# Project: TaskMaster API

## Tech Stack
- Node.js 18.x with TypeScript 5.x
- Express 4.x for REST API
- PostgreSQL 14 with TypeORM
- Redis for caching and rate limiting
- Jest for testing

## Architecture
RESTful API following repository pattern:
- Controllers handle HTTP
- Services contain business logic
- Repositories abstract database access
- Middleware for auth, validation, rate limiting

## Project Structure
```
src/
├── controllers/    # HTTP request handlers
├── services/       # Business logic
├── repositories/   # Database access
├── middleware/     # Express middleware
├── models/         # TypeORM entities
└── utils/          # Shared utilities
tests/              # Jest tests
migrations/         # TypeORM migrations
```

## Development
```bash
npm install          # Install dependencies
npm run dev          # Start dev server (port 3000)
npm test             # Run all tests
npm run migrate      # Run database migrations
```

## Conventions
- **Naming:** camelCase for functions, PascalCase for classes
- **Files:** One class per file, match file name to class name
- **Tests:** Co-located with source (*.test.ts)
- **Commits:** Conventional commits (feat:, fix:, etc.)
- **Branches:** feature/, bugfix/, hotfix/

## Authentication
- JWT access tokens (15min expiry)
- Refresh tokens stored in Redis (7 day expiry)
- bcrypt for password hashing (12 rounds)
- Rate limiting on auth endpoints (5 attempts/15min)

## Recent Changes (Last 3 months)
- 2024-10: Added rate limiting (express-rate-limit + Redis)
- 2024-09: Migrated from Sequelize to TypeORM
- 2024-08: Added refresh token rotation for security
```

### B. Example Domain CLAUDE.md

```markdown
# Authentication Module

## Purpose
Handles user authentication, token management, and session security.

## Key Patterns

### JWT Token Strategy
- **Access tokens:** 15 minute expiry, stored in memory
- **Refresh tokens:** 7 day expiry, stored in Redis
- **Rotation:** Refresh tokens rotate on use (one-time use)

### Password Security
- bcrypt with 12 rounds (balance of security and performance)
- Validation: minimum 8 chars, 1 uppercase, 1 number, 1 special
- Never log passwords or tokens (security audit requirement)

### Rate Limiting
- Per-IP rate limiting: 5 attempts per 15 minutes
- Applies to: /login, /register, /reset-password
- Implementation: express-rate-limit with Redis store
- Health checks excluded from rate limiting

## API / Public Interface

### Authentication Endpoints
- `POST /auth/login` - Email/password authentication
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Invalidate tokens
- `POST /auth/register` - Create new user

### Middleware
- `authenticate()` - Verify JWT access token
- `rateLimitAuth()` - Apply rate limiting

## Recent Learnings

### Rate Limiting Implementation (Oct 2024)
- express-rate-limit has excellent TypeScript support
- Remember to exclude health check endpoints (/health, /metrics)
- Redis store required for distributed rate limiting
- Rate limit headers (X-RateLimit-*) automatically added

### Token Rotation (Sept 2024)
- Refresh token rotation prevents reuse attacks
- Need to invalidate old refresh token immediately
- Redis TTL handles automatic cleanup

### Common Mistakes
- ❌ Forgetting to hash passwords in tests (use test fixtures)
- ❌ Logging full JWT tokens (use token.substring(0, 10))
- ❌ Not handling Redis connection failures (fallback gracefully)

## Dependencies
- External: jsonwebtoken, bcrypt, express-rate-limit
- Internal: src/models/User, src/repositories/UserRepository

## Testing
- Unit tests: src/auth/*.test.ts
- Integration tests: tests/integration/auth.test.ts
- Mock Redis in tests (redis-mock package)
```

### C. Example Work File

```markdown
# Issue #1234: Add rate limiting to authentication

**GitHub:** https://github.com/myuser/taskmaster-api/issues/1234
**Status:** completed
**Started:** 2024-10-23T10:00:00Z
**Completed:** 2024-10-23T16:00:00Z

## Issue Description
Add rate limiting to authentication endpoints to prevent brute force attacks.

## Approach
1. Use express-rate-limit middleware (widely used, good TypeScript support)
2. Redis store for distributed rate limiting (already in stack)
3. Apply to /login, /register, /reset-password
4. Conservative limits initially (5 per 15min)
5. Exclude health check endpoints

## Progress Log

### 2024-10-23 16:00
- ✅ All tests passing (unit + integration)
- ✅ Updated API documentation
- ✅ Deployed to staging
- Ready for review

### 2024-10-23 14:30
- Implemented rate limiter middleware in src/auth/middleware/rateLimiter.ts
- Configured limits: 5 requests per 15 minutes for /login
- Configured limits: 3 requests per 15 minutes for /reset-password
- Applied middleware to auth routes

### 2024-10-23 12:00
- Researched options: express-rate-limit vs rate-limiter-flexible
- Decided on express-rate-limit (simpler, sufficient for needs)
- Installed dependencies: express-rate-limit, rate-limit-redis

### 2024-10-23 10:00
- Started work on issue
- Read issue description and requirements
- Reviewed existing auth implementation

## Decisions Made

1. **Rate limit strategy:** Per-IP for unauthenticated routes
   - Rationale: Simplest approach, prevents IP-based brute force
   - Future: Consider per-user for authenticated routes

2. **Storage backend:** Redis (not in-memory)
   - Rationale: Already using Redis, need distributed limiting
   - Alternative considered: In-memory (rejected - won't work with multiple instances)

3. **Limit values:** 5 per 15min (login), 3 per 15min (reset)
   - Rationale: Conservative start, can adjust based on monitoring
   - Based on: Typical user behavior research

4. **Health check exclusion:** Exclude /health and /metrics
   - Rationale: Monitoring shouldn't be rate limited
   - Implementation: Separate middleware chain

## Files Modified
- src/auth/middleware/rateLimiter.ts (created)
  - Main rate limiter middleware
  - Redis store configuration
  - Error handling

- src/auth/routes.ts (modified)
  - Applied rate limiting to auth routes
  - Excluded health checks

- src/auth/middleware/index.ts (modified)
  - Export rate limiter middleware

- package.json (modified)
  - Added: express-rate-limit ^7.0.0
  - Added: rate-limit-redis ^4.0.0

- tests/unit/auth/rateLimiter.test.ts (created)
  - Tests for rate limiter middleware
  - Mock Redis for tests

- tests/integration/auth/rateLimiting.test.ts (created)
  - End-to-end rate limiting tests
  - Verify limits enforced correctly

- docs/api/authentication.md (modified)
  - Documented rate limits
  - Added X-RateLimit-* headers

## Learnings

1. **express-rate-limit TypeScript support**
   - Excellent type definitions out of the box
   - Easy to configure with our Redis setup

2. **Health check exclusion pattern**
   - Need to apply rate limiting selectively
   - Use route-specific middleware, not global

3. **Rate limit headers**
   - X-RateLimit-Limit, X-RateLimit-Remaining automatically added
   - Helps clients implement retry logic

4. **Testing with Redis**
   - Use redis-mock for unit tests (fast, isolated)
   - Use real Redis for integration tests (accurate)

5. **Error handling**
   - If Redis fails, rate limiting degrades gracefully
   - Falls back to in-memory (per instance, but better than nothing)

## Tests Status
- ✅ Unit tests: 8/8 passing
- ✅ Integration tests: 5/5 passing
- ✅ Manual testing: Completed on staging

## Next Actions
- Monitor rate limit hits in production (week 1)
- Create follow-up issue for monitoring dashboard (#1250)
- Consider per-user rate limiting for authenticated routes (future)

## Related Issues
- #1100 - JWT implementation (prerequisite)
- #1250 - Add monitoring for rate limit hits (follow-up, created)
```

### D. Example State File

```markdown
# Session State

**Last Updated:** 2024-10-23T16:05:00Z

## Active Work

No active work currently.

## Recent Work

**Completed:** #1234 - Add rate limiting (2024-10-23)
**Completed:** #1200 - User authentication (2024-10-22)
**Completed:** #1150 - Database migrations (2024-10-20)

## Context
- Recent focus: Authentication and security
- Hot area: src/auth/ (worked here last 3 issues)
- Current branch: main (feature branches merged)

## Notes
- Next recommended: #1250 (monitoring) - builds on #1234
```

---

## Summary

Keep provides the core benefits of CCPM (memory, GitHub integration, parallel agents) with 90% less complexity:

- **1 Skill + 5 Commands** instead of 50+
- **Nested CLAUDE.md** instead of custom context loaders
- **Lightweight file structure** instead of complex frontmatter
- **Natural workflows** instead of rigid pipelines
- **Solo-optimized** while remaining team-ready

The system is designed to be built in 6-7 weeks by a single developer working with Claude Code, and can be immediately used on real projects for continuous dogfooding.

Ready to build? Start with Phase 1 and iterate from there.
