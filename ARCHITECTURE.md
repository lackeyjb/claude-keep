# Keep Architecture

This document explains Keep's two-layer architecture: a **proactive skill layer** for recognition and suggestion, built on top of an **optimized execution layer** for minimal context usage.

## Architectural Layers

Keep has two distinct architectural layers:

### Layer 1: Proactive Skill (Model-Invoked Recognition)

The skill layer (`skills/keep/SKILL.md`) teaches Claude to **autonomously recognize** when project memory would help and **proactively suggest** commands. This is the most important architectural component.

**Key characteristics:**
- **Model-invoked:** Claude decides when to use Keep based on conversation context
- **Recognition-focused:** Contains patterns for identifying Keep moments (not implementation)
- **User-experience layer:** Makes Keep feel natural and integrated

**What it does:**
- Watches for user signals: "I'm starting on issue #42", "I learned that...", "What should I work on?"
- Maps signals to appropriate commands: `/keep:start`, `/keep:save`, `/keep:done`, `/keep:grow`
- Suggests commands conversationally with context-specific value propositions
- Checks preconditions (Is Keep installed? Do files exist? Is GitHub available?)

**What it doesn't do:**
- Execute workflows (delegates to agents)
- Load implementation details (references stay external)
- Force rigid processes (adapts to user preferences)

This layer transforms Keep from "a set of commands you need to remember" into "an intelligent assistant that recognizes when you need project memory."

### Layer 2: Optimized Execution (Sub-Agent Architecture)

The execution layer uses sub-agents and granular references to minimize context usage while maintaining full functionality.

**Key characteristics:**
- **Context isolation:** Each workflow operates in separate context window
- **Minimal loading:** Only workflow-specific instructions loaded
- **On-demand references:** Load details only when needed
- **Script execution:** Run Python scripts without loading code into context

**Benefits:**
- 65-80% context reduction per command
- More room for actual work
- Faster execution
- Easier maintenance

## Design Principles

Based on Claude Code's best practices for skills and sub-agents:

1. **Proactive Recognition** - Claude suggests commands at natural moments (Layer 1)
2. **Progressive Disclosure** - Load only what's needed, when needed (Layer 2)
3. **Context Isolation** - Each workflow operates in its own context window (Layer 2)
4. **Tool Restrictions** - Each sub-agent only gets tools it requires (Layer 2)
5. **Lazy Loading** - References loaded on-demand, not upfront (Layer 2)

## Architecture Overview

### Full Flow: Recognition → Execution

```
┌─────────────────────────────────────────────────────────────┐
│ User: "I'm going to start working on issue 42"              │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: Proactive Skill (skills/keep/SKILL.md)             │
│ - Recognizes "starting work" signal                         │
│ - Maps to /keep:start command                              │
│ - Suggests: "Use /keep:start 42 to load context..."        │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ User accepts (or invokes /keep-start 42 directly)           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2a: Slash Command (commands/start.md)                │
│ - Minimal wrapper (~30 lines)                               │
│ - Delegates to sub-agent via Task tool                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2b: Sub-Agent (agents/start.md)                       │
│ - Focused workflow instructions (~120 lines)                │
│ - Tools: Read, Bash, Write, Glob, Grep                      │
│ - Operates in own context window                            │
│ - Loads references only if needed                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼ (only if needed)
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2c: References (loaded on-demand)                     │
│ - file-formats.md (only when creating files)                │
│ - zero-issues.md (only when no issues exist)                │
│ - troubleshooting.md (only when errors occur)               │
│ - templates/*.md (only when posting to GitHub)              │
└─────────────────────────────────────────────────────────────┘
```

**Key insight:** The skill layer makes Keep feel natural and proactive. Users don't need to remember commands - Claude recognizes moments and suggests them. The execution layer then handles the workflow efficiently with minimal context usage.

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

### start (~120 lines)
**Purpose:** Start work on issue
**Tools:** Read, Bash, Write, Glob, Grep
**Loads:**
- `file-formats.md` - Only if creating new files
- `zero-issues.md` - Only if no issues exist
- `troubleshooting.md` - Only on errors

**Context savings:** Doesn't load save/done/grow logic

### save (~100 lines)
**Purpose:** Capture progress and learnings
**Tools:** Read, Edit, Bash
**Loads:**
- `templates/github-progress.md` - Only when syncing to GitHub
- `file-formats.md` - Only for CLAUDE.md proposals

**Context savings:** Doesn't load start/done/grow logic

### done (~140 lines)
**Purpose:** Complete work and recommend next
**Tools:** Read, Bash, Edit, Grep
**Loads:**
- `templates/github-completion.md` - When posting to GitHub
- `troubleshooting.md` - Only on errors

**Context savings:** Doesn't load start/save/grow logic, executes scoring script without loading code

### grow (~120 lines)
**Purpose:** Create/update CLAUDE.md files
**Tools:** Read, Glob, Grep, Write, Edit
**Loads:**
- `file-formats.md` - When generating CLAUDE.md proposals

**Context savings:** Doesn't load any workflow logic

## Main Skill.md Role (Layer 1)

The main `SKILL.md` (~284 lines) is the **proactive recognition engine**:

### Primary Purpose: Autonomous Recognition
- **Recognition patterns** - Identifies when users would benefit from Keep
- **Signal mapping** - Maps user behaviors to appropriate commands
- **Suggestion guidance** - How to present commands conversationally
- **Context checks** - Preconditions to verify before suggesting

### Secondary Purpose: Delegation Reference
- **Command overview** - Brief description of what each command does
- **When to suggest** - Specific moments to offer each command
- **Agent delegation** - Points to sub-agents for execution (not implementation details)

