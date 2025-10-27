# Keep File Format Specifications

This document contains complete specifications for all Keep file formats. Load this file when creating new files or when needing format details.

---

## Root CLAUDE.md

**Purpose:** Project-wide context that Claude Code automatically loads

**Location:** `{project-root}/CLAUDE.md`

**Structure:**
```markdown
# Project: {Project Name}

## Tech Stack
- Runtime/Language versions
- Major frameworks and libraries
- Database and infrastructure

## Architecture
- High-level architecture pattern (MVC, microservices, etc.)
- Key architectural decisions and rationale

## Project Structure
- Directory organization
- Module responsibilities
- Important file locations

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
- Deprecations
```

**Management:**
- Created manually or by Keep skill
- Updated by Keep skill suggestions (with user approval)
- Kept concise (aim for < 200 lines)

**Example:**
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

## Authentication
- JWT access tokens (15min expiry)
- Refresh tokens stored in Redis (7 day expiry)
- bcrypt for password hashing (12 rounds)
- Rate limiting on auth endpoints (5 attempts/15min)

## Recent Changes (Last 3 months)
- 2024-10: Added rate limiting (express-rate-limit + Redis)
- 2024-09: Migrated from Sequelize to TypeORM
- 2024-08: Added refresh token rotation for security
```

---

## Nested CLAUDE.md Files

**Purpose:** Domain-specific context for modules/directories

**Location:** `{project-root}/{directory}/CLAUDE.md`

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
- Security considerations
- Common mistakes to avoid

## Dependencies
- External dependencies specific to this module
- Internal dependencies (other modules)

## Testing
- Testing approach for this module
- Key test files
```

**Management:**
- Created by Keep skill when working in new area (with user approval)
- Updated as patterns emerge and learnings accumulate
- Keep skill suggests updates, user reviews and approves

**When to Create:**
- Working in a directory for 2nd+ time
- Patterns are emerging that should be documented
- Complex logic that benefits from explanation
- Don't create prematurely - let need emerge

**Example:**
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

### Token Rotation (Sept 2024)
- Refresh token rotation prevents reuse attacks
- Need to invalidate old refresh token immediately
- Redis TTL handles automatic cleanup

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

## .claude/state.md

**Purpose:** Current session state - what you're working on right now

**Location:** `.claude/state.md`

**Structure:**
```markdown
# Session State

**Last Updated:** {ISO 8601 timestamp}

## Active Work

**Current Issue:** #{number} - {title}
**Branch:** {branch-name}
**Started:** {ISO 8601 timestamp}

### Progress
- ✅ {completed item}
- ✅ {completed item}
- 🔄 {in progress item} ({percentage}% done)
- ⏸️ {pending item}
- ⏸️ {pending item}

### Next Steps
1. {next action}
2. {next action}
3. {next action}

### Open Questions
- {question}
  → Decision: {decision if made, or "TBD"}
- {question}
  → Decision: {decision if made, or "TBD"}

## Recent Work

**Previous Issue:** #{number} - {title} (Completed {YYYY-MM-DD})
**Previous Issue:** #{number} - {title} (Completed {YYYY-MM-DD})
**Previous Issue:** #{number} - {title} (Completed {YYYY-MM-DD})

## Blockers
{description of blocker, or "None currently"}

## Context
- Working primarily in {directories}
- Related to {epic or theme}
- Builds on work from #{related-issue}
```

**Management:**
- Updated by Keep skill on `/keep:start`, `/keep:save`, `/keep:done`
- **Read by Keep skill at session start** for intelligent resume detection
- Auto-saved every 15 minutes during active work (if auto-save enabled)
- Human-readable markdown (Keep skill parses it)

**Resume Detection:**
- Checked proactively at conversation start (session boundary detection)
- **Active Work** section with recent timestamp (< 48h) = resumable work
- Issue number from "Current Issue" field used for `/keep:start {issue}` suggestion
- Time since "Last Updated" determines suggestion strategy:
  - < 48 hours: Proactively suggest resume
  - ≥ 48 hours: Mention stale work, ask if user wants to resume
- Missing "Active Work" section = no resume suggestion

