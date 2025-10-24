# Keep

> Lightweight, intelligent project memory for Claude Code

Keep helps you track work on GitHub issues, capture learnings as you code, and grow project context naturally through CLAUDE.md files.

## What is Keep?

Keep is a skill + commands system for Claude Code that provides:

- **Persistent memory** across sessions via `.claude/work/` tracking files
- **Intelligent learning capture** - decisions, patterns, and gotchas documented automatically
- **Context evolution** - proactive suggestions to create/update CLAUDE.md files as patterns emerge
- **GitHub integration** - sync progress to issues, recommend next work based on continuity
- **Zero ceremony** - natural workflows that enhance rather than constrain

## Why Keep?

- **No complex setup** - leverages native Claude Code CLAUDE.md loading
- **Solo-optimized** - built for individual developers, not enterprise ceremony
- **Graceful degradation** - works offline, without GitHub, with minimal files
- **Intelligence over automation** - suggests and learns, doesn't enforce rigid processes

## Quick Start

### Installation

1. Copy `.claude/` directory to your project root
2. Ensure you have `gh` CLI installed (optional, for GitHub integration)
3. Create initial project context:
   ```bash
   /keep:grow .
   ```
   Keep will analyze your project and suggest creating a root CLAUDE.md with tech stack, architecture, and conventions.
4. Start using commands!

### Directory Structure

```
your-project/
├── CLAUDE.md                    # Root context (create manually or let Keep suggest)
├── src/
│   └── auth/
│       └── CLAUDE.md            # Module context (Keep suggests when patterns emerge)
└── .claude/
    ├── work/                    # Active issue tracking
    ├── archive/                 # Completed issues
    ├── state.md                 # Current session state
    ├── commands/
    │   ├── keep-start.md        # Start work command
    │   ├── keep-save.md         # Save progress command
    │   ├── keep-done.md         # Complete work command
    │   └── keep-grow.md         # Grow context command
    └── skills/keep/
        ├── SKILL.md             # Keep skill intelligence
        ├── references/          # File format specs, workflows
        └── scripts/             # GitHub helpers, scoring algorithm
```

## Commands

### `/keep:start [issue-number]`

Start work on a GitHub issue with full context loading.

```bash
/keep:start 1234
```

**What it does:**
- Fetches issue from GitHub
- Loads relevant CLAUDE.md files for context
- Reads recent work from `.claude/state.md` and archive
- Creates `.claude/work/1234.md` tracking file
- Suggests approach based on project patterns

**Flags:**
- `--offline` - Skip GitHub, work locally only
- `--no-fetch` - Resume existing work file

### `/keep:save`

Save progress and capture learnings.

```bash
/keep:save
/keep:save --sync  # Also post update to GitHub
```

**What it does:**
- Reviews recent conversation for progress, decisions, learnings
- Updates `.claude/work/{issue}.md` with timestamped entries
- Checks if patterns emerged (3+ decisions in same area)
- Suggests CLAUDE.md updates when threshold met
- Optional: Sync progress summary to GitHub

**Flags:**
- `--sync` - Force sync to GitHub
- `--local` - Skip GitHub sync confirmation

### `/keep:done`

Complete work and sync to GitHub.

```bash
/keep:done
/keep:done --close  # Also close the issue
```

**What it does:**
- Generates comprehensive summary of work completed
- Suggests CLAUDE.md updates for accumulated learnings
- Posts completion summary to GitHub issue
- Archives work file to `.claude/archive/`
- Updates session state
- Recommends next work based on continuity + priority

**Flags:**
- `--close` - Close the GitHub issue
- `--no-close` - Leave issue open
- `--no-sync` - Skip GitHub interaction
- `--no-recommend` - Skip next work suggestions

### `/keep:grow [directory]`

Create or update CLAUDE.md files for project context.

```bash
/keep:grow .           # Analyze project root
/keep:grow src/auth    # Analyze specific module
/keep:grow --update    # Update existing CLAUDE.md
```

**What it does:**
- Analyzes directory for patterns and abstractions
- Assesses if CLAUDE.md would be valuable
- Generates complete CLAUDE.md proposal
- Shows proposal for review/editing
- Creates file if approved

**When to use:**
- Initial setup on existing project (create root CLAUDE.md)
- Document a module after patterns emerge
- Update existing CLAUDE.md with new learnings
- Manually trigger if automatic suggestion was missed

**Flags:**
- `--update` - Update existing CLAUDE.md
- `--force` - Create even if patterns unclear

## Example Workflow

```bash
# Start work on issue
/keep:start 1234

# Work on implementation...
# (Keep observes decisions and learnings)

# Save progress checkpoint
/keep:save

# Continue working...

# Complete and sync
/keep:done --close
```

**Keep automatically:**
- Captures 5 decisions about authentication patterns
- Suggests updating `src/auth/CLAUDE.md` with rate limiting pattern
- Posts comprehensive summary to GitHub issue #1234
- Recommends issue #1250 as next work (builds on #1234, same area)

