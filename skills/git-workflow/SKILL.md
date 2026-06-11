---
name: git-workflow
description: "Expert Git workflow guidance: branch strategy selection, rebase vs. merge trade-offs, bisect with test scripts, stash hygiene, worktree patterns, shallow clone pitfalls, reflog recovery, and precision index use. Trigger phrases: git strategy, branching model, rebase or merge, git bisect, worktree, stash, reflog, recover branch, partial staging."
---

# Git Workflow

## Mindset

- Branch strategy is a CI maturity decision, not a preference. The question is: can your pipeline validate a commit in under 10 minutes? If not, trunk-based development will drown your team in broken main.
- The index is a precision instrument. Practitioners who understand `git add -p` and `git reset HEAD <file>` make reviewable commits; everyone else makes noise.
- Rebase rewrites history — that is its power and its danger. On a private branch it's surgery; on a shared branch it's sabotage.
- `git bisect` is only as good as your test script. A flaky test makes bisect produce wrong answers with high confidence — more dangerous than no bisect at all.
- Reflog is your time machine, but it expires in 30 days by default. The window is not infinite; act within it.

## Navigation

**Use this skill when**: choosing a branching model, deciding rebase vs. merge, automating bisect, troubleshooting stash conflicts, running parallel work with worktrees, recovering from reset/delete/detached HEAD, or staging partial changes.

**Do NOT use this skill when**: writing commit messages (use `commit-work`), creating PRs, or setting up CI pipelines — those warrant dedicated treatment.

**Strategy decision tree**:
```
Team size ≤ 5 AND releases are continuous (no scheduled releases)?
  └─ YES → GitHub Flow (short-lived feature branches, merge to main, deploy immediately)
  └─ NO → Release cadence is scheduled (weekly/monthly/quarterly)?
            └─ YES → Gitflow (develop, release/, hotfix/ branches for parallel support)
            └─ NO → CI pipeline validates in < 10 min AND team practices feature flags?
                      └─ YES → Trunk-Based Development (TBD) — single main, short-lived branches ≤ 2 days
                      └─ NO → GitHub Flow with protected main (gate merges behind CI green)
```

**Rebase vs. merge decision tree**:
```
Branch is shared (others have checked it out or pushed to it)?
  └─ YES → MERGE ONLY. Never rebase.
  └─ NO → Want linear history for bisect and log readability?
            └─ YES → Rebase onto target before merging (rebase locally, merge with --no-ff or fast-forward)
            └─ NO → Preserving merge topology (shows when a feature was integrated)?
                      └─ YES → Merge with --no-ff
                      └─ NO → Fast-forward merge (linear, no merge commit)
```

## Philosophy

Git's power is that every operation is reversible if you know where to look — the reflog, the index, the stash list. Expert Git practice is less about knowing commands and more about knowing which state you're in and what the escape routes are before you act.

## NEVER

- NEVER `git add -A` or `git add .` before inspecting untracked files — `git status` first, every time. Build artifacts, `.env` files, and IDE configs are silently swept in; once pushed, secrets require a full history rewrite to remove.
- NEVER rebase a branch others have checked out — their local branches are built on the SHA history you're about to rewrite. The only resolution is `git pull --rebase` or force-push on their end, and they will miss it if you don't coordinate. This is how teams lose commits.
- NEVER `git commit --amend` after push — amend rewrites the local tip commit SHA. The remote still has the original. Every subsequent `git push` will reject with "non-fast-forward." The only escape is `--force-with-lease`, which rewrites remote history. If others have already pulled, their branches now diverge from an SHA that no longer exists on origin.
- NEVER `git reset --hard` without `git status` first — there is no recovery path for uncommitted changes after `--hard`. The working tree and index are destroyed silently. Reflog cannot recover unstaged changes — only committed work is recoverable.
- NEVER `git stash pop` after switching branches without checking `git stash list` and noting which branch the stash was created on — stash pop applies the diff with no context awareness. Popping a stash from a different branch causes conflicts that are structurally wrong (not just textually wrong), and resolving them produces subtly broken code.
- NEVER delete a branch with `git branch -d` and assume it's safe because `-d` "checks" it — `-d` only checks whether the branch is reachable from the current HEAD's branch. If the branch is merged into a different branch than the one you're currently on, `-d` will refuse but `-D` will silently delete unmerged work. Use `git branch --merged <target>` to verify against the actual target branch first.
- NEVER run `git bisect` on a shallow clone (`--depth N`) — shallow clones truncate history. Bisect will exhaust the available commits and either error out or identify the wrong commit as the culprit because the actual introducing commit is below the shallow boundary.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| `git push` rejected after commit | Local and remote diverged (likely a prior amend or reset) | `git fetch && git log --oneline origin/branch..HEAD` to see what diverged; if yours is right, `git push --force-with-lease` (not `--force`) |
| Detached HEAD after `git checkout <SHA>` | You checked out a commit directly, not a branch | `git branch recover-work` while still detached — this names the current state; then `git checkout recover-work` |
| `git stash pop` caused unexpected conflicts | Stash was created on a different branch with different base | `git stash drop` after careful inspection; re-apply changes manually with `git diff stash@{0}` |
| Bisect points to a merge commit as "bad" | The regression was introduced in a branch merged here | `git bisect` the source branch directly: `git bisect start <merge-commit> <merge-base>` |
| Branch deleted before verifying merge | Panicked `-D` or automated cleanup | `git reflog` to find the last SHA on that branch; `git branch recover-name <SHA>` |
| Reset --hard wiped uncommitted work | No stash, no commit | Unstaged changes: unrecoverable. Staged changes: `git fsck --lost-found` may surface dangling blobs if the index was written |

## Detailed References

Heavy reference content is in `references/`:

- [Branch strategies deep dive](references/branch-strategies.md) — trunk-based CI requirements, gitflow release mechanics, GitHub Flow edge cases
- [Bisect mastery](references/bisect-mastery.md) — automated bisect scripts, flaky test handling, merge-commit bisect
- [Worktree patterns](references/worktree-patterns.md) — when worktrees beat stash, concurrent build patterns, CI simulation
- [Reflog and recovery](references/reflog-recovery.md) — complete recovery playbook for every common disaster scenario
- [Index precision](references/index-precision.md) — partial staging, hunk splitting, resetting individual files
