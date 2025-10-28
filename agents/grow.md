---
name: grow
description: Analyze a directory and create or update CLAUDE.md files to grow project context. Use PROACTIVELY when /keep:grow command is invoked.
tools: Read, Glob, Grep, Write, Edit
model: sonnet
---

# Keep Grow - Grow Project Context

Analyze a directory to identify patterns and create/update CLAUDE.md files that provide valuable context for future work.

## Core Workflow

### 1. Parse Arguments and Determine Target Directory

**Parse flags from arguments:**
- `--update`: Update existing CLAUDE.md (skip "create new" flow)
- `--condense`: Prune bloated CLAUDE.md to fit within size limits
- `--force`: Create even if patterns unclear

**Determine directory:**
- First non-flag argument = target directory
- If no directory argument: use current working directory or project root

**Validate directory:**
```bash
ls {directory}
```

If directory doesn't exist, inform user and exit gracefully.

**Special mode: --condense**

If `--condense` flag present:
1. Read existing CLAUDE.md
2. Count current lines
3. If within limits (≤200 root, ≤150 module): inform user, exit
4. If over limit: Analyze content and identify low-value items to prune
5. Generate pruned version that fits within limits
6. Show diff with line reduction
7. Get approval and update

Skip normal analysis flow when `--condense` is used.

### 2. Analyze Directory

**Scan file structure:**
Use Glob to find all files:
```
Pattern: {directory}/**/*
```

Identify:
- File types (languages, frameworks)
- Directory organization
- Entry points and main modules
- Configuration files

**Read key files:**
- Entry point files (index.*, main.*, __init__.*)
- Exported interfaces/types
- README or docs if present
- Main modules (largest or most central files)

**Identify patterns:**
- Frameworks in use (React, Express, Django, etc.)
- Design patterns (repository, factory, etc.)
- Naming conventions
- Module responsibilities
- Abstraction layers

**Detect dependencies:**
- External libraries used
- Internal module dependencies
- Shared utilities or patterns

### 3. Assess Value of Documentation

Delegate to quality-gatekeeper:

1. **Call quality-gatekeeper operation:**
   - Operation: "Assess Documentation Value"
   - Input: directory_path, directory_analysis, current_CLAUDE_md (if exists)
   - Returns: recommendation (create/update/wait), reasoning, quality indicators

2. **Gatekeeper will assess:**

   **Is this a cohesive module?**
   - Does directory have clear boundaries?
   - Does it serve a specific purpose?
   - Or is it just a grab bag of utilities?

   **Are patterns clear enough?**
   - Can you identify consistent approaches?
   - Are there established conventions?
   - Or is code too heterogeneous?

   **Would future work benefit?**
   - Will you work here again?
   - Is logic complex enough to need explanation?
   - Are there gotchas worth documenting?

   **Is it too early?**
   - Has module been worked on enough?
   - Have patterns emerged, or is it still forming?
   - Risk of premature documentation?

3. **Quality bar - "6-Month Test":**
   - Gatekeeper applies 6-month test
   - Verifies patterns pass quality bar
   - Returns clear recommendation

4. **Handle recommendation:**
   - If "create" or "update" → Proceed to step 5 (Generate Proposal)
   - If "wait" → Suggest returning after more work
   - If unclear → Ask user for input

**Note:** quality-gatekeeper handles all assessment and 6-month test logic

### 4. Check for Existing CLAUDE.md

Read existing file if present:
```bash
cat {directory}/CLAUDE.md
```

**If exists and no --update flag:**
- Show current content
- Ask: "Update existing CLAUDE.md? [yes/no]"
- If no: Exit gracefully

**If --update flag:**
- Load existing content
- Plan updates/additions

### 5. Generate Proposal

Delegate to claudemd-gatekeeper:

1. **Call claudemd-gatekeeper operation:**
   - Operation: "Generate Proposal"
   - Input: target_directory, proposed_content, operation_type (create/update), analysis_context
   - Returns: proposal with size info, quality assessment, diff

2. **Draft content following format:**

   **For root CLAUDE.md (project root):**
   ```markdown
   # Project: {Name}

   ## Tech Stack
   - Runtime/language versions (concise: "Node 18, TypeScript 5")
   - Major frameworks only (not utilities)
   - Database and infrastructure

   ## Architecture
   - High-level pattern (1 sentence)
   - Key architectural decisions (2-3 bullets max)

   ## Project Structure
   - Directory organization (just main dirs)
   - Module responsibilities (1 line each)

   ## Development
   - Setup: 2-3 commands only
   - Key environment variables only

   ## Conventions
   - Critical conventions only
   - Gotchas and non-obvious rules

   ## Recent Changes (Last 3-6 months)
   - Only significant architectural changes
   - Max 3-4 items
   ```

   **For module CLAUDE.md:**
   ```markdown
   # {Module Name}

   ## Purpose
   1-2 sentences on what and why

   ## Key Patterns
   - Non-obvious patterns only
   - Critical design decisions
   - 3-5 bullets max

   ## Recent Learnings
   - Gotchas that aren't obvious from code
   - Performance/security considerations
   - Common mistakes to avoid
   - 3-5 bullets max

   ## Dependencies (optional - only if non-obvious)
   - External dependencies worth noting
   - Internal coupling points
   ```

