# Output Template: Backend Requirements

Save to: `.claude/docs/ai/<feature-name>/backend-requirements.md`

---

```markdown
# Backend Requirements: <Feature Name>

**Author**: [frontend dev name or team]
**Date**: [YYYY-MM-DD]
**Status**: Draft / In Review / Agreed

## Context

[What we're building, who uses it, and what problem it solves. 2-4 sentences.
Include: user type, the workflow they're in, and why this data matters to them.]

## Screens / Components

### <Screen or Component Name>

**Purpose**: [One sentence — what this screen does for the user]

**Data I need to display**:
- [Description of data piece — describe it in user-facing terms, not field names]
- [Another piece — note any relationship: "for each X, I also need its Y"]
- [Note if anything is computed/derived vs. stored]

**Actions the user can perform**:
- [Action] → [Immediate feedback user sees] → [Expected outcome after completion]
- [Another action] → ...

**States I need to handle**:
- **Loading**: [What's being fetched; what the user sees during load]
- **Empty**: [When/why this happens; what the user sees]
- **Error**: [What can go wrong; what error message or fallback the user sees]
- **Special**: [Any edge case states: partial data, expired items, permission-blocked, etc.]

**Business rules affecting UI**:
- [Rule that changes what's visible or enabled — e.g., "Delete button only shows for admin users"]
- [Date-based or count-based rules]
- [Anything you're not sure about — flag it]

---

### <Next Screen or Component>

[Repeat structure above]

---

## Uncertainties

Things I'm not sure about — please help clarify:

- [ ] Not sure if [X] should appear when [Y condition] — guessing yes, but could be wrong
- [ ] Don't understand the business rule for [Z] — assuming it works like [A], let me know
- [ ] Is [B] always present, or can it be null? I'm not handling null today but can add it

## Questions for Backend

Open questions — push back or suggest a better approach:

- Would it make sense to combine [X] and [Y] into a single call, or does that create problems on your end?
- Should I expect [Z] to always be present, or do I need to handle it being missing?
- Is there existing data I can reuse for [W], or will this require new work?
- I'm thinking of [approach] — does that make your life harder or easier?

## Discussion Log

[Add backend responses, decisions, and agreed changes here as the conversation progresses]

| Date | From | Note |
|------|------|------|
| [date] | [name] | [decision or response] |
```