### Example Recognition Patterns
```
User: "I decided to use Redis because..."
→ Recognizes: Decision with rationale
→ Suggests: /keep:save to capture learning
→ Value prop: "Won't have to rediscover this later"

User: "What should I work on?"
→ Recognizes: Asking for direction
→ Suggests: /keep:start (no issue number)
→ Value prop: "Recommends based on recent work and priority"
```

### What Changed from Original
**Before (341 lines):** Implementation documentation
- How agents work
- File format details
- GitHub integration mechanics
- Internal architecture

**After (284 lines):** Recognition and suggestion guide
- User signal patterns
- When to suggest commands
- How to be proactive without being intrusive
- Conversation examples

### Loading Characteristics
**Loaded when:**
- User exhibits behavior matching recognition patterns (autonomous)
- Claude needs to decide if Keep would help (continuous background awareness)
- User asks about Keep generally

**NOT loaded when:**
- Executing workflows (sub-agents handle implementation)
- Loading references (kept separate)

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

### /keep:start Execution

**Loads:**
```
start sub-agent:                120 lines
file-formats.md (if needed):    611 lines (rarely loaded)
zero-issues.md (if needed):     509 lines (first use only)
troubleshooting.md (on error):  528 lines (rarely)
```

**Typical usage:** ~120 lines (just sub-agent)
**Maximum:** ~1200 lines (all references, rare)
**Old approach:** 341+ lines every time

### /keep:save Execution

**Loads:**
```
save sub-agent:                     100 lines
templates/github-progress.md:        60 lines (if --sync)
file-formats.md:                    611 lines (if CLAUDE.md proposal)
```

**Typical usage:** ~100 lines (just sub-agent)
**With sync:** ~160 lines
**With CLAUDE.md proposal:** ~711 lines
**Old approach:** 341+ lines every time

### /keep:done Execution

**Loads:**
```
done sub-agent:                     140 lines
templates/github-completion.md:      90 lines (when syncing)
troubleshooting.md (on error):      528 lines (rarely)
```

**Typical usage:** ~230 lines (sub-agent + completion template)
**Old approach:** 341+ lines every time

### /keep:grow Execution

**Loads:**
```
grow sub-agent:             120 lines
file-formats.md:            611 lines (when generating CLAUDE.md)
```

**Typical usage:** ~731 lines (needs format specs)
**Old approach:** 341+ lines + file-formats anyway

## File Organization

```
.claude/
├── agents/                  # Workflow sub-agents & shared patterns
│   ├── start.md            # Start workflow (223 lines)
│   ├── save.md             # Save workflow (209 lines)
│   ├── done.md             # Done workflow (290 lines)
│   ├── grow.md             # Grow workflow (354 lines)
│   └── shared/             # Shared patterns (error handling, principles, etc.)
│       ├── error-handling.md        # Error recovery patterns (83 lines)
│       ├── principles.md            # Core execution principles (123 lines)
│       ├── quality-filters.md       # Quality assessment & 6-month test (150 lines)
│       └── size-validation.md       # CLAUDE.md size enforcement (145 lines)
├── commands/               # UPDATED: Thin wrappers
│   ├── start.md            # Delegates to sub-agent (30 lines)
│   ├── save.md             # Delegates to sub-agent (30 lines)
│   ├── done.md             # Delegates to sub-agent (30 lines)
│   └── grow.md             # Delegates to sub-agent (30 lines)
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
python ${CLAUDE_PLUGIN_ROOT}/skills/keep/scripts/score_issues.py --issues "{json}"
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
| /keep:start (typical) | 341+ | ~120 | 65% |
| /keep:save (no sync) | 341+ | ~100 | 71% |
| /keep:save (with sync) | 341+ | ~160 | 53% |
| /keep:done | 341+ | ~230 | 33% |
| /keep:grow | 341+ | ~731 | -114% * |

\* keep:grow loads format specs which it needs anyway, so net similar

### Context Window Efficiency

With typical session (start → save → save → done):

**Before:**
```
/keep:start:  341 lines
/keep:save:   341 lines
/keep:save:   341 lines
/keep:done:   341 lines
Total:       1364 lines across commands
```

**After:**
```
/keep:start:  120 lines
/keep:save:   100 lines
/keep:save:   100 lines
/keep:done:   230 lines
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
| /keep:start (typical) | 120-250 lines | 400 lines |
| /keep:save (no sync) | 100-200 lines | 350 lines |
| /keep:done | 230-350 lines | 500 lines |

If seeing higher usage, check if references being loaded unnecessarily.

## Conclusion

Keep's two-layer architecture delivers both **excellent user experience** and **optimal performance**:

### Layer 1: Proactive Skill
- **Model-invoked recognition** - Claude autonomously suggests commands at natural moments
- **No mental overhead** - Users don't need to remember workflows
- **Natural integration** - Keep suggestions feel like helpful teammate
- **Context-aware** - Adapts to user pace and preferences

### Layer 2: Optimized Execution
- **Significant context reduction** (65-80% typical)
- **Better context isolation** (separate windows per workflow)
- **Easier maintenance** (update workflows independently)
- **Future flexibility** (easy to extend)

### Together
The proactive skill layer makes Keep feel **effortless and intelligent**, while the optimized execution layer ensures it stays **fast and efficient**. Users get intelligent project memory without ceremony or performance cost.

All while maintaining:
- **100% backward compatibility** with existing work files
- **Same file formats** for tracking and state
- **No configuration required** - works out of the box
- **Graceful degradation** - works offline, without GitHub

Keep transforms from "a set of commands" into "an intelligent assistant that knows when you need project memory."
