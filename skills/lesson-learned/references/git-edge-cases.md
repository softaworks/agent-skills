---
description: Git edge cases and error handling for lesson-learned skill. Load when git commands fail or produce unexpected output.
---

# Git Edge Cases

Reference for handling unusual repository states when gathering diff context.

## Shallow Clone

**Symptom:** `git log` shows truncated history; `git diff main...HEAD` errors with "fatal: no merge base".

**Detection:** `git rev-parse --is-shallow-repository` returns `true`.

**Recovery:**
```bash
# Deepen enough to get useful history without full clone
git fetch --deepen=50
# Then retry your original diff command
```

**Lesson-learned impact:** If the diff is unavailable, fall back to `git show HEAD` for the latest commit only. Tell the user: "This is a shallow clone — analysis limited to the most recent commit visible."

**NEVER do:** `git commit --amend` in a shallow clone when there is a remote tracking branch. Amending rewrites the tip SHA; a subsequent `git push --force` can silently drop commits that exist on the remote but not in the shallow history. Recover orphaned commits via `git fetch origin <sha>`.

## Detached HEAD

**Symptom:** `git branch` shows `* (HEAD detached at <sha>)`. `git log main..HEAD` may return nothing or error.

**Detection:** `git symbolic-ref --quiet HEAD` exits non-zero.

**Recovery:**
```bash
# Identify what the detached HEAD contains vs. nearest branch
git log --oneline $(git merge-base HEAD main)..HEAD
```

**Lesson-learned impact:** Use commit-range mode rather than branch-mode analysis. Default to `git log --oneline -5` + `git diff HEAD~5..HEAD`.

## No Commits Yet (Empty Repo)

**Symptom:** `git log` returns "fatal: your current branch 'main' does not have any commits yet."

**Recovery:** Nothing to analyze. Tell the user: "No commits found — make at least one commit before running a lesson-learned analysis."

## Merge Commits in Range

**Symptom:** `git diff main...HEAD` includes changes from merged branches that are unrelated to the user's work.

**Detection:** `git log --merges main..HEAD` returns results.

**Recovery:** Use `--no-merges` and `--first-parent` flags:
```bash
git log --no-merges --first-parent --oneline main..HEAD
git diff --no-merges main...HEAD
```

**Lesson-learned impact:** Ignore merge-only commits. Analyze only the substantive commits.

## Very Large Diffs (>1000 lines)

**Symptom:** `git diff` output exceeds context budget.

**Recovery strategy (in order):**
1. Run `git diff --stat` to identify the top 3-5 most-changed files
2. Read each file's diff individually: `git diff main...HEAD -- path/to/file`
3. Focus on the files with the highest semantic change (not just line count)
4. If a single file dominates (e.g., a generated file), skip it and note: "Excluding auto-generated file X from analysis."

## Binary or Generated Files

**Symptom:** `git diff` shows "Binary files differ" or a massive JSON/CSS/lock file change.

**Recovery:** Skip binary files entirely. For generated files (package-lock.json, yarn.lock, *.min.js, dist/), note: "Lock/generated files excluded from analysis — these contain no engineering lessons."

## Uncommitted Staged + Unstaged Mix

**Symptom:** User says "analyze these changes" before committing; both staged and unstaged changes exist.

**Recovery:**
```bash
git diff          # unstaged
git diff --cached # staged
```

Present both diffs together as the full working set. Note which changes are staged vs. not, as that itself may be a lesson (partial staging as a discipline).

## Remote Tracking Branch Mismatch

**Symptom:** `git log main..HEAD` shows 0 commits even though local changes exist, because local `main` is behind remote.

**Recovery:**
```bash
git fetch --dry-run  # check without modifying
git log origin/main..HEAD --oneline
```

Use `origin/main` as the base when local `main` hasn't been updated.
