# Quality Filters for Context Documentation

Standards for deciding what's worth capturing in CLAUDE.md files.

## The 6-Month Test

Before suggesting CLAUDE.md updates, ask: **"Would this matter to me 6 months from now?"**

This is the primary filter for all learnings and patterns.

## High-Value Content (DO Capture)

These are worth documenting:

- **Non-obvious gotchas and surprises:** Things that surprised you or are unintuitive
- **Security or performance implications:** Critical for system integrity
- **Architectural decisions with lasting impact:** "Why" decisions that affect code structure
- **Patterns that prevent common mistakes:** Lessons learned from failures
- **Framework/library quirks worth remembering:** Non-obvious behaviors of dependencies
- **Recurring patterns:** Issues or solutions that appear multiple times
- **Critical patterns that work well:** Proven approaches in this codebase

## Low-Value Content (DON'T Capture)

These don't need documenting:

- **Implementation details visible in code:** Anyone reading code can see this
- **Obvious patterns anyone would use:** Standard ways of doing things
- **Temporary workarounds or hacks:** Code-level fixes, not patterns
- **Tool installation steps:** In package.json, setup docs, or README
- **Standard framework usage:** How to use libraries per their docs
- **File paths/structure:** Visible via `ls` and directory browsing
- **Generic best practices:** Advice available everywhere
- **API documentation:** Use code comments instead

## Examples: Good vs Bad

### Save/Done/Grow Learnings

❌ "Used express-rate-limit for rate limiting"
- Obvious from code, visible in package.json

✅ "express-rate-limit auto-adds X-RateLimit-* headers - don't manually set them"
- Non-obvious gotcha, prevents mistakes

---

❌ "Created middleware in src/auth/middleware/"
- Visible in file structure

✅ "Health checks must exclude rate limiting or monitoring breaks"
- Important pattern, gotcha worth remembering

---

❌ "Updated CORS configuration"
- Implementation detail

✅ "CORS must allow internal origin for health checks or load balancer fails"
- Critical pattern, prevents production issues

### Grow Analysis

❌ "Module has 5 files total"
- Obvious from scanning directory

✅ "Authentication module uses custom token validation - doesn't follow standard middleware pattern"
- Non-obvious design decision

---

❌ "Entry point is index.js"
- Visible in file listing

✅ "Entry point handles both ES6 and CommonJS imports for compatibility with legacy code"
- Architectural decision, gotcha to know

## Learning Threshold Detection

For Save workflow, count decisions by directory:

- **3+ decisions** in same directory → Suggest CLAUDE.md update
- **2+ sessions** in same directory → Consider new CLAUDE.md
- **Recurring patterns** → Document in relevant CLAUDE.md
- **Security/performance insights** → Always capture

## Quality Assessment Criteria

Ask these questions about each learning:

1. **Is it non-obvious?** Does it surprise developers unfamiliar with the code?
2. **Will it prevent mistakes?** Does it help avoid common pitfalls?
3. **Is it durable?** Will this still matter in 6 months?
4. **Is it specific?** Does it apply to this codebase, not everywhere?
5. **Is it actionable?** Can developers use this guidance?

**If all 5 are yes:** Include it.
**If 3+ are yes:** Consider including it.
**If fewer than 3 are yes:** Skip it.

## Writing Style for Quality Content

- Use bullets, not paragraphs
- 1 line per point when possible
- Examples only for non-obvious cases
- Focus on "why" and "watch out for"
- Be ruthlessly concise

## Decision Capture Quality

**What makes a good decision capture:**
- Include the choice AND the rationale
- Note alternatives considered
- Explain impact on codebase
- Be specific to this project

**Format:**
```markdown
{number}. **{decision}:** {rationale}
   - Alternative considered: {alternative} (rejected because {reason})
   - Impact: {what this affects}
```

## Learning Capture Quality

**What makes a good learning:**
- Focus on non-obvious insights
- Document gotchas to avoid
- Note patterns that work well
- Be specific to this project

**Format:**
```markdown
- {insight or gotcha}
```

## Evolution Over Time

Good CLAUDE.md files:
- Start empty or minimal
- Grow based on actual learnings
- Remove outdated information
- Evolve as the code evolves
- Stay focused and concise

Bad CLAUDE.md files:
- Comprehensive documentation of everything
- Detailed guides for obvious things
- Outdated information retained
- Generic advice mixed with specific insights
