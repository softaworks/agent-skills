---
name: code-review
description: Expert code review covering severity calibration, diff-vs-full-file gaps, feedback categorization (correctness/comprehensibility/conventions), language-specific anti-patterns in JS/TS/Python/SQL, the second-read technique, test review, and feedback phrasing. Use when performing a code review, reviewing a pull request, giving or receiving PR feedback, or evaluating code quality. Triggers on phrases like "review this code", "review this PR", "give me feedback on this diff", "how should I review this", "what should I check", "code quality feedback", or "how do I respond to review comments".
---

# Code Review

A code review has one job: find the things the author couldn't find because they're the author.

---

## Mindset

1. **Severity inflation is a social phenomenon, not a technical one.** Reviewers upgrade findings to blockers to feel impactful or to ensure they're taken seriously. The result: authors stop distinguishing real blockers from theater, and everything becomes a negotiation. Your credibility as a reviewer lives and dies by accurate severity labels — one false blocker devalues the next ten real ones.
2. **A diff is a crime scene, not the crime.** What you see changed; you don't see what accumulated. Dead code that's been there three years, a function that grew from 20 to 80 lines across six PRs, a pattern that diverged from the rest of the codebase six months ago — none of these appear in the diff, but all of them compound every time a new diff lands on top of them.
3. **The author knows things you don't — but that's the bug.** If understanding the code requires knowing the PR description, the Slack thread, or the author's intent, the code is wrong. The code must communicate that context itself. Feedback that says "I needed the PR description to understand this" is always valid.
4. **Tests are the second implementation.** A test that always passes regardless of what the implementation does is not a test — it is false confidence deployed at scale. Reviewing tests is not optional; it is the highest-leverage activity in the review because a missed test failure will appear in production, not in a review thread.
5. **"I'd do it differently" is not a review finding.** Style preference dressed as correctness feedback is the primary source of reviewer-author friction. Know which category your feedback belongs to before you type it.

---

## Navigation

**Use this skill when**:
- Performing a code review on a PR, diff, or file set
- Drafting review comments and need calibration on tone or label
- Receiving review comments and deciding how to respond
- Designing a code review process or checklist for a team