**Example:**
```markdown
# Session State

**Last Updated:** 2024-10-23T14:30:00Z

## Active Work

**Current Issue:** #1234 - Add rate limiting to authentication
**Branch:** feature/rate-limiting
**Started:** 2024-10-23T10:00:00Z

### Progress
- ✅ Researched rate limiting approaches
- ✅ Installed express-rate-limit
- 🔄 Implementing middleware (80% done)
- ⏸️ Need to add tests
- ⏸️ Need to update API docs

### Next Steps
1. Complete middleware implementation
2. Write unit tests for rate limiter
3. Add integration tests
4. Update API documentation

### Open Questions
- Should rate limit be per IP or per user?
  → Decision: Per IP for unauthenticated, per user for authenticated
- What are the limits?
  → TBD: Need to discuss with team

## Recent Work

**Previous Issue:** #1200 - User authentication (Completed 2024-10-22)
**Previous Issue:** #1150 - Database migrations (Completed 2024-10-20)

## Blockers
None currently

## Context
- Working primarily in src/auth/
- Related to security improvements epic
- Builds on work from #1100 (JWT implementation)
```

---

## .claude/work/{issue-number}.md

**Purpose:** Detailed tracking for a specific issue

**Location:** `.claude/work/{issue-number}.md`

**Structure:**
```markdown
# Issue #{number}: {title}

**GitHub:** {full URL to issue}
**Pull Request:** {full URL to PR, if exists}
**Status:** {in_progress|completed}
**Started:** {ISO 8601 timestamp}
**Last Updated:** {ISO 8601 timestamp}

## Issue Description
{description from GitHub}

## Approach
{planned approach - can be filled in during work start}

## Progress Log

### {ISO 8601 timestamp}
- {what was done}
- {what was done}

### {ISO 8601 timestamp}
- {what was done}

## Decisions Made

1. **{decision}:** {rationale}
   - Alternative considered: {alternative} (rejected because {reason})
   - Impact: {what this affects}

2. **{decision}:** {rationale}

## Files Modified

- {file path} ({created|modified})
  - {brief description of changes}

- {file path} ({created|modified})
  - {brief description of changes}

## Learnings

- {learning or gotcha}
- {learning or gotcha}

## Tests

- [ ] {test to write}
- [ ] {test to write}
- [x] {completed test}

## Next Actions

1. {next action}
2. {next action}

## Related Issues

- #{number} - {title} ({prerequisite|follow-up|related})
- #{number} - {title} ({relationship})
```

**Management:**
- Created by `/keep-start` command
- Updated by Keep skill during work (progress, decisions, learnings)
- Moved to `.claude/archive/` when issue completed
- Source for GitHub issue updates

