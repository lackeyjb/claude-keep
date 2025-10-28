# CLAUDE.md Size Validation

Size limits and enforcement for CLAUDE.md files.

## Size Limits

- **Root CLAUDE.md:** 200 line maximum (warn at 160 lines)
- **Module CLAUDE.md:** 150 line maximum (warn at 120 lines)

## Validation Process

### Step 1: Count Current Lines

1. Read existing CLAUDE.md (if exists)
2. Count current lines (exclude blank lines from count)
3. Determine size budget remaining

### Step 2: Determine Available Space

```
Root: 200 line maximum
Module: 150 line maximum

Warning threshold: 80% of maximum
Hard limit: 100% of maximum
```

### Step 3: Budget Calculation for Updates

When updating existing CLAUDE.md:

1. Count current lines
2. If >80% capacity:
   - MUST identify stale or low-value content to prune
   - Plan removals BEFORE additions
   - Target net-zero or negative line growth
3. Calculate available space for additions

### Step 4: Proposal Size Check

1. Count lines in proposed addition
2. If updating:
   - Current lines + proposed lines = total
   - If total > maximum: require pruning first
3. Show size before/after for user approval

### Step 5: Hard Enforcement

**Non-negotiable:**
- Never create CLAUDE.md >200 lines (root) or >150 lines (module)
- If proposal exceeds limit: ask user to trim further
- Only write file if within limits

## Presentation Format

### For New Files

```markdown
📝 Proposed CLAUDE.md for {directory}

Proposed content ({X} lines, target: {target}):
─────────────────────────────────
{show full content}
─────────────────────────────────

Create {directory}/CLAUDE.md?
[yes / edit / later / no]
```

### For Updating Existing

```markdown
💡 Suggestion: Update {path}/CLAUDE.md with {pattern-name}?

Current size: {current} / {max} lines ({percentage}%)

{If >80% capacity:}
To maintain conciseness, I'm suggesting both additions and removals:

Proposed changes (net {+/-X} lines → {final} lines):
─────────────────────────────────
{show complete diff with adds/removes}
─────────────────────────────────

{If <80% capacity:}
Proposed addition ({+X} lines):
─────────────────────────────────
{show proposed content}
─────────────────────────────────

Add this to {path}/CLAUDE.md?
[yes / edit / later / no]
```

### Size Warnings

- **At 80% capacity:** "⚠️  Approaching size limit - consider pruning on next update"
- **At/Over limit:** "❌ Would exceed size limit - pruned to fit within {max} lines"

## Final Validation

Before writing any changes:

1. Count lines in final approved content
2. Verify ≤200 (root) or ≤150 (module)
3. If over: ask user to trim further
4. Only write if within limits

## Confirmation

After successful write:

```markdown
✅ {Created|Updated} {directory}/CLAUDE.md ({final_lines} / {max} lines, {percentage}%)

{If >80% capacity:}
💡 File is {percentage}% of max size - consider pruning old content before adding more.
```

## Size Management Strategy

### When Creating
- Target 120-150 lines for root
- Target 80-100 lines for modules
- Leave room for future growth

### When Updating
- Prioritize pruning over adding
- Remove outdated content first
- Target net-zero or negative growth
- Only add high-value insights

### Content to Prune (Examples)
- Outdated architectural decisions
- Obvious patterns now visible in code
- Temporary workarounds that are gone
- Generic advice available in docs
- Implementation details

## Capacity Tiers

- **0-60%:** Comfortable, plenty of room
- **60-80%:** Getting full, monitor growth
- **80-100%:** At risk, must prune before adding
- **>100%:** Exceeds limit, invalid state
