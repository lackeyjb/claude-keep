# Keep - System Architecture & Vision

**Version:** 1.0
**Created:** 2024-10-23
**Purpose:** A lightweight, intelligent project memory and workflow system for Claude Code that uses GitHub Issues for persistence and nested CLAUDE.md files for context.

---

## Executive Summary

Keep is a drastically simplified alternative to complex project management systems. It leverages Claude Code's native features (nested CLAUDE.md files) and GitHub Issues to provide:

- **Persistent memory** across sessions
- **Intelligent context management** that grows with your project
- **Lightweight GitHub integration** without ceremony
- **Natural workflows** that enhance rather than constrain

**Key Metrics:**
- 1 Skill + 3 Core Commands (vs 50+ in alternatives)
- 90% fewer files to manage
- Zero custom context loaders (uses native Claude Code features)
- Works with or without GitHub

---

## Core Philosophy

### Design Principles

1. **Leverage Native Features** - Use Claude Code's built-in CLAUDE.md reading instead of custom loaders
2. **Intelligence Over Automation** - Skill suggests and learns rather than rigidly enforcing process
3. **Minimal Ceremony** - No multi-stage pipelines or complex file naming schemes
4. **Solo-First** - Optimized for individual developers, extensible for teams
5. **Fail Gracefully** - Works offline, works without GitHub, degrades elegantly

### Anti-Patterns We Avoid

❌ Complex multi-file frontmatter manipulation
❌ File renaming ceremonies (001.md → 1234.md)
❌ Rigid multi-stage pipelines (PRD → Epic → Tasks)
❌ 50+ bash scripts to maintain
❌ Git worktrees for every feature
❌ Static context that goes stale

---

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────┐
│                    User                              │
└──────────────┬──────────────────────────────────────┘
               │
               │ Invokes commands
               ▼
┌─────────────────────────────────────────────────────┐
│              Slash Commands                          │
│  /keep:start  /keep:save  /keep:done               │
└──────────────┬──────────────────────────────────────┘
               │
               │ Invokes skill
               ▼
┌─────────────────────────────────────────────────────┐
│              Keep Skill                              │
│  • Loads context (CLAUDE.md)                        │
│  • Captures learnings                               │
│  • Suggests updates                                 │
│  • Manages state                                    │
│  • Syncs with GitHub                                │
└──────────────┬──────────────────────────────────────┘
               │
               │ Reads/Writes
               ▼