**Example:**
```markdown
# Issue #1234: Add rate limiting to authentication

**GitHub:** https://github.com/myuser/taskmaster-api/issues/1234
**Pull Request:** https://github.com/myuser/taskmaster-api/pull/456
**Status:** completed
**Started:** 2024-10-23T10:00:00Z
**Completed:** 2024-10-23T16:00:00Z

## Issue Description
Add rate limiting to authentication endpoints to prevent brute force attacks.

## Approach
1. Use express-rate-limit middleware (widely used, good TypeScript support)
2. Redis store for distributed rate limiting (already in stack)
3. Apply to /login, /register, /reset-password
4. Conservative limits initially (5 per 15min)
5. Exclude health check endpoints

## Progress Log

### 2024-10-23T16:00:00Z
- ✅ All tests passing (unit + integration)
- ✅ Updated API documentation
- ✅ Deployed to staging
- Ready for review

### 2024-10-23T14:30:00Z
- Implemented rate limiter middleware in src/auth/middleware/rateLimiter.ts
- Configured limits: 5 requests per 15 minutes for /login
- Configured limits: 3 requests per 15 minutes for /reset-password
- Applied middleware to auth routes

### 2024-10-23T12:00:00Z
- Researched options: express-rate-limit vs rate-limiter-flexible
- Decided on express-rate-limit (simpler, sufficient for needs)
- Installed dependencies: express-rate-limit, rate-limit-redis

### 2024-10-23T10:00:00Z
- Started work on issue
- Read issue description and requirements
- Reviewed existing auth implementation

## Decisions Made

1. **Rate limit strategy:** Per-IP for unauthenticated routes
   - Rationale: Simplest approach, prevents IP-based brute force
   - Alternative considered: Per-user for authenticated (complexity not needed yet)
   - Impact: Future enhancement could add per-user for authenticated routes

2. **Storage backend:** Redis (not in-memory)
   - Rationale: Already using Redis, need distributed limiting
   - Alternative considered: In-memory (rejected - won't work with multiple instances)
   - Impact: Requires Redis connection, but we already have it

3. **Limit values:** 5 per 15min (login), 3 per 15min (reset)
   - Rationale: Conservative start, can adjust based on monitoring
   - Alternative considered: 10 per 15min (rejected - too permissive)
   - Impact: May need tuning after observing real usage

4. **Health check exclusion:** Exclude /health and /metrics
   - Rationale: Monitoring shouldn't be rate limited
   - Alternative considered: Apply to all routes (rejected - breaks monitoring)
   - Impact: Need separate middleware chain for health endpoints

## Files Modified

- src/auth/middleware/rateLimiter.ts (created)
  - Main rate limiter middleware
  - Redis store configuration
  - Error handling for Redis failures

- src/auth/routes.ts (modified)
  - Applied rate limiting to auth routes
  - Excluded health checks from rate limiting

- src/auth/middleware/index.ts (modified)
  - Export rate limiter middleware

- package.json (modified)
  - Added: express-rate-limit ^7.0.0
  - Added: rate-limit-redis ^4.0.0

- tests/unit/auth/rateLimiter.test.ts (created)
  - Tests for rate limiter middleware
  - Mock Redis for unit tests

- tests/integration/auth/rateLimiting.test.ts (created)
  - End-to-end rate limiting tests
  - Verify limits enforced correctly

- docs/api/authentication.md (modified)
  - Documented rate limits
  - Added X-RateLimit-* headers documentation

## Learnings

1. **express-rate-limit TypeScript support**
   - Excellent type definitions out of the box
   - Easy to configure with our Redis setup

2. **Health check exclusion pattern**
   - Need to apply rate limiting selectively
   - Use route-specific middleware, not global

3. **Rate limit headers**
   - X-RateLimit-Limit, X-RateLimit-Remaining automatically added
   - Helps clients implement retry logic

4. **Testing with Redis**
   - Use redis-mock for unit tests (fast, isolated)
   - Use real Redis for integration tests (accurate)

5. **Error handling**
   - If Redis fails, rate limiting degrades gracefully
   - Falls back to in-memory (per instance, but better than nothing)

## Tests

- [x] Unit tests for rateLimiter middleware (8/8 passing)
- [x] Integration tests for login rate limiting (3/3 passing)
- [x] Test rate limit header presence (2/2 passing)
- [x] Manual testing on staging environment

## Next Actions

None - work complete

## Related Issues

- #1100 - JWT implementation (prerequisite)
- #1250 - Add monitoring for rate limit hits (follow-up, created)
```

---

## Archive Files

**Purpose:** Completed work files preserved for reference

**Location:** `.claude/archive/{issue-number}.md`

**Format:** Same as `.claude/work/{issue-number}.md`

**Management:**
- Moved from `.claude/work/` when issue completed
- Preserved indefinitely for reference
- Can be searched for related patterns/decisions
- Not actively updated after archival

**Usage:**
- Load when starting similar work
- Reference for "how did we solve X before?"
- Source of patterns for CLAUDE.md suggestions

---

## Format Conventions

### Timestamps
- Always use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- Use UTC timezone (Z suffix)
- Examples: `2024-10-23T14:30:00Z`

### Issue References
- Always prefix with `#`: `#1234`
- Include title after dash: `#1234 - Add rate limiting`
- Link full URL in work files: `https://github.com/user/repo/issues/1234`

### Status Indicators
- ✅ Completed
- 🔄 In progress
- ⏸️ Pending/not started
- ❌ Blocked or failed

### File Paths
- Always use relative paths from project root
- Use forward slashes: `src/auth/middleware/rateLimiter.ts`
- Note create vs modify: `(created)` or `(modified)`

### Markdown Structure
- Use `##` for major sections
- Use `###` for timestamps in progress log
- Use `**bold**` for field names: `**Status:** in_progress`
- Use lists for progress items, decisions, learnings

---

## Validation

When creating or updating files, ensure:

1. **All required sections present**
2. **Timestamps in ISO 8601 format**
3. **Issue numbers prefixed with #**
4. **Status indicators consistent**
5. **File paths valid and relative**
6. **Markdown formatting correct**
7. **Links functional (for GitHub URLs)**

If file format invalid or corrupted:
- Warn user
- Attempt to repair if possible
- Preserve user data above all else
- Never silently delete or overwrite