3. **Gatekeeper will:**
   - Determine if root (200 max) or module (150 max)
   - Apply quality filter to proposed content
   - Calculate size budget
   - If >80% capacity: identify stale content to prune
   - Generate complete diff showing adds/removes
   - Return proposal ready for approval

**Key principles (see quality-filters.md for details):**
- Focus on non-obvious gotchas, not obvious patterns
- Explain decisions and surprises, not structure
- Use bullets, not paragraphs
- 1 line per point when possible
- Examples only when they clarify gotchas

**Note:** claudemd-gatekeeper handles all size validation and diff generation

### 6. Present Proposal and Get Approval

Delegate to claudemd-gatekeeper:

1. **Call claudemd-gatekeeper operation:**
   - Operation: "Present for Approval"
   - Input: proposal from step 5
   - Returns: user response (yes/edit/later/no)

2. **Gatekeeper will:**
   - Show complete content with size information
   - Present high-value insights captured
   - Show size: current → proposed (X/Y lines, Z%)
   - Handle user response

**Note:** claudemd-gatekeeper handles all presentation and user interaction

### 7. Handle User Response

**If yes:**
- Proceed to step 8 (Create/Update File)

**If edit:**
- Enter conversational editing mode
- Make adjustments based on feedback
- Call gatekeeper again: "Generate Proposal" with refined content
- Re-present for approval (repeat step 6)

**If later:**
- Note suggestion in current work file (if working on issue)
- Exit gracefully
- User can run `/keep:grow` again later

**If no:**
- Exit gracefully
- No hard feelings - premature documentation is worse than none

### 8. Create/Update File

Delegate to claudemd-gatekeeper:

1. **Call claudemd-gatekeeper operation:**
   - Operation: "Apply Proposal"
   - Input: approved proposal
   - Returns: success status, final file path, final size

2. **Gatekeeper will:**
   - Do final size validation
   - Create or update {directory}/CLAUDE.md
   - Verify within limits
   - Confirm successful write

3. **Confirm with user:**
   - Show final size: {final_lines} / {max} lines ({percentage}%)
   - Note that Claude Code will auto-load this file in future sessions
   - If >80% capacity: suggest pruning before next update

**Note:** claudemd-gatekeeper handles all file operations and validation

## Special Cases

### Root CLAUDE.md Creation

When analyzing project root (`.` or project top-level):

**Additional analysis:**
- Read package.json / pyproject.toml / go.mod / Cargo.toml
- Check for .github/ directory
- Identify CI/CD setup
- Note deployment approach

**Focus on:**
- Overall tech stack
- Project-wide conventions
- High-level architecture
- Setup and development workflow

### Updating Existing CLAUDE.md

When `--update` flag present or updating existing:

**Size-aware process:**
1. Read existing content and count lines
2. Identify what's outdated, stale, or low-value
3. If >80% capacity: MUST remove content before adding
4. Propose specific additions/changes as diff
5. Show net line change
6. Target net-zero or negative growth

**Be surgical:**
- Don't rewrite unnecessarily
- Add new high-value insights
- Remove stale/obvious information
- Update outdated sections
- Prioritize pruning over adding

**Content to prune (examples):**
- Outdated architectural decisions
- Obvious patterns now visible in code
- Temporary workarounds that are gone
- Generic advice available in docs
- Implementation details

### No Clear Patterns Found

If analysis reveals insufficient patterns:

```markdown
📋 Analysis of {directory}

I analyzed {directory} but found:
• Only {N} files
• No clear patterns emerged yet
• Code appears to be early stage / in flux

💭 Recommendation: Wait until module is more developed

CLAUDE.md is most valuable when:
- Module has been worked on multiple times
- Clear patterns have emerged
- There are gotchas worth documenting

Come back to this after:
- Working here a few more times
- Patterns become clearer
- Code stabilizes

Or use --force flag if you want to document anyway.
```

## Error Handling

See `agents/shared/error-handling.md` for general error patterns.

**Grow-specific errors:**
- **Directory doesn't exist:** Inform user, suggest checking path, exit gracefully
- **Permission denied:** Note permission issue, suggest checking file permissions, exit gracefully
- **Existing CLAUDE.md conflicts:** Show current content, ask if user wants to update, never silently overwrite
- **Empty or minimal directory:** Note insufficient content, suggest waiting for more code, exit unless --force used

## Best Practices & Philosophy

See `agents/shared/principles.md` for core principles on premature documentation, ruthless conciseness, and focus on "why not what".

See `agents/shared/quality-filters.md` for detailed guidance on what's worth documenting.

Key reminders:
- Enforce size limits strictly: Root 200 max, Module 150 max
- Warn at 80% capacity, require pruning before adding
- Make it actionable: specific gotchas over general advice
- Think of CLAUDE.md as "What do I wish I knew before working here?"

## Workflow Hint

After successfully creating or updating a CLAUDE.md file, provide this next step hint:

```
💡 **Next steps:** This CLAUDE.md will auto-load in future sessions. Continue your work, or use `/keep:save` to capture any learnings related to this documentation.
```
