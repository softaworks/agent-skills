# Index Precision: The Staging Area as a Tool

## The Core Concept

The index is a buffer between your working tree and the object store. Most developers treat it as a formality ("staging area = just run git add"). Expert usage treats it as a precision assembly tool: you construct the exact snapshot you want committed, independent of what the working tree currently looks like.

---

## Partial Staging with `git add -p`

`git add -p` (patch mode) breaks each changed file into hunks and asks about each one individually. This lets you commit a subset of your changes — half a file, specific functions, everything except the debug print statements.

```bash
git add -p [file]    # omit file to review all changed tracked files
```

**Hunk commands** (type `?` during add -p for the full list):
- `y` — stage this hunk
- `n` — skip this hunk
- `s` — split the hunk into smaller hunks (if Git thinks the gap between changes is large enough)
- `e` — manually edit the hunk (most powerful — opens the diff in $EDITOR)
- `q` — quit, leaving remaining hunks unstaged

**The `e` (edit) command** is the escape hatch when hunks are too coarse. You edit the raw diff format:
- Lines starting with `+` are additions — remove a `+` line to not stage that addition
- Lines starting with `-` are deletions — change `-` to ` ` (space) to not stage that deletion
- Do not change context lines (starting with ` `)

---

## Resetting Individual Files Without Touching Working Tree

`git reset HEAD <file>` (or `git restore --staged <file>` in newer Git) removes a file from the index without changing the working tree. Use this when you've staged something you didn't intend to.

```bash
# Unstage a file (but keep working tree changes)
git restore --staged path/to/file.py
# equivalent older form:
git reset HEAD path/to/file.py

# Unstage specific hunks (reverse of git add -p)
git restore -p --staged path/to/file.py
# or:
git checkout -p HEAD -- path/to/file.py
```

---

## Restoring Working Tree from Index (or Commit)

```bash
# Discard working tree changes to a file, restoring to what's staged
git restore path/to/file.py

# Discard working tree changes and staged changes, restoring to HEAD
git restore --staged --worktree path/to/file.py
# equivalent older form:
git checkout HEAD -- path/to/file.py
```

**Critical distinction**: `git checkout HEAD -- file` overwrites BOTH the index and working tree. `git restore --staged file` only resets the index. Choose based on whether you want to preserve the working tree state.

---

## Viewing the Index State

```bash
git diff --cached           # diff between index and HEAD (what you're about to commit)
git diff                    # diff between working tree and index (unstaged changes)
git diff HEAD               # diff between working tree and HEAD (all changes)

# Show what's staged with filenames only:
git diff --cached --name-only

# Show the actual content of a file as it exists in the index:
git show :path/to/file.py
```

---

## Common Precision Index Patterns

### Pattern: Split one file's changes into two commits

```bash
# File has both a bug fix and a refactor mixed together
git add -p auth.py
# Stage only the bug fix hunks → commit 1: "fix: null check on user token"
git commit -m "fix: null check on user token"

# Now stage the refactor
git add auth.py
git commit -m "refactor: extract token validation to separate method"
```

### Pattern: Commit with a generated file excluded

```bash
git add src/           # stage everything in src/
git restore --staged src/generated/api_client.py  # unstage the generated file
git commit -m "feat: add payment endpoint"
# generated file remains modified in working tree but is not committed
```

### Pattern: Stage a deleted file but keep it locally

```bash
# You want to stop tracking a file but keep the local copy (e.g., config with secrets)
git rm --cached path/to/config.local
echo "config.local" >> .gitignore
git add .gitignore
git commit -m "chore: untrack local config, add to gitignore"
# config.local still exists locally, just no longer tracked
```

---

## Index State During Conflicts

During a merge or rebase conflict, the index holds three versions of each conflicted file (stages 1, 2, 3):

```bash
git ls-files -u             # list all unmerged (conflict) entries with stage numbers
# 100644 abc1234 1    path/to/file  (common ancestor = base)
# 100644 def5678 2    path/to/file  (ours = current branch)
# 100644 ghi9012 3    path/to/file  (theirs = incoming branch)

# Extract any version manually:
git show :1:path/to/file    # ancestor
git show :2:path/to/file    # ours
git show :3:path/to/file    # theirs
```

This is the mechanism that merge tools use. You can use it to manually resolve conflicts by comparing all three versions before editing.
