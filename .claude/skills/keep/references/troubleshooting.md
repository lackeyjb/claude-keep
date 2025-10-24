# Keep Troubleshooting Guide

Error handling, recovery procedures, and graceful degradation strategies for Keep.

---

## GitHub Issues

### GitHub CLI Not Installed

**Symptom:**
```
Error: gh: command not found
```

**Detection:**
```bash
which gh  # Returns empty
```

**Response:**
```markdown
⚠️  GitHub CLI not installed

Keep can work in local-only mode:
• Track work locally in .claude/work/
• Manually sync to GitHub later
• Install gh CLI anytime to enable GitHub features

Continue in local-only mode? [yes / abort]
```

**Graceful degradation:**
- Continue with all local operations
- Skip GitHub fetching/posting
- Note in work files that sync needed
- Remind user periodically about GitHub features

---

### Network Errors

**Symptoms:**
```
Error: failed to fetch issue: network unreachable
Error: timeout connecting to api.github.com
```

**Response:**
```markdown
⚠️  GitHub unavailable (network error)

Work saved locally:
• .claude/work/{issue}.md updated
• .claude/state.md updated

Will sync to GitHub when connection restored.

Continue working? [yes / abort]
```

**Graceful degradation:**
- Save all progress locally
- Mark work files with "sync pending"
- Offer retry on next operation
- Continue full workflow without GitHub

---

### Rate Limiting

**Symptom:**
```
Error: API rate limit exceeded for user
```

**Detection:**
Parse error response from `gh` commands

**Response:**
```markdown
⚠️  GitHub API rate limit exceeded

Rate limit resets at: {reset_time}

You can:
1. Wait {minutes} minutes
2. Continue in local-only mode
3. Use cached/local data

Continue with local-only mode? [yes / wait / abort]
```

**Graceful degradation:**
- Use cached issue data if available
- Continue with local operations
- Retry GitHub ops after reset time

---

### Authentication Errors

**Symptoms:**
```
Error: authentication required
Error: HTTP 401: Unauthorized
```

**Response:**
```markdown
⚠️  GitHub authentication failed

Please authenticate:
  gh auth login

Or continue in local-only mode.

[retry / local-only mode / abort]
```

**Graceful degradation:**
- Switch to local-only mode
- Note that sync will require auth
- Remind user to authenticate later

---

## File System Issues

### Corrupted State File

**Symptom:**
- `.claude/state.md` has invalid format
- Missing required sections
- Conflicting data

**Detection:**
- Markdown parse errors
- Missing required fields
- Active issue mismatch with work files

**Recovery:**
```markdown
⚠️  State file corrupted - reconstructing from work files

Found active work:
• #1234 - Add rate limiting (started 2024-10-23)

Recent work:
• #1200 - Authentication (completed 2024-10-22)

Reconstructed state:
[Show reconstructed state.md content]

Does this look correct? [yes / no / edit]
```

**Recovery procedure:**
1. Check `.claude/work/` for active issues (not archived)
2. Check `.claude/archive/` for recent completed work (last 3)
3. Rebuild state.md structure
4. Populate with discovered data
5. Show user for confirmation
6. Save reconstructed state

**Preserve user data:**
- Backup corrupted file to `.claude/state.md.backup`
- Never silently delete
- Ask user to confirm reconstruction

---

### Missing Work File

**Symptom:**
- `state.md` references issue but no work file exists
- User tries to save progress but no active work file

**Response:**
```markdown
⚠️  Work file missing for issue #1234

I can recreate it from:
1. GitHub issue (if available)
2. Git history
3. Fresh start

Choose recovery method: [github / fresh / abort]
```

**Recovery options:**

**Option 1: From GitHub**
1. Fetch issue details via `gh issue view`
2. Create new work file with issue data
3. Note in work file: "Recreated {timestamp}"
4. Continue normally

**Option 2: Fresh start**
1. Create minimal work file
2. Prompt user for context
3. Continue from current point

---

### Conflicting State

**Symptom:**
- Active work in state.md but work file is archived
- Multiple work files not archived
- Branch doesn't match active issue

**Detection:**
Compare state.md with file system state

**Response:**
```markdown
⚠️  State conflict detected

State says: #1234 active
Found: .claude/archive/1234.md (archived)

Possible causes:
• /keep-done ran but state update failed
• Manual file operations

Fix by:
1. Clear active work from state (mark #1234 complete)
2. Restore #1234 to active (un-archive)

Choose resolution: [1 / 2 / manual review]
```

**Resolution:**
- Present user with options
- Never auto-resolve ambiguity
- Explain what each choice does
- Preserve all data

---

### Permission Errors

**Symptom:**
```
Error: EACCES: permission denied, open '.claude/work/1234.md'
```

**Response:**
```markdown
⚠️  Permission denied writing to .claude/work/

Check file permissions:
  ls -la .claude/work/

Required permissions:
  User needs write access to .claude/ directory

[retry after fixing / abort]
```

