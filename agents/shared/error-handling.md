# Error Handling Patterns

Common error scenarios and recovery strategies for Keep workflows.

## GitHub Unavailable

**Check availability first:**
```bash
which gh
```

**If missing or network error:**
- Warn user that GitHub is unavailable
- Offer local-only mode (continue workflow without GitHub)
- Continue without GitHub
- Note that sync will be needed for later

**Recovery:**
- Cache all work locally
- Retry operations only if GitHub becomes available
- Don't fail the entire workflow

## Issue Not Found

**When GitHub returns 404 or issue doesn't exist:**
- Verify issue number with user
- Suggest checking GitHub web UI directly
- Offer to create new issue if needed
- Or offer to continue working locally without tracking

## Corrupted State Files

**If `.claude/state.md` is invalid (malformed YAML/markdown):**
1. Back up to `.claude/state.md.backup` (never silently delete)
2. Reconstruct state from available work files in `.claude/work/`
3. Show reconstructed state to user for confirmation
4. Ask user to approve before using reconstructed version

**If work file is corrupted:**
1. Back up to `.claude/work/{issue}.md.backup`
2. Attempt to repair based on GitHub issue data
3. Show reconstructed content for user confirmation
4. Get explicit approval before overwriting

**General principle:** Never silently delete or lose user data.

## Work File Issues

**Missing work file that state.md references:**
- Check if state.md active issue exists in `.claude/work/`
- If file missing but state says active: offer to recreate from GitHub
- If truly no files: inform user and suggest `/keep:start`

## File Operations

**If directory creation fails:**
- Check permissions
- Note issue clearly
- Exit gracefully (don't fail workflow)

**If file write fails:**
- Try backup location
- Inform user about the issue
- Preserve what was successfully written
- Never overwrite without success

## GitHub Rate Limiting

**If rate limit hit:**
- Note how long until reset
- Continue with local-only work
- Don't fail the workflow
- Suggest retrying later

## General Principles

- **Fail gracefully:** Degrade features, don't break the entire workflow
- **Preserve data:** Never lose user work due to errors
- **Be clear:** Inform user of failures, don't hide problems
- **Offline first:** Support local-only mode when GitHub unavailable
- **Recoverable:** Design all operations to be retryable

See `skills/keep/references/troubleshooting.md` for detailed error handling and recovery patterns - load only when encountering errors.
