# Documentation Review Checklist

Use this checklist when reviewing or updating Keep documentation to maintain low duplication and high quality.

## Before Committing Documentation Changes

- [ ] Is this concept explained elsewhere? If yes, reference it instead of repeating
- [ ] Does this duplicate agent/shared content? Extract to `agents/shared/` if it does
- [ ] Are examples necessary or just illustrative? Remove non-essential examples
- [ ] Would this pass the 6-month test for Keep itself? (Would we need this in 6 months?)
- [ ] Can diagrams be simplified or consolidated? Check for redundant patterns
- [ ] Are error examples generic or specific? Remove duplicates across files
- [ ] Does this file reference other files properly? Add explicit links where relevant
- [ ] Is this concise? Could it be 50% shorter while keeping value?

## Duplication Red Flags

Watch for these patterns that indicate duplication:

- **Same concept explained in 2+ files** → Extract to shared file
- **Repeated examples with same pattern** → Keep one canonical example
- **"See also" references without actual deduplication** → Consolidate instead
- **Size limits mentioned multiple times** → Use shared/size-validation.md
- **Error handling explained in each agent** → Use shared/error-handling.md
- **Best practices repeated** → Use shared/principles.md
- **Quality filters explained multiple ways** → Use shared/quality-filters.md
- **Directory structure shown multiple places** → Show once, reference from others

## Consolidation Opportunities (Completed)

✅ **Phase 1: Shared Agent Resources**
- [x] Created `agents/shared/error-handling.md`
- [x] Created `agents/shared/principles.md`
- [x] Created `agents/shared/size-validation.md`
- [x] Created `agents/shared/quality-filters.md`
- [x] Updated all 4 agents to reference shared files
- [x] Removed 800+ lines of duplication from agents

✅ **Phase 2: Template Files**
- [x] Deleted redundant `github-templates.md` (split templates still exist)
- [x] Removed 185 lines

## Consolidation Opportunities (Future - Low Priority)

Consider these for future updates:

- [ ] **file-formats.md examples:** Consolidate repeated explanatory text (~220 lines potential savings)
- [ ] **workflows.md diagrams:** Unify diagram patterns (~320 lines potential savings)
- [ ] **Directory structure:** Keep in README only, reference from ARCHITECTURE.md (~35 lines potential savings)
- [ ] **README examples:** Remove intermediate examples, reference workflows.md (~116 lines potential savings)

## File Ownership Reference

Each concept has a primary location. Other files reference it:

| Concept | Primary Location | How to Reference |
|---------|------------------|------------------|
| Error handling | troubleshooting.md | "See troubleshooting.md for detailed error recovery" |
| Best practices | agents/shared/principles.md | "See agents/shared/principles.md for core principles" |
| 6-month test | agents/shared/quality-filters.md | "See agents/shared/quality-filters.md for quality assessment" |
| Size limits | agents/shared/size-validation.md | "See agents/shared/size-validation.md for size enforcement" |
| Resume detection | agents/start.md | Reference from SKILL.md lightly |
| Workflow examples | workflows.md | "Detailed examples in workflows.md" |
| File formats | file-formats.md | "Load for format details" |
| GitHub templates | templates/*.md | Reference specific template files, not github-templates.md |

## Quality Standards

### What's Worth Documenting

- Non-obvious gotchas that surprise developers
- Security or performance implications
- Architectural decisions with "why" explanations
- Patterns that prevent common mistakes
- Framework/library quirks not in official docs

### What's NOT Worth Documenting

- Implementation details visible in code
- Obvious patterns anyone would use
- Generic best practices from documentation
- File structure (use `ls` instead)
- Standard framework usage
- Tool installation steps

## Agent-Specific Patterns

### Start Agent
- Focus on resume detection and context loading
- Error handling → agents/shared/error-handling.md
- Best practices → agents/shared/principles.md

### Save Agent
- Focus on progress capture and learning extraction
- Quality filtering → agents/shared/quality-filters.md
- Size validation → agents/shared/size-validation.md
- Best practices → agents/shared/principles.md

### Done Agent
- Focus on completion, archiving, and recommendations
- Error handling → agents/shared/error-handling.md
- Best practices → agents/shared/principles.md

### Grow Agent
- Focus on analyzing code and creating/updating CLAUDE.md
- Quality assessment → agents/shared/quality-filters.md
- Size validation → agents/shared/size-validation.md
- Best practices → agents/shared/principles.md

## Reference File Structure

```
skills/keep/references/
├── file-formats.md          # Format specifications (canonical)
├── workflows.md             # Detailed workflow examples
├── troubleshooting.md       # Error recovery patterns
├── zero-issues.md           # Issue discovery patterns
└── templates/
    ├── github-progress.md   # Progress update template
    └── github-completion.md # Completion summary template
```

**Note:** `github-templates.md` was deleted (content duplicated in templates/ directory)

## Size Management Rules

- **Root CLAUDE.md:** 200 lines MAXIMUM
- **Module CLAUDE.md:** 150 lines MAXIMUM
- Warn at 80% capacity
- Require pruning before adding when near limit
- Show size on every update

## Going Forward

1. Use this checklist on every documentation change
2. Reference shared files instead of repeating content
3. Extract common patterns to shared/ directory
4. Keep documentation concise and valuable
5. Apply the 6-month test to all new content

## Metrics

**Before consolidation:**
- Total documentation: ~6,000 lines
- Estimated duplication: 25-30%
- Redundant templates: github-templates.md

**After Phase 1 & 2:**
- Total documentation: ~4,800 lines
- Estimated duplication: <15%
- Lines saved: ~1,200
- Agent file reduction: -43%

**Future opportunities:**
- Additional consolidation could save ~650 more lines
- Total potential reduction: ~1,850 lines (31%)
