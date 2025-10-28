# Keep

> Lightweight, intelligent project memory for Claude Code

Keep helps you track work, capture learnings as you code, and grow project context naturally through CLAUDE.md files. Claude detects resumable work at session start and provides workflow hints to help you build a natural cadence.

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

## How Keep Works

**Keep provides session continuity and workflow hints** - Claude detects when you have resumable work at the start of a new conversation, and agents provide helpful next-step hints to teach you the natural rhythm.

You invoke Keep commands manually as you work:
- **Starting work:** Run `/keep:start [issue]` to load context and begin tracking
- **Saving progress:** Run `/keep:save` at natural breakpoints (after features, decisions, or every 30-45 min)
- **Completing tasks:** Run `/keep:done` when tests pass and you're ready to move on
- **Growing context:** Run `/keep:grow [directory]` to document patterns in CLAUDE.md files

Keep integrates into your workflow through helpful hints:
```
You: /keep:start 42
Claude: *loads issue, context, creates tracking file*
        💡 Next steps: As you work, use /keep:save to checkpoint progress
        and capture decisions.

You: *work for 45 minutes, implement feature*

You: /keep:save
Claude: *captures progress and decisions*
        💡 Next steps: Continue working, or use /keep:done when you've
        completed the issue and tests pass.
```

**Session resume detection:** When you start a new conversation with active work from a recent session (< 48h), Claude will suggest resuming where you left off.

## Quick Start

### Installation

#### Option 1: Install from GitHub (Recommended)

```bash
# Add the Keep marketplace
/plugin marketplace add https://github.com/lackeyjb/claude-keep

# Install the plugin
/plugin install keep@keep-marketplace
```

#### Option 2: Install Locally

```bash
# Clone the repository
git clone https://github.com/lackeyjb/claude-keep.git

# Add as local marketplace
/plugin marketplace add ./claude-keep

# Install the plugin
/plugin install keep@keep-marketplace
```

#### Getting Started

1. Ensure you have `gh` CLI installed (optional, for GitHub integration)
2. Keep will automatically create `.claude/` directory structure in your projects when you first use a command
3. Create initial project context:
   ```bash
   /keep:grow .
   ```
   Keep will analyze your project and suggest creating a root CLAUDE.md with tech stack, architecture, and conventions.
4. Start using commands!

### Directory Structure

**In your project** (auto-created by Keep):
```
your-project/
├── CLAUDE.md                    # Root context (create manually or let Keep suggest)
├── src/
│   └── auth/
│       └── CLAUDE.md            # Module context (Keep suggests when patterns emerge)
└── .claude/
    ├── work/                    # Active issue tracking (auto-created)
    ├── archive/                 # Completed issues (auto-created)
    └── state.md                 # Current session state (auto-created)
```

**Plugin structure** (installed via `/plugin install`):
```
keep/
├── .claude-plugin/
│   ├── plugin.json              # Plugin metadata
│   └── marketplace.json         # Marketplace configuration
├── commands/
│   ├── start.md                 # Start work command
│   ├── save.md                  # Save progress command
│   ├── done.md                  # Complete work command
│   └── grow.md                  # Grow context command
├── agents/
│   ├── start.md                 # Start workflow agent
│   ├── save.md                  # Save workflow agent
│   ├── done.md                  # Done workflow agent
│   └── grow.md                  # Grow workflow agent
└── skills/keep/
    ├── SKILL.md                 # Keep skill intelligence
    ├── references/              # File format specs, workflows
    └── scripts/                 # GitHub helpers, scoring algorithm
```

## Commands

### `/keep:start [issue-number]`

Start work on a GitHub issue with full context loading. **Automatically detects and resumes interrupted work.**

```bash
/keep:start 1234
```

**What it does:**
- **Intelligent resume:** Detects if you're resuming previous work on this issue
  - Recent work (< 24h): Instantly resumes with cached data, skips GitHub fetch
  - Moderate (24-48h): Asks whether to resume cached or refetch fresh data
  - Stale (> 48h): Refetches from GitHub to ensure latest status
- Fetches issue from GitHub (when starting fresh or data is stale)
- Loads relevant CLAUDE.md files for context
- Reads recent work from `.claude/state.md` and archive
- Creates/updates `.claude/work/1234.md` tracking file
- Suggests approach based on project patterns

**Proactive resume detection:**
Keep watches for session boundaries. When you start a new conversation and have active work from a recent session (< 48h), Claude will proactively suggest resuming:

```
You: [starts new session]
Claude: "I see you were working on issue #1234 (Add rate limiting) - last updated
        6 hours ago. You had made good progress: middleware 80% complete, 3 decisions
        captured. Want to pick up where you left off?"
```

**Zero-issues workflow:**
When no issue number is provided and no issues exist:
1. **Discover** - Searches planning docs (ROADMAP.md, TODO.md) and code signals (TODO/FIXME comments, missing tests)
2. **Synthesize** - Generates 3-5 actionable issue suggestions with source attribution
3. **Create** - You select which issues to create, Keep generates and posts them to GitHub
4. **Start** - You pick which issue to work on, Keep begins normal workflow

