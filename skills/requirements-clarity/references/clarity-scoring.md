# Clarity Scoring Rubric

Score each dimension after every user response. Stop asking when total ≥ 90.

## Dimensions

| Dimension | Max | What Counts |
|-----------|-----|-------------|
| Functional Clarity | 30 | Clear inputs/outputs (+10), user interaction defined (+10), success criteria stated (+10) |
| Technical Specificity | 25 | Tech stack named (+8), integration points identified (+8), constraints specified (+9) |
| Implementation Completeness | 25 | Edge cases enumerated (+8), error handling described (+9), data validation specified (+8) |
| Business Context | 20 | Problem statement clear (+7), target users identified (+7), success metrics defined (+6) |

## Round-by-Round Question Strategy

**Round 1 — highest-impact gaps first** (usually Functional Clarity + Business Context):
- What problem does this solve for which users?
- What are the inputs and expected outputs?
- What does success look like — how will you measure it?

**Round 2 — technical grounding**:
- What's the existing tech stack and where does this fit?
- What are the hard constraints (latency, cost, compliance)?
- What integrations are required vs. optional?

**Round 3 — edge cases and failure modes**:
- What happens when [most likely failure]?
- What's explicitly out of scope for v1?
- What's the rollback plan if this breaks?

## YAGNI Gate (ask before scoring Technical Specificity)

Before scoring, ask: "Is this feature confirmed needed now, or is it anticipated future need?"
- If anticipated future need → surface the YAGNI tension explicitly; offer to scope down.
- If confirmed need → proceed.

## KISS Gate (ask before scoring Implementation Completeness)

Ask: "Have we considered a simpler solution that gets 80% of the value?"
- If a simpler path exists → document both options in the PRD with tradeoffs.
- If complex is justified → document the justification.
