---
description: Output templates for the lesson-learned skill. Load during Phase 4 when formatting the final lesson presentation.
---

# Output Templates

## Primary Lesson (always present)

```markdown
## Lesson: [Principle Name]

**What happened in the code:**
[2-3 sentences describing the specific change, referencing files and commits]

**The principle at work:**
[1-2 sentences explaining the SE principle]

**Why it matters:**
[1-2 sentences on the practical consequence — what would go wrong without this, or what goes right because of it]

**Takeaway for next time:**
[One concrete, actionable sentence the user can apply to future work]
```

## Secondary Lessons (maximum 2, optional)

```markdown
---

### Also worth noting: [Principle Name]

**In the code:** [1 sentence pointing to specific file/line]
**The principle:** [1 sentence]
**Takeaway:** [1 sentence]
```

## Trivial Changes (no lesson)

Use when the diff contains only config tweaks, typo fixes, dependency bumps, or trivial reformatting:

```markdown
These changes are straightforward — no deep lesson here, just good housekeeping.

[Optional: 1 sentence noting what was done, e.g., "Bumped dependency versions and fixed a typo in the README."]
```

## Anti-Pattern Found

Use when the primary observation is a code smell, not a positive pattern:

```markdown
## Observation: [Anti-Pattern Name]

**What the code shows:**
[2-3 sentences describing the specific signal observed in the diff]

**The concern:**
[1-2 sentences explaining why this pattern creates problems]

**One thing to try next time:**
[One concrete, non-judgmental suggestion]
```

## Formatting Rules

- Always reference specific file names and commit SHAs or short hashes
- Never use "you should have" — use "next time, consider..." or "the code here shows..."
- Lead with what works before noting what could improve
- Cap total output at 3 lessons (1 primary + 2 secondary); more dilutes the insight
- If the lesson is about an anti-pattern, still find something positive to anchor first
