# Reflog and Recovery

## What Reflog Is (and Is Not)

Reflog records every time a ref (branch, HEAD) moves — commits, checkouts, resets, rebases, merges, cherry-picks. It is local only — `git push` does not push reflog entries, and cloning does not copy them.

**Reflog expires**: default expiry is 90 days for reachable entries, 30 days for unreachable (dangling) entries. Configure with `gc.reflogExpire` and `gc.reflogExpireUnreachable`.

**What reflog CAN recover**:
- Commits that were on a branch before reset
- Deleted branches (until garbage collected)
- Detached HEAD state
- Commits overwritten by `--amend`

**What reflog CANNOT recover**:
- Uncommitted changes destroyed by `reset --hard` or `checkout --`
- Changes never added to the index (untracked files deleted by `git clean`)
- Entries older than the expiry window

---

## Recovery Playbook

### Scenario 1: Detached HEAD — work committed to no branch

```bash
# You committed work while in detached HEAD state
# git checkout main moved HEAD and you've "lost" the commits

git reflog
# 5a3b2c1 HEAD@{0}: checkout: moving from 9e8d7f6 to main
# 9e8d7f6 HEAD@{1}: commit: add rate limiting logic
# 4f3e2d1 HEAD@{2}: commit: refactor token validation

# The SHA you want is 9e8d7f6 (the most recent commit before checkout)
git branch recover-detached-work 9e8d7f6
git checkout recover-detached-work
```

### Scenario 2: Branch deleted before merge

```bash
git branch -D feature/my-work   # oops

# Find the last commit SHA on that branch
git reflog | grep "feature/my-work"
# or scan for the commit message:
git reflog | grep "my-work"
# abc1234 HEAD@{14}: commit: implement payment webhook handler

git branch feature/my-work abc1234
```

### Scenario 3: `git reset --hard` wiped commits

```bash
git reset --hard HEAD~5   # removed 5 commits

git reflog
# current HEAD@{0}: reset: moving to HEAD~5
# abc1234 HEAD@{1}: commit: fifth commit
# def5678 HEAD@{2}: commit: fourth commit
# ...

# Restore to before the reset:
git reset --hard abc1234   # SHA of the commit before reset
```

### Scenario 4: Rebase went wrong — restore pre-rebase state

Git creates a `ORIG_HEAD` ref before any destructive operation (rebase, reset, merge). If reflog is confusing, check ORIG_HEAD first:

```bash
git rebase main   # something went wrong

# Option A: abort if rebase is still in progress
git rebase --abort

# Option B: reset to pre-rebase state if already completed
git reset --hard ORIG_HEAD
```

For rebases that completed but produced wrong results, use reflog:
```bash
git reflog | grep "rebase"
# Find the entry just before "rebase (start)"
git reset --hard HEAD@{N}   # where N is the step before the rebase started
```

### Scenario 5: `--amend` created an orphan (especially in shallow clones)

```bash
# You amended a commit, then pushed --force; someone else has the original SHA
# Or: you're in a shallow clone and amend created an orphan

git reflog
# abc1234 HEAD@{0}: commit (amend): updated commit message
# def5678 HEAD@{1}: commit: original commit

# The original commit is def5678 — it's still in local reflog
# To recover it as a branch:
git branch recover-original def5678
```

---

## Reflog Navigation

```bash
git reflog                  # HEAD movements
git reflog show main        # movements of the main branch specifically
git reflog show --all       # all refs

# Time-based navigation
git checkout HEAD@{2.hours.ago}
git checkout main@{yesterday}

# Show with timestamps
git reflog --date=relative
git reflog --date=iso
```

---

## Shallow Clone Recovery Procedures

Shallow clones (created with `--depth N`) have truncated history. The truncation point is marked with a "grafts" mechanism in newer Git. Issues that arise:

**Bisect fails**: `git bisect` needs to traverse history to the good commit. If that commit is below the shallow boundary, bisect reports "Not a valid object name."

**Amend creates orphan**: In a shallow clone, the commit behind the tip is synthetic. Amending the tip commit creates a new SHA; the old SHA is still referenced on the remote. A subsequent `push --force` replaces the remote's tip but the original is still reachable via fetch-by-SHA:
```bash
# Recover the original from remote after a force-push in shallow clone
git fetch origin <original-SHA>
git branch recover-from-orphan FETCH_HEAD
```

**Detection and fix**:
```bash
git rev-parse --is-shallow-repository
# "true" = shallow

# Deepen to cover the range you need:
git fetch --depth=1000
# Or fully unshallow:
git fetch --unshallow
```
