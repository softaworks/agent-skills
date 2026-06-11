---
name: commit-work
description: "Create high-quality git commits: review/stage intended changes, split into logical commits, write Conventional Commits messages. Trigger phrases: commit this work, craft a commit message, stage changes, split into commits, create a commit."
---

# Commit Work

## Mindset

- A commit is a unit of reviewability, not a unit of work. If a reviewer can't understand it in isolation, split it.
- The diff is wrong until proven otherwise. Run `git diff` before touching the index — surprises live there.
- Pre-commit hooks are enforcement, not suggestions. A failed hook means the commit did NOT happen; recover with a new commit, never `--amend` on the same HEAD.
- Bisect-safety trumps narrative coherence. A commit that breaks tests is more expensive than two awkward commits that don't.
- Staging is a separate thinking step. Deciding what to commit and how to describe it are different cognitive modes — don't conflate them.

## Navigation

**Use this skill when**: staging changes, crafting commit messages, splitting mixed changes into logical commits, applying Conventional Commits format.

**Do NOT use this skill when**: pushing to remote, creating pull requests, resolving merge conflicts, or rebasing — those workflows carry different risk profiles and should be handled explicitly.

**Quick decision tree**:
- Working tree has changes in 2+ unrelated concerns → split into multiple commits
- Changes touch secrets, generated files, or debug logs → exclude before staging
- Pre-commit hook failed → fix issue, re-stage, new commit (never amend)
- Repo is a shallow clone (`git rev-parse --is-shallow-repository` returns `true`) → do not amend; new commit only

## Philosophy

A commit is a promise to future readers: "this set of changes is coherent, tested, and describes its own intent." Violate that promise and you tax every future `git blame`, `git bisect`, and code review.

## NEVER

- NEVER run `git add -A` or `git add .` — these silently include `.env` files, build artifacts, and generated lock-file changes that belong in a separate commit or `.gitignore`. Review every path explicitly.
- NEVER `git commit --amend` in a shallow clone (`--depth N`) — amending rewrites the tip commit; a subsequent `push --force` will orphan the original on the remote and cannot be recovered without the SHA. Use a new commit instead.
- NEVER skip pre-commit hooks with `--no-verify` unless the user explicitly requests it and understands the consequence — hooks exist to catch secrets, linting errors, and test failures before they enter history.
- NEVER commit when `git status` shows a merge in progress (`MERGE_HEAD` exists) or a rebase is active (`REBASE_HEAD` / `rebase-merge/` directory present) — committing in this state creates a malformed merge commit or corrupts the rebase sequence.
- NEVER write a commit message that describes the implementation ("added null check on line 42") instead of the behavior ("prevent crash when user list is empty") — implementation is in the diff; the message must explain the intent.
- NEVER stage test file changes in the same commit as the production code they cover when the tests were written first (TDD) — the test-first commit is evidence of the design decision and has independent value in `git log`.
- NEVER assume `git diff --cached` is empty before committing — a prior interrupted session or a hook script can leave hunks staged without your knowledge.

## Workflow

**1. Inspect before touching the index**
```
git status
git diff                  # unstaged
git diff --cached         # already staged (should be empty at start)
```
Check for: merge/rebase state, shallow clone, stale staged hunks.

**2. Decide commit boundaries**
Split by: feature vs refactor, logic vs formatting, prod vs test, dep bump vs behavior change.
If a file contains mixed concerns, plan patch staging (`git add -p`) before touching the index.

**3. Stage selectively**
```
git add -p <file>         # preferred for mixed-concern files
git add <explicit-path>   # acceptable for clean single-concern files
```
After staging: `git diff --cached` must match your intent exactly.

**4. Safety check on staged diff**
Scan for: secrets/tokens, `console.log`/`debugger`/`TODO` left over, unrelated whitespace churn, generated files.

**5. Describe the change in 1-2 sentences before writing the message**
If you cannot describe it cleanly → the commit is too big. Return to step 2.

**6. Write the commit message**
See `references/commit-message-template.md`. Required format:
```
type(scope): short imperative summary

What changed and why — not how.

BREAKING CHANGE: (if applicable)
```
Use `git commit -v` to see the diff while composing.

**7. Verify before moving on**
Run the repo's fastest meaningful check (unit tests, lint, typecheck). A commit that breaks CI is more expensive to fix than a 30-second lint run now.

**8. Repeat until `git status` is clean**

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Pre-commit hook failed | Hook caught lint/test/secret issue | Fix the issue, `git add` the fix, create a NEW commit — do NOT `--amend` |
| Committed wrong hunks | `git add -A` or inattentive `git add -p` | `git reset HEAD~1` (soft) to unstage, re-stage correctly, new commit |
| `git commit --amend` in shallow clone | `--depth N` clone, rewrote tip | Recover original via `git fetch origin <SHA>` if you still have it; otherwise the original is gone unless the remote ref is intact |
| Merge/rebase in progress | `MERGE_HEAD` or `rebase-merge/` present | Complete or abort the merge/rebase first: `git merge --abort` / `git rebase --abort` |
| Hook added files you didn't stage | Formatter hook auto-staged changes | Run `git diff --cached` again after the hook; unstage unintended changes with `git restore --staged -p` |
| Bisect breaks on a commit | Mixed concerns in one commit | Future prevention: split logic/test/format; immediate: `git bisect skip` to mark untestable commits |

## Bisect Safety Heuristics

When splitting commits, order them so every intermediate state is buildable and testable:
1. Dependency/config changes first
2. New production code (feature/fix) second
3. Tests that exercise that code third
4. Formatting/cleanup last

A commit series that cannot be bisected is a commit series that cannot be debugged.
