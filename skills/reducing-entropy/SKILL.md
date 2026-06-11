---
name: reducing-entropy
description: Manual-only skill for minimizing total codebase size. Activate when user says "reduce entropy", "simplify this", "make this smaller", "delete what we don't need", or asks to minimize code. Measures success by final line count, not effort. Bias toward deletion over abstraction.
---

# Reducing Entropy

More code begets more code. Entropy accumulates. This skill biases toward the smallest possible codebase.

**Core question:** "What does the codebase look like *after*?"

## Mindset

Expert heuristics that separate practitioners from beginners:

1. **Count lines, not concepts.** The unit of entropy is lines of code. "Better architecture" with more lines is worse. A 50-line function that replaces 200 lines of abstraction is a win, even if it feels inelegant.

2. **Deletion is a feature.** Every line deleted is a line that can never have a bug, never need documentation, never block a future refactor. The best code review comment is "can we delete this instead?"

3. **Abstractions have a break-even point.** An abstraction only pays off if it eliminates more code than it adds. A 30-line base class shared by two 10-line subclasses is net-negative — you wrote 30 lines to avoid writing 20. Count before abstracting.

4. **"No churn" is a false virtue.** Resistance to change preserves entropy. The question is never "how disruptive is this?" — it's "does the end state have less code?"

5. **Measure the delta, not the task.** Track lines-before vs lines-after for every change. If after > before, the change increased entropy regardless of other virtues claimed for it.

## Navigation

### When to apply this skill

- User explicitly asks to reduce entropy, simplify, minimize, or delete code
- Codebase has grown organically and accumulated abstractions with unclear value
- A feature is being removed or replaced and cleanup is in scope
- Refactor task where smaller result is the stated goal

### When NOT to apply this skill

- Codebase is already minimal for what it does (stop here — don't invent deletions)
- Working inside a framework with strong conventions (don't fight Rails, Django, etc.)
- Regulatory/compliance requirements mandate certain structures
- The user wants a refactor for readability, not size (different goal — use a different lens)
- Active incident or hot path — this is a calm-waters skill

### Decision Tree: Which Pattern to Apply

```
Is there dead code (unused functions, unreachable branches)?
  YES → Delete it first. No abstraction needed.
  NO  ↓

Are there 3+ similar code blocks doing the same thing?
  YES → Consolidate into one function. Does the function add more lines than it saves?
          YES → Leave the duplication. (Rule of Three, not Rule of Two)
          NO  → Consolidate.
  NO  ↓

Are there wrapper classes/types that add no behavior?
  YES → Replace with generic data structures (map, list, tuple).
        Load references/data-over-abstractions.md
  NO  ↓

Are there multiple abstraction layers where one would do?
  YES → Flatten. Load references/design-is-taking-apart.md
  NO  ↓

Is the interface complex because the implementation is complex?
  YES → Acceptable — implementation complexity is hidden. Interface simplicity wins.
        Load references/worse-is-better.md
  NO  ↓

Are you adding something "for later flexibility"?
  YES → Is it a PAGNI (timestamps, API versioning, audit logs)?
          YES → Add it. Load references/expensive-to-add-later.md
          NO  → YAGNI. Delete or don't add.
  NO  ↓

Is "simple" confused with "familiar" here?
  YES → Load references/simplicity-vs-easy.md — the familiar choice may be the complex one.
```

### Load Reference Mindsets

Before proceeding on a non-trivial reduction task, load at least one mindset from `references/`:

| File | Use when |
|------|----------|
| `data-over-abstractions.md` | Classes/types wrapping data that could be plain maps |
| `design-is-taking-apart.md` | God objects, mixed concerns, coupling to untangle |
| `expensive-to-add-later.md` | Tempted to skip something that will be painful to retrofit |
| `simplicity-vs-easy.md` | Team gravitates to familiar pattern over simpler one |
| `worse-is-better.md` | Completeness is blocking shipping; perfectionism over pragmatism |

**Load the file, state its core principle, then proceed.**

## Philosophy

Every codebase trends toward entropy. Reducing it is not cleanup — it is the primary act of software design. The discipline is asymmetric: adding code is easy and feels productive; deleting code is uncomfortable and requires conviction. This skill supplies the conviction.

## The Goal

The goal is **less total code in the final codebase** — not less code to write right now.

- Writing 50 lines that delete 200 lines = net win (+150 lines reduced)
- Keeping 14 functions to avoid writing 2 = net loss (12 functions of unnecessary overhead)
- "No churn" is not a goal. Less code is the goal.

**Measure the end state, not the effort.**

## Three Questions

### 1. What's the smallest codebase that solves this?

Not "what's the smallest change" — what's the smallest *result*.

- Could this be 2 functions instead of 14?
- Could this be 0 functions (delete the feature)?
- What would we delete if we did this?

### 2. Does the proposed change result in less total code?

Count lines before and after. If after > before, reject it.

- "Better organized" but more code = more entropy
- "More flexible" but more code = more entropy
- "Cleaner separation" but more code = more entropy

### 3. What can we delete?

Every change is an opportunity to delete. Ask:

- What does this make obsolete?
- What was only needed because of what we're replacing?
- What's the maximum we could remove?

## NEVER

- **NEVER add an abstraction that doesn't reduce total lines.** An abstraction with negative ROI (adds more than it removes) is pure entropy. The reason this is non-obvious: abstractions feel productive while you're writing them. Count afterward.

- **NEVER treat "better organized" as equivalent to "less entropy."** More files, more layers, more interfaces — even well-organized ones — all increase entropy. Organization is not simplicity; it's rearrangement. Unless the reorganization also deletes code, it doesn't count.

- **NEVER abstract from two examples.** Two similar things may diverge. Abstract at three (Rule of Three). Premature abstraction locks in a contract before you understand the full shape of the problem, requiring more code to handle the exceptions later.

- **NEVER preserve code "just in case."** Deleted code is not lost — it's in git. "We might need it later" is a category error: you're paying a permanent maintenance tax against a speculative future benefit. If you need it later, resurrect it.

- **NEVER count effort as a win.** "We wrote only 10 lines to fix this" is irrelevant if the result has 50 more lines than before. The metric is the delta in total codebase size, not the size of the diff you submitted.

- **NEVER mistake interface complexity for implementation complexity.** A complex implementation behind a simple interface is acceptable (worse-is-better). A simple implementation behind a complex interface is never acceptable — you've exported the complexity to every caller.

- **NEVER apply this skill to a codebase that is already at its minimum.** Forced deletions manufacture debt. If nothing obviously can be removed, stop. The skill is finding real entropy, not inventing entropy to remove.

## When Things Go Wrong

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Deleted code that turned out to be needed | Insufficient dependency mapping before deletion | Use `git log -S <term>` and grep callers before deleting; check test coverage |
| Abstraction added more lines than it saved | Counted the happy path only; missed edge-case handling in generic code | Revert. Inline the specialization. Abstract only when net-negative is confirmed. |
| Team pushes back on "unnecessary churn" | Status quo bias framing deletion as risk | Reframe: "we are paying X lines/month maintenance tax for Y lines of rarely-used code" |
| Refactor broke the interface | Reduction goal conflated with internal restructuring | Keep external interfaces stable; reduce internally first, then negotiate interface changes separately |
| Tests now cover less after reduction | Tests were testing implementation, not behavior | Write behavior tests first; then reduce implementation behind them |

---

**Bias toward deletion. Measure the end state.**
