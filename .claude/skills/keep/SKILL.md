---
name: keep
description: Intelligent project memory and workflow management. Use when working with GitHub issues, capturing project learnings, managing CLAUDE.md context files, or deciding what to work on next.
---

# Keep - Intelligent Project Memory

## Overview

Keep is an intelligent system for managing project memory, context, and workflows. It helps track work on GitHub issues, capture learnings as they emerge, evolve project context through CLAUDE.md files, and recommend what to work on next.

**Core capabilities:**
- Track work on issues with structured progress files
- Capture decisions, learnings, and patterns automatically
- Suggest CLAUDE.md updates when patterns emerge
- Sync progress to GitHub Issues
- Recommend next work based on context and continuity

**Design philosophy:**
- Leverage Claude Code's native CLAUDE.md loading
- Intelligence over automation
- Minimal ceremony, maximum value
- Fail gracefully (works offline, without GitHub)

---

## When to Use Keep

Keep should be invoked by slash commands in `.claude/commands/`:
- `/keep:start` - Begin work on a GitHub issue
- `/keep:save` - Save progress and capture learnings
- `/keep:done` - Complete work and sync to GitHub

When invoked, load this skill's instructions and apply the intelligence described below.

---

## Core Responsibilities

### 1. Context Loading and Management

**On work start:**
- Identify relevant CLAUDE.md files for the current issue
- Parse `.claude/state.md` for recent context
- Check `.claude/archive/` for related work
- Surface relevant patterns and decisions from past issues

**During work:**
- Monitor which directories and files are being modified
- Track decision-making patterns
- Identify when context would be valuable but is missing

**Progressive CLAUDE.md creation:**
- Don't create CLAUDE.md files prematurely
- Wait until patterns emerge (2nd+ session in directory, or 3+ related decisions)
- When suggesting new CLAUDE.md, provide complete draft for review
- Focus on patterns, gotchas, and design decisions

---

### 2. Learning Capture

**What to capture:**
- **Decisions** - Technical choices with rationale (e.g., "Use Redis for rate limiting because we already have it in stack")
- **Learnings** - Gotchas, non-obvious behaviors, things that surprised you (e.g., "express-rate-limit auto-adds X-RateLimit-* headers")
- **Patterns** - Approaches that work well (e.g., "Exclude health checks from rate limiting")
- **Mistakes** - Common errors to avoid (e.g., "Don't log full JWT tokens")

**When to capture:**
- During `/keep:save` - explicit checkpoint
- Throughout work session - observe conversation for decisions/learnings
- On `/keep:done` - comprehensive review of entire work session

**How to capture:**
- Add timestamped entries to `.claude/work/{issue}.md` Progress Log
- Document decisions in Decisions Made section
- Store learnings in Learnings section
- Update files modified list

**Structure decisions clearly:**
```markdown
## Decisions Made

1. **{Decision}:** {rationale}
   - Alternative considered: {alternative} (rejected because {reason})
   - Impact: {what this affects}
```

---

### 3. Context Evolution

**Threshold detection:**
- **3+ decisions** in same area → Suggest CLAUDE.md update
- **2+ sessions** in same directory → Consider new CLAUDE.md
- **Recurring patterns** → Document in relevant CLAUDE.md
- **Security/performance insights** → Always capture

**Suggesting CLAUDE.md updates:**

1. **Detect the need:**
   - Count decisions/learnings by directory
   - Identify emerging patterns
   - Check if existing CLAUDE.md needs updates

2. **Generate proposal:**
   - Read existing CLAUDE.md (if present)
   - Draft new section or updates
   - Show as diff/addition
   - Explain why this would help future work

3. **Present for approval:**
   - Show complete proposed change
   - Explain benefit ("Future work in auth/ will have this rate limiting context")
   - Offer options: yes / edit / later / no
   - If "edit", enter conversational editing

4. **Apply updates:**
   - Only if user approves
   - Maintain consistent format
   - Keep concise (each CLAUDE.md < 200 lines ideally)

**What makes a good CLAUDE.md:**
- **Purpose** - What this module does and why
- **Key Patterns** - Important abstractions and approaches
- **API/Interface** - How to interact with this module
- **Recent Learnings** - Gotchas and insights
- **Common Mistakes** - What to avoid
- **Dependencies** - What this relies on
- **Testing** - How to test this module

