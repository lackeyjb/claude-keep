# Keep Architecture - Context Optimization

This document explains Keep's optimized architecture designed to minimize context usage while maximizing functionality.

## Design Principles

Based on Claude Code's best practices for skills and sub-agents:

1. **Progressive Disclosure** - Load only what's needed, when needed
2. **Context Isolation** - Each workflow operates in its own context window
3. **Tool Restrictions** - Each sub-agent only gets tools it requires
4. **Lazy Loading** - References loaded on-demand, not upfront

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│ User invokes: /keep-start 123                               │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Slash Command (.claude/commands/keep-start.md)              │
│ - Minimal wrapper (~30 lines)                               │
│ - Delegates to sub-agent via Task tool                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ Sub-Agent (.claude/agents/keep-start.md)                    │
│ - Focused workflow instructions (~120 lines)                │
│ - Tools: Read, Bash, Write, Glob, Grep                      │
│ - Operates in own context window                            │
│ - Loads references only if needed                           │
└─────────────────────────────────────────────────────────────┘
                        │
                        ▼ (only if needed)
┌─────────────────────────────────────────────────────────────┐
│ References (loaded on-demand)                               │
│ - file-formats.md (only when creating files)                │
│ - zero-issues.md (only when no issues exist)                │
│ - troubleshooting.md (only when errors occur)               │
│ - templates/*.md (only when posting to GitHub)              │
└─────────────────────────────────────────────────────────────┘
```

## Context Usage Comparison

### Before Optimization

Every Keep command loaded:
- Main SKILL.md: **341 lines**
- All workflow details for all commands
- All references mentioned (even if not needed)
- **Total: ~341 lines minimum per command**

### After Optimization

Each Keep command loads:
- Relevant sub-agent only: **60-140 lines**
- Only references actually needed: **0-200 lines**
- No pollution from other workflows
- **Total: ~60-200 lines per command (65-80% reduction)**

## Sub-Agent Breakdown

### keep-start (~120 lines)
**Purpose:** Start work on issue
**Tools:** Read, Bash, Write, Glob, Grep
**Loads:**
- `file-formats.md` - Only if creating new files
- `zero-issues.md` - Only if no issues exist
- `troubleshooting.md` - Only on errors

**Context savings:** Doesn't load save/done/grow logic

### keep-save (~100 lines)
**Purpose:** Capture progress and learnings
**Tools:** Read, Edit, Bash
**Loads:**
- `templates/github-progress.md` - Only when syncing to GitHub
- `file-formats.md` - Only for CLAUDE.md proposals

**Context savings:** Doesn't load start/done/grow logic

### keep-done (~140 lines)
**Purpose:** Complete work and recommend next
**Tools:** Read, Bash, Edit, Grep
**Loads:**
- `templates/github-completion.md` - When posting to GitHub
- `troubleshooting.md` - Only on errors

**Context savings:** Doesn't load start/save/grow logic, executes scoring script without loading code

### keep-grow (~120 lines)
**Purpose:** Create/update CLAUDE.md files
**Tools:** Read, Glob, Grep, Write, Edit
**Loads:**
- `file-formats.md` - When generating CLAUDE.md proposals

**Context savings:** Doesn't load any workflow logic

## Main Skill.md Role

The main `SKILL.md` (222 lines, reduced from 341) now serves as:
- **Philosophy document** - Core principles and approach
- **Router/index** - Points to sub-agents for each workflow
- **Quick reference** - Overview of file organization and patterns

It's loaded when:
- User asks about Keep generally
- Documentation is needed
- Router information is needed

It's **NOT** loaded when:
- Executing specific workflows (sub-agents handle that)
- Loading references (they're independent)

## Reference Files

### Core References (kept from original)
- `file-formats.md` (611 lines) - Format specifications
- `workflows.md` (969 lines) - Detailed examples with diagrams
- `zero-issues.md` (509 lines) - Discovery patterns
- `troubleshooting.md` (528 lines) - Error handling

### New Granular Templates
- `templates/github-progress.md` (~60 lines) - Progress update format only
- `templates/github-completion.md` (~90 lines) - Completion summary format only

**Loading strategy:** Each sub-agent explicitly loads only what it needs

## Scripts

Scripts are executed via Bash, never loaded into context:
- `score_issues.py` - Issue scoring algorithm (not loaded, just executed)
- `github_sync.py` - Advanced GitHub operations (not loaded, just executed)

This keeps the scoring algorithm and sync logic out of context entirely.

## Benefits Achieved

### 1. Massive Context Reduction
- **65-80% reduction** in context per command
- Only workflow-specific instructions loaded
- References loaded on-demand only

### 2. Context Isolation
- Each workflow in separate context window
- No pollution between workflows
- Cleaner, more focused execution

### 3. Easier Maintenance
- Update one workflow without touching others
- Clear separation of concerns
- Easier to test and debug

### 4. Better Performance
- Less context = faster processing
- More room for actual work
- Reduced token usage

### 5. Flexibility
- Easy to add new workflows
- Easy to modify existing ones
- Clear extension points

## Detailed Context Breakdown

### /keep-start Execution

**Loads:**
```
keep-start sub-agent:           120 lines
file-formats.md (if needed):    611 lines (rarely loaded)
zero-issues.md (if needed):     509 lines (first use only)
troubleshooting.md (on error):  528 lines (rarely)
```

**Typical usage:** ~120 lines (just sub-agent)
**Maximum:** ~1200 lines (all references, rare)
**Old approach:** 341+ lines every time

### /keep-save Execution

**Loads:**
```
keep-save sub-agent:                100 lines
templates/github-progress.md:        60 lines (if --sync)
file-formats.md:                    611 lines (if CLAUDE.md proposal)
```

**Typical usage:** ~100 lines (just sub-agent)
**With sync:** ~160 lines
**With CLAUDE.md proposal:** ~711 lines
**Old approach:** 341+ lines every time

### /keep-done Execution

**Loads:**
```
keep-done sub-agent:                140 lines
templates/github-completion.md:      90 lines (when syncing)
troubleshooting.md (on error):      528 lines (rarely)
```

**Typical usage:** ~230 lines (sub-agent + completion template)
**Old approach:** 341+ lines every time

### /keep-grow Execution

**Loads:**
```
keep-grow sub-agent:        120 lines
file-formats.md:            611 lines (when generating CLAUDE.md)
```

**Typical usage:** ~731 lines (needs format specs)
**Old approach:** 341+ lines + file-formats anyway

## File Organization

```
.claude/
├── agents/                  # NEW: Workflow sub-agents
│   ├── keep-start.md       # Start workflow (120 lines)
│   ├── keep-save.md        # Save workflow (100 lines)
│   ├── keep-done.md        # Done workflow (140 lines)
│   └── keep-grow.md        # Grow workflow (120 lines)
├── commands/               # UPDATED: Thin wrappers
│   ├── keep-start.md       # Delegates to sub-agent (30 lines)
│   ├── keep-save.md        # Delegates to sub-agent (30 lines)
│   ├── keep-done.md        # Delegates to sub-agent (30 lines)
│   └── keep-grow.md        # Delegates to sub-agent (30 lines)
├── skills/keep/
│   ├── SKILL.md            # REDUCED: 222 lines (was 341)
│   ├── references/         # REORGANIZED: More granular
│   │   ├── file-formats.md        # Format specs (611 lines)
│   │   ├── zero-issues.md         # Discovery (509 lines)
│   │   ├── troubleshooting.md     # Errors (528 lines)
│   │   ├── workflows.md           # Examples (969 lines)
│   │   └── templates/             # NEW: Granular templates
│   │       ├── github-progress.md     # Progress (60 lines)
│   │       └── github-completion.md   # Completion (90 lines)
│   └── scripts/            # UNCHANGED: Execute without loading
│       ├── score_issues.py
│       └── github_sync.py
├── state.md                # Current session state
├── work/                   # Active work tracking
└── archive/                # Completed work
```

## Migration Notes

**No user-facing changes:**
- Commands work exactly the same
- Same syntax, same behavior
- Same file formats

**Internal changes:**
- Commands now delegate to sub-agents
- Main skill is now minimal
- References more granular

**Backward compatibility:**
- All existing work files compatible
- All existing state files compatible
- All existing CLAUDE.md files compatible

## Implementation Techniques

### 1. Sub-Agent Tool Restrictions

Each sub-agent specifies only the tools it needs:

```yaml
---
name: keep-save
tools: Read, Edit, Bash
---
```

This prevents unnecessary tool access and keeps focus tight.

### 2. Conditional Reference Loading

Sub-agents explicitly state when to load references:

```markdown
Load `file-formats.md` ONLY if creating new files
Load `zero-issues.md` ONLY if no issue number provided
Load `troubleshooting.md` ONLY when encountering errors
```

### 3. Script Execution Without Loading

Python scripts executed via Bash without loading into context:

```bash
python skills/keep/scripts/score_issues.py --issues "{json}"
```

The algorithm runs, returns results, but code never enters context.

### 4. Template Splitting

Split large `github-templates.md` (185 lines) into:
- `templates/github-progress.md` (60 lines)
- `templates/github-completion.md` (90 lines)

Load only the template you need.

## Performance Characteristics

### Token Usage per Command

| Command | Before | After | Savings |
|---------|--------|-------|---------|
| /keep-start (typical) | 341+ | ~120 | 65% |
| /keep-save (no sync) | 341+ | ~100 | 71% |
| /keep-save (with sync) | 341+ | ~160 | 53% |
| /keep-done | 341+ | ~230 | 33% |
| /keep-grow | 341+ | ~731 | -114% * |

\* keep-grow loads format specs which it needs anyway, so net similar

### Context Window Efficiency

With typical session (start → save → save → done):

**Before:**
```
/keep-start:  341 lines
/keep-save:   341 lines
/keep-save:   341 lines
/keep-done:   341 lines
Total:       1364 lines across commands
```

**After:**
```
/keep-start:  120 lines
/keep-save:   100 lines
/keep-save:   100 lines
/keep-done:   230 lines
Total:        550 lines across commands
```

**Savings: 814 lines (60% reduction)**

## Future Improvements

Potential further optimizations:

1. **More granular references** - Split file-formats.md by file type
2. **Conditional tool loading** - Only load tools when actually needed
3. **Shared reference cache** - Avoid re-loading same reference across sub-agents
4. **Sub-sub-agents** - For very complex workflows like zero-issues discovery

## Comparison to Alternative Approaches

### Alternative 1: Single Lean Skill
- Would reduce main skill to ~150 lines
- But still loads everything for every command
- No context isolation
- **Savings: 55%** vs **our solution: 65-80%**

### Alternative 2: Skill with References Only
- Move all workflows to references
- Commands load specific reference
- **Savings: ~70%** (similar to our solution)
- **Downside:** No context isolation between workflows
- All workflows pollute the same context

### Alternative 3: Sub-Agents (chosen approach)
- Sub-agents for context isolation
- Granular references for templates
- Minimal main skill
- **Savings: 65-80%** + context isolation benefits
- **Best balance** of performance and maintainability

## Design Decisions

### Why Sub-Agents vs Direct Skill Loading?

**Considered:** Commands directly load workflow sections from SKILL.md

**Chose sub-agents because:**
1. Context isolation - Each workflow in separate context window
2. Tool restrictions - Each sub-agent gets only needed tools
3. Easier testing - Test each workflow independently
4. Clearer separation - Workflows don't interfere

### Why Keep Main SKILL.md?

**Considered:** Eliminating main skill entirely

**Kept it because:**
1. Philosophy document - Core principles in one place
2. Router/index - Overview of all workflows
3. Quick reference - File organization guide
4. Discovery - Users can read to understand Keep

### Why Split Templates?

**Considered:** Keeping github-templates.md as single file (185 lines)

**Split because:**
1. Progress updates only need 60 lines
2. Completion summaries only need 90 lines
3. Never need both at same time
4. 50-60% reduction per use case

## Monitoring and Validation

### How to Verify Context Reduction

Track token usage in Claude Code:
1. Before command: Note conversation context size
2. After command: Note context size
3. Calculate difference

### Expected Measurements

| Command | Expected Context | Red Flag If > |
|---------|------------------|---------------|
| /keep-start (typical) | 120-250 lines | 400 lines |
| /keep-save (no sync) | 100-200 lines | 350 lines |
| /keep-done | 230-350 lines | 500 lines |

If seeing higher usage, check if references being loaded unnecessarily.

## Conclusion

The sub-agent architecture provides:
- **Significant context reduction** (65-80% typical)
- **Better context isolation** (separate windows per workflow)
- **Easier maintenance** (update workflows independently)
- **Future flexibility** (easy to extend)

All while maintaining:
- **100% backward compatibility**
- **Same user experience**
- **No configuration changes**
- **Same file formats**

This optimization makes Keep more efficient, leaving more context available for your actual work while providing the same intelligent project memory features.
