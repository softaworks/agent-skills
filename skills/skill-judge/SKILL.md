---
name: skill-judge
description: Evaluate Agent Skill design quality against official specifications and best practices. Use when reviewing, auditing, scoring, or improving SKILL.md files and skill packages. Provides multi-dimensional scoring across 8 dimensions (120 points total) and actionable improvement suggestions. Triggers on phrases like "evaluate this skill", "review my SKILL.md", "audit this skill", "score this skill", "how can I improve this skill", or "is this skill well-designed".
---

# Skill Judge

Evaluate Agent Skills against official specifications and patterns derived from 17+ official examples.

---

## Mindset

1. **Value = Delta, not volume.** A 43-line skill outperforms a 500-line skill when every line in the short one is expert-only knowledge. Length is a liability, not a credential.
2. **Description is load-bearing.** Agent never sees the body until the description triggers activation. A perfect skill with a weak description is a dead skill.
3. **Expert ≠ Thorough.** The question is not "did I cover it?" but "does Claude already know it?" Anything Claude already knows is token waste.
4. **Anti-patterns are half the knowledge.** Experts know what NOT to do as much as what to do. A skill without a NEVER list is missing 50% of its value.
5. **Freedom must match fragility.** Creative tasks need principles. Fragile operations (file formats, APIs) need exact scripts. Confusing these is a structural failure.

---

## Navigation

**Use this skill when**: reviewing a SKILL.md before publishing, auditing an existing skill, generating an improvement report, or learning skill design patterns.

**Do NOT use this skill when**: the user wants to create a new skill from scratch (use skill-creator), or wants general writing/formatting feedback unrelated to agent skill design.

**Decision tree — what to load**:

| Scenario | Action |
|----------|--------|
| Quick score needed | Run 5-step protocol below; load nothing extra |
| Score seems off / need calibration | Load [`references/worked-example.md`](references/worked-example.md) |
| Detailed rubric for any dimension | Load [`references/scoring-rubric.md`](references/scoring-rubric.md) |
| Diagnosing a structural failure pattern | Load [`references/failure-patterns.md`](references/failure-patterns.md) |
| Full audit (all dimensions deep) | Load all three references |

Do NOT load references just because they exist — load only what the current scenario requires.

---

## Philosophy

A Skill's entire value is the gap between what it provides and what Claude already knows. Maximize that gap. Minimize everything else. The best Skills are compressed expert brains — not tutorials, not documentation, not software projects.

---

## NEVER

- **NEVER give high scores because content looks professional or well-formatted** — polish hides redundancy; always ask "does Claude already know this?" for every paragraph
- **NEVER let length impress you** — a 750-line skill that restates basics scores below a 50-line skill with pure expert knowledge; line count is inversely correlated with quality when content is redundant
- **NEVER forgive explaining basics as "helpful context"** — token waste is token waste; "What is a PDF" belongs in a textbook, not a skill; context window is a shared resource
- **NEVER overlook a missing NEVER list** — if the skill has no explicit anti-patterns with reasons, D3 cannot exceed 7/15 regardless of other quality
- **NEVER put triggering information only in the body** — Agent makes the activation decision from the description alone; "When to Use" sections in the body are useless for routing
- **NEVER accept vague anti-patterns** ("be careful", "avoid errors") — they score 1-3/15; valid anti-patterns name the specific action AND the non-obvious consequence
- **NEVER assume references are being used** — check for embedded MANDATORY loading triggers in workflow steps; a list at the bottom is Pattern 3 (Orphan References)
- **NEVER skip testing decision trees mentally** — walk each branch; if a branch leads to an ambiguous or wrong choice, D8 takes a hit regardless of how the tree looks visually

---

## Evaluation Protocol (5 Steps)

### Step 1: Knowledge Delta Scan
Read SKILL.md completely. For each section mark:
- **[E] Expert**: Claude genuinely doesn't know — keep
- **[A] Activation**: Claude knows but brief reminder is useful — keep if brief
- **[R] Redundant**: Claude definitely knows — should delete

