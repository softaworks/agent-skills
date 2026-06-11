# QA Expert Heuristics

Practitioner decision trees and anti-pattern catalogs. This file contains domain knowledge that belongs outside the main SKILL.md to preserve progressive disclosure.

---

## Risk-Based Test Prioritization

When time is short (and it always is), allocate effort using this stack-ranked model:

```
TIER 1 — Test always, no exceptions
  ├── Flows that touch money (payment, billing, refunds)
  ├── Auth/session management (login, logout, token expiry)
  ├── Data persistence (save, delete, import/export)
  └── Security surfaces (input fields, file uploads, API endpoints)

TIER 2 — Test on every release
  ├── Primary user journeys for the feature under test
  ├── Any flow that changed in this release (regression)
  └── Integration points with external services

TIER 3 — Test before major releases
  ├── Edge cases and boundary values
  ├── Low-traffic but high-consequence paths
  └── Accessibility (keyboard nav, screen reader)

TIER 4 — Test when explicitly scoped
  ├── Performance under load
  ├── Cross-browser matrix beyond the primary browser
  └── Pixel-perfect visual matching
```

**Rule:** If you're told "we only have 2 hours," run all Tier 1 and the directly-changed Tier 2 items. Document what was skipped and why.

---

## Boundary Value Selection Rules

Don't test random values. Use these rules to find the inputs most likely to expose bugs:

| Input type | Values to test |
|------------|----------------|
| Numeric range (e.g., age 1-120) | Min (1), Max (120), Min-1 (0), Max+1 (121), midpoint (60) |
| String length limit (e.g., max 255 chars) | 0, 1, limit-1, limit, limit+1 |
| Required field | Empty string, whitespace-only, null (if API) |
| Select/dropdown | Each option individually; invalid option via API bypass |
| File upload | Min size (1 byte), max size, max+1, wrong MIME type, no extension |
| Date field | Today, past, future, 2/28/leap year, 12/31, timezone boundaries |
| Currency/decimal | $0.00, $0.01, large amount, negative, 3 decimal places |

**Anti-pattern:** Testing `username = "testuser"` and calling it coverage. Mid-range valid values don't find the bugs; boundaries do.

---

## Equivalence Partitioning: Which Partition to Pick

When an input space is too large to test exhaustively, identify partitions where all values in the partition should behave identically:

1. Identify valid partitions (inputs the system should accept)
2. Identify invalid partitions (inputs the system should reject)
3. Pick **one representative value per partition** — not several
4. Verify you've covered all invalid partitions, not just one

**Example — email field:**
- Valid: `user@domain.com` (standard format)
- Invalid #1: `nodomain` (no @)
- Invalid #2: `@nodomain.com` (no local part)
- Invalid #3: `user@` (no domain)
- Invalid #4: `user@domain` (no TLD — debatable by spec; clarify)
- Invalid #5: SQL injection: `'; DROP TABLE users; --`
- Invalid #6: XSS: `<script>alert(1)</script>@test.com`

---

## Blocked Test Escalation Decision Tree

```
Test is blocked →
  Can I work around it and test the same behavior another way?
    YES → document workaround, proceed, note in report
    NO  → Is the blocker expected to resolve within this sprint?
            YES → flag as BLOCKED, estimate when to retest
            NO  → escalate: this is a test environment/infrastructure risk
                  → notify lead, add to risk register, adjust exit criteria
```

**Rule:** Never mark a blocked test as PASS to maintain metrics. Mark it BLOCKED with a reason and estimated resolution.

---

## Regression Suite Culling Policy Template

Use this policy to prevent suite bloat:

```
RETIRE a test case when ALL of the following are true:
  1. It has passed 20+ consecutive runs without modification
  2. The underlying code area has not changed in 90+ days
  3. No production bug has been filed against this area in 6 months

ARCHIVE (don't delete) — move to archive/ folder with:
  - Date archived
  - Rationale
  - Reactivation condition ("reactivate if payment module changes")

ADD to suite immediately when:
  - A production bug is fixed (test for the exact defect)
  - A new integration point is added
  - A security finding is remediated
```

---

## Release Gate: Go / No-Go Checklist

Before signing off on a release, verify:

**Hard stops (any NO = no-go):**
- [ ] All P0 (critical) test cases passed
- [ ] Zero open severity-critical bugs
- [ ] Zero open severity-high bugs without an approved workaround
- [ ] Regression suite executed on release build (not a branch build)
- [ ] Security surfaces tested (auth, input validation, file upload)

**Risk accepts (document if NO, owner must sign off):**
- [ ] P1 tests ≥90% pass rate
- [ ] Mobile/responsive tested on primary device matrix
- [ ] Accessibility spot-checked
- [ ] Performance baseline within 20% of previous release

**Documentation complete:**
- [ ] Test run report filed with pass/fail counts
- [ ] All open bugs triaged with priority and ETA
- [ ] Rollback plan identified if critical bug emerges post-release

---

## Severity vs. Priority: The Matrix

Teams conflate these constantly. Use this:

| | Low Priority (can wait) | High Priority (fix now) |
|---|---|---|
| **High Severity** (data loss, crash) | Admin-only import crash with 3 users/month | Checkout crash on primary flow |
| **Low Severity** (cosmetic, typo) | Misaligned icon in footer | Wrong price text on pricing page |

**Severity** = scope of damage if triggered  
**Priority** = urgency of fix relative to release timeline

Always set them independently. If they always match, your team is conflating them.

---

## Common QA Anti-Patterns With Non-Obvious Reasons

| Anti-Pattern | Why It's Harmful (non-obvious) |
|---|---|
| Testing only with admin accounts | Admin users often bypass the permission/validation logic that regular users hit; bugs hide in lower-privilege flows |
| Running regression on staging with prod data | Test data side-effects (deletions, state changes) on prod data cause incidents; staging must use synthetic data |
| Writing test cases after execution | Confirmation bias — you write the expected result as what you observed, not what the spec says; bugs get missed |
| Using sequential test IDs without feature prefix | TC-1 through TC-500 in a flat namespace means a deleted test leaves a gap and you can't tell which feature lost coverage |
| Logging every UI variation as a separate bug | 10 bugs for "button color wrong on 10 pages" creates triage noise; one bug with a list of affected pages is the right pattern |
| Retesting the same happy path repeatedly | Happy paths don't find bugs; they confirm the system works when nothing goes wrong. Invest retest cycles in boundary and negative cases |
