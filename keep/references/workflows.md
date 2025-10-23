# Keep Workflow Examples

This document contains detailed workflow examples showing how Keep operates in practice. Load this file when need detailed workflow guidance or when users ask "how does X work?"

---

## Workflow 1: Start New Work

### User Invocation
```
User: /keep:start 1234
```

### System Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. Fetch Issue from GitHub                          │
│    gh issue view 1234 --json title,body,labels      │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 2. Load Context                                      │
│    ├─ CLAUDE.md (auto-loaded by Claude Code)        │
│    ├─ Relevant module CLAUDE.md (auto-loaded)       │
│    ├─ Read .claude/state.md                         │
│    └─ Search .claude/archive/ for related work      │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 3. Parse Issue                                       │
│    ├─ Extract requirements                          │
│    ├─ Identify dependencies ("depends on #...")     │
│    ├─ Note labels and priorities                    │
│    └─ Analyze acceptance criteria                   │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 4. Suggest Approach                                  │
│    Based on:                                         │
│    ├─ Project patterns (from CLAUDE.md)             │
│    ├─ Similar past work (from archive)              │
│    └─ Technical constraints (from issue)            │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 5. Create Work File                                  │
│    .claude/work/1234.md with:                       │
│    ├─ Issue metadata (URL, status, timestamps)      │
│    ├─ Description                                   │
│    ├─ Suggested approach                            │
│    └─ Empty sections (progress, decisions, etc.)    │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 6. Update State                                      │
│    .claude/state.md:                                │
│    ├─ Set active issue: #1234                       │
│    ├─ Record start time                             │
│    ├─ Note branch if specified                      │
│    └─ Move previous issue to "Recent Work"          │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 7. Present to User                                   │
│    Conversational presentation with:                │
│    ├─ Issue summary                                 │
│    ├─ Context loaded                                │
│    ├─ Suggested approach                            │
│    ├─ Related work                                  │
│    └─ Questions if clarification needed             │
└─────────────────────────────────────────────────────┘
```

### Example Output

```
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
│ 🔗 Related work:                       │
│ └─ #1100 - JWT implementation          │
│                                         │
│ 💡 Suggested approach:                 │
│ Based on existing auth patterns, I     │
│ suggest using express-rate-limit with  │
│ Redis store. This fits our current     │
│ architecture and JWT pattern from      │
│ #1100.                                 │
│                                         │
│ The issue mentions preventing brute    │
│ force attacks. Should we:              │
│ • Rate limit per-IP (simpler)          │
│ • Rate limit per-user (more complex)   │
│ • Both (comprehensive)                 │
│                                         │
│ Where would you like to start?         │
└────────────────────────────────────────┘
```

---

## Workflow 2: Save Progress

### User Invocation
```
User: /keep:save
```

Or automatic trigger (if auto-save enabled):
```
[15 minutes elapsed since last save]
[Auto-save triggered]
```

### System Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. Review Recent Conversation                        │
│    Analyze last 30 minutes (or since last save):    │
│    ├─ Concrete steps completed                      │
│    ├─ Decisions made with rationale                 │
│    ├─ Learnings and gotchas discovered              │
│    └─ Questions raised or resolved                  │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 2. Update Work File                                  │
│    .claude/work/{issue}.md:                         │
│    ├─ Add timestamped progress log entry            │
│    ├─ Document decisions in Decisions section       │
│    ├─ Capture learnings in Learnings section        │
│    └─ Update files modified list                    │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 3. Update State                                      │
│    .claude/state.md:                                │
│    ├─ Update progress indicators                    │
│    ├─ Update next steps                             │
│    └─ Note any new questions                        │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 4. Check Learning Threshold                          │
│    Count decisions by directory:                    │
│    ├─ src/auth/: 3 decisions                        │
│    └─ Threshold met! (3+ decisions)                 │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 5. Generate CLAUDE.md Proposal (if threshold met)   │
│    ├─ Read current src/auth/CLAUDE.md               │
│    ├─ Draft new section or updates                  │
│    ├─ Generate diff showing changes                 │
│    └─ Prepare rationale                             │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 6. Present to User                                   │
│    ├─ Confirm what was captured                     │
│    ├─ Show proposed CLAUDE.md updates (if any)      │
│    └─ Ask for approval                              │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 7. Optional GitHub Sync                              │
│    If --sync flag or user confirms:                 │
│    ├─ Generate progress summary                     │
│    ├─ Post as issue comment                         │
│    └─ Record sync timestamp                         │
└─────────────────────────────────────────────────────┘
```