See `references/file-formats.md` for complete specifications.

---

### 4. GitHub Integration

**Fetching issues:**
```bash
gh issue view {number} --json title,body,labels,state
```

Parse issue body for:
- Requirements and acceptance criteria
- Dependencies ("depends on #123")
- Related issues
- Technical constraints

**Posting updates:**

Generate concise, valuable summaries. Focus on outcomes, not process.

**Progress update format:**
```markdown
## Progress Update - {date} {time}

✅ Completed:
- {completed item}
- {completed item}

🔄 In Progress:
- {current item} ({percentage}% done)

💡 Key Decisions:
- {decision}: {rationale}

Next: {next steps}
```

**Completion summary format:**
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

**Post to GitHub:**
```bash
gh issue comment {number} --body "{summary}"
```

**Graceful degradation:**
- If `gh` not available, warn user and continue in local-only mode
- If network fails, save progress locally and note sync needed
- Never fail workflow due to GitHub issues

---

### 5. State Management

**`.claude/state.md` structure:**
- **Active Work** - Current issue, branch, progress, next steps
- **Recent Work** - Last 3 completed issues for context
- **Context** - Hot areas of codebase, current focus
- **Notes** - Open questions, blockers

**Update state on:**
- `/keep:start` - Set active issue, note start time
- `/keep:save` - Update progress, next steps
- `/keep:done` - Clear active, add to recent, update context

**Maintain history:**
- Keep last 3 completed issues in "Recent Work"
- Track which directories have been worked in recently
- Note patterns (e.g., "Recent focus: authentication and security")

See `references/file-formats.md` for complete state.md specification.

---

### 6. Work File Management

**`.claude/work/{issue-number}.md` lifecycle:**

**On start:**
- Create file with issue metadata
- Parse issue description into approach
- Initialize empty sections (Progress, Decisions, Learnings, Tests)
- Link to GitHub issue

**During work:**
- Append to Progress Log with timestamps
- Add decisions as they're made
- Capture learnings as they emerge
- Update files modified list
- Track tests written/needed

**On completion:**
- Generate comprehensive summary
- Ensure all decisions/learnings captured
- List all files modified (can use `git diff --name-only`)
- Note test status
- Identify follow-up work
- Move to `.claude/archive/{issue-number}.md`

See `references/file-formats.md` for complete work file specification.

---

### 7. Next Work Recommendation

**When to recommend:**
- After `/keep:done` completes
- When explicitly asked via `/keep:next`
- When user asks "what should I work on?"

**Scoring algorithm:**

```
score = (continuity × 0.30) + (priority × 0.30) + (freshness × 0.20) + (dependency × 0.20)
```

**Continuity (0-100):**
- Same directory as recent work: +50
- Related labels/topic: +30
- Similar tech stack: +20

**Priority (0-100):**
- Label "urgent": 100
- Label "high-priority": 75
- Label "medium" or no priority: 50
- Label "low-priority": 25

**Freshness (0-100):**
- Updated in last 7 days: 100
- Updated 8-14 days ago: 75
- Updated 15-30 days ago: 50
- Updated 31+ days ago: 25

**Dependency (0-100):**
- No blockers: 100
- Blockers cleared: 90
- Pending blockers: 50
- Hard blockers: 0

**Parse dependencies:**
- Look for "depends on #123" or "blocked by #456" in issue body
- Check if referenced issues are closed
- Factor into scoring

**Present recommendations:**
```
🎯 Recommended Next Work

🔥 Hot Recommendation:
#{number} - {title}
├─ {why this is recommended}
├─ Same area: {directory}
└─ Estimated: {size estimate}

📋 Other Good Options:
2. #{number} - {title} [{label}]
   └─ {brief rationale}

3. #{number} - {title} [{label}]
   └─ {brief rationale}

Start #{number}? [yes / show more / other]
```

See `scripts/score_issues.py` for scoring implementation.

---

### 8. Zero-Issues Project Initialization

**When to trigger:**
- `/keep:start` called without issue number
- `gh issue list` returns empty array
- User asks "what should I work on?" with no open issues

**Three-phase workflow using Claude's native tools:**

**Phase 1: Discovery**

