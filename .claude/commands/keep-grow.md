---
description: Create or update CLAUDE.md files for project context
---

# Keep: Grow Context

Load the Keep skill to analyze a directory and create/update CLAUDE.md files.

## Task

Invoke the Keep skill by loading `.claude/skills/keep/SKILL.md` to grow project context.

## Target Directory

{{#if args}}
Target directory: {{args}}
{{else}}
No directory specified. The Keep skill should:
1. Default to current working directory
2. Or analyze project root if no work in progress
3. Or prompt user for which directory to analyze
{{/if}}

## Instructions

1. Load the Keep skill
2. Follow the "Creating New CLAUDE.md" workflow from the skill
3. Analyze the target directory for patterns

## Expected Outcome

The Keep skill should:
- Analyze directory contents:
  - Scan file names and types
  - Read key files (exports, interfaces, main modules)
  - Identify patterns and abstractions
  - Detect frameworks/libraries in use
- Assess if CLAUDE.md would be valuable:
  - Is this a cohesive module?
  - Are patterns clear enough to document?
  - Would future work benefit from context?
  - Is it too early? (avoid premature documentation)
- If valuable, generate proposal:
  - Draft complete CLAUDE.md content
  - Include: Purpose, Key Patterns, API, Recent Learnings, Dependencies, Testing
  - Show to user for review
- Present for approval:
  - Show complete proposed content
  - Explain benefit to future work
  - Offer options: yes / edit / later / no
- If approved:
  - Create or update `{directory}/CLAUDE.md`
  - Confirm creation
  - Note that future work will auto-load this context

## Use Cases

**Initial setup on existing project:**
```
/keep-grow .
```
Analyzes project root and suggests creating root CLAUDE.md with tech stack, architecture, conventions.

**Document a module:**
```
/keep-grow src/auth
```
Analyzes `src/auth/` directory and suggests creating `src/auth/CLAUDE.md` with authentication patterns.

**Update existing context:**
```
/keep-grow src/api --update
```
Updates existing `src/api/CLAUDE.md` with new patterns discovered since it was created.

**Catch up on missed suggestions:**
If Keep suggested CLAUDE.md during `/keep-save` but you dismissed it, run `/keep-grow` to regenerate the suggestion.

## Flags

- `--update` - Update existing CLAUDE.md (vs create new)
- `--force` - Create even if patterns unclear (use with caution)

## Guidelines

**When to create CLAUDE.md:**
- Working in a directory for 2nd+ time
- Patterns are emerging that should be documented
- Complex logic that benefits from explanation
- Module has clear boundaries and purpose

**When NOT to create CLAUDE.md:**
- Directory is just a collection of unrelated utilities
- Too early - patterns haven't emerged yet
- Logic is self-explanatory
- Would duplicate information from root CLAUDE.md

The Keep skill will help assess whether CLAUDE.md is valuable or premature.

## Error Handling

If directory doesn't exist:
- Inform user
- Suggest checking path
- Don't fail

If CLAUDE.md already exists and `--update` not specified:
- Show existing content
- Ask if user wants to update or cancel
- Offer to merge or replace

If directory is empty or has no clear patterns:
- Inform user that patterns not clear enough yet
- Suggest waiting until more code exists
- Don't create premature documentation

## Example Output

```
📝 Analyzing src/payments/ ...

Found patterns worth documenting:
• Stripe API integration (5 files)
• Webhook validation pattern
• Idempotency key usage for retries
• Payment record repository pattern

Proposed CLAUDE.md for src/payments/:
─────────────────────────────────────
# Payments Module

## Purpose
Handles payment processing via Stripe API...

[... full proposal ...]
─────────────────────────────────────

This will help future work in src/payments/ by:
- Documenting Stripe patterns and gotchas
- Explaining webhook validation approach
- Noting idempotency requirements

Create src/payments/CLAUDE.md?
[yes / edit / later / no]
```

## Integration with Workflow

`/keep-grow` complements the automatic suggestions:
- **Automatic** (during `/keep-save`) - Keep suggests when threshold met
- **Manual** (via `/keep-grow`) - You trigger when needed

Both use the same intelligence from the Keep skill.
