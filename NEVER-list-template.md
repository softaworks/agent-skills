# NEVER List Template — agent-toolkit Canonical Standard

## Purpose

NEVER lists encode hard-earned practitioner knowledge about failure modes that are not obvious from documentation, type signatures, or surface-level reading of code. They exist because some mistakes are silent, some consequences are delayed, and some anti-patterns look correct until they destroy something in production.

A vague NEVER item ("NEVER do X — it causes errors") is nearly worthless. The value is in the mechanism: WHY does it fail, and HOW does it fail in a way that would surprise a competent engineer? NEVER items must name the non-obvious consequence — the corrupted state, the silent discard, the race condition, the phantom retry — so the reader understands the failure mode, not just the prohibition.

## Format Standard

Each NEVER item must contain two parts:

1. **The specific thing to avoid** — not a category, not a vague verb. Name the exact action, flag, parameter pattern, call sequence, or assumption.
2. **The non-obvious reason WHY** — not "it causes errors" or "it breaks things." Explain the mechanism: what gets corrupted, what gets silently ignored, what downstream system misreads the output, what timing assumption breaks.

Template structure:

```
- NEVER [specific action or pattern] — because [precise mechanism of failure from practitioner experience]
```

Both parts are required. An item missing either part must be revised before it is accepted into a SKILL.md.

### Bullet format is mandatory (not numbered)

Each NEVER item **MUST** be a top-level Markdown bullet beginning `- NEVER …` or `- **NEVER …`. Do **NOT** use a numbered list (`1. NEVER …`, `2. NEVER …`).

This is not stylistic. Automated graders, link-integrity checks, and the QA scorecard count NEVER items by anchoring on a line that starts with `- ` (regex `/^- (\*\*)?NEVER/`). A numbered item (`1. **NEVER …`) is **silently skipped** by that anchor: the skill renders identically to a human reviewer but scores **zero** NEVER items in the gate, so a fully-authored skill is failed (or, worse, a thin skill passes because its numbered items were never counted at all). The failure is invisible at authoring time and only surfaces when the scorecard runs.

Acceptable alternate presentation: a NEVER **table** (`| Anti-pattern | Why it fails |`) is recognized for leaf reference skills that catalog many anti-patterns at once. If you use a table, the column-two cell must still carry the non-obvious WHY mechanism, and the section heading must still be `## NEVER` so the section is discoverable. Prose lists, however, must be bullets — never numbered.

## Minimum Requirement

Every `SKILL.md` in the agent-toolkit library **must contain a dedicated `## NEVER` section with at least 5 items** that meet the format standard above.

Skills with fewer than 5 items, items missing the WHY clause, or items with vague WHY clauses ("it may fail," "it could cause issues") do not meet the standard and must be updated before the skill is considered complete.

## Placement

The `## NEVER` section belongs **near the top of `SKILL.md`, before the first workflow section** (before `## Usage`, `## Steps`, `## Workflow`, or equivalent). Practitioners reading a new skill should encounter failure modes before they encounter instructions — the NEVER list is a pre-flight checklist, not an appendix.

Recommended order in `SKILL.md`:

```
# Skill Name
[one-line description]

## NEVER
[5+ items]

## [First workflow or usage section]
...
```

## Fill-In Template

Copy this block into a new `SKILL.md` and replace each placeholder:

```markdown
## NEVER

- NEVER [specific action] — because [non-obvious consequence: what breaks, how it breaks, what the failure looks like]
- NEVER [specific action] — because [non-obvious consequence: what breaks, how it breaks, what the failure looks like]
- NEVER [specific action] — because [non-obvious consequence: what breaks, how it breaks, what the failure looks like]
- NEVER [specific action] — because [non-obvious consequence: what breaks, how it breaks, what the failure looks like]
- NEVER [specific action] — because [non-obvious consequence: what breaks, how it breaks, what the failure looks like]
```

Add additional items beyond 5 whenever field experience surfaces a new failure mode.

## Examples: GOOD vs BAD

### Example 1 — Git operations in shallow clones

**BAD (vague):**
> NEVER amend commits in shallow clones — it may cause push failures.

**GOOD (specific + non-obvious mechanism):**
> NEVER run `git commit --amend` inside a `--depth 1` shallow clone — because amend rewrites the tip commit without the full ancestry graph present, producing an orphan commit whose SHA is unknown to the remote; a subsequent `push --force` then overwrites the remote branch with a history that begins at the orphan, permanently discarding all prior commits that no local ref still points to.

---

### Example 2 — Airtable field ID substitution

**BAD (vague):**
> NEVER use field names instead of field IDs — it will not work.

**GOOD (specific + non-obvious mechanism):**
> NEVER substitute a human-readable field name (e.g., `"Status"`) for an Airtable field ID in filter or sort parameters — because the API silently accepts the name without error but treats it as an unknown field, returning an empty result set rather than raising a validation error; the caller receives zero records and has no indication that the filter was discarded rather than applied.

---

### Example 3 — Mermaid diagram rendering flags

**BAD (vague):**
> NEVER pass unsupported flags to mmdc — it causes rendering to fail.

**GOOD (specific + non-obvious mechanism):**
> NEVER pass `--no-sandbox` as a direct CLI flag to mmdc v11.x — because mmdc does not recognize it as a top-level argument and silently drops it, causing Puppeteer to launch with the sandbox enabled inside a rootless container, which then crashes with a cryptic `SIGILL` or permission error that appears to be a Chromium binary fault rather than a flag-parsing issue; the correct mechanism is to pass sandbox args through a Puppeteer config JSON file via the `-p` flag (e.g., `-p puppeteer.json` where the file contains `{"args":["--no-sandbox","--disable-setuid-sandbox"]}`).

---

## Checklist Before Submitting a NEVER Item

- [ ] The action described is specific enough that a reader cannot misinterpret which action is prohibited
- [ ] The WHY clause names a mechanism, not just an outcome
- [ ] The failure mode would surprise a competent engineer who had not encountered it before
- [ ] The item was derived from actual practitioner experience or a documented incident, not a general heuristic
- [ ] The item is in the `## NEVER` section, placed before the first workflow section in the file
