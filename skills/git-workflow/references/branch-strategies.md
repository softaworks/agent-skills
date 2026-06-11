# Branch Strategy Deep Dive

## Trunk-Based Development (TBD)

### Requirements (non-negotiable)
TBD fails without these — teams that try it without them end up with a permanently broken main:

1. **CI pipeline < 10 minutes** — developers must get a green/red signal before moving to the next task. 20+ minute pipelines cause developers to push without waiting, which defeats the whole model.
2. **Feature flags** — incomplete features must be hidden behind flags, not branches. Without flags, TBD forces you to either ship incomplete features or delay commits, which negates the trunk benefit.
3. **Branch life ≤ 2 days** — if a branch lives longer than 2 days, merge conflicts compound faster than the team resolves them. The rule is not arbitrary; it's the empirical threshold where integration pain exceeds the protection benefit.
4. **Comprehensive automated test suite** — trunk is only safe if a broken commit is caught before others pull it. Manual QA gates defeat the model.

### Non-obvious failure modes
- **Monorepo + TBD without module isolation**: changing a shared dependency breaks all consumers simultaneously on main. Mitigate with internal package versioning or explicit API contracts even for internal libs.
- **TBD with no deploy pipeline**: TBD assumes every green main commit is deployable. If deployment is manual, you'll cherry-pick commits eventually, which reintroduces branch management overhead.

---

## Gitflow

### When it's actually correct
Gitflow gets dismissed as overengineered, but it's the right model when:
- You support **multiple active release versions simultaneously** (e.g., v2.x and v3.x both get security patches)
- Releases are **date-gated** (quarterly, compliance-driven, or tied to external partners) with a stabilization period
- Teams are **large enough** that direct trunk commits create merge contention on main

### The non-obvious mechanics
- `develop` is not a "staging" branch — it's an integration branch. Treating it as staging causes teams to test on develop instead of in isolated environments, which pollutes develop with debugging commits.
- `release/` branches exist to **freeze scope** while allowing bug fixes. The correct flow is: branch `release/x.y` from develop, only bug-fixes go into release, merge release into both main AND develop on completion. Many teams skip the back-merge to develop, then rediscover the bug in the next release cycle.
- `hotfix/` branches must merge to both main AND develop. Skipping the develop merge means the hotfix is in production but not in the next scheduled release — a category of regression that's hard to diagnose months later.

### Team size threshold
Gitflow adds overhead. Under ~8 engineers, the branch management cost typically exceeds the isolation benefit. The inflection point is when two engineers can simultaneously be working on features that conflict — small teams can coordinate verbally.

---

## GitHub Flow

### The edge cases nobody documents

**Long-running PRs and drift**: GitHub Flow assumes short-lived branches, but product work doesn't always cooperate. A PR open for 2+ weeks will drift significantly from main. The convention `git fetch origin && git rebase origin/main` keeps it current, but rebasing a PR branch you've already force-pushed once means the remote PR history becomes fragmented in code review tools.

**Hotfix pattern**: GitHub Flow has no explicit hotfix branch. The correct approach is to branch from main (not from an existing feature branch), push directly to a `hotfix/desc` branch, open a PR, get expedited review, merge. Don't tag it differently — the merge commit to main IS the record.

**The "squash merge" trap**: GitHub Flow repos often enable squash-merge. Squash merge produces clean history but destroys individual commit context. `git bisect` on a squash-merged repo will identify a squash commit as bad, but that commit may encompass 40 individual changes — you've narrowed to a PR, not a change. Use squash merge only if your PRs are already single-unit commits.

---

## Choosing Between Models: The Real Criteria

| Criterion | TBD | GitHub Flow | Gitflow |
|-----------|-----|-------------|---------|
| CI < 10 min | Required | Helpful | Not required |
| Feature flags in codebase | Required | Optional | Not needed |
| Multiple supported versions | No | No | Yes |
| Scheduled release dates | No | No | Yes |
| Team size | Any (with CI) | ≤ 20 | Large or distributed |
| Release cadence | Continuous | Weekly or faster | Monthly+ |
