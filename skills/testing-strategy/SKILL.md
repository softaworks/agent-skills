---
name: testing-strategy
description: Design automated test suites — test double taxonomy, pyramid vs. trophy tradeoffs, TDD applicability, Playwright vs. Cypress selection, flakiness diagnosis, coverage policy, and boundary-value patterns. Use when asked to "design a test strategy", "choose a test framework", "fix flaky tests", "set coverage thresholds", "write unit vs. integration tests", or "should I TDD this". Sits alongside qa-test-planner (manual testing) and code-review (correctness review).
trigger: explicit
---

## Mindset

- **The test that never fails has negative value.** It consumes maintenance time, produces false confidence, and is invisible until it misleads someone at a critical moment. Before writing any test, ask: "What specific incorrect behavior would this catch?" If you can't answer, don't write it.
- **Integration is where bugs live, not units.** A system where every unit test passes and users still see errors is telling you something: the units are wrong, or the contracts between them are. Heavy unit pyramids are a bet that your units are the failure mode — that bet loses constantly.
- **Mocks are a debt instrument.** Every mock you write is a promise to keep the mock in sync with the real implementation. That promise defaults silently: the test keeps passing, the production call has changed, users see the failure. Prefer fakes; they break loudly when the contract changes.
- **Flakiness is determinism debt.** A flaky test has a hidden dependency on time, ordering, or external state. It will not spontaneously fix itself. Treat the first flaky test in a suite as a severity-1 issue: it destroys trust in the entire suite, because developers start ignoring red builds.
- **Coverage is a floor detector, not a quality signal.** A line covered without an assertion proves only that the code ran. Mutation testing reveals what coverage hides: tests that watch code execute but assert nothing meaningful.

## Navigation

**Use this skill when**:
- Designing the automated test architecture for a new project or service
- Choosing between unit-heavy pyramid vs. integration-heavy trophy structure
- Selecting Playwright vs. Cypress for an E2E layer
- Diagnosing and fixing flaky tests in CI
- Setting or challenging coverage threshold policies
- Deciding whether to TDD a component or feature
- Untangling stub/mock/fake/spy confusion in an existing suite

**Do NOT use this skill when**:
- Writing manual test cases, test plans, or regression suites — use **qa-test-planner**
- Reviewing production code for logic bugs — use **code-review**
- Designing acceptance criteria during sprint planning — that's requirements-clarity territory

**Ambiguous input decision tree**:
```
"Write tests for X"
  Is X a pure function with defined I/O? → YES → unit tests, consider TDD
                                         → NO  ↓
  Is X a UI component or page flow?      → YES → integration or E2E; skip unit layer
  Is X a cross-service contract?         → YES → contract test (Pact) or integration test
  Does X involve a database?             → YES → integration with real DB in container; no mocks

"Our tests are flaky"
  Fails intermittently in CI, passes locally? → timing/environment drift (see Flakiness section)
  Fails when run in bulk, passes alone?       → shared mutable state (see State Pollution)
  Fails after unrelated code change?          → over-specified mock (replace mock with fake)

"What coverage should we target?"
  Greenfield project:                    → 80% line as floor, enforce branch coverage
  Legacy codebase:                       → ratchet (never allow regression), not arbitrary target
  Critical financial/safety system:      → mutation testing required; line % is insufficient
```

## Philosophy

A test suite is a safety net, not a trophy case. Its job is to catch regressions fast enough that the team trusts it and runs it constantly. Speed, reliability, and signal-to-noise ratio matter more than total test count or coverage percentage. A slow, flaky suite that developers skip in CI is worse than no suite: it's actively misleading.

## NEVER

- **NEVER use `sleep()` in tests** — it sets a minimum wait that will still race on slow CI, while adding that minimum latency to every run forever. Use `waitFor`, polling assertions (`expect.poll`), or event-driven synchronization (`waitForSelector`, `waitForResponse`).
- **NEVER assert on implementation details (function was called with X) instead of observable behavior (output is Y)** — implementation assertions break on every valid refactor, training developers to treat red tests as expected noise. Mock-verification tests confirm process, not outcomes.
- **NEVER share mutable state between tests without explicit reset** — the test that fails on CI but passes locally has exactly one cause 90% of the time: run ordering. Global state initialized once becomes an implicit ordering dependency that the test runner will eventually expose.
- **NEVER use a mock when a working fake is available** — mocks couple test assertions to call signatures; fakes exercise real behavior through the real interface. A fake breaks loudly when behavior changes; a mock passes silently while the production code diverges.
- **NEVER write a test that cannot fail** — a `describe` block wrapping an empty `it` block, a catch that swallows assertion errors, or a `try/catch` around `expect(...)` all produce permanently-green tests. They consume maintenance time and generate false confidence.
- **NEVER use real network calls in unit or integration tests** — latency makes the suite slow; network unavailability makes it flaky; third-party rate limits make it unreliable in burst CI. Seal all HTTP with MSW (browser/Node), Nock (Node), or WireMock (JVM/polyglot).
- **NEVER treat 80% line coverage as a goal** — it's a floor. A suite at 80% line coverage with no branch coverage and no assertions on edge cases is theater. Mutation testing is the only tool that distinguishes covered-and-asserting from covered-and-watching.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Test passes locally, fails in CI | Environment drift or timing dependency | Add `CI=true` locally to reproduce; eliminate `sleep`; audit shared state reset |
| Test passes alone, fails in suite | Mutable global state leaked between tests | Add `beforeEach` reset; grep for module-level mutables; run in random order to surface more |
| Refactor breaks 30 tests that should still pass | Tests assert on implementation (mocks verifying call args) | Replace mock-verification tests with behavior assertions; rewrite to test outputs, not calls |
| Coverage drops after adding features | New branches not covered; not a problem if thresholds are branch-based | Add boundary tests for new conditionals; do not chase line coverage alone |
| E2E suite takes 45+ minutes | Too many E2E tests covering what integration tests should handle | Audit which E2E tests duplicate integration coverage; move them down the pyramid |
| Flaky test fixed with a longer sleep | The race condition was treated, not cured | Find the event or state change that indicates readiness and wait on that explicitly |

