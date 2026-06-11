# Worktree Patterns

## When Worktrees Beat Stash + Branch Switch

Stash + branch switch is optimized for "save my work for 5 minutes." Worktrees are optimized for "I need two or more complete working states simultaneously." The break-even is roughly: does your other work require a build, test run, or server process?

| Situation | Use stash | Use worktree |
|-----------|-----------|--------------|
| Quick hotfix while mid-feature | Yes, if the fix is < 30 min | Yes, if it needs a full build |
| Reviewing a PR while working on your own branch | No — both need build artifacts | Yes — each worktree has its own build output |
| Running tests on two branches simultaneously | No — single working tree | Yes — both test suites run independently |
| CI simulation locally | No | Yes — mount the worktree as the CI would see it |
| Long-lived parallel work (> 1 day) | No — stash is not meant for this | Yes — name it descriptively |

## Creating and Using Worktrees

```bash
# Create a worktree for a new branch
git worktree add ../my-project-hotfix hotfix/auth-bypass

# Create a worktree for an existing remote branch
git worktree add ../my-project-review origin/feature/payments --track

# List all worktrees
git worktree list

# Remove a worktree (clean up)
git worktree remove ../my-project-hotfix
# or if the worktree directory was manually deleted:
git worktree prune
```

**Naming convention**: use a parallel directory structure:
```
~/projects/
  my-project/          # main working tree
  my-project-hotfix/   # worktree for hotfix
  my-project-pr-142/   # worktree for reviewing PR #142
```

## Worktree Constraints (Non-Obvious)

- **A branch can only be checked out in one worktree at a time.** Attempting to check out a branch that's already active in another worktree will fail with "already checked out." You must either remove that worktree or create a new branch from it.
- **Worktrees share the `.git` directory** (as a pointer file to the main repo's `.git`). This means: stashes, refs, and config are shared. A `git stash` in one worktree is visible in all others.
- **Build artifacts are NOT shared** — each worktree has its own working tree directory, so compiled output, `node_modules`, `.venv`, etc. are independent. This is the entire point for concurrent build scenarios.
- **Submodules are not initialized in new worktrees** — run `git submodule update --init --recursive` in the new worktree if your project uses submodules.

## CI Local Simulation Pattern

The canonical worktree use case for CI simulation:

```bash
# Create a clean worktree from the PR branch with no local modifications
git worktree add /tmp/ci-sim origin/feature/my-pr

# Run tests exactly as CI would — no local .env, no cached artifacts
cd /tmp/ci-sim
git clean -fdx          # remove all untracked/ignored files (CI starts clean)
npm ci                  # install from lockfile, not cache
npm test

# Clean up
cd -
git worktree remove /tmp/ci-sim
```

This catches environment contamination bugs — cases where tests pass locally due to a `.env`, local config file, or cached build artifact that won't exist in CI.

## Stash Hygiene

### Named stashes are mandatory for anything non-trivial

```bash
# Bad — impossible to know what this is 3 days later
git stash

# Good — inspectable and intentional
git stash push -m "WIP: auth refactor, token validation incomplete" --include-untracked
```

### `--include-untracked` is almost always what you want

Plain `git stash` does not stash untracked files. New files you've created are left behind. If you switch branches, those new files are now in the wrong branch context. Use `--include-untracked` as the default unless you intentionally want to leave new files behind.

```bash
git stash push --include-untracked -m "WIP: feature name"
```

### Before popping, check your stash list and context

```bash
git stash list
# stash@{0}: On feature/auth: WIP: auth refactor, token validation incomplete
# stash@{1}: On main: quick experiment with rate limiting

# Confirm you're on the right branch before popping
git branch --show-current
git stash show stash@{0}   # view the diff summary without applying
git stash show -p stash@{0}  # view the full diff
```

Popping `stash@{1}` (created on main) while on `feature/auth` will conflict on any file that both the stash and feature branch touched. The conflicts are not wrong code — they're the right code in the wrong context, which is harder to detect than a normal merge conflict.

### When pop creates unexpected conflicts: recovery

```bash
# git stash pop failed with conflicts
# Option A: abort and apply manually
git checkout -- .          # discard the conflicted merge attempt
git stash show -p stash@{0} > /tmp/stash.patch
# review /tmp/stash.patch, apply manually

# Option B: stage the conflict resolution and drop the stash
# (resolve conflicts, then:)
git add -A
git stash drop stash@{0}   # stash is consumed — do NOT pop again
```