### Example Output (without context update)

```
┌────────────────────────────────────────┐
│ 💾 Progress saved (14:30)              │
│                                         │
│ 📝 Captured:                           │
│ - 1 progress entry                     │
│ - 2 decisions                          │
│ - 1 learning                           │
└────────────────────────────────────────┘
```

### Example Output (with context update suggestion)

```
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
│ Proposed addition:                     │
│ ─────────────────────────────────      │
│ ## Rate Limiting                       │
│                                         │
│ - Use express-rate-limit middleware    │
│ - Redis store for distributed limiting │
│ - Limits: 5/15min for /login          │
│ - Exclude health checks                │
│ ─────────────────────────────────      │
│                                         │
│ This will help future work in auth/    │
│ have this rate limiting context ready. │
│                                         │
│ Add this to src/auth/CLAUDE.md?        │
│ [yes / edit / later / no]              │
└────────────────────────────────────────┘
```

---

## Workflow 3: Complete Work

### User Invocation
```
User: /keep:done
```

### System Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. Read Complete Work File                           │
│    Load .claude/work/{issue}.md:                    │
│    ├─ All progress entries                          │
│    ├─ All decisions made                            │
│    ├─ All learnings captured                        │
│    └─ Files modified list                           │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 2. Generate Comprehensive Summary                    │
│    ├─ What was accomplished (outcomes)              │
│    ├─ Why decisions were made (rationale)           │
│    ├─ What was learned (insights)                   │
│    ├─ Testing status                                │
│    └─ Follow-up needed (if any)                     │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 3. Check for Context Updates                         │
│    Review all learnings:                            │
│    ├─ Which CLAUDE.md files should be updated?      │
│    ├─ Generate proposed updates                     │
│    └─ Prepare diffs for review                      │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 4. Present Summary and Get Approvals                 │
│    ├─ Show work summary                             │
│    ├─ Show proposed CLAUDE.md updates               │
│    └─ Get user approval for updates                 │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 5. Sync to GitHub                                    │
│    ├─ Post completion comment with summary          │
│    ├─ Ask about closing issue                       │
│    └─ If confirmed: gh issue close {number}         │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 6. Archive Work File                                 │
│    mv .claude/work/{issue}.md                       │
│       .claude/archive/{issue}.md                    │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 7. Update State                                      │
│    .claude/state.md:                                │
│    ├─ Clear active issue                            │
│    ├─ Add to recent work                            │
│    └─ Update context (hot areas)                    │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 8. Recommend Next Work                               │
│    ├─ Fetch open issues from GitHub                 │
│    ├─ Score using algorithm                         │
│    ├─ Present top 3-5 recommendations                │
│    └─ Offer to start immediately                    │
└─────────────────────────────────────────────────────┘
```

### Example Output

```
┌────────────────────────────────────────┐
│ 🎉 Issue #1234 complete!               │
│                                         │
│ 📊 Summary:                            │
│ - 4 files modified                     │
│ - 5 decisions documented               │
│ - 3 learnings captured                 │
│ - All tests passing ✅                 │
│                                         │
│ 💡 Context updates:                    │
│ ✅ src/auth/CLAUDE.md (already done)   │
│                                         │
│ 🔗 Posting summary to GitHub...        │
│                                         │
│ Summary posted:                        │
│ https://github.com/user/repo/issues/   │
│ 1234#issuecomment-123456               │
│                                         │
│ Close issue #1234?                     │
│ [yes / no / later]                     │
└────────────────────────────────────────┘

User: yes