## Features

### Intelligent Learning Capture

Keep observes your work and automatically captures:
- **Decisions** - Technical choices with rationale
- **Learnings** - Gotchas, non-obvious behaviors, surprises
- **Patterns** - Approaches that work well
- **Mistakes** - Common errors to avoid

### Context Evolution

When patterns emerge (3+ related decisions, or 2+ sessions in directory):
- Keep suggests creating/updating CLAUDE.md files
- Shows proposed changes as diffs
- Gets your approval before updating
- Keeps context concise and current

### Smart Recommendations

After completing work, Keep recommends next issues based on:
- **Continuity (30%)** - Same area as recent work (hot cache)
- **Priority (30%)** - Labels like "urgent", "high-priority"
- **Freshness (20%)** - Recently updated issues
- **Dependencies (20%)** - Blockers cleared

### GitHub Integration

Optional but powerful:
- Fetches issue details and dependencies
- Posts concise progress updates
- Generates professional completion summaries
- Gracefully degrades when offline

## File Formats

### `.claude/work/{issue}.md`

Tracks a single issue with:
- Progress log (timestamped entries)
- Decisions made (with rationale)
- Learnings captured
- Files modified
- Tests status
- Next actions

### `.claude/state.md`

Current session state:
- Active issue and progress
- Recent completed work (last 3)
- Open questions and blockers
- Context (hot areas)

### Root `CLAUDE.md`

Project-wide context (auto-loaded by Claude Code):
- Tech stack
- Architecture patterns
- Project structure
- Development setup
- Conventions
- Recent changes

### Module `CLAUDE.md` (e.g., `src/auth/CLAUDE.md`)

Domain-specific context (auto-loaded when working in directory):
- Purpose of module
- Key patterns and abstractions
- API/interface
- Recent learnings and gotchas
- Common mistakes
- Dependencies and testing

See `.claude/skills/keep/references/file-formats.md` for complete specifications.

## Advanced Usage

### Offline Mode

Keep works without GitHub:
```bash
/keep:start --offline
# Provide issue details manually
# Keep tracks locally, can sync later
```

### Custom Scripts

Keep includes helper scripts:

**`github_sync.py`** - GitHub API operations with retry logic:
```bash
python .claude/skills/keep/scripts/github_sync.py fetch-issue 1234
```

**`score_issues.py`** - Score open issues for recommendations:
```bash
gh issue list --json number,title,labels,body,updatedAt | \
  python .claude/skills/keep/scripts/score_issues.py --recent-work .claude/state.md
```

### Context Growth

Manually trigger CLAUDE.md creation or updates:
```bash
# Analyze and create root CLAUDE.md
/keep:grow .

# Document a specific module
/keep:grow src/auth

# Update existing CLAUDE.md with new patterns
/keep:grow src/api --update
```

Keep also suggests CLAUDE.md updates automatically during `/keep:save` when patterns emerge (3+ decisions in same area).

## Configuration

Keep is designed to work with minimal configuration. All intelligence lives in `.claude/skills/keep/SKILL.md`.

To customize behavior, edit the skill file to adjust:
- Learning thresholds (default: 3 decisions)
- Scoring weights (default: 30% continuity, 30% priority, 20% freshness, 20% dependencies)
- Auto-save intervals (if enabled)

## Philosophy

**Intelligence over automation** - Keep suggests and learns rather than enforcing rigid processes.

**Minimal ceremony** - No multi-stage pipelines, complex frontmatter, or file renaming ceremonies.

**Progressive disclosure** - Context grows naturally as patterns emerge, not created prematurely.

**Fail gracefully** - Works offline, without GitHub, with minimal files. Degrades features, never breaks workflows.

**Solo-first** - Optimized for individual developers, extensible for teams.

## Comparison to Alternatives

| Feature | Keep | Complex PM Tools |
|---------|------|------------------|
| Commands | 4 core | 50+ |
| Files to manage | Minimal | Hundreds |
| Setup time | < 5 minutes | Hours |
| Context loaders | Native CLAUDE.md | Custom |
| Offline support | ✅ Full | ❌ Limited |
| Learning curve | Low | High |
| Ceremony | Minimal | High |

## Requirements

- Claude Code
- `gh` CLI (optional, for GitHub integration)
- Git repository (optional, for best experience)

## License

MIT

## Contributing

This is a personal project but suggestions welcome! The skill is designed to be customized - edit `.claude/skills/keep/SKILL.md` to suit your workflow.

## Learn More

- Skill documentation: `.claude/skills/keep/SKILL.md`
- File format specs: `.claude/skills/keep/references/file-formats.md`
- Workflow examples: `.claude/skills/keep/references/workflows.md`
- GitHub templates: `.claude/skills/keep/references/github-templates.md`
- Troubleshooting: `.claude/skills/keep/references/troubleshooting.md`
- Zero-issues workflow: `.claude/skills/keep/references/zero-issues.md`
- GitHub scripts: `.claude/skills/keep/scripts/`