**Graceful degradation:**
- Not applicable (can't continue without write access)
- Guide user to fix permissions
- Offer to retry after fix

---

## Data Integrity

### Preserve User Data - Golden Rule

**Never silently:**
- Delete files
- Overwrite without backup
- Discard user content

**Always:**
- Backup before destructive operations
- Warn user of data loss
- Ask confirmation for ambiguous operations
- Preserve original data somewhere

**Backup pattern:**
```bash
# Before overwriting corrupted file
cp .claude/state.md .claude/state.md.backup.{timestamp}
# Then recreate
```

---

### Validation Before Destructive Operations

**Before archiving work file:**
1. Confirm work is complete
2. Verify state.md updated
3. Confirm GitHub synced (if online)
4. Only then move to archive

**Before overwriting state.md:**
1. Validate new state structure
2. Backup existing file
3. Write new file
4. Verify readable

---

## Git Issues

### Detached HEAD State

**Symptom:**
```
warning: You are in 'detached HEAD' state
```

**Response:**
```markdown
⚠️  Git is in detached HEAD state

Keep can still work, but commits won't be on a branch.

Suggested fix:
  git checkout -b feature/issue-1234

Continue anyway? [yes / fix first]
```

---

### Merge Conflicts in .claude/

**Symptom:**
```
<<<<<<< HEAD
**Current Issue:** #1234
=======
**Current Issue:** #1235
>>>>>>> feature-branch
```

**Response:**
```markdown
⚠️  Merge conflict in .claude/state.md

Keep cannot resolve this automatically.

Please resolve the conflict manually:
  1. Edit .claude/state.md
  2. Remove conflict markers
  3. Keep correct active issue
  4. Run /keep-save to validate

[done - retry / abort]
```

**Prevention:**
- Recommend: Don't work on multiple issues in parallel
- Use feature branches per issue
- Complete work before switching

---

## Recovery Commands

### Validate State

If user reports issues, validate state:

```bash
# Check state file exists and is readable
cat .claude/state.md

# Check for active work files
ls -la .claude/work/

# Check recent archives
ls -la .claude/archive/ | head -5

# Verify GitHub connectivity
gh auth status
gh issue list --limit 1
```

### Rebuild Index

If state is completely lost:

```bash
# Find all work files
find .claude/work/ -name "*.md"

# Find recent archives (last 30 days)
find .claude/archive/ -name "*.md" -mtime -30

# Use to rebuild state.md
```

### Clear Stuck State

If state is irrecoverably broken:

```markdown
⚠️  State cannot be recovered automatically

Recommended: Start fresh
1. Backup: cp .claude/state.md .claude/state.md.broken
2. Delete: rm .claude/state.md
3. Restart: /keep-start {issue-number}

Proceed? [yes / manual recovery]
```

---

## Error Messages

### User-Friendly Format

**Good error messages:**
```markdown
⚠️  {What went wrong}

{Why this happened (if known)}

{What user can do about it}

[Action choices]
```

**Example:**
```markdown
⚠️  Cannot save progress - no active work

This happens when:
• No issue is currently being worked on
• Work was completed but state not updated

To fix:
• Start new work: /keep-start {issue-number}
• Resume existing: /keep-start {issue-number}

What would you like to do?
```

### Avoid Technical Jargon

**Bad:**
```
Error: ENOENT: no such file or directory, open '.claude/work/undefined.md'
```

**Good:**
```markdown
⚠️  Work file not found

I couldn't find a work file for the current issue.

This usually means work hasn't been started yet.

Start work with: /keep-start {issue-number}
```

---

## Testing Error Scenarios

When implementing error handling, test these scenarios:

**GitHub:**
- [ ] gh CLI not installed
- [ ] Network offline
- [ ] Rate limit exceeded
- [ ] Authentication failed
- [ ] Repository not found
- [ ] Issue doesn't exist

**File System:**
- [ ] state.md corrupted
- [ ] state.md missing
- [ ] work file missing
- [ ] Permission denied
- [ ] Disk full
- [ ] Conflicting work files

**Git:**
- [ ] Detached HEAD
- [ ] Merge conflicts in .claude/
- [ ] Dirty working directory
- [ ] No git repo
- [ ] Corrupted git state

**Data:**
- [ ] Invalid timestamps
- [ ] Malformed markdown
- [ ] Missing required sections
- [ ] Conflicting state data

---

## Philosophy

**Fail gracefully:**
- Degrade features, don't break workflows
- Continue with reduced functionality
- Never lose user data

**Be transparent:**
- Explain what went wrong
- Explain why it matters
- Explain options to fix

**Preserve state:**
- Backup before destructive operations
- Never silently delete or overwrite
- Ask user to resolve ambiguity

**Guide recovery:**
- Offer specific fix suggestions
- Provide commands when helpful
- Link to documentation if complex

**Learn and prevent:**
- Log common errors
- Add validation to prevent recurrence
- Improve error messages based on user feedback