┌────────────────────────────────────────┐
│ ✅ Issue #1234 closed                  │
│                                         │
│ ⏭️  Recommended next work:             │
│                                         │
│ 🔥 Hot: #1250 - Add rate limit         │
│         monitoring                      │
│ ├─ Builds on #1234                     │
│ ├─ Same area: src/auth/                │
│ ├─ Labels: enhancement                 │
│ └─ Estimated: 2-3 hours                │
│                                         │
│ 📋 Other options:                      │
│ 2. #1245 - OAuth integration           │
│    └─ Same area, larger scope          │
│                                         │
│ 3. #1180 - Fix session bug [urgent]    │
│    └─ Different area, high priority    │
│                                         │
│ Start #1250?                           │
│ [yes / show more / choose different]   │
└────────────────────────────────────────┘
```

### GitHub Comment Format

What gets posted to the issue:

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

## Workflow 4: Recommend Next Work

### User Invocation
```
User: /keep:next
```

Or automatically after `/keep:done`

### System Flow

```
┌─────────────────────────────────────────────────────┐
│ 1. Fetch Open Issues                                 │
│    gh issue list --state open                       │
│         --json number,title,labels,body,updatedAt   │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 2. Load Context                                      │
│    ├─ Read .claude/state.md (recent work)           │
│    ├─ Read .claude/archive/ (last 3 completed)      │
│    └─ Note hot directories and patterns             │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 3. Score Each Issue                                  │
│    For each open issue:                             │
│    ├─ Continuity score (0-100)                      │
│    ├─ Priority score (0-100)                        │
│    ├─ Freshness score (0-100)                       │
│    ├─ Dependency score (0-100)                      │
│    └─ Weighted total                                │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 4. Sort and Select Top Recommendations              │
│    ├─ Sort by total score (descending)              │
│    ├─ Group: hot recommendation vs other options    │
│    └─ Select top 3-5 for presentation               │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 5. Prepare Rationale                                 │
│    For each recommendation:                         │
│    ├─ Why it scores high                            │
│    ├─ Relationship to recent work                   │
│    ├─ Effort estimate (if possible)                 │
│    └─ Key labels/priorities                         │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 6. Present Recommendations                           │
│    ├─ Top recommendation with detail                │
│    ├─ Other good options (brief)                    │
│    └─ Offer to start, show more, or choose other    │
└─────────────────────────────────────────────────────┘
```

### Scoring Details

```python
# Continuity Score (0-100)
continuity = 0
if same_directory(issue, recent_work):
    continuity += 50
if overlapping_labels(issue, recent_work):
    continuity += 30
if similar_tech(issue, recent_work):
    continuity += 20

# Priority Score (0-100)
if "urgent" in labels:
    priority = 100
elif "high-priority" in labels:
    priority = 75
elif "medium" in labels or no priority label:
    priority = 50
else:  # "low-priority"
    priority = 25

# Freshness Score (0-100)
days_since_update = (now - issue.updated_at).days
if days_since_update <= 7:
    freshness = 100
elif days_since_update <= 14:
    freshness = 75
elif days_since_update <= 30:
    freshness = 50
else:
    freshness = 25

# Dependency Score (0-100)
dependency = 100  # Assume unblocked
blockers = find_blockers(issue.body)  # Parse "depends on #123"
for blocker_id in blockers:
    blocker_issue = get_issue(blocker_id)
    if blocker_issue.state == "open":
        dependency -= 25  # Reduce for each open blocker

# Weighted Total
score = (
    continuity * 0.30 +
    priority * 0.30 +
    freshness * 0.20 +
    dependency * 0.20
)
```

### Example Output

```
┌────────────────────────────────────────┐
│ 🎯 Recommended Next Work               │
│                                         │
│ 🔥 Hot Recommendation:                 │
│ #1250 - Add monitoring for rate limits │
│ ├─ Score: 92/100                       │
│ ├─ Builds directly on #1234 (just done)│
│ ├─ Same area: src/auth/                │
│ ├─ Context is fresh in memory          │
│ └─ Estimated: 2-3 hours                │
│                                         │
│ 📋 Other Good Options:                 │
│                                         │
│ 2. #1245 - OAuth integration [high]    │
│    └─ Score: 78 | Same area, larger    │
│       scope (1-2 days)                 │
│                                         │
│ 3. #1180 - Fix session bug [urgent]    │
│    └─ Score: 75 | Different area but   │
│       marked urgent                    │
│                                         │
│ 4. #1300 - Add API documentation       │
│    └─ Score: 55 | No blockers, medium  │
│       priority                         │
│                                         │
│ Start #1250?                           │
│ [yes / show more / choose different]   │
└────────────────────────────────────────┘
```

---

## Error Handling Workflows

### GitHub Unavailable

```
┌─────────────────────────────────────────────────────┐
│ Attempt GitHub Operation                             │
│    gh issue view 1234                               │
└──────────────┬──────────────────────────────────────┘
               │
               ▼ [Error]
