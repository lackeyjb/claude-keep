# GitHub Progress Update Template

Use this template when posting progress updates to GitHub issues (from `/keep-save --sync`).

## Template Format

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

## Best Practices

**Focus on outcomes:**
- ✅ "Implemented rate limiting to prevent brute force attacks"
- ❌ "Added code to rate limit authentication"

**Explain rationale:**
- ✅ "Used Redis store to enable distributed rate limiting across instances"
- ❌ "Used Redis store"

**Keep it concise:**
- Highlight key progress only
- Summarize decisions, don't list all details
- Keep next steps brief (1-2 items)

**Use clear status indicators:**
- ✅ for completed
- 🔄 for in progress (with percentage if known)
- Note blocking issues if any

## Example

```markdown
## Progress Update - 2024-10-23 14:30

✅ Completed:
- Installed express-rate-limit and rate-limit-redis
- Configured rate limiter middleware with Redis store
- Applied rate limiting to authentication routes

🔄 In Progress:
- Writing unit tests for rate limiter (60% done)

💡 Key Decisions:
- Using per-IP rate limiting for unauthenticated routes (simpler than per-user)
- Conservative limits: 5 per 15min for login, 3 per 15min for password reset
- Excluded health check endpoints to preserve monitoring

Next: Complete unit tests, then add integration tests
```

## Posting to GitHub

Post via `gh` CLI:

```bash
gh issue comment {number} --body "$(cat <<'EOF'
## Progress Update - {timestamp}

✅ Completed:
- {item}

Next: {next steps}
EOF
)"
```