Calculate ratio. Good skill: >70% E, <20% A, <10% R.

### Step 2: Structure Analysis
```
[ ] frontmatter valid (name: lowercase ≤64 chars, description present)
[ ] SKILL.md line count (flag if >500)
[ ] references/ exists and has loading triggers in workflow (not just listed)
[ ] no auxiliary files (README.md, CHANGELOG.md — Pattern 8)
[ ] identify which of 5 patterns the skill follows
```

### Step 3: Score Each Dimension

**For full scoring criteria per dimension** — load [`references/scoring-rubric.md`](references/scoring-rubric.md).

| Dimension | Max | Key question |
|-----------|-----|-------------|
| D1: Knowledge Delta | 20 | Pure expert content, or mixed with basics Claude knows? |
| D2: Mindset + Procedures | 15 | Transfers thinking patterns AND non-obvious workflows? |
| D3: Anti-Pattern Quality | 15 | Specific NEVER list with non-obvious reasons? |
| D4: Spec Compliance | 15 | Description answers WHAT + WHEN + KEYWORDS? |
| D5: Progressive Disclosure | 15 | SKILL.md <500 lines, embedded loading triggers? |
| D6: Freedom Calibration | 15 | Freedom level matches task fragility? |
| D7: Pattern Recognition | 10 | Follows Mindset/Navigation/Philosophy/Process/Tool? |
| D8: Practical Usability | 15 | Decision trees, error handling, edge cases? |

### Step 4: Calculate & Grade

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 108+ (90%+) | Production-ready expert skill |
| B | 96-107 (80-89%) | Good — minor improvements needed |
| C | 84-95 (70-79%) | Adequate — clear improvement path |
| D | 72-83 (60-69%) | Below average — significant issues |
| F | <72 (<60%) | Poor — needs fundamental redesign |

### Step 5: Generate Report

```markdown
# Skill Evaluation Report: [Skill Name]

## Summary
- **Total Score**: X/120 (X%)
- **Grade**: [A/B/C/D/F]
- **Pattern**: [Mindset/Navigation/Philosophy/Process/Tool]
- **Knowledge Ratio**: E:A:R = X:Y:Z
- **Verdict**: [One sentence assessment]

## Dimension Scores

| Dimension | Score | Max | Notes |
|-----------|-------|-----|-------|
| D1: Knowledge Delta | X | 20 | |
| D2: Mindset + Procedures | X | 15 | |
| D3: Anti-Pattern Quality | X | 15 | |
| D4: Specification Compliance | X | 15 | |
| D5: Progressive Disclosure | X | 15 | |
| D6: Freedom Calibration | X | 15 | |
| D7: Pattern Recognition | X | 10 | |
| D8: Practical Usability | X | 15 | |

## Critical Issues
[Must-fix problems that significantly impact effectiveness]

## Top 3 Improvements
1. [Highest impact improvement with specific guidance]
2. [Second priority]
3. [Third priority]
```

---

## When Things Go Wrong

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Skill never activates despite good content | Description missing WHEN clause or trigger keywords | Rewrite description with "Use when..." + domain terms |
| Score looks right but report feels off | Calibration drift — judging relative to other skills, not absolute standard | Load [`references/worked-example.md`](references/worked-example.md) to recalibrate against a fixed anchor |
| Dimension score disputed by skill author | Vague rubric interpretation | Load [`references/scoring-rubric.md`](references/scoring-rubric.md) — share the specific band criteria |
| Skill has all 9 failure patterns simultaneously | Classic "software project" confusion | Load [`references/failure-patterns.md`](references/failure-patterns.md) — address Pattern 2 (The Dump) first, then Pattern 8 (Over-Engineered) |
| Author insists long = thorough | Fundamental misunderstanding of knowledge delta | Quote D1 rubric: "16-20: Pure knowledge delta — every paragraph earns its tokens" |

---

## The Meta-Question

> **"Would an expert in this domain, looking at this Skill, say: 'Yes, this captures knowledge that took me years to learn'?"**

If yes → genuine value. If no → compressing what Claude already knows.