Check for CLAUDE.md context:
- If root CLAUDE.md missing/stale: Offer `/keep:grow .` first
- Ensure project context loaded before suggesting work

Find planning documents (use Glob):
- `{ROADMAP,TODO,PLAN,BACKLOG,VISION,CONTRIBUTING}*.md`
- Read found docs, parse list items and checkboxes (- [ ] patterns)
- Extract actionable items with source file and line numbers

Scan codebase signals (use Grep):
- Pattern: `TODO:|FIXME:|HACK:|BUG:` with `-n` for line numbers, `-B 1 -A 1` for context
- Categorize by type: FIXME/BUG (high priority), TODO (medium), HACK (refactor)

Assess test coverage (use Glob):
- Find tests: `**/*.{test,spec}.{js,ts,py,go,rs}`
- Find source: `{src,lib}/**/*.{js,ts,py,go,rs}`
- Identify directories with missing test coverage

**Phase 2: Synthesis**

Prioritize findings:
1. Planning docs (ROADMAP, etc.) - highest priority
2. FIXME/BUG comments - important fixes
3. TODO comments - planned improvements
4. Missing tests - quality improvements
5. Documentation gaps - lower priority

Generate 3-5 issue suggestions with:
- Clear, actionable title
- Full description with context
- **Source attribution** (file:line or document name)
- Suggested labels (enhancement, bug, testing, documentation)
- Affected files if known

**Phase 3: Interactive Creation**

Present findings conversationally (example):

```markdown
I notice you don't have any open issues. Let me help find starter work!

📚 Project context: ✅ CLAUDE.md found

📋 Planning documents:
   • ROADMAP.md: 5 planned features
   • TODO.md: 3 pending tasks

🔍 Codebase analysis:
   • 12 TODO/FIXME comments
   • 8 files missing tests

🎯 5 Starter Issue Suggestions:

1. **Implement user authentication** [enhancement, high]
   Source: ROADMAP.md line 15

2. **Fix rate limiting in API** [bug, medium]
   Source: FIXME in src/api/routes.ts:34

3. **Add tests for payment module** [testing, medium]
   Source: Missing coverage in src/payments/

Which issues should I create? [all / 1,2,3 / none - work locally]
```

Before creating issues:
- Collect all unique labels from selected issues
- Check existing labels: `gh label list --json name --jq '.[].name'`
- For any missing labels, create with default color: `gh label create "label-name"`

For each selected issue:
- Generate natural issue body (describe what, why, where, source)
- Create via `gh issue create --title "..." --body "..." --label "..."`
- Display created issue URL

Ask which to start, then transition to normal `/keep:start {number}` workflow.

**Graceful degradation:**
- No planning docs → Focus on code signals
- No TODOs → Focus on test coverage
- Nothing found → Suggest `/keep:grow` or manual issue creation
- Offline → Work locally, sync later

**Philosophy:**
- Source transparency (always show where suggestions came from)
- User control (select which issues to create)
- Natural generation (no templates needed)

---

## Workflow Intelligence

### Starting Work

1. Fetch issue from GitHub (if issue number provided)
2. Parse issue for requirements, dependencies, acceptance criteria
3. Load relevant context:
   - Root CLAUDE.md (always loaded by Claude Code)
   - Module-specific CLAUDE.md files (loaded automatically by Claude Code)
   - `.claude/state.md` (read manually)
   - Related archived work (search `.claude/archive/` for keywords)
4. Suggest approach based on:
   - Project patterns from CLAUDE.md files
   - Similar past work from archive
   - Technical constraints from issue
5. Create work file with structure
6. Update state.md
7. Present comprehensive starting point

**Be conversational:** Don't just dump information. Present context naturally, highlight key insights, ask clarifying questions if requirements unclear.

---

### Saving Progress

1. Review recent conversation (since last save or start)
2. Extract:
   - Concrete progress made
   - Decisions with rationale
   - Learnings and gotchas
   - Questions raised or answered
3. Update work file with timestamped entries
4. Check learning threshold:
   - Count decisions by directory
   - Count sessions in each directory
   - Identify emerging patterns
5. If threshold met (3+ decisions or 2+ sessions):
   - Generate CLAUDE.md proposal
   - Show diff/addition
   - Get approval before updating
6. If `--sync` flag or user confirms:
   - Generate progress summary
   - Post to GitHub
   - Record sync timestamp
