# Git Bisect Mastery

## Automated Bisect with a Test Script

The most powerful bisect usage runs a script instead of manual good/bad marking. The script must exit 0 for "good", non-zero for "bad", and 125 to skip the commit (skip is critical for handling build failures mid-bisect).

```bash
git bisect start
git bisect bad HEAD                  # current commit is bad
git bisect good v2.3.0               # last known good tag or SHA

git bisect run ./scripts/test-regression.sh
```

**`test-regression.sh` structure**:
```bash
#!/usr/bin/env bash
set -e

# Build the project — if it fails, skip (exit 125) rather than marking bad
make build 2>/dev/null || exit 125

# Run the specific test for the regression
# Exit 0 = good, non-zero = bad
python -m pytest tests/test_payment_processing.py::test_refund_calculation -x -q
exit_code=$?

exit $exit_code
```

**Critical exit code contract**:
- `0` — commit is good (test passes)
- `1`–`124`, `126`–`127` — commit is bad (test fails)
- `125` — skip this commit (build broken, unrelated failure, or flaky test hit — don't mark it)

---

## Handling Flaky Tests During Bisect

Flaky tests are the silent bisect killer. If a test is flaky at the 10% rate, bisect will produce a wrong answer roughly once per 7 bisect steps — which means on a 1000-commit range (10 bisect steps), you will likely get a wrong answer.

**Strategies**:

### Retry wrapper
```bash
#!/usr/bin/env bash
# Retry up to 3 times; only mark bad if all attempts fail
for i in 1 2 3; do
    python -m pytest tests/test_feature.py -x -q && exit 0
done
exit 1
```
This reduces flake impact at the cost of 2x–3x runtime per bisect step.

### Skip on known flaky conditions
```bash
#!/usr/bin/env bash
# If the test infrastructure isn't available, skip rather than marking bad
curl -sf http://localhost:8080/health > /dev/null 2>&1 || exit 125
python -m pytest tests/test_feature.py -x -q
```

### Validate bisect result independently
After bisect identifies a commit, **always verify manually**:
```bash
git checkout <bisect-identified-bad-commit>
# Run the test 5 times
for i in $(seq 5); do python -m pytest tests/test_feature.py -x -q; done
```
If it passes sometimes, bisect was fooled by a flaky test. Restart bisect with a retry wrapper.

---

## When Bisect Points to a Merge Commit

Bisect points to a merge commit when the regression was introduced in a branch but the individual commits in that branch were not bisected — only the merge commit itself was marked as the boundary.

**What this means**: The regression exists somewhere in the commits that were merged, not in the merge commit itself (unless the merge had conflicts that were resolved incorrectly).

**Recovery procedure**:
```bash
# bisect told us this merge commit is the first bad:
# abc1234 Merge branch 'feature/payment-v2' into main

# Find the parent SHAs of the merge commit
git log --merges --oneline -1 abc1234
git cat-file -p abc1234 | grep ^parent
# parent def5678   (first parent = main before merge)
# parent ghi9012   (second parent = tip of the merged branch)

# Bisect the source branch directly
git bisect start
git bisect bad ghi9012              # tip of the merged branch (bad)
git bisect good def5678             # main before the merge (good — doesn't have the feature at all)
git bisect run ./scripts/test-regression.sh
```

**The merge conflict resolution case**: If the regression was introduced during conflict resolution (not in a commit in either branch), bisect within the branch won't find it. Check the merge commit diff directly:
```bash
git diff def5678..abc1234 -- path/to/relevant/file
# Or compare both parents to the merge result:
git diff def5678 abc1234
git diff ghi9012 abc1234
```
Hunks that differ from both parents are the merge resolution — examine those first.

---

## Bisect with Shallow Clones

Do not attempt bisect on a shallow clone. The history is truncated; bisect will either fail with "Not a valid object name" when it tries to check out commits below the shallow boundary, or worse, it will identify the oldest available commit as "bad" because the actual introducing commit is not present.

**Detection**:
```bash
git rev-parse --is-shallow-repository
# "true" = shallow clone, bisect will be unreliable
```

**Fix**:
```bash
git fetch --unshallow
# or fetch enough history to cover the good..bad range:
git fetch --depth=500
```

---

## Bisect Cleanup

Always end a bisect session properly:
```bash
git bisect reset         # returns to original HEAD and cleans bisect state
```
Failing to reset leaves `BISECT_HEAD` and related state files in `.git/`, which will cause confusing errors on next checkout.
