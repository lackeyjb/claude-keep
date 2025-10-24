---
name: keep
description: Intelligent project memory and workflow management. Use when working with GitHub issues, capturing project learnings, managing CLAUDE.md context files, or deciding what to work on next.
---

# Keep - Intelligent Project Memory

Keep provides intelligent project memory through structured issue tracking, automatic learning capture, proactive context evolution, and seamless GitHub integration.

**Core capabilities:**
- Track work on issues with structured progress files in `.claude/work/`
- Capture decisions, learnings, and patterns automatically during work sessions
- Suggest CLAUDE.md updates when patterns emerge (3+ decisions or 2+ sessions in directory)
- Sync progress and completion summaries to GitHub Issues
- Recommend next work based on context continuity, priority, and freshness

**Design philosophy:**
- Leverage Claude Code's native CLAUDE.md loading
- Intelligence over automation - suggest when valuable, don't overwhelm
- Minimal ceremony, maximum value
- Fail gracefully - works offline, without GitHub, with corrupted state

See `references/file-formats.md` for all file format specifications.

---

## Command Workflows

Keep is invoked via slash commands in `.claude/commands/`:

### /keep-start [issue-number]

Begin work on a GitHub issue (or discover work if no issues exist).

**Workflow:**
1. **Fetch issue** - `gh issue view {number}` (parse requirements, dependencies, labels)
2. **Load context:**
   - Root CLAUDE.md (auto-loaded by Claude Code)
   - Module CLAUDE.md files (auto-loaded by Claude Code)
   - `.claude/state.md` (read manually)
   - `.claude/archive/` (search for related past work)
3. **Create work file** - `.claude/work/{issue}.md` with issue metadata, approach, empty sections
4. **Update state** - `.claude/state.md` with active issue, start time, clear previous
5. **Present starting point** - Conversational summary with context, approach, questions

**Zero-issues project initialization:**

When no issues exist, discover starter work using native tools:
1. Check CLAUDE.md context (offer `/keep-grow .` if missing)
2. Scan planning docs (Glob: `{ROADMAP,TODO,PLAN}*.md`), code signals (Grep: `TODO:|FIXME:|BUG:`), test gaps
3. Generate 3-5 issue suggestions with source attribution
4. User selects issues to create
5. Ensure GitHub labels exist, create via `gh issue create`
6. Transition to normal start workflow

See `references/zero-issues.md` for detailed discovery patterns and logic.

---

### /keep-save [--sync]

Save progress and capture learnings during work session.

**Workflow:**
1. **Review conversation** - Extract progress, decisions with rationale, learnings, questions
2. **Update work file** - Add timestamped progress log, document decisions/learnings, update files modified
3. **Update state** - `.claude/state.md` with progress indicators, next steps, questions
4. **Check threshold** - Count decisions by directory (3+ decisions → suggest CLAUDE.md update)
5. **Generate CLAUDE.md proposal** (if threshold met):
   - Read existing CLAUDE.md
   - Draft updates as diff
   - Present for approval with rationale
   - Only update if approved
6. **Optional GitHub sync** (if `--sync` flag):
   - Generate progress summary (see `references/github-templates.md`)
   - Post via `gh issue comment {number}`
   - Record sync timestamp

**What to capture:**
- **Decisions** - Technical choices with rationale (e.g., "Use Redis for rate limiting - already in stack")
- **Learnings** - Gotchas, non-obvious behaviors (e.g., "express-rate-limit auto-adds X-RateLimit-* headers")
- **Patterns** - Approaches that work well (e.g., "Exclude health checks from rate limiting")
- **Mistakes** - Common errors to avoid (e.g., "Don't log full JWT tokens")

---

### /keep-done [--close]

Complete work, sync to GitHub, archive, and recommend next work.