7. Confirm what was captured

---

### Completing Work

1. Read complete work file
2. Aggregate all progress, decisions, learnings
3. Generate comprehensive summary:
   - What was accomplished (outcomes)
   - Why decisions were made (rationale)
   - What was learned (insights)
   - What was tested (status)
   - What follow-up needed (if any)
4. Check for context updates:
   - Review all learnings
   - Identify which CLAUDE.md files should be updated
   - Generate proposals
   - Get approval
5. Sync to GitHub:
   - Post completion summary
   - Ask about closing issue
   - If close requested: `gh issue close {number}`
6. Archive work file:
   - Move `.claude/work/{issue}.md` to `.claude/archive/`
   - Preserve all content
7. Update state:
   - Clear active issue
   - Add to recent work
   - Update context (hot areas)
8. Recommend next work:
   - Fetch open issues
   - Score using algorithm above
   - Present top 3-5 recommendations
   - Offer to start immediately

---

## Working with Bundled Resources

### References

**`references/file-formats.md`**
- Complete specifications for all file formats
- Load when creating new files or need format details
- Reference for exact structure and conventions

**`references/workflows.md`**
- Detailed workflow examples with ASCII diagrams
- Load when need detailed workflow guidance
- Shows complete interaction flows

**When to load references:**
- When user asks about file formats
- When creating new CLAUDE.md or work files
- When need detailed workflow guidance
- Not needed for routine operations (keep context lean)

### Scripts

**`scripts/github_sync.py`**
- Helper for GitHub API operations
- Handles authentication, rate limiting, retries
- Use when `gh` CLI not available or for programmatic access

**`scripts/score_issues.py`**
- Implements issue scoring algorithm
- Can be executed without loading into context
- Use for `/keep:next` recommendations

**When to use scripts:**
- When deterministic logic needed
- When same operation repeated frequently
- When `gh` CLI insufficient
- Execute via Bash tool, don't need to read unless patching

---

## Best Practices

### Be Concise Yet Complete
- Capture key information without verbosity
- Focus on "why" not just "what"
- Make it useful for future you (6 months later)

### Progressive Disclosure
- Don't overwhelm with all context at once
- Load references only when needed
- Present information conversationally

### Fail Gracefully
- Work offline if needed
- Continue without GitHub if unavailable
- Degrade features, don't break workflows

### Learn and Adapt
- Notice when patterns emerge
- Suggest context updates proactively (but not annoyingly)
- Help context evolve with project

### Respect User Control
- Always get approval before creating/updating CLAUDE.md
- Show proposed changes as diffs
- Offer edit option, not just yes/no
- Never force workflow steps

---

## Error Handling

**GitHub unavailable:**
- Check for `gh` CLI: `which gh`
- If missing: Warn user, offer local-only mode
- If network error: Save locally, note sync needed

**Corrupted state:**
- If `.claude/state.md` invalid: Recreate from work files
- If work file missing: Create from GitHub issue
- Always preserve user data, never silently delete

**Conflicting state:**
- If active work in state.md but no work file: Warn and fix
- If work file exists but not in state: Reconcile
- Ask user to resolve ambiguity if unclear

**GitHub rate limits:**
- Catch rate limit errors
- Suggest waiting period
- Continue with cached/local data

---

## Command Integration

This skill is invoked by slash commands:

**`/keep:start [issue-number]`** - Invokes this skill to begin work
- Load context
- Fetch issue
- Create work file
- Update state
- Present starting point

**`/keep:save [--sync]`** - Invokes this skill to save progress
- Capture learnings
- Update files
- Check thresholds
- Suggest context updates
- Optional GitHub sync

**`/keep:done [--close]`** - Invokes this skill to complete work
- Generate summary
- Suggest context updates
- Sync to GitHub
- Archive work
- Recommend next

See `.claude/commands/` for command implementations.

---

## Summary

Keep provides intelligent project memory through:
- Structured tracking of issues and progress
- Automatic learning capture and pattern recognition
- Proactive context evolution suggestions
- Seamless GitHub integration
- Smart next work recommendations

Focus on being helpful, not intrusive. Suggest when valuable, don't overwhelm. Learn from patterns, adapt to project needs. Make project memory effortless and valuable.
