---
name: requirements-clarity
description: Transform vague requirements into development-ready PRDs through focused dialogue. Trigger phrases: "clarify requirements", "need a PRD", "spec out this feature", "what do I need before coding", "requirement is unclear". Use when features are ambiguous, complex (>2 days), or cross-team. Do NOT use for bug fixes with clear repro steps.
---

## Mindset

- **Ambiguity is expensive late, cheap early.** A 20-minute clarification session prevents a 3-day rewrite. The user asking for "a login feature" has a mental model — your job is to surface it, not fill gaps with assumptions.
- **YAGNI before elaborating.** Before exploring implementation depth, ask "Is this confirmed needed now, or anticipated future need?" Features built for imagined futures become maintenance debt.
- **KISS before complexity.** After the user describes what they want, ask "Is there a simpler version that gets 80% of the value?" Complex solutions chosen by default — not by necessity — are a practitioner anti-pattern.
- **Questions reveal assumptions, not ignorance.** Each question you ask exposes a hidden assumption the user was carrying. Surface it, confirm it, and document it — that's the whole job.
- **The PRD is a contract, not a template.** A PRD filled with placeholders is worse than no PRD — it creates false confidence. Every section must contain substance before you write it.

## Navigation

**Use this skill when**:
- Requirements are vague ("add authentication", "build a dashboard", "implement payments")
- No acceptance criteria, success metrics, or edge cases mentioned
- Feature is estimated > 2 days or touches multiple teams
- User explicitly asks to "clarify", "spec out", or "write a PRD"

**Do NOT use this skill when**:
- Specific file paths, line numbers, or code snippets are provided
- Bug fix with clear reproduction steps
- Refactoring within existing clearly-scoped function/class
- User asks for implementation, not specification

**Decision tree for ambiguous invocations**:
```
Has the user provided concrete acceptance criteria?
  YES → Skip to gap analysis; you may reach 90+ in one pass
  NO  → Full clarification flow (Steps 1-4)

Is the request a bug report?
  YES → Exit this skill; suggest code-review or direct debugging
  NO  → Continue
```

## Philosophy

Clarity is not achieved by asking more questions — it is achieved by asking the *right* questions in the right order. Ask for the business problem before the technical solution, the user's definition of success before the implementation details, and the explicit exclusions before the edge cases.

## NEVER

- **NEVER generate the PRD before clarity score ≥ 90** — because a low-score PRD looks complete but omits exactly the constraints that cause implementation failures (security requirements, performance bounds, error states). False completeness is more dangerous than an acknowledged gap.
- **NEVER ask all questions at once** — because users answer fewer questions when overwhelmed, and the answers become shallower. Two focused questions get more signal than twelve scattered ones.
- **NEVER assume a technical choice the user hasn't confirmed** — because framework choices, database decisions, and API contracts constrain future work. An unconfirmed assumption embedded in a PRD becomes a hidden dependency that breaks integration.
- **NEVER skip the YAGNI gate** — because "we might need this later" is the most common driver of scope bloat in PRDs, and scope bloat in a PRD becomes scope creep in implementation. Surface the tension before it enters the document.
- **NEVER write vague acceptance criteria** — "the feature should work correctly" is not a criterion. Every acceptance criterion must be testable: a specific behavior, a measurable threshold, or a verifiable state. Untestable criteria guarantee disputed completions.
- **NEVER close a clarification round without updating the score** — because the score is the only shared signal that tells the user how close they are. Skipping score updates makes the process feel arbitrary and erodes trust in the output.
- **NEVER ask about solutions before understanding the problem** — asking "what tech stack?" before "what problem does this solve?" anchors the conversation in implementation details and obscures whether the feature is necessary at all.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| User gives one-word answers to every question | Questions are too abstract or feel like a test | Switch to example-anchored questions: "Would this be more like X or Y?" |
| Score plateaus below 90 after 4+ rounds | Hitting a genuine unknown (the user doesn't know yet) | Document the gap explicitly in the PRD as a decision deferred to implementation; don't block on it |
| User wants to skip clarification and just start | They've clarified mentally but not in writing | Run a rapid single-pass: surface only the non-negotiable gaps (security, data model, external integrations) and proceed |
| PRD scope grows with every round | No explicit exclusion list established early | Stop and co-author an "Out of Scope" section before continuing inward questions |
| User approves PRD with obvious gaps | Rubber-stamp behavior / cognitive overload | Call out the three riskiest open items explicitly; get explicit confirmation on each before closing |

## Clarification Process

### Step 1: Initial Analysis

Parse the requirement, assign a clarity score (0-100), identify what's clear and what's missing.

Score dimensions and weights → see `references/clarity-scoring.md`

Initial response format:
```
Current Clarity Score: X/100

Clear: [what you understand]
Gaps: [what's missing, grouped by dimension]

[First 2-3 questions, highest-impact first]
```

### Step 2: YAGNI + KISS Gates

Before proceeding to technical depth, explicitly run:
1. **YAGNI**: "Is this feature confirmed needed now?" Surface if it's speculative.
2. **KISS**: "Is there a simpler path that delivers 80% of the value?" Document both options if found.

### Step 3: Interactive Clarification

- 2-3 questions per round, highest-impact gaps first
- Update score after each round
- If score < 90: continue; if ≥ 90: generate PRD
- Reference `references/clarity-scoring.md` for round-by-round question strategy

### Step 4: PRD Generation

Once score ≥ 90, generate the PRD using the template in `references/prd-template.md`.

Output path: `./docs/prds/{feature-name}-v{version}-prd.md`

Every section must contain substance. Placeholders are not acceptable in a finalized PRD.

Once clarity ≥ 90 and the PRD is generated, the natural next step is gepetto to create a sectionized implementation plan from the PRD.

## References

- `references/clarity-scoring.md` — scoring rubric, YAGNI/KISS gates, round-by-round question strategy
- `references/prd-template.md` — complete PRD structure with all required sections
