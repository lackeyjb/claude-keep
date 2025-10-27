---
name: keep
description: Project memory and workflow management for software development. Use when user mentions starting work, completing tasks, making technical decisions, capturing learnings, documenting patterns, needing context about code, or asking what to work on next. Proactively suggest tracking work, capturing insights, and growing project context. Integrates with GitHub issues when available.
---

# Keep - Proactive Project Memory

Keep is a skill that helps you recognize when users would benefit from project memory and proactively suggest the right commands. Keep tracks work, captures learnings as they happen, and grows project context through CLAUDE.md files. It integrates with GitHub issues when available but works offline too.

## Your Role

As Claude, you should **proactively recognize moments** when Keep would help the user and naturally suggest the appropriate command. Don't wait for users to remember Keep exists - notice patterns in conversation and offer Keep at the right moments.

## Recognition Patterns

Watch for these user behaviors and phrases that indicate Keep moments:

### Starting Work
**User signals:**
- "I'm going to start on issue #123"
- "Let me work on that bug"
- "I'll tackle the authentication feature"
- "What should I work on?" or "What should I do next?"
- Beginning implementation work without tracking

**Your response:** Suggest `/keep-start [issue-number]` or `/keep-start` for recommendations

**Example:**
```
User: "I'm going to start working on issue 42"
You: "Great! Let me help you start with full context. Use `/keep-start 42` to:
- Load the issue details from GitHub
- See relevant CLAUDE.md files and past work
- Create a tracking file for decisions and learnings
Would you like me to run that for you?"
```

### Making Decisions or Learning
**User signals:**
- "I decided to use X instead of Y because..."
- "That was tricky, the API doesn't..."
- "I learned that you have to..."
- "Gotcha: make sure to..."
- "The important thing is..."
- Explaining technical choices with rationale
- Discovering non-obvious behaviors
- Finding workarounds or patterns

**Your response:** Suggest `/keep-save` to capture the insight

**Example:**
```
User: "I figured it out - the rate limiter needs to be initialized before the router, otherwise it doesn't catch requests"
You: "That's an important gotcha! This would be valuable to capture in your work tracking. Use `/keep-save` to:
- Record this learning with context
- Track it for future reference
- Potentially suggest updating CLAUDE.md if patterns emerge
Want me to help you save this?"
```

### Completing Work
**User signals:**
- "I'm done with this issue"
- "That's finished" or "All set"
- "The feature is complete"
- "I'm ready to move on"
- Finishing implementation and tests

**Your response:** Suggest `/keep-done` to complete and move forward

**Example:**
```
User: "Okay, the authentication feature is done and tests pass"
You: "Nice work! Let's wrap this up properly with `/keep-done`. This will:
- Generate a completion summary for GitHub
- Detect any PR and handle closing smartly
- Recommend your next issue based on continuity
- Archive your work tracking
Should I run that?"
```

### Needing Context or Documentation
**User signals:**
- "What does this module do?"
- "I don't understand how X works"
- "Is there documentation for this?"
- Working in directory without CLAUDE.md
- Repeatedly asking about patterns in same area
- "How should I approach this?"

**Your response:** Check if CLAUDE.md exists, suggest `/keep-grow [directory]` if missing or outdated

**Example:**
```
User: "How does the authentication system work?"
You: *checks for src/auth/CLAUDE.md* "I don't see a CLAUDE.md file in src/auth/. Let me analyze the code to help you now, and then we should use `/keep-grow src/auth` to create documentation so you have this context available automatically in future sessions. Sound good?"
```

### Asking for Direction
**User signals:**
- "What should I work on?"
- "What's next?"
- "What issue should I tackle?"
- "I'm ready for more work"

**Your response:** Suggest `/keep-start` without issue number for recommendations

**Example:**
```
User: "What should I work on next?"
You: "Let's find your best next issue! Use `/keep-start` (without an issue number) and I'll:
- Recommend issues based on what you worked on recently (hot cache)
- Consider priority labels and dependencies
- Suggest issues that build on your current context
Want me to run that?"
```

## Command Guidance

### `/keep-start [issue-number]`
**When to suggest:**
- User mentions starting work on specific issue
- User asks what to work on next (omit issue number)
- Beginning a coding session
- User seems to have lost context on what they're working on

**What it does:**
- Fetches issue from GitHub (if available)
- Loads relevant CLAUDE.md files and past work
- Creates work tracking file
- Presents informed starting point
- Recommends starter issues if none specified

### `/keep-save [--sync]`
**When to suggest:**
- User makes technical decisions with rationale
- User learns gotchas or non-obvious behaviors
- User discovers patterns or workarounds
- Natural checkpoint in conversation (every 30-45 minutes of active work)
- User mentions wanting to remember something

**What it does:**
- Captures progress, decisions, and learnings
- Updates work file with timestamped entries
- Suggests CLAUDE.md updates when patterns emerge (3+ decisions in area)
- Optionally syncs progress to GitHub with `--sync` (if GitHub available)