┌─────────────────────────────────────────────────────┐
│              File System                             │
│  • Nested CLAUDE.md (context)                       │
│  • .claude/work/*.md (tracking)                     │
│  • .claude/state.md (current state)                 │
└─────────────────────────────────────────────────────┘
               │
               │ Syncs to
               ▼
┌─────────────────────────────────────────────────────┐
│              GitHub Issues                           │
│  • Source of truth                                  │
│  • Progress updates                                 │
│  • Team visibility                                  │
└─────────────────────────────────────────────────────┘
```

### Directory Structure

```
project-root/
├── CLAUDE.md                           # Root project context (auto-loaded)
├── src/
│   ├── CLAUDE.md                       # Source code patterns
│   ├── auth/
│   │   └── CLAUDE.md                   # Domain-specific context
│   └── api/
│       └── CLAUDE.md                   # API-specific context
├── tests/
│   └── CLAUDE.md                       # Testing patterns
└── .claude/
    ├── work/
    │   ├── 1234.md                     # Active issue tracking
    │   └── 5678.md                     # Another active issue
    ├── archive/
    │   └── 1200.md                     # Completed issues (for reference)
    ├── state.md                        # Current session state
    ├── commands/                       # Slash commands
    │   ├── keep-start.md               # Start work command
    │   ├── keep-save.md                # Save progress command
    │   └── keep-done.md                # Complete work command
    └── skills/keep/                    # The Keep Skill
        ├── SKILL.md                    # Skill instructions
        ├── references/
        │   ├── file-formats.md         # File format specifications
        │   └── workflows.md            # Workflow examples
        └── scripts/
            ├── github_sync.py          # GitHub API helpers
            └── score_issues.py         # Issue recommendation logic
```

---

## Implementation Phases

### Phase 1: Core Foundation (MVP) ⭐

**Goal:** Basic structure and core workflows working

**Tasks:**
1. Create directory structure (`.claude/work/`, `.claude/archive/`, `.claude/state.md`)
2. Implement 3 core commands: `keep-start`, `keep-save`, `keep-done`
3. Create Keep skill with core intelligence
4. File format specs in `references/`
5. GitHub sync (fetch issue, post comments)

**Deliverable:** Can track work on issues, capture learnings, sync to GitHub

---

### Phase 2: Intelligence Layer ⭐

**Goal:** Proactive learning and context suggestions

**Tasks:**
1. Implement learning capture logic
   - Detect decisions during work
   - Identify patterns and gotchas
   - Store in work file

2. Implement context suggestion logic
   - Detect when CLAUDE.md update would help
   - Generate proposed updates
   - Present diffs for approval

3. Add threshold detection
   - 3+ decisions in same area → suggest CLAUDE.md update
   - 2+ sessions in directory → suggest new CLAUDE.md

**Deliverable:** Skill actively learns and suggests context updates

---

### Phase 3: Growth Features ⭐

**Goal:** Next work recommendations and context growth

**Tasks:**
1. Implement `/keep:next` command
   - Fetch open issues from GitHub
   - Parse labels and metadata
   - Basic scoring algorithm (continuity + priority)

2. Implement `/keep:grow` command
   - Analyze directory
   - Assess if CLAUDE.md would help
   - Generate proposal

3. Add scoring logic
   - Continuity (same area)
   - Priority (labels)
   - Basic recommendations

**Deliverable:** Smart recommendations for next work, easy context growth

---

### Phase 4+: Polish (Later iterations)

Based on real usage, consider:

- **Auto-save** - Timer-based saves every 15 minutes (if manual saves are annoying)
- **Parallel agents** - For large issues worth parallelizing
- **Advanced scoring** - Dependencies, freshness, complexity estimation
- **Analytics** - Velocity tracking, time per area, pattern detection

---

## File Format Specifications

### Root CLAUDE.md

**Purpose:** Project-wide context that Claude Code automatically loads

**Structure:**
```markdown
# Project: {Project Name}

## Tech Stack
- Runtime/Language versions
- Major frameworks and libraries
- Database and infrastructure

## Architecture
- High-level architecture pattern
- Key architectural decisions

## Project Structure
- Directory organization
- Module responsibilities

## Development
- Setup instructions
- Common commands
- Environment variables

## Conventions
- Naming conventions
- Code style guidelines
- Testing approach

## Recent Changes (Last 3-6 months)
- Significant architectural changes
- New patterns adopted
```

**Management:**
- Created manually or by Keep skill
- Updated by Keep skill suggestions (with user approval)
- Kept concise (aim for < 200 lines)

---

### Nested CLAUDE.md Files

**Purpose:** Domain-specific context for modules/directories

**Structure:**
```markdown
# {Module Name}

## Purpose
What this module does and why it exists

## Key Patterns
- Specific patterns used in this module
- Important abstractions
- Design decisions

## API / Public Interface
- Key functions/classes
- How other modules interact with this

## Recent Learnings
- Gotchas discovered while working here
- Performance considerations
- Common mistakes to avoid

## Dependencies
- External dependencies
- Internal dependencies (other modules)

## Testing
- Testing approach for this module
- Key test files
```

**When to Create:**
- Working in a directory for 2nd+ time
- Patterns are emerging that should be documented
- Complex logic that benefits from explanation
- Don't create prematurely - let need emerge

---

### .claude/state.md

**Purpose:** Current session state - what you're working on right now

**Structure:**
```markdown
# Session State

**Last Updated:** {timestamp}

## Active Work

**Current Issue:** #{number} - {title}
**Branch:** {branch-name}
**Started:** {timestamp}

### Progress
- ✅ {completed item}
- 🔄 {in progress item}
- ⏸️ {pending item}

### Next Steps
1. {next action}
2. {next action}

### Open Questions
- {question}
  → Decision: {decision if made}

## Recent Work

**Previous Issue:** #{number} - {title} (Completed {date})
**Previous Issue:** #{number} - {title} (Completed {date})

## Context
- Working primarily in {directories}
- Related to {epic or theme}
```

---

### .claude/work/{issue-number}.md

**Purpose:** Detailed tracking for a specific issue

**Structure:**
```markdown
# Issue #{number}: {title}

**GitHub:** {url}
**Status:** {in_progress|completed}
**Started:** {timestamp}
**Last Updated:** {timestamp}

## Issue Description
{description from GitHub}

## Approach
{planned approach}

## Progress Log

### {timestamp}
- {what was done}

## Decisions Made
1. **{decision}:** {rationale}

## Files Modified
- {file path} ({created|modified})

## Learnings
- {learning}

## Tests
- [ ] {test to write}

## Next Actions
1. {next action}

## Related Issues
- #{number} - {title} (relationship)
```

---

## Core Workflows

### Workflow 1: Start New Work

```
User: /keep:start 1234

Keep System:
1. Fetch issue #1234 from GitHub
2. Load relevant context (CLAUDE.md files)
3. Create .claude/work/1234.md
4. Update .claude/state.md
5. Present starting point to user

Output:
┌────────────────────────────────────────┐
│ ✅ Ready to work on issue #1234        │
│                                         │
│ 📋 Issue: Add rate limiting to auth    │
│ 🏷️  Labels: security, enhancement      │
│                                         │
│ 📚 Context loaded:                     │
│ ├─ CLAUDE.md (project overview)        │
│ ├─ src/CLAUDE.md (code patterns)       │
│ └─ src/auth/CLAUDE.md (auth patterns)  │
│                                         │
│ 💡 Suggested approach: [...]           │
│                                         │
│ Where would you like to start?         │
└────────────────────────────────────────┘
```

---

### Workflow 2: Save Progress

```
User: /keep:save

Keep System:
1. Update .claude/work/{issue}.md with progress
2. Capture learnings from recent work
3. Check if threshold met for context updates
4. If yes, suggest CLAUDE.md updates
5. Optional: Sync to GitHub

Output:
┌────────────────────────────────────────┐
│ 💾 Progress saved                      │
│                                         │
│ 📝 Captured:                           │
│ - 2 progress entries                   │
│ - 3 decisions                          │
│ - 1 learning                           │
│                                         │
│ 💡 Suggestion: Update src/auth/        │
│    CLAUDE.md with rate-limiting        │
│    pattern?                            │
│                                         │
│ [Proposed changes shown]               │
│                                         │
│ Add this? [yes / edit / later / no]   │
└────────────────────────────────────────┘
```

---

### Workflow 3: Complete Work

```
User: /keep:done

Keep System:
1. Generate comprehensive summary
2. Suggest context updates (if not already done)
3. Sync to GitHub
4. Archive work file
5. Update state
6. Recommend next work

Output:
┌────────────────────────────────────────┐
│ 🎉 Issue #1234 complete!               │
│                                         │
│ 📊 Summary:                            │
│ - 4 files modified                     │
│ - 5 decisions documented               │
│ - 3 learnings captured                 │
│                                         │
│ 🔗 Synced to GitHub                    │
│                                         │
│ Close issue? [yes / no / later]       │
└────────────────────────────────────────┘
```

---

## Example Files

### Example Root CLAUDE.md

```markdown
# Project: TaskMaster API

## Tech Stack
- Node.js 18.x with TypeScript 5.x
- Express 4.x for REST API
- PostgreSQL 14 with TypeORM
- Redis for caching and rate limiting
- Jest for testing

## Architecture
RESTful API following repository pattern:
- Controllers handle HTTP
- Services contain business logic
- Repositories abstract database access
- Middleware for auth, validation, rate limiting

## Project Structure
```
src/
├── controllers/    # HTTP request handlers
├── services/       # Business logic
├── repositories/   # Database access
├── middleware/     # Express middleware
├── models/         # TypeORM entities
└── utils/          # Shared utilities
tests/              # Jest tests
migrations/         # TypeORM migrations
```

## Development
```bash
npm install          # Install dependencies
npm run dev          # Start dev server (port 3000)
npm test             # Run all tests
npm run migrate      # Run database migrations
```

## Conventions
- **Naming:** camelCase for functions, PascalCase for classes
- **Files:** One class per file, match file name to class name
- **Tests:** Co-located with source (*.test.ts)
- **Commits:** Conventional commits (feat:, fix:, etc.)
- **Branches:** feature/, bugfix/, hotfix/

## Recent Changes (Last 3 months)
- 2024-10: Added rate limiting (express-rate-limit + Redis)
- 2024-09: Migrated from Sequelize to TypeORM
- 2024-08: Added refresh token rotation for security
```

---

### Example Domain CLAUDE.md

```markdown
# Authentication Module

## Purpose
Handles user authentication, token management, and session security.

## Key Patterns

### JWT Token Strategy
- **Access tokens:** 15 minute expiry, stored in memory
- **Refresh tokens:** 7 day expiry, stored in Redis
- **Rotation:** Refresh tokens rotate on use (one-time use)

### Password Security
- bcrypt with 12 rounds (balance of security and performance)
- Validation: minimum 8 chars, 1 uppercase, 1 number, 1 special
- Never log passwords or tokens (security audit requirement)

### Rate Limiting
- Per-IP rate limiting: 5 attempts per 15 minutes
- Applies to: /login, /register, /reset-password
- Implementation: express-rate-limit with Redis store
- Health checks excluded from rate limiting

## API / Public Interface

### Authentication Endpoints
- `POST /auth/login` - Email/password authentication
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - Invalidate tokens
- `POST /auth/register` - Create new user

### Middleware
- `authenticate()` - Verify JWT access token
- `rateLimitAuth()` - Apply rate limiting

## Recent Learnings

### Rate Limiting Implementation (Oct 2024)
- express-rate-limit has excellent TypeScript support
- Remember to exclude health check endpoints (/health, /metrics)
- Redis store required for distributed rate limiting
- Rate limit headers (X-RateLimit-*) automatically added

### Common Mistakes
- ❌ Forgetting to hash passwords in tests (use test fixtures)
- ❌ Logging full JWT tokens (use token.substring(0, 10))
- ❌ Not handling Redis connection failures (fallback gracefully)

## Dependencies
- External: jsonwebtoken, bcrypt, express-rate-limit
- Internal: src/models/User, src/repositories/UserRepository

## Testing
- Unit tests: src/auth/*.test.ts
- Integration tests: tests/integration/auth.test.ts
- Mock Redis in tests (redis-mock package)
```

---

## Future Enhancements

### Beyond MVP

**Advanced Intelligence:**
- Learn project-specific patterns over time
- Predict effort for issues
- Suggest issue breakdowns
- Detect technical debt

**Team Features:**
- Detect when multiple people working on same issue
- Coordinate through GitHub comments
- Share CLAUDE.md updates across team

**Integrations:**
- Linear, Jira, other issue trackers
- Slack notifications
- CI/CD integration

**Analytics:**
- Velocity tracking
- Time spent per area
- Most valuable context files
- Pattern detection (common issues)

---

## Migration from Other Systems

If transitioning from CCPM or similar:

### Migration Steps

1. **Preserve GitHub Issues** - Already in GitHub ✓

2. **Convert Context**
   ```bash
   # Merge existing context files into root CLAUDE.md
   # Manual curation recommended
   ```

3. **Migrate Active Work**
   ```bash
   # Convert active epics → work files
   # Map to GitHub issue numbers
   ```

4. **Clean Up**
   ```bash
   # Archive old structure
   # Remove deprecated files
   ```

5. **Verify**
   - Run `/keep:start` on existing issue
   - Verify context loads
   - Verify GitHub sync works

### What You Gain

- 90% fewer files to manage
- No frontmatter manipulation
- No file renaming
- Simpler mental model
- Faster execution
- Same core benefits (memory, GitHub, intelligence)

---

## Summary

Keep provides intelligent project memory with minimal complexity:

- **1 Skill + 3 Core Commands** instead of 50+
- **Nested CLAUDE.md** instead of custom context loaders
- **Lightweight file structure** instead of complex frontmatter
- **Natural workflows** instead of rigid pipelines
- **Solo-optimized** while remaining team-ready

The system is designed to be built iteratively, starting with a solid MVP and growing based on real usage patterns.