## Test Double Taxonomy

Practitioners use these terms interchangeably and incorrectly. Precision matters because the choice changes what the test proves:

| Double | Definition | Tests | Breaks When |
|--------|-----------|-------|-------------|
| **Stub** | Returns canned data; no call verification | Code handles specific return values | Canned data drifts from real API response shape |
| **Mock** | Verifies specific calls were made | A specific interaction occurred | Refactor changes the call signature (even correctly) |
| **Fake** | Working implementation with shortcuts (in-memory DB) | Real behavior through real interface | Fake diverges from real implementation semantics |
| **Spy** | Records calls without blocking them | Side effects occurred while real logic ran | The real call has unacceptable side effects in test |

**Decision rule**: Use fakes by default. Use stubs when you control the return value shape and it won't drift. Use spies when you need to verify side effects without blocking production logic. Use mocks only when you have no other option and accept that the test is coupled to implementation.

## Pyramid vs. Trophy

The test pyramid (many unit, fewer integration, few E2E) is the right default when:
- The system is composed of pure functions and well-scoped units
- Integration points are thin and well-defined (a single API client, a single DB adapter)
- Unit tests run in milliseconds and give fast feedback loops

The test trophy (fewer unit, more integration, some E2E) is the right choice when:
- The system is CRUD-heavy and the "business logic" is mostly data transformation through layers
- Integration failures are the most common bug category (mismatched schemas, wrong query, missing join)
- The team has historically seen unit-passing/integration-failing bugs

**Diagnostic**: Look at your last 10 production bugs. Were they unit-level logic errors or integration/contract failures? The answer tells you which shape your suite should be.

See `references/pyramid-vs-trophy.md` for worked examples.

## TDD Decision Framework

TDD accelerates when:
- The interface is known before you start (function signature is defined by a contract)
- The behavior is pure and well-scoped (no UI, no external I/O in the unit)
- You need to drive the design (writing the test first reveals bad API surface before implementation locks it in)

TDD fights you when:
- The interface is unknown and exploratory (you're figuring out what the function should look like)
- The unit under test is UI-heavy (the test framework overhead exceeds the feedback value)
- The code is data-pipeline heavy and test data setup dominates test writing time
- You're working in a system where the seams don't exist yet and you'd spend 80% of the time creating test infrastructure

**Practical rule**: TDD for business logic and domain functions. Spike-then-test for UI, data ingestion, and exploratory integrations. Retrofit tests on spikes before merging.

## Playwright vs. Cypress

| Criterion | Playwright | Cypress |
|-----------|-----------|---------|
| Multi-browser (Chromium, Firefox, WebKit) | Native | Chrome/Electron primarily |
| Multi-tab / multi-window testing | Native | Not supported |
| API mocking (intercept, mock route) | `route.fulfill()` — first-class | `cy.intercept()` — good but browser-scoped |
| CI performance | Parallel sharding out of the box | Requires Cypress Cloud for parallelism |
| Interactive debugging DX | Trace Viewer (after the fact) | Time-travel with real-time UI |
| Network request inspection | Built-in HAR capture | DevTools integration |
| Component testing | Available (experimental) | Mature component testing mode |

**Decision rule**: Choose Playwright when multi-browser, multi-tab, or strong API mocking is required, or when CI parallelism is important at scale. Choose Cypress when the team needs interactive debugging in Chrome-only projects and component testing maturity matters.

See `references/e2e-framework-patterns.md` for CI configuration patterns for both.

## Boundary-Value Pattern

Bugs live at boundaries, not in the middle of ranges. For every conditional in business logic:

```
If condition is: value >= minimum
Test:            minimum - 1 (should fail)
                 minimum     (should pass — the exact boundary)
                 minimum + 1 (should pass)

If condition is: array.length > 0
Test:            empty array (0 items)
                 single item (1 item)
                 two items (behavior stable)
```

Common missed boundaries: empty string vs. whitespace-only string, null vs. undefined vs. missing key, zero vs. negative, max integer overflow, end of month/year in date logic, timezone boundaries at midnight.

See `references/boundary-testing-patterns.md` for a full catalog by data type.

## Coverage Policy

- **Line coverage 80%**: minimum floor; below this, you have blind spots large enough to hide feature-scale bugs
- **Branch coverage**: more meaningful than line; a line with three branches at 100% line coverage but 33% branch coverage is a test gap
- **Mutation testing** (Stryker, PITest): the only tool that distinguishes "covered" from "asserting"; run on critical modules; a mutation score below 70% means your tests are watching, not verifying
- **Ratchet pattern for legacy code**: set threshold to current value; enforce "never go below current"; add tests incrementally rather than chasing an arbitrary target in one sprint