**Flags:**
- `--offline` - Skip GitHub, work locally only

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
- Detects associated PR on current branch
- Posts completion summary to GitHub issue (includes PR link if exists)
- Smart PR-aware issue closing:
  - **PR merged**: Notes issue auto-closed via PR (GitHub auto-closes)
  - **PR open**: Keeps issue open (will auto-close when PR merges)
  - **PR closed (unmerged)**: Asks if you want to close manually
  - **No PR**: Asks about closing issue
- Archives work file to `.claude/archive/`
- Updates session state
- Recommends next work based on continuity + priority

**Flags:**
- `--close` - Close the GitHub issue without asking
- `--no-close` - Leave issue open without asking
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
# Save progress periodically
/keep:save

# Continue working...
# Save again at natural breakpoints
/keep:save

# Complete and sync
/keep:done --close
```

**Keep automatically:**
- Captures decisions and learnings from your saves
- Suggests updating `src/auth/CLAUDE.md` when patterns emerge (3+ decisions in same area)
- Posts comprehensive summary to GitHub issue #1234
- Recommends issue #1250 as next work (builds on #1234, same area)

## Workflow Patterns & User Cadence

### Natural Rhythm

Keep works best when used at natural checkpoints in your workflow:

**Start of work:**
- New session? Claude may suggest resuming recent work
- Starting new issue? Run `/keep:start [issue]`
- Not sure what to work on? Run `/keep:start` for recommendations

**During work (every 30-45 min or at natural breakpoints):**
- Made key decisions? Run `/keep:save`
- Implemented a feature? Run `/keep:save`
- Learning something non-obvious? Run `/keep:save`
- Use `--sync` flag if you want to post update to GitHub

**Completing work:**
- Tests pass and PR up? Run `/keep:done`
- Keep will summarize, recommend next work, and archive
- Use `--close` to auto-close issue, `--no-recommend` to skip suggestions

**Context gaps:**
- Missing docs for a module? Run `/keep:grow [directory]`
- Keep will analyze and propose CLAUDE.md content
- Happens automatically after 3+ decisions in same area via `/keep:save`

### Example Session

```bash
# Morning: Start fresh
/keep:start 1234

# Work for 45 min, implement auth middleware
/keep:save

# Lunch break - checkpoint progress
/keep:save --sync

# Afternoon: finish implementation
# ... more work ...

# Tests pass, PR created
/keep:done --close

# Keep recommends issue #1250 (builds on #1234)
/keep:start 1250
```

### Tips

- **Don't overthink it:** Save when it feels natural, not on a strict schedule
- **Use flags:** `--sync` for GitHub updates, `--no-recommend` to skip suggestions
- **Let patterns emerge:** After 3+ saves in a directory, Keep suggests documentation
- **Offline works:** All commands work without GitHub, just skip sync features

## Features

### Intelligent Learning Capture

When you run `/keep:save`, Keep captures from recent conversation:
- **Decisions** - Technical choices with rationale
- **Learnings** - Gotchas, non-obvious behaviors, surprises
- **Patterns** - Approaches that work well
- **Progress** - What you accomplished

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

### Optimized Context Usage

Keep uses a sub-agent architecture for minimal context consumption:
- **65-80% reduction** in context per command vs traditional approaches
- Each workflow (start/save/done/grow) operates in its own context window
- References loaded on-demand only when needed
- Main skill reduced to 222 lines (from 341)
- No context pollution between workflows

This means:
- Faster command execution
- More room for your actual work
- Reduced token usage
- Better performance on long sessions

See [ARCHITECTURE.md](ARCHITECTURE.md) for technical implementation details.

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

See `skills/keep/references/file-formats.md` for complete specifications.

## Advanced Usage

### Offline Mode

Keep works without GitHub:
```bash
/keep-start --offline
# Provide issue details manually
# Keep tracks locally, can sync later
```

### Custom Scripts

Keep includes helper scripts:

**`github_sync.py`** - GitHub API operations with retry logic:
```bash
python ${CLAUDE_PLUGIN_ROOT}/skills/keep/scripts/github_sync.py fetch-issue 1234
```

**`score_issues.py`** - Score open issues for recommendations:
```bash
gh issue list --json number,title,labels,body,updatedAt | \
  python ${CLAUDE_PLUGIN_ROOT}/skills/keep/scripts/score_issues.py --recent-work .claude/state.md
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

Keep is designed to work with minimal configuration. All intelligence lives in `skills/keep/SKILL.md`.

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

This is a personal project but suggestions welcome! The skill is designed to be customized - edit `skills/keep/SKILL.md` to suit your workflow.

## Learn More

- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md) - Context optimization and sub-agent design
- **Skill documentation:** `skills/keep/SKILL.md` - Core philosophy and principles
- **File format specs:** `skills/keep/references/file-formats.md`
- **Workflow examples:** `skills/keep/references/workflows.md`
- **GitHub templates:** `skills/keep/references/github-templates.md`
- **Troubleshooting:** `skills/keep/references/troubleshooting.md`
- **Zero-issues workflow:** `skills/keep/references/zero-issues.md`
- **GitHub scripts:** `skills/keep/scripts/`
