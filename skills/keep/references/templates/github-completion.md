# GitHub Completion Summary Template

Use this template when posting completion summaries to GitHub issues (from `/keep-done`).

## Template Format

```markdown
## ✅ Work Complete - {date} {time}

{If PR exists: Completed via PR #{number}}

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

## Best Practices

**Summary:**
- Focus on what was accomplished and why
- Explain the value delivered
- Keep to 1-2 paragraphs
- Be conversational but professional

**Changes Made:**
- List key files with brief descriptions
- Focus on major changes, not every file
- Group related changes if many files

**Key Decisions:**
- Include the decision AND rationale
- Note alternatives considered
- Explain impact on codebase
- Limit to top 3-5 decisions

**Testing:**
- Note what tests passed
- Note what testing is still needed
- Include manual testing if relevant

**Learnings:**
- Share insights useful to team
- Document gotchas discovered
- Note patterns that worked well
- Keep concise - 2-4 key learnings

**Follow-up:**
- Link to created follow-up issues
- Note known limitations
- Mention future improvements
- Omit if no follow-up needed

## Example

```markdown
## ✅ Work Complete - 2024-10-23 16:00

Completed via PR #456

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

## Posting to GitHub

Post via `gh` CLI:

```bash
gh issue comment {number} --body "$(cat <<'EOF'
## ✅ Work Complete - {timestamp}

### Summary
{summary here}

### Changes Made
- {file}: {description}

### Key Decisions
1. **{decision}**: {rationale}

### Testing
- ✅ {tests passing}

### Learnings
{learnings}
EOF
)"
```