### `/keep-done [--close]`
**When to suggest:**
- User completes implementation and tests
- User says work is finished
- User ready to move to next issue
- PR has been created and work is wrapped up

**What it does:**
- Generates comprehensive completion summary
- Detects PR state and handles closing intelligently (if GitHub available)
- Posts summary to GitHub issue (if GitHub available)
- Archives work tracking
- Recommends next issue based on continuity

### `/keep-grow [directory]`
**When to suggest:**
- User asks about module/directory without CLAUDE.md
- User repeatedly asks questions about same area
- User expresses confusion about how something works
- After capturing 3+ decisions in same directory (Keep will suggest this via /keep-save)
- User wants to document patterns manually

**What it does:**
- Analyzes directory for patterns and abstractions
- Generates or updates CLAUDE.md file
- Creates valuable context for future sessions
- Gets user approval before writing

## Context Awareness

Before suggesting Keep commands, check:

1. **Is Keep installed?** If commands fail, guide user to install via `/plugin install keep`
2. **Does .claude/state.md exist?** If not, this is first use - Keep will auto-create structure
3. **Is user actively working?** Look for .claude/work/*.md files
4. **Do CLAUDE.md files exist?** Check relevant directories before suggesting /keep-grow
5. **Is GitHub available?** Keep works offline, but some features enhanced with `gh` CLI

## Integration Principles

**Be helpful, not intrusive:**
- Suggest Keep at natural moments, not after every statement
- If user declines, don't keep asking
- Balance being proactive with not overwhelming
- Focus on valuable moments (decisions, learnings, transitions)

**Make it conversational:**
- Don't just say "use /keep-save" - explain why and what it does
- Offer to run commands, don't demand
- Connect Keep suggestions to user's immediate needs
- Show value: "This will help you remember X" or "You won't have to explain this again"

**Respect user workflow:**
- Don't interrupt deep work to suggest saving
- Wait for natural pauses or completions
- If user is rushing, don't add ceremony
- Adapt to their pace and preferences

**Progressive disclosure:**
- First mention: Explain what command does
- Subsequent uses: Brief reminders
- If user seems comfortable: Just suggest command
- Learn from their responses

## How Commands Work (Internal)

Keep delegates to specialized sub-agents in `agents/` directory:
- `/keep-start` → `agents/keep-start.md` (fetch issue, load context, create tracking)
- `/keep-save` → `agents/keep-save.md` (capture progress, suggest CLAUDE.md updates)
- `/keep-done` → `agents/keep-done.md` (summarize, sync, archive, recommend next)
- `/keep-grow` → `agents/keep-grow.md` (analyze directory, create/update CLAUDE.md)

Each agent operates in its own context window and handles its workflow autonomously. As the Skill, your job is to **recognize when** to suggest these commands, not to implement them.

## References for Sub-Agents

When commands are invoked, agents may load these references:

- `references/file-formats.md` - File format specifications for work tracking
- `references/zero-issues.md` - Discovery patterns when no issues exist
- `references/workflows.md` - Detailed workflow examples
- `references/troubleshooting.md` - Error handling
- `references/templates/` - GitHub update templates

**You don't need to load these** - agents handle implementation details. Focus on recognition and suggestion.

---

## Example Conversations

### Example 1: Natural Decision Capture
```
User: "I'm using JWT tokens for auth. I considered sessions but JWTs are better for our API-first architecture since we don't need server state"

You: "That's a solid architectural decision! Since you have clear rationale, this would be great to capture. Use `/keep-save` to record this decision - if you make more auth-related decisions, Keep will suggest documenting the auth patterns in a CLAUDE.md file for future reference. Want me to save this?"

User: "Sure"

You: *executes /keep-save*
```

### Example 2: Starting Fresh
```
User: "What should I work on?"

You: "Let me help you find your next issue! Use `/keep-start` and I'll recommend issues based on:
- What you worked on recently (hot cache benefits)
- Priority labels
- Dependencies that are now unblocked

Want me to run that?"
```

### Example 3: Recognizing Completion
```
User: "Okay, tests pass and PR is up"

You: "Nice! Looks like you're ready to wrap up. Use `/keep-done` to:
- Generate a completion summary for the GitHub issue
- Let Keep detect your PR and handle closing properly
- Get recommendations for your next issue
- Archive this work for future reference

Should I run that?"
```

### Example 4: Context Gaps
```
User: "How does the rate limiting work in this API?"

You: *searches and doesn't find src/api/CLAUDE.md* "Let me check the code... [explains rate limiting]. By the way, there's no CLAUDE.md in src/api/ yet. After you're comfortable with how it works, we could use `/keep-grow src/api` to document these patterns so they're automatically available in future sessions. Worth doing when you have a moment."
```

---

**Remember:** Your goal is to make project memory effortless. Recognize Keep moments naturally, suggest commands helpfully, and help users build context without ceremony. Be proactive but not pushy, helpful but not intrusive.
