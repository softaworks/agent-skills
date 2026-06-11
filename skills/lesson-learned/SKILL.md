---
name: lesson-learned
description: "Analyze recent code changes via git history and extract software engineering lessons. Use when the user asks 'what is the lesson here?', 'what can I learn from this?', 'engineering takeaway', 'what did I just learn?', 'reflect on this code', or wants to extract principles from recent work."
---

# Lesson Learned

Extract specific, grounded software engineering lessons from actual code changes. Not a lecture — a mirror. Show the user what their code already demonstrates.

## Mindset

1. **The diff is the truth.** Commit messages declare intent; the diff reveals what actually happened. When they conflict, the diff wins.
2. **One sharp lesson beats seven vague ones.** Resist the pull to list every applicable principle. Find the single most instructive pattern and go deep on it.
3. **Recognition is as valuable as correction.** Naming a good pattern the user applied reinforces it just as powerfully as identifying a flaw. Most diffs contain both.
4. **Specificity is the only currency.** Every claim must point to a real file, a real line, a real commit. "Your code shows good separation of concerns" is worthless without: "see how `auth.js` no longer imports from `db.js` after commit `a3f2b1`."
5. **Trivial is a valid answer.** Not every change teaches something. Forcing a lesson out of a config tweak or typo fix is worse than saying "good housekeeping — nothing deeper here."

## Navigation

### When to Use

- User asks "what's the lesson?", "what did I learn?", "reflect on this", "engineering takeaway"
- After a PR merge or feature branch completion
- When a user wants to turn a debugging session into transferable knowledge
- Post-incident: "what does this bug teach me?"

### When NOT to Use

- User wants a code *review* (correctness/bugs) → use `/code-review` instead
- User wants architectural advice without a diff → use general reasoning, not this skill
- No git repo or no commits yet → tell the user directly, don't fake a lesson
- The user wants to understand *what the code does*, not *what it teaches*

### Decision Tree: Principle Selection

```
Is there a dominant structural change? (split file, extracted function, new abstraction)
  YES → Design/Structural principles (SRP, SoC, DIP, Encapsulation)
  NO ↓

Is the change primarily a bug fix or edge-case handler?
  YES → Pragmatic principles (Fail Fast, Defensive Programming, Boy Scout Rule)
  NO ↓

Is there duplicated or consolidated code?
  YES → Simplicity principles (DRY, Rule of Three, KISS)
  NO ↓

Is the change adding speculative features or over-engineering?
  YES → YAGNI or Premature Abstraction (anti-pattern)
  NO ↓

Is the change scattered across many unrelated files?
  YES → Shotgun Surgery (anti-pattern) — question the abstraction boundaries
  NO → Default to "Boy Scout Rule" — incremental improvement, no single dominant lesson
```

## Philosophy

A lesson learned from code is only real if it changes how the engineer writes the *next* line. Ground every observation so tightly in the actual diff that the user cannot mistake it for generic advice.

## Before You Begin

**Load references first.**

1. Read `references/se-principles.md` — principle catalog for mapping observations
2. Read `references/anti-patterns.md` if the diff signals code smells
3. If git commands fail or behave unexpectedly, load `references/git-edge-cases.md`

**Do not proceed until you've loaded at least `se-principles.md`.**

## Phase 1: Determine Scope

| Scope | Git Commands | When to Use |
|-------|-------------|-------------|
| Feature branch | `git log main..HEAD --oneline` + `git diff main...HEAD` | On a non-main branch (default) |
| Last N commits | `git log --oneline -N` + `git diff HEAD~N..HEAD` | User specifies range, or on main (default N=5) |
| Specific commit | `git show <sha>` | User references a specific commit |
| Working changes | `git diff` + `git diff --cached` | "What about these changes?" before committing |

**Default behavior:**
- Feature branch → analyze branch commits vs. main
- On main → last 5 commits
- User-specified → use that

**Git failures:** If any git command errors (shallow clone, detached HEAD, empty repo), load `references/git-edge-cases.md` before continuing. Do not silently ignore errors.

## Phase 2: Gather Changes

1. Run `git log` with the determined scope — read commit messages as primary intent signals
2. Run `git diff` for the full diff
3. If diff >500 lines: use `git diff --stat` first, then selectively read the top 3-5 most-changed files
4. Skip binary files, lock files, and generated files (package-lock.json, *.min.js, dist/) — note the exclusion
5. Only read changed files. Do not read the entire repo.

## Phase 3: Analyze

Use the **Decision Tree** in the Navigation section to identify which class of principle applies. Then find the **dominant pattern** — the single most instructive thing about these changes.

Look for:
- **Structural decisions** — How was the code organized? Why those boundaries?
- **Trade-offs made** — What was gained vs. sacrificed? (readability vs. performance, DRY vs. clarity)
- **Problems solved** — What was the before/after? What made the "after" better?
- **Missed opportunities** — Where could the code improve? (present gently as "next time, consider...")

Map findings to specific principles from `references/se-principles.md`. Quote actual code, reference actual file names and line changes.

## Phase 4: Present the Lesson

Load `references/output-template.md` for the exact formatting templates. Key rules:
- 1 primary lesson, maximum 2 secondary
- Always reference specific files and commits
- Lead with what works before noting what could improve
- Trivial diffs get the "good housekeeping" response, not a forced lesson

## NEVER

- **NEVER analyze files not in the diff.** Reading the whole repo for "context" is scope creep that introduces irrelevant principles and wastes context budget.
- **NEVER list every principle that loosely applies.** Presenting 5+ principles for one diff signals you couldn't identify what actually matters — it's noise, not signal.
- **NEVER say "you should have..."** It's past tense and implies failure. The user can't undo committed code. Use "next time, consider..." to keep the lesson forward-facing.
- **NEVER force a lesson on trivial changes.** A config bump or typo fix has no engineering lesson. Fabricating one trains the user to distrust the skill's signal.
- **NEVER ignore git errors silently.** A shallow clone, detached HEAD, or empty repo changes which commands work. Running `git diff main...HEAD` in a detached HEAD silently returns an empty diff — you'll present a lesson based on nothing.
- **NEVER present anti-pattern findings without a positive anchor.** Leading with "your code has a God Object problem" without first acknowledging what works is demoralizing and incomplete analysis.
- **NEVER use generic principle names as the lesson title without code evidence.** "Lesson: DRY" is not a lesson. "Lesson: DRY — the shared `validateInput()` extracted in commit `b2d4a1` eliminated 47 lines of duplication across 3 handlers" is.

## When Things Go Wrong

| Symptom | Recovery |
|---------|----------|
| `git diff` returns empty output | Check: detached HEAD? Shallow clone? Wrong base branch? Load `references/git-edge-cases.md`. Never present "no changes found" without diagnosing why. |
| Diff is >1000 lines | Use `git diff --stat` + selectively read top 3-5 files by semantic importance (not line count). Skip generated/lock files. Tell the user what was excluded. |
| No clear dominant principle | Default to Boy Scout Rule if the changes are scattered small cleanups. If the changes are large but structurally incoherent, that *is* the lesson: Shotgun Surgery. |
| User disagrees with the lesson | Ask: "What did you feel was the hardest decision in this change?" Their answer is the real lesson. Revise based on their actual intent. |
| Shallow clone blocks history | Run `git fetch --deepen=50`, then retry. If still blocked, fall back to `git show HEAD` for the latest commit only and note the limitation. |
