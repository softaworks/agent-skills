---
name: qa-test-planner
description: Generate test plans, manual test cases, regression suites, and bug reports for QA engineers. Use when asked to write test cases, create a test plan, build a regression suite, validate a Figma design, or document a bug. Trigger phrases: "write test cases", "create test plan", "regression suite", "bug report", "QA plan", "validate against Figma".
trigger: explicit
---

# QA Test Planner

## Mindset

**Coverage is not quality.** 200 shallow test cases that don't find bugs are worse than 20 deep ones targeting real risk. Always ask: "What could go wrong here that would hurt users or the business?" — not "What steps can I list?"

**Test design reveals missing requirements.** When you can't write a test case because the expected result is undefined, that IS the bug — a requirements gap. Surface it instead of guessing.

**Regression suites rot.** A suite that hasn't been touched since it was written is a liability: it produces false confidence. Every new bug fixed in production is evidence that something escaped your suite — add a test for it immediately.

**Severity ≠ Priority.** A cosmetic bug on the checkout confirmation page (low severity, high priority) blocks revenue. A crash in an admin-only import tool (high severity, low priority) does not block release. Conflating these causes wrong release decisions.

**Bug reproduction is half the fix.** A bug report without a reliable repro is a guess. Before logging, validate that your steps reproduce the issue 3/3 times on a clean environment. If you can't get 3/3, say so explicitly.

---

## Navigation

**Use this skill when:**
- Writing manual test cases for a feature, flow, or API
- Producing a test plan document for a sprint, release, or project
- Building or triaging a regression suite (smoke, targeted, full)
- Validating UI implementation against Figma design specs
- Filing a structured bug report with reliable reproduction steps
- Reviewing test coverage gaps before a release

**Do NOT use this skill when:**
- Writing automated test code (unit tests, Selenium, Cypress, Playwright) — use a coding skill
- Defining acceptance criteria during sprint planning — that's product, not QA
- Reviewing PRs for logic bugs — use a code-review skill

**Ambiguous input decision tree:**

```
"Test X" →
  Has expected behavior defined? → YES → write test cases
                                 → NO  → surface requirements gap first
  Is X a feature or a bug? → FEATURE → test plan + cases
                           → BUG     → bug report + regression test
  Is there a Figma link? → YES → include Figma validation checklist
```

If test case writing reveals undefined expected behavior (requirements gap), pause and use requirements-clarity to surface and formalize the missing requirement before continuing.

---

## Philosophy

Test design is a risk-reduction activity, not a checklist activity. Allocate test effort proportional to consequence-of-failure, not proportional to feature size. The goal is to find bugs before users do — not to maximize test count.

---

## NEVER

- **NEVER write a test case without a specific expected result** — "it works correctly" is untestable. An expected result must be observable and falsifiable (exact text, HTTP status, pixel dimension, state change).

- **NEVER omit preconditions** — a test case that says "log in and navigate to checkout" without specifying which user account, what items are in the cart, or what environment is in use will produce inconsistent results and waste retest cycles.

- **NEVER rate severity and priority identically by default** — severity is about damage, priority is about when to fix it. Defaulting both to the same value causes triage meetings to debate bugs that don't need debating.

- **NEVER let a regression suite grow unbounded without a culling policy** — suites that only ever add tests become unmaintainable. Every suite needs an owner and a rule: "if a test has passed 20 consecutive runs with no related code changes, retire it to archive."

- **NEVER log a bug against design ambiguity as a severity-high defect** — if the spec doesn't define the behavior, the implementation isn't wrong, the spec is incomplete. Log it as a requirements clarification, not a defect; otherwise it creates adversarial dev-QA dynamics.

- **NEVER skip environment documentation in a bug report** — "it broke" without browser version, OS, build hash, and test account details cannot be reproduced by a developer in a different environment. Unreproducible bugs get closed or deprioritized.

- **NEVER treat Figma pixel-perfect matching as the exit criterion for UI** — Figma shows design intent, not the only valid implementation. ±2px on padding is noise; wrong color token, missing disabled state, or broken focus ring is a real bug. Calibrate accordingly.

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Tests pass but bugs still reach production | Suite covers happy paths only; no negative/edge-case tests | Audit the last 5 production bugs — add a test for each; add boundary and error-state cases |
| Developer closes bugs as "not reproducible" | Missing environment/build details in reports | Add a "verified repro: 3/3" line to every bug; include build hash and account used |
| Test plan is ignored by the team | Too long, too generic, not linked to actual tickets | Cut to 1 page; link every test area to a JIRA/ticket; include a go/no-go checklist |
| Figma validation produces endless disputes | No agreed tolerance defined | Agree upfront: layout ±4px OK, color tokens exact, interactive states exact |
| Regression suite takes too long to run | No smoke-first gating; suite not tiered | Add a 15-min smoke gate; if smoke fails, halt and do not run full suite |

---

## Usage

**Natural language requests:**

| Request | Output |
|---------|--------|
| "Create test plan for {feature}" | Test plan with scope, strategy, risks, entry/exit criteria |
| "Generate test cases for {flow}" | Step-by-step cases with preconditions and expected results |
| "Build smoke test suite" | Prioritized critical-path tests, execution order |
| "Compare with Figma at {URL}" | Component-by-component validation checklist |
| "Document bug: {description}" | Structured bug report with severity/priority guidance |

**Scripts:**

| Script | Purpose |
|--------|---------|
| `./scripts/generate_test_cases.sh` | Interactive test case generation |
| `./scripts/create_bug_report.sh` | Guided bug report input |

---

## Core Outputs

**Test Plans** — scope (in/out), strategy, environment requirements, entry/exit criteria, risk assessment with mitigations. See [test_case_templates.md](references/test_case_templates.md).

**Manual Test Cases** — atomic steps, explicit expected results per step, preconditions, test data, priority. See [test_case_templates.md](references/test_case_templates.md).

**Regression Suites** — tiered by duration (smoke 15-30 min / targeted 30-60 min / full 2-4 hr), execution order, pass/fail gate criteria. See [regression_testing.md](references/regression_testing.md).

**Figma Validation** — color token exact match, spacing within ±4px tolerance, all interactive states (hover/focus/disabled/active), responsive breakpoints. See [figma_validation.md](references/figma_validation.md).

**Bug Reports** — severity vs. priority matrix, verified repro steps (3/3), environment block, impact statement. See [bug_report_templates.md](references/bug_report_templates.md).

---

## Expert Heuristics Reference

See [heuristics.md](references/heuristics.md) for practitioner decision trees covering:
- Risk-based test prioritization (what to test first when time is short)
- Boundary value and equivalence partitioning selection rules
- When to escalate a blocked test vs. log it and move on
- Regression culling policy templates
- Release gate go/no-go checklist
