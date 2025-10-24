# Zero-Issues Project Initialization

Detailed patterns and implementation guide for discovering starter work when a project has no open GitHub issues.

---

## When to Trigger

Zero-issues initialization starts when:
- `/keep:start` called without issue number
- `gh issue list` returns empty array
- User asks "what should I work on?" with no open issues

---

## Three-Phase Workflow

### Phase 1: Discovery

Use Claude Code's native tools to find actionable work:

#### 1.1 Check CLAUDE.md Context

```bash
# Check if root CLAUDE.md exists and is recent
```

**Decision logic:**
- If root CLAUDE.md missing: Offer `/keep:grow .` first
- If root CLAUDE.md stale (>3 months): Suggest updating
- If present and current: Continue to discovery

**Rationale:** Project context is essential before suggesting work

#### 1.2 Find Planning Documents

**Use Glob to find planning docs:**
```
Pattern: {ROADMAP,TODO,PLAN,BACKLOG,VISION,CONTRIBUTING}*.md
Path: project root
```

**Parse patterns:**
- List items: `- [ ] Task description` (checkboxes)
- List items: `- Task description` (bullets)
- Numbered items: `1. Task description`
- Headers as categories: `## Feature Name` followed by description

**Extract:**
- Task description
- Source file and line number
- Any priority indicators (!, HIGH, P0, etc.)
- Any size estimates (small, 2h, etc.)

**Example parse:**
```markdown
ROADMAP.md:
15: - [ ] Implement user authentication
16:   - JWT tokens with refresh
17:   - Estimated: 2 days
```
→ Extract: "Implement user authentication", source: "ROADMAP.md:15", estimate: "2 days"

#### 1.3 Scan Codebase Signals

**Use Grep to find code comments:**
```
Pattern: TODO:|FIXME:|HACK:|BUG:
Options: -n (line numbers), -B 1 -A 1 (context), -i (case insensitive)
```

**Categorize by type:**
- `FIXME:` / `BUG:` → High priority (bugs/issues)
- `TODO:` → Medium priority (planned improvements)
- `HACK:` → Medium priority (refactoring needed)

**Extract context:**
```typescript
// FIXME: Rate limiting not implemented for login endpoint
// This allows brute force attacks
async function login(req, res) { ... }
```
→ Extract: "Add rate limiting to login endpoint", source: "src/auth/login.ts:45", priority: high

#### 1.4 Assess Test Coverage

**Find test files (Glob):**
```
Pattern: **/*.{test,spec}.{js,ts,py,go,rs}
```

**Find source files (Glob):**
```
Pattern: {src,lib}/**/*.{js,ts,py,go,rs}
```

**Identify gaps:**
- Directories with source but no tests
- Modules with partial test coverage
- Critical paths without tests (auth, payments, etc.)

**Example:**
```
src/payments/
  ├── stripe.ts
  ├── processor.ts
  └── refunds.ts
tests/
  └── (no payments/ directory)
```
→ Extract: "Add tests for payment module", source: "Missing coverage in src/payments/"

---

### Phase 2: Synthesis

#### 2.1 Prioritization Logic

**Priority ranking:**
1. **Planning docs** (ROADMAP, TODO, etc.) - Explicitly planned work
2. **FIXME/BUG comments** - Important fixes
3. **TODO comments** - Planned improvements
4. **Missing tests** - Quality improvements
5. **Documentation gaps** - Lower priority

**Within each category, prioritize by:**
- Explicit priority markers (!, HIGH, urgent)
- Frequency (multiple TODOs in same area)
- Recency (recent comments)
- Critical areas (auth, payments, security)

#### 2.2 Generate Issue Suggestions

**For each potential issue:**

**Title generation:**
- Imperative mood: "Add", "Fix", "Implement", "Refactor"
- Specific and actionable
- Clear scope

**Description generation:**
```markdown
{What needs to be done - 1-2 sentences}

**Context:**
{Why this matters or what problem it solves}

**Source:**
{file:line or document name}

**Affected files:**
{list of files if known}

**Acceptance criteria:**
- {criterion 1}
- {criterion 2}
```

