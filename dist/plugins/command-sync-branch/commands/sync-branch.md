---
description: Sync feature branch with the latest main branch.
argument-hint: [target]
---

1. Fetch latest upstream refs: `git fetch origin --prune`.
2. Identify target branch (default `main`, or override via argument).
3. Rebase current branch onto target:
   ```bash
   git rebase origin/${target:-main}
   ```
4. Resolve any conflicts
5. Force-with-lease push to update the PR:
   ```bash
   git push --force-with-lease origin $(git branch --show-current)
   ```