**Workflow:**
1. **Generate summary** - Read complete work file, aggregate all progress/decisions/learnings
2. **Check context updates** - Review all learnings, propose CLAUDE.md updates if patterns emerged
3. **Detect PR** - Check for associated PR via `gh pr view --json state,number,url`
4. **Sync to GitHub:**
   - Generate completion summary (see `references/github-templates.md`)
   - Include PR link in summary if PR exists
   - Post via `gh issue comment {number}`
   - **PR-aware closing:**
     - **PR merged**: Check if issue already closed (GitHub auto-closes when PR with "Fixes #X" merges). Don't ask - note "issue auto-closed via PR #X"
     - **PR open**: Don't close issue. Inform user it will auto-close when PR merges
     - **PR closed (unmerged)**: Ask if they want to close issue manually
     - **No PR**: Ask about closing issue (current behavior)
   - If closing confirmed/needed: `gh issue close {number}`
5. **Archive work file** - Move `.claude/work/{issue}.md` → `.claude/archive/{issue}.md` (preserve PR info)
6. **Update state** - Clear active issue, add to recent work, update hot areas
7. **Recommend next work:**
   - Fetch open issues via `gh issue list`
   - Score using `scripts/score_issues.py` (continuity 30%, priority 30%, freshness 20%, dependency 20%)
   - Present top 3-5 recommendations
   - Offer to start immediately

**Scoring algorithm:**
- **Continuity** (0-100): Same directory +50, related labels +30, similar tech +20
- **Priority** (0-100): urgent=100, high=75, medium/none=50, low=25
- **Freshness** (0-100): <7 days=100, 8-14=75, 15-30=50, 31+=25
- **Dependency** (0-100): No blockers=100, -25 for each open blocker (parse "depends on #X")

---

## CLAUDE.md Evolution

### When to Suggest Updates

**Threshold detection:**
- **3+ decisions** in same directory → Suggest CLAUDE.md update
- **2+ sessions** in same directory → Consider new CLAUDE.md
- **Recurring patterns** → Document in relevant CLAUDE.md
- **Security/performance insights** → Always capture

### Suggesting Updates

**Process:**
1. **Detect need** - Count decisions/learnings by directory, identify patterns
2. **Generate proposal** - Read existing CLAUDE.md, draft new section, show as diff
3. **Present for approval** - Show complete change, explain benefit, offer yes/edit/later/no
4. **Apply** (if approved) - Maintain consistent format, keep concise (<200 lines)

**What makes good CLAUDE.md:**
- **Purpose** - What this module does and why
- **Key Patterns** - Important abstractions and approaches
- **API/Interface** - How to interact with this module
- **Recent Learnings** - Gotchas and insights
- **Common Mistakes** - What to avoid
- **Dependencies** - What this relies on
- **Testing** - How to test this module

Don't create CLAUDE.md prematurely - wait until patterns emerge.

---

## GitHub Integration

### Fetching Issues

```bash
gh issue view {number} --json title,body,labels,state
```

Parse issue body for:
- Requirements and acceptance criteria
- Dependencies ("depends on #123")
- Related issues
- Technical constraints

### Pull Request Detection

Check for associated PR on current branch:
```bash
gh pr view --json state,number,url
```

**PR-aware workflow:**
- Track PR URL in work file when detected
- Include PR link in GitHub completion summaries
- Smart issue closing based on PR state:
  - **Merged PR**: Issue should be auto-closed, verify and note
  - **Open PR**: Don't close issue (will auto-close on merge if properly linked)
  - **Closed PR (unmerged)**: Ask user about closing issue
  - **No PR**: Standard close confirmation

**GitHub auto-close:** Issues automatically close when PRs that reference them (e.g., "Fixes #123", "Closes #123") are merged. Keep respects this behavior.

### Posting Updates

Generate concise, valuable summaries. Focus on outcomes, not process.

Use formats from `references/github-templates.md`:
- **Progress update** - Completed items, in-progress, key decisions, next steps
- **Completion summary** - Summary, changes made, key decisions, testing, learnings, follow-up, PR link

Post via:
```bash
gh issue comment {number} --body "{summary}"
```

### Graceful Degradation

- If `gh` not available → Warn user, continue in local-only mode
- If network fails → Save locally, note sync needed
- If rate limit hit → Wait or continue with local data
- If PR detection fails → Continue with standard workflow
- Never fail workflow due to GitHub issues

See `references/troubleshooting.md` for detailed error handling.