**Label suggestions:**
- `enhancement` - New features
- `bug` - Bug fixes
- `testing` - Test additions
- `documentation` - Docs
- `refactor` - Code cleanup
- `security` - Security issues

**Priority labels:**
- FIXME/BUG → `high`
- Roadmap items → `medium` or `high`
- TODO → `medium`
- Tests/docs → `low` or `medium`

#### 2.3 Limit to 3-5 Suggestions

**Selection criteria:**
- Mix of types (features, bugs, tests)
- Mix of sizes (quick wins + larger work)
- Highest priority items
- Diverse areas (avoid all from one module)

**Presentation order:**
1. Highest value/priority first
2. Group by type if helpful
3. Include source attribution for each

---

### Phase 3: Interactive Creation

#### 3.1 Present Findings

**Conversational presentation:**
```markdown
I notice you don't have any open issues. Let me help find starter work!

📚 Project context: ✅ CLAUDE.md found

📋 Planning documents:
   • ROADMAP.md: 5 planned features
   • TODO.md: 3 pending tasks

🔍 Codebase analysis:
   • 12 TODO/FIXME comments
   • 8 files missing tests

🎯 5 Starter Issue Suggestions:

1. **Implement user authentication** [enhancement, high]
   Source: ROADMAP.md line 15

2. **Fix rate limiting in API** [bug, medium]
   Source: FIXME in src/api/routes.ts:34

3. **Add tests for payment module** [testing, medium]
   Source: Missing coverage in src/payments/

4. **Document database schema** [documentation, low]
   Source: Undocumented src/db/

5. **Refactor user service** [refactor, medium]
   Source: TODO in src/services/user.ts:12

Which issues should I create? [all / 1,2,3 / none - work locally]
```

#### 3.2 Create Issues

**Before creating:**
1. Collect all unique labels from selected issues
2. Check existing labels: `gh label list --json name --jq '.[].name'`
3. Create missing labels: `gh label create "label-name"` (uses default color)

**For each selected issue:**

1. **Generate natural issue body:**
```markdown
{Description of what needs to be done}

**Context:**
{Why this matters or what problem it solves}

**Source:**
{Where this came from - file:line or document}

**Affected files:**
{List of relevant files if known}

**Acceptance criteria:**
- {What defines done}
```

2. **Create via gh CLI:**
```bash
gh issue create \
  --title "Title here" \
  --body "Body here" \
  --label "label1,label2"
```

3. **Display created issue URL**

#### 3.3 Transition to Start

**After creating issues:**
```markdown
🎉 Created 3 issues!

Which issue would you like to start working on?
[1 / 2 / 3 / none]
```

**If user selects issue:**
- Transition to normal `/keep:start {number}` workflow
- Load context
- Create work file
- Begin work

---

## Handling Edge Cases

### No Planning Docs Found

```markdown
📋 Searching for planning documents...
   ℹ️  No planning documents found

🔍 Analyzing codebase...
   • 12 TODO comments found
   • 8 files missing tests

🎯 Suggestions based on codebase signals:
[Continue with TODO/test-based suggestions]
```

### No TODOs, No Test Gaps

```markdown
📋 Searching for planning documents...
   ℹ️  No planning documents found

🔍 Analyzing codebase...
   • No TODO comments found
   • No obvious gaps detected

💭 No automated suggestions available.

Would you like to:
1. Create a ROADMAP.md to plan features
2. Create an issue manually
3. Use /keep:grow to document code first
4. Work in local-only mode

What would you prefer?
```

### GitHub Offline

```markdown
⚠️  GitHub unavailable (gh not found)

I can still analyze your codebase for potential work:
[Show findings]

However, I can't create issues without GitHub. You can:
1. Install gh CLI and retry
2. Create issues manually later
3. Work in local-only mode

Continue analyzing? [yes / no]
```

### Context Missing

```markdown
⚠️  No CLAUDE.md found at project root

Before suggesting work, I recommend creating project context:

Run /keep:grow . to create CLAUDE.md

This will help me:
- Understand your tech stack
- Suggest relevant work
- Provide better context

Create CLAUDE.md first? [yes / skip and continue]
```

---

## Search Patterns Reference

### Planning Document Patterns

