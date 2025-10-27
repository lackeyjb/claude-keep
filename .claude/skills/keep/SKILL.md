---
name: keep
description: Intelligent project memory and workflow management. Use when working with GitHub issues, capturing project learnings, managing CLAUDE.md context files, or deciding what to work on next.
---

# Keep - Intelligent Project Memory

Keep provides intelligent project memory through structured issue tracking, automatic learning capture, proactive context evolution, and seamless GitHub integration.

## Core Philosophy

**Intelligence over automation**
- Suggest when valuable, don't overwhelm
- Learn patterns, don't just log actions
- Adapt to project needs

**Minimal ceremony, maximum value**
- Capture what matters, skip the rest
- Focus on "why" not just "what"
- Make it useful for future you (6 months later)

**Leverage Claude Code's native capabilities**
- CLAUDE.md files auto-load (no manual loading needed)
- Use Claude's tools (Glob, Grep, Read, Edit, Bash)
- Progressive disclosure - load details when needed

**Fail gracefully**
- Work offline without GitHub
- Degrade features, don't break workflows
- Preserve user data above all else
- Never silently delete or overwrite

## Workflow Delegation

Keep delegates to specialized sub-agents for each workflow:

**`/keep-start [issue]`** → `.claude/agents/keep-start.md`
- Fetch issue from GitHub
- Load project context
- Create work tracking file
- Present informed starting point
- Handle zero-issues project initialization

**`/keep-save [--sync]`** → `.claude/agents/keep-save.md`
- Capture progress and learnings
- Update work file and state
- Suggest CLAUDE.md updates when patterns emerge
- Optional sync to GitHub

**`/keep-done [--close]`** → `.claude/agents/keep-done.md`
- Generate comprehensive summary
- Detect and handle PR state
- Sync to GitHub with smart closing
- Archive work and recommend next issue

**`/keep-grow [directory]`** → `.claude/agents/keep-grow.md`
- Analyze directory for patterns
- Create or update CLAUDE.md
- Grow project context deliberately

Each sub-agent operates in its own context with only the tools and knowledge it needs.

## File Organization

```
.claude/
├── agents/               # Workflow sub-agents (invoked by commands)
│   ├── keep-start.md
│   ├── keep-save.md
│   ├── keep-done.md
│   └── keep-grow.md
├── commands/            # Slash commands (thin wrappers)
│   ├── keep-start.md
│   ├── keep-save.md
│   ├── keep-done.md
│   └── keep-grow.md
├── skills/keep/
│   ├── SKILL.md         # This file - minimal core philosophy
│   ├── references/      # Load as needed
│   │   ├── file-formats.md        # File format specs
│   │   ├── zero-issues.md         # Discovery patterns
│   │   ├── troubleshooting.md     # Error handling
│   │   ├── workflows.md           # Detailed examples
│   │   └── templates/
│   │       ├── github-progress.md
│   │       └── github-completion.md
│   └── scripts/         # Execute without loading
│       ├── score_issues.py
│       └── github_sync.py
├── state.md            # Current session state
├── work/               # Active work tracking
│   └── {issue}.md
└── archive/            # Completed work
    └── {issue}.md
```

## State Management

**`.claude/state.md`** - Current session state
- Active work (current issue, progress, next steps)
- Recent work (last 3 completed issues)
- Blockers and context

**`.claude/work/{issue}.md`** - Detailed issue tracking
- Issue metadata and description
- Progress log (timestamped entries)
- Decisions made (with rationale)
- Learnings and insights
- Files modified
- Tests and next actions

**`.claude/archive/{issue}.md`** - Completed work
- Preserved for reference
- Searchable for related patterns
- Source for CLAUDE.md suggestions

## CLAUDE.md Evolution

**When to suggest updates:**
- 3+ decisions in same directory
- 2+ sessions in same directory
- Recurring patterns emerge
- Security or performance insights

**How to suggest:**
- Detect threshold during work
- Generate specific proposal
- Show complete diff
- Get user approval
- Never force updates

**What makes good CLAUDE.md:**
- Purpose - What this module does and why
- Key Patterns - Important abstractions
- API/Interface - How to interact
- Recent Learnings - Gotchas and insights
- Common Mistakes - What to avoid
- Dependencies - What this relies on
- Testing - How to test

## GitHub Integration

**Graceful degradation:**
- Check for `gh` CLI: `which gh`
- If missing → Warn, offer local-only mode
- If network error → Save locally, note sync needed
- If rate limit → Wait or continue with local data
- Never fail workflow due to GitHub issues

**PR-aware closing:**
- Merged PR → Issue auto-closes (respect this)
- Open PR → Don't close (will auto-close on merge)
- Closed PR → Ask about closing issue
- No PR → Standard close confirmation

## References

Load these files only when needed:

**`references/file-formats.md`** - Complete file format specifications
- Load when creating files or need format details

**`references/zero-issues.md`** - Zero-issues discovery patterns
- Load only when no issues exist

**`references/workflows.md`** - Detailed workflow examples with diagrams
- Load when need detailed workflow guidance

**`references/troubleshooting.md`** - Error handling and recovery
- Load when encountering errors

**`references/templates/github-progress.md`** - Progress update template
- Load when posting progress to GitHub

**`references/templates/github-completion.md`** - Completion summary template
- Load when posting completion to GitHub

## Scripts

Execute these via Bash without loading into context:

**`scripts/score_issues.py`** - Issue scoring for recommendations
- Implements continuity + priority + freshness + dependency algorithm
- Execute via Bash, don't load code

**`scripts/github_sync.py`** - GitHub API helper
- Advanced GitHub operations when `gh` CLI insufficient

## Best Practices

**Respect user control:**
- Always get approval for CLAUDE.md updates
- Show complete changes, not summaries
- Offer edit option, not just yes/no
- Never force workflow steps

**Be concise yet complete:**
- Capture key information without verbosity
- Focus on "why" not just "what"
- Make notes useful for future reference

**Progressive disclosure:**
- Don't load all references upfront
- Load details only when needed
- Present information conversationally

**Learn and adapt:**
- Notice when patterns emerge
- Suggest context updates proactively but not annoyingly
- Help context evolve with project

---

Keep provides intelligent project memory without ceremony:
- Start work with full context
- Capture learnings automatically
- Evolve CLAUDE.md files deliberately
- Seamless GitHub integration
- Smart next work recommendations

Focus on being helpful, not intrusive. Suggest when valuable, don't overwhelm. Learn from patterns, adapt to project needs. Make project memory effortless and valuable.