---

## State Management

### .claude/state.md

Current session state - what you're working on right now.

**Sections:**
- **Active Work** - Current issue, branch, progress, next steps, open questions
- **Recent Work** - Last 3 completed issues for context
- **Blockers** - Current blockers or "None"
- **Context** - Hot directories, current focus areas

**Update on:**
- `/keep-start` - Set active issue, start time
- `/keep-save` - Update progress, next steps
- `/keep-done` - Clear active, add to recent, update context

### .claude/work/{issue-number}.md

Detailed tracking for specific issue during active work.

**Sections:**
- Issue metadata (GitHub URL, status, timestamps)
- Issue description
- Planned approach
- Progress log (timestamped entries)
- Decisions made (with rationale)
- Files modified (with descriptions)
- Learnings
- Tests (checklist)
- Next actions
- Related issues

**Lifecycle:**
- Created on `/keep-start`
- Updated during work (progress, decisions, learnings)
- Moved to `.claude/archive/` on `/keep-done`

See `references/file-formats.md` for complete specifications.

---

## Bundled Resources

### References

Load as needed to inform work:

**`references/file-formats.md`** - Complete specifications for all Keep file formats (state.md, work files, CLAUDE.md). Load when creating files or need format details.

**`references/workflows.md`** - Detailed workflow examples with ASCII diagrams showing complete interaction flows. Load when need detailed workflow guidance.

**`references/github-templates.md`** - Templates for GitHub issue comments (progress updates, completion summaries). Load when posting to GitHub.

**`references/zero-issues.md`** - Detailed zero-issues discovery patterns (Glob/Grep patterns, prioritization logic, issue generation). Load when no issues exist.

**`references/troubleshooting.md`** - Error handling, recovery procedures, graceful degradation strategies. Load when encountering errors.

### Scripts

Execute without loading into context:

**`scripts/score_issues.py`** - Implements issue scoring algorithm for next work recommendations. Execute via Bash for `/keep-done` recommendations.

**`scripts/github_sync.py`** - Helper for GitHub API operations with authentication, rate limiting, retries. Use when `gh` CLI insufficient.

---

## Best Practices

**Be concise yet complete:**
- Capture key information without verbosity
- Focus on "why" not just "what"
- Make it useful for future you (6 months later)

**Progressive disclosure:**
- Don't overwhelm with all context at once
- Load references only when needed
- Present information conversationally

**Fail gracefully:**
- Work offline if needed
- Continue without GitHub if unavailable
- Degrade features, don't break workflows
- Preserve user data above all else

**Learn and adapt:**
- Notice when patterns emerge
- Suggest context updates proactively (but not annoyingly)
- Help context evolve with project

**Respect user control:**
- Always get approval before creating/updating CLAUDE.md
- Show proposed changes as diffs
- Offer edit option, not just yes/no
- Never force workflow steps

---

## Error Handling

**Corrupted state:**
- If `.claude/state.md` invalid → Recreate from work files, show for confirmation
- If work file missing → Recreate from GitHub or fresh start
- Always preserve user data, never silently delete

**Conflicting state:**
- If active work in state but file archived → Ask user to resolve
- If multiple work files active → Present options, let user choose
- Never auto-resolve ambiguity

**GitHub unavailable:**
- Check for `gh` CLI: `which gh`
- If missing → Warn, offer local-only mode
- If network error → Save locally, note sync needed
- If rate limit → Suggest waiting, continue with local data

See `references/troubleshooting.md` for comprehensive error handling guide.

---

## Summary

Keep provides intelligent project memory without ceremony:

- **Start work** - Load context, track in structured files, present informed starting point
- **Capture learnings** - Automatic extraction of decisions, learnings, patterns as they emerge
- **Evolve context** - Proactive CLAUDE.md suggestions when thresholds met, always with approval
- **GitHub integration** - Seamless sync, graceful offline operation
- **Next work** - Smart recommendations based on continuity, priority, and freshness

Focus on being helpful, not intrusive. Suggest when valuable, don't overwhelm. Learn from patterns, adapt to project needs. Make project memory effortless and valuable.