**Do NOT use this skill when**:
- The task is security-specific (use `security-review` for XSS, injection, auth — the coverage there is deeper)
- The task is purely formatting or style (configure a linter; don't use human attention)
- The code has no test suite at all and the task is to add one (that's authoring, not reviewing)

**Decision tree — what to load for the current scenario**:

| Scenario | Action |
|----------|--------|
| Quick diff review | Apply 2-pass protocol below; no references needed |
| Reviewing tests specifically | Load [`references/test-review.md`](references/test-review.md) |
| JS/TS or Python/SQL anti-patterns | Load [`references/language-antipatterns.md`](references/language-antipatterns.md) |
| Writing or improving review comments | Load [`references/feedback-phrasing.md`](references/feedback-phrasing.md) |
| Receiving and responding to comments | Load [`references/feedback-phrasing.md`](references/feedback-phrasing.md) |
| Full review audit (all dimensions) | Load all three references |

Load only what the scenario requires.

---

## Philosophy

The goal of a code review is not to demonstrate that you read the code — it is to transfer knowledge, catch failure modes the author cannot see, and ensure the codebase is maintainable by people who weren't in the room. Every comment should serve one of those three purposes or it shouldn't be there.

---

## NEVER

- **NEVER approve a PR without checking the test diff** — untested code is the single most common regression source regardless of how clean the logic looks; no test diff means no confidence in correctness.
- **NEVER leave a comment without a severity label** — unlabeled feedback forces the author to guess whether the review is blocking; when in doubt, authors merge; the bug ships.
- **NEVER comment "this could be simplified" without showing the simplification** — vague suggestions create back-and-forth that stalls the PR and wastes two people's time; if you can't show it, it's not actionable feedback.
- **NEVER review style inconsistencies that a linter should catch** — your review attention is finite and nonrenewable; automating what's automatable is not laziness, it is correct resource allocation.
- **NEVER mark a PR "changes requested" for nits** — that status should be reserved for correctness and major issues; nits should accompany an approval with suggestions; blocking a PR over naming is reviewer overreach.
- **NEVER skip the PR description** — a missing or bad description is itself a review finding; a description that doesn't explain *why* the change exists tells you the author may not have thought it through, which means the code deserves extra scrutiny.
- **NEVER mix unlabeled correctness and style feedback in the same comment** — when a comment conflates "this is wrong" with "I prefer another approach," authors fix the preference and miss the bug.
- **NEVER use "just" in review comments** ("just rename this", "just extract a function") — "just" signals that the reviewer thinks the change is trivial; it is almost always perceived as dismissive even when the reviewer doesn't intend it.

---

## The 4-Tier Severity System

| Tier | Label | Meaning | PR action |
|------|-------|---------|-----------|
| 1 | **blocker** | Correctness failure, security hole, data loss, or contract violation | Must fix before merge |
| 2 | **major** | Significant maintainability damage, performance regression, or design smell | Should fix; author must acknowledge if not |
| 3 | **minor** | Improvement with meaningful but non-urgent value | Can defer; approve with suggestions |
| 4 | **nit** | Preference, style, trivial naming | Approve; author decides |

**Calibration rule**: before labeling a finding "blocker," ask: "Does merging this today cause a user-visible failure, data corruption, or a security breach?" If no, it is at most "major."

The over-promotion failure mode: reviewers label things blocker because they want to be heard. This is understandable and wrong. It trains authors to treat blockers as negotiating positions rather than hard stops. When a real blocker appears, it gets the same response as the last five false ones.

---

## The 2-Pass Review Protocol

### Pass 1: Correctness

Read the diff as if you're testing it. For each changed function or method:
- What are the inputs? What happens at the boundaries?
- What invariants does the caller assume? Does this maintain them?
- What is the error path? Is it handled or silently swallowed?
- For async/concurrent code: where are the race conditions?

Do not think about style. Do not think about naming. Find things that are wrong.

### Pass 2: The Second Read

Close the diff. Imagine you are a maintainer picking up this code in two years. You have no PR context, no author to ask, no Slack thread. Read the changed files (not the diff — the full files in context):
- Is the function's purpose clear from its name and signature alone?
- Does the complexity of this function fit on one screen? Has it grown past the point where a new contributor can hold it in working memory?
- Does this code follow the patterns established elsewhere in this file? In this module?
- Is there dead code that the change didn't need but also didn't clean up?

Findings from Pass 2 are typically "major" or "minor" — they are about the future cost of the code, not correctness today.

---

## 3 Categories of Feedback

Label every comment with its category. When categories are mixed unlabeled, authors don't know what's mandatory.

| Category | Definition | Label prefix |
|----------|-----------|-------------|
| **Correctness** | The code is wrong — it will produce incorrect results, errors, or security failures in some input condition | `correctness:` |
| **Comprehensibility** | The code is hard to understand — a future maintainer will spend extra time here | `comprehensibility:` |
| **Conventions** | The code diverges from team patterns — it's not wrong, but it increases cognitive load for the team | `conventions:` |

**Why this matters**: A reviewer who comments "this is confusing" is giving comprehensibility feedback. If the author hears it as conventions feedback, they'll rename a variable and consider it resolved. The label removes the ambiguity.

---

## Reviewing Tests

Load [`references/test-review.md`](references/test-review.md) for the full protocol. Core principle:

A test that would pass even if the implementation were wrong is not a test. It is a coverage number.

Checklist for each test in the diff:
- [ ] Would this test fail if you deleted the function under test?
- [ ] Would this test fail if the function returned the wrong type but not an error?
- [ ] Is the assertion on the thing that actually matters, or on a proxy?
- [ ] Are edge cases tested (empty, null, boundary values, error paths)?
- [ ] Is there a test for the behavior described in the PR, not just the happy path?

Tests that mock everything and assert on mock calls test the implementation, not the behavior. Implementation-coupled tests break on refactors and provide no correctness signal.

---

## Giving Feedback

- Prefix every comment with its category and severity: `correctness (blocker):`, `nit:`, `comprehensibility (minor):`
- Ask questions when uncertain rather than asserting: "Does this handle the case where X is null?" not "This will crash if X is null."
- Distinguish "I'd do it differently" from "this is wrong" — explicitly. Writing "I'd probably extract this into a helper, but I could see the case for keeping it inline" is better than either asserting wrongness or staying silent.
- When you suggest a simplification, show the simplified version. If you can't show it in a comment, it wasn't a clear enough idea to be actionable.

## Receiving Feedback

Load [`references/feedback-phrasing.md`](references/feedback-phrasing.md) for the full receiving protocol. The single most important rule:

**NEVER explain the context that makes the feedback wrong — fix the code so it communicates that context itself.**

If a reviewer misunderstood your code, the code is unclear regardless of your intent. The correct response to "I don't understand why this is a loop" is not "I explained it in the PR description" — it is a clarifying comment in the code.

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| PR review becomes a negotiation with the author | Reviewer didn't label severity; author is treating all findings as "major" by default | Re-label every comment with explicit tier; distinguish blockers from suggestions explicitly |
| Reviews take 3+ rounds of back-and-forth | Feedback is vague ("simplify this") or unlabeled; author is guessing what's required | Rewrite comments with category prefix, severity, and concrete suggestion inline |
| Author merged without addressing a blocker | Blocker wasn't marked as such; or reviewer mixed blockers and nits with no differentiation | Post-merge: open a follow-up issue immediately; in the team: calibrate what "blocker" means |
| Test coverage is high but bugs still ship | Tests are asserting on implementation details (mock calls) rather than behavior; or tests have tautological assertions | Review test assertions against the "would this fail if the impl were wrong?" checklist |
| Reviewer finds nothing in a large PR | Diff-only review mode; missed accumulation issues; or false confidence from clean diff | Run Pass 2 (full file in context); specifically look for growing function complexity and pattern drift |
| Author rewrites code in response to a nit | Reviewer marked a nit as blocker or changes-requested; author is being overly compliant | Establish team-level norms: nits accompany approvals, not change requests |