┌─────────────────────────────────────────────────────┐
│ Check Error Type                                     │
│    ├─ gh not installed                              │
│    ├─ Network error                                 │
│    └─ Rate limit                                    │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ Graceful Degradation                                 │
│    ├─ Warn user about limitation                    │
│    ├─ Offer local-only mode                         │
│    ├─ Continue workflow without GitHub              │
│    └─ Note sync needed for later                    │
└─────────────────────────────────────────────────────┘
```

**Example:**
```
⚠️  GitHub unavailable (gh not found)

I'll continue in local-only mode. You can:
• Manually provide issue details
• Work without issue tracking
• Install gh CLI later and sync

Continue? [yes / abort]
```

### Corrupted State File

```
┌─────────────────────────────────────────────────────┐
│ Attempt to Read .claude/state.md                    │
└──────────────┬──────────────────────────────────────┘
               │
               ▼ [Parse Error]
┌─────────────────────────────────────────────────────┐
│ Detect Corruption                                    │
│    ├─ Invalid format                                │
│    ├─ Missing sections                              │
│    └─ Conflicting data                              │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ Reconstruct from Work Files                          │
│    ├─ Check .claude/work/ for active issues         │
│    ├─ Check .claude/archive/ for recent work        │
│    └─ Rebuild state.md from available data          │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ Notify User                                          │
│    ├─ Explain what was repaired                     │
│    ├─ Show reconstructed state                      │
│    └─ Ask for confirmation                          │
└─────────────────────────────────────────────────────┘
```

**Example:**
```
⚠️  State file corrupted, reconstructed from work files

Found active work:
• #1234 - Add rate limiting (started 2024-10-23)

Recent work:
• #1200 - Authentication (completed 2024-10-22)

Does this look correct? [yes / no]
```

---

## Advanced Workflows

### Creating New CLAUDE.md

**Triggered by:**
- User runs `/keep:grow src/payments/`
- Keep detects threshold (2+ sessions in directory)
- Keep notices missing context in active area

```
┌─────────────────────────────────────────────────────┐
│ 1. Analyze Directory                                 │
│    ├─ Scan file names and types                     │
│    ├─ Read key files (exports, interfaces)          │
│    ├─ Identify patterns and abstractions            │
│    └─ Detect frameworks/libraries in use            │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 2. Assess Value                                      │
│    ├─ Is this a cohesive module?                    │
│    ├─ Are patterns clear enough?                    │
│    ├─ Would future work benefit?                    │
│    └─ Is it too early? (avoid premature docs)       │
└──────────────┬──────────────────────────────────────┘
               │
               ▼ [If valuable]
┌─────────────────────────────────────────────────────┐
│ 3. Generate Proposal                                 │
│    Draft CLAUDE.md with:                            │
│    ├─ Purpose                                       │
│    ├─ Key Patterns                                  │
│    ├─ API/Interface                                 │
│    ├─ Recent Learnings (from current work)          │
│    └─ Dependencies and Testing                      │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 4. Present for Review                                │
│    ├─ Show complete proposed content                │
│    ├─ Explain benefit                               │
│    └─ Offer: create / edit / skip                   │
└──────────────┬──────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────────────┐
│ 5. Create File (if approved)                         │
│    ├─ Write src/payments/CLAUDE.md                  │
│    ├─ Confirm creation                              │
│    └─ Note auto-loading for future work             │
└─────────────────────────────────────────────────────┘
```

**Example Output:**
```
┌────────────────────────────────────────┐
│ 📝 Proposed CLAUDE.md for src/payments/│
│                                         │
│ I've analyzed src/payments/ and found  │
│ clear patterns worth documenting:      │
│                                         │
│ • Stripe API integration               │
│ • Webhook validation pattern           │
│ • Idempotency key usage                │
│ • Payment record repository            │
│                                         │
│ [Full proposed content shown...]       │
│                                         │
│ Create src/payments/CLAUDE.md?         │
│ [yes / edit / later / no]              │
│                                         │
│ This will help future work in payments/│
│ have immediate context about patterns. │
└────────────────────────────────────────┘
```

---

## Summary

These workflows show Keep in action:
- **Start**: Fetch issue, load context, create tracking, present starting point
- **Save**: Capture progress/learnings, suggest context updates, optional sync
- **Done**: Summarize, sync to GitHub, archive, recommend next
- **Next**: Score open issues, recommend based on context and continuity
- **Grow**: Create CLAUDE.md when patterns emerge

All workflows degrade gracefully when GitHub unavailable, preserve user data, and respect user control through approval gates.
