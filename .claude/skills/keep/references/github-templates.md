# GitHub Comment Templates

This document contains templates for GitHub issue comments. Load when posting updates or summaries to GitHub.

---

## Progress Update Format

Use this format when posting progress updates during work (`/keep:save --sync`):

```markdown
## Progress Update - {date} {time}

✅ Completed:
- {completed item}
- {completed item}

🔄 In Progress:
- {current item} ({percentage}% done)

💡 Key Decisions:
- {decision}: {rationale}

Next: {next steps}
```

### Example

```markdown
## Progress Update - 2024-10-23 14:30

✅ Completed:
- Installed express-rate-limit and rate-limit-redis
- Configured rate limiter middleware with Redis store

🔄 In Progress:
- Writing tests (60% done)

💡 Key Decisions:
- Using per-IP rate limiting for unauthenticated routes (simpler than per-user)
- Conservative limits: 5 per 15min for login, 3 per 15min for password reset

Next: Complete unit tests, then integration tests
```

---

## Completion Summary Format

Use this format when completing work (`/keep:done`):

```markdown
## ✅ Work Complete - {date} {time}

### Summary
{1-2 paragraph summary of what was accomplished and why}

### Changes Made
- {file}: {what changed}
- {file}: {what changed}

### Key Decisions
1. **{decision}**: {rationale}
2. **{decision}**: {rationale}

### Testing
- ✅ {test type} passing
- ⏸️ {test type} needed

### Learnings
{key insights captured}

### Follow-up
- {follow-up item if any}
```

### Example

```markdown
## ✅ Work Complete - 2024-10-23 16:00

### Summary
Implemented rate limiting for authentication endpoints using express-rate-limit with Redis store. The solution prevents brute force attacks by limiting login attempts to 5 per 15 minutes per IP address, while excluding health check endpoints from rate limiting to preserve monitoring capabilities.

### Changes Made
- `src/auth/middleware/rateLimiter.ts` - Created rate limiter middleware with Redis store and error handling
- `src/auth/routes.ts` - Applied rate limiting to auth routes, excluded health checks
- `tests/unit/auth/rateLimiter.test.ts` - Added comprehensive unit tests
- `tests/integration/auth/rateLimiting.test.ts` - Added end-to-end tests
- `docs/api/authentication.md` - Documented rate limits and response headers

### Key Decisions
1. **Per-IP rate limiting**: Simplest approach for unauthenticated routes, prevents IP-based brute force
2. **Redis store**: Enables distributed rate limiting across multiple instances
3. **Conservative limits**: 5/15min for login, 3/15min for password reset - can adjust based on monitoring
4. **Health check exclusion**: Monitoring endpoints excluded to preserve availability monitoring

### Testing
- ✅ Unit tests passing (8/8)
- ✅ Integration tests passing (5/5)
- ✅ Manual testing completed on staging

### Learnings
- express-rate-limit has excellent TypeScript support and auto-adds X-RateLimit-* headers
- Redis store required for distributed limiting; gracefully degrades to in-memory if Redis fails
- Health endpoints need separate middleware chain to exclude from rate limiting

### Follow-up
Created #1250 to add monitoring dashboard for rate limit hits
```

---

## Best Practices

### Writing Summaries

**Focus on outcomes, not process:**
- ✅ "Implemented rate limiting to prevent brute force attacks"
- ❌ "Added code to rate limit authentication"

**Explain rationale:**
- ✅ "Used Redis store to enable distributed rate limiting across instances"
- ❌ "Used Redis store"

**Be concise but complete:**
- Include what was done
- Explain why decisions were made
- Note what was learned
- Mention follow-up if needed

### Formatting

- Use markdown formatting (code blocks, bold, lists)
- Include file paths with backticks
- Use status indicators (✅, 🔄, ⏸️)
- Keep paragraphs short and scannable
- Use timestamps in `YYYY-MM-DD HH:MM` format

### Content Guidelines

**Do include:**
- Concrete outcomes
- Decision rationale
- Test status
- Key learnings
- Follow-up work

**Don't include:**
- Verbose progress details
- Implementation minutiae
- Repetitive information
- Internal tool commands

---

## Posting to GitHub

Use `gh` CLI to post comments:

```bash
gh issue comment {number} --body "$(cat <<'EOF'
{template content here}
EOF
)"
```

Example:

```bash
gh issue comment 1234 --body "$(cat <<'EOF'
## Progress Update - 2024-10-23 14:30

✅ Completed:
- Implemented rate limiter middleware

Next: Writing tests
EOF
)"
```
