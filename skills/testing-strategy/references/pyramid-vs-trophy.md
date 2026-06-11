# Pyramid vs. Trophy: Worked Examples

## When the Pyramid Wins

**Scenario**: A tax calculation engine with 40 business rules.

The business logic is pure: inputs are financial values, outputs are computed amounts. Each rule is testable in isolation. Integration is thin: one DB read at start, one write at end. Running 400 unit tests takes 2 seconds.

Pyramid shape: 400 unit tests, 10 integration tests (DB round-trip), 3 E2E (critical user paths).

The unit tests catch: wrong formula, wrong rounding mode, wrong bracket boundary, missing deduction.
The integration tests catch: wrong ORM query, missing transaction, schema mismatch.
The E2E tests catch: page crashes, form submission failure, result display error.

**Signal that pyramid is right**: look at recent bugs — they were arithmetic errors in the logic layer, not integration failures.

---

## When the Trophy Wins

**Scenario**: A CRUD admin panel — users, roles, organizations, permission inheritance.

The "business logic" is: read from DB, transform slightly, write to DB. Unit testing the transformation layer tests almost nothing useful. The real failure modes are: wrong JOIN producing incorrect permission inheritance, missing WHERE clause exposing wrong tenant's data, ORM eager-loading N+1 that works in tests but crashes production under load.

Trophy shape: 20 unit tests (pure transformation utilities), 150 integration tests (real DB in Docker, full request-to-response), 10 E2E (auth flow, permission boundary, multi-tenant isolation).

The integration tests catch: wrong query, missing RLS policy, incorrect cascade behavior.
The unit tests would have caught: none of the real bugs.

**Signal that trophy is right**: every recent production bug was an integration failure; your unit tests have never caught a bug in production.

---

## The Diagnostic Test

Before choosing pyramid or trophy for a new system, run this exercise:

1. List the last 10 bugs that reached production.
2. Classify each: "Would a unit test have caught this?" vs. "Would an integration test have caught this?"
3. The ratio tells you your bug distribution. Match your test distribution to your bug distribution.

If 8/10 were integration bugs and you build a unit-heavy pyramid, 80% of your test investment covers 20% of your risk.

---

## The Hybrid Trap

Teams often build a hybrid without realizing it: unit tests for everything, plus integration tests for everything, plus E2E for everything — triple coverage with triple maintenance. This happens when the pyramid is applied as a rule ("always write unit tests") rather than a tool.

Signs of the hybrid trap:
- A unit test and an integration test for the same behavior in the same commit
- E2E tests that test the same flows as integration tests, just slower
- Test suite takes 30+ minutes; nobody runs it locally

Fix: audit which layer is actually catching bugs. Cut the layers that aren't. The rule is coverage of risk, not coverage of layers.