**File patterns (Glob):**
```
{ROADMAP,TODO,PLAN,BACKLOG,VISION,CONTRIBUTING}*.md
{roadmap,todo,plan,backlog,vision,contributing}*.md
docs/{ROADMAP,TODO,PLAN}*.md
.github/{ROADMAP,TODO}*.md
```

**Content patterns (parse with Read):**
- Checkboxes: `- [ ] {task}`
- Bullets: `- {task}`
- Numbered: `{number}. {task}`
- Headers: `## {feature}` + description

### Code Comment Patterns

**Grep patterns:**
```
Pattern: TODO:|FIXME:|HACK:|BUG:|XXX:|NOTE:
Options: -i -n -B 1 -A 1
Type: All code files (or use --type for specific languages)
```

**Priority mapping:**
- FIXME, BUG → high
- TODO, XXX → medium
- HACK, NOTE → low/medium
- With "urgent", "critical" → high
- With "nice-to-have", "maybe" → low

### Test Coverage Patterns

**Test file patterns (Glob):**
```
**/*.{test,spec}.{js,ts,jsx,tsx}
**/*.{test,spec}.py
**/*_test.{go,rs}
tests/**/*
__tests__/**/*
```

**Source file patterns (Glob):**
```
src/**/*.{js,ts,jsx,tsx}
lib/**/*.{js,ts}
src/**/*.py
*.go (in relevant dirs)
src/**/*.rs
```

---

## Example Outputs

### Full Discovery with Planning Docs

```markdown
📚 Project context: ✅ CLAUDE.md found (updated 2024-10-15)

📋 Planning documents:
   • ROADMAP.md: 8 planned features
   • CONTRIBUTING.md: 2 good-first-issues

🔍 Codebase analysis:
   • 3 FIXME comments (high priority)
   • 9 TODO comments
   • 5 directories missing tests
   • 2 modules need documentation

🎯 5 Starter Issue Suggestions:

1. **Fix rate limiting bypass in login** [bug, high]
   Source: FIXME in src/auth/login.ts:45
   Files: src/auth/login.ts

2. **Implement user profile page** [enhancement, high]
   Source: ROADMAP.md line 23
   Files: src/pages/, src/components/

3. **Add tests for payment processing** [testing, high]
   Source: Missing coverage in src/payments/
   Files: tests/payments/

4. **Refactor database connection pooling** [refactor, medium]
   Source: TODO in src/db/pool.ts:12
   Files: src/db/pool.ts

5. **Document API authentication flow** [documentation, low]
   Source: Undocumented in docs/
   Files: docs/api/

Which issues should I create? [all / 1,2,3 / custom selection]
```

### Code-Only Discovery (No Planning Docs)

```markdown
📚 Project context: ✅ CLAUDE.md found

📋 Searching for planning documents...
   ℹ️  No planning documents found

🔍 Analyzing codebase...
   • 15 TODO/FIXME comments found
   • 8 files missing test coverage
   • 3 security-related comments

🎯 4 Starter Issue Suggestions:

1. **Fix SQL injection vulnerability** [bug, security, high]
   Source: FIXME in src/db/queries.ts:67
   Files: src/db/queries.ts

2. **Add input validation to API endpoints** [enhancement, security, high]
   Source: TODO in src/api/validation.ts:23
   Files: src/api/

3. **Write tests for authentication module** [testing, medium]
   Source: Missing coverage in src/auth/
   Files: tests/auth/

4. **Optimize database queries** [performance, medium]
   Source: TODO in src/db/users.ts:45
   Files: src/db/users.ts

Which issues should I create? [all / 1,2,3 / custom]
```

---

## Philosophy

**Source transparency:**
- Always show where suggestions came from
- Include file:line references
- Link to planning docs

**User control:**
- Let user select which issues to create
- Offer "none - work locally" option
- Allow custom selection (e.g., "1,3,5")

**Natural generation:**
- Generate natural, helpful issue bodies
- No rigid templates
- Context-aware descriptions
- Clear acceptance criteria

**Graceful degradation:**
- Work offline (can't create issues, but show suggestions)
- No planning docs → Focus on code signals
- Nothing found → Offer alternatives
- Missing context → Suggest creating it first
