---
description: Create or update CLAUDE.md files for project context. Use --update to update existing, --condense to prune bloated files.
---

# Keep: Grow Context

Orchestrate context documentation by coordinating gatekeepers and the grow sub-agent.

## Target Directory & Flags

{{#if args}}
Arguments: {{args}}

Parse flags from args:
- --update: Update existing CLAUDE.md
- --condense: Prune bloated CLAUDE.md to fit size limits
- --force: Create even if patterns unclear

Target directory: First non-flag argument (or current directory if none)
{{else}}
No directory specified. Will default to current working directory or project root.
{{/if}}

## Pre-Flight Checks

1. **Verify target directory exists**
   - Extract directory from arguments (first non-flag argument)
   - If directory doesn't exist: inform user, suggest valid directory

2. **Verify it's a valid project directory**
   - Check for code files or subdirectories
   - Warn if directory appears empty

3. **Check if CLAUDE.md already exists**
   - If exists and --update flag not provided: warn user they may want to use --update
   - If exists and over size limits: suggest using --condense flag

## Workflow Orchestration

### Step 1: Analyze Directory

**Call grow sub-agent to analyze directory:**

Use Task tool with sub-agent `grow`:
- **Input:** target_directory, flags (--update, --condense, --force)
- **Task:** Analyze directory structure and identify patterns

**Sub-agent will:**
1. Parse flags and validate directory
2. Handle special --condense mode (prune existing CLAUDE.md)
3. Scan file structure and identify patterns
4. Read key files and detect dependencies
5. Return: directory_analysis, patterns_found, existing_content (if --update)

### Step 2: Assess Documentation Value

**Call quality-gatekeeper to determine if documentation is warranted:**

Use Task tool with sub-agent `quality-gatekeeper`:
- **Operation:** "Assess Documentation Value"
- **Input:** directory_path, directory_analysis, current_CLAUDE_md (if exists)
- **Returns:** recommendation (create/update/wait), reasoning, quality_indicators

**Gatekeeper will assess:**
- Is this a cohesive module with clear boundaries?
- Are patterns clear enough to document?
- Would future work benefit from documentation?
- Is it too early (patterns haven't emerged)?
- Apply 6-month test for quality bar

**Handle recommendation:**
- If "create" or "update": Continue to Step 3
- If "wait": Suggest returning after more work, exit workflow
- If unclear: Ask user for input

### Step 3: Generate CLAUDE.md Proposal

**Call claudemd-gatekeeper to generate proposal:**

Use Task tool with sub-agent `claudemd-gatekeeper`:
- **Operation:** "Generate Proposal"
- **Input:** target_directory, proposed_content, operation_type (create/update), analysis_context
- **Returns:** proposal with size info, quality assessment, diff

**Gatekeeper will:**
- Determine size limits (root: 200 lines, module: 150 lines)
- Read existing CLAUDE.md if exists, count lines
- Apply quality filter to proposed content
- Calculate size budget
- If >80% capacity: identify stale content to prune
- Generate complete diff showing adds/removes
- Return validated proposal

### Step 4: Present Proposal for Approval

**Call claudemd-gatekeeper to present proposal:**

Use Task tool with sub-agent `claudemd-gatekeeper`:
- **Operation:** "Present for Approval"
- **Input:** proposal from Step 3
- **Returns:** user_response (yes/edit/later/no)

**Gatekeeper will:**
- Show complete content with size information
- Present high-value insights captured
- Show size: current → proposed (X/Y lines, Z%)
- Handle user response

**Handle user response:**
- **If yes:** Continue to Step 5 (Apply Proposal)
- **If edit:** Enter conversational editing, regenerate proposal, re-present
- **If later:** Note suggestion, exit gracefully
- **If no:** Exit gracefully (premature documentation is worse than none)

### Step 5: Apply Proposal

**Call claudemd-gatekeeper to write file:**

Use Task tool with sub-agent `claudemd-gatekeeper`:
- **Operation:** "Apply Proposal"
- **Input:** approved_proposal
- **Returns:** success status, final_file_path, final_size

**Gatekeeper will:**
- Do final size validation
- Create or update {directory}/CLAUDE.md
- Verify within limits
- Confirm successful write

### Step 6: Confirm Creation

Present confirmation to user:
```markdown
✅ CLAUDE.md {{#if update}}updated{{else}}created{{/if}} at {path}

📊 Size: {lines} / {max} lines ({percentage}%)
{{#if over_80}}⚠️  Over 80% capacity - suggest pruning before next update{{/if}}

💡 This file will auto-load in future sessions.
```

**Workflow hint:**
```
💡 **Next steps:** This CLAUDE.md will auto-load in future sessions. Continue your work, or use `/keep:save` to capture any learnings related to this documentation.
```

## Error Handling

- **Directory doesn't exist:** Inform user, suggest checking path
- **Permission denied:** Note permission issue, suggest checking file permissions
- **Empty directory:** Note insufficient content, suggest waiting for more code (unless --force)
- **Existing CLAUDE.md conflicts:** Show current content, ask if user wants to update
- **No clear patterns:** Suggest waiting until module is more developed

## Architecture

This command orchestrates three sub-agents:
1. **grow** - Directory analysis and pattern detection
2. **quality-gatekeeper** - Documentation value assessment
3. **claudemd-gatekeeper** - Proposal generation, presentation, and file writing

Each operates in its own context window with focused tools.
