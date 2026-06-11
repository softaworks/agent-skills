# Skill Anti-Patterns — Detailed Reference

Load this file when: a draft skill matches one of the three patterns below, or when skill-judge scores D1 below 12/20.

---

## Pattern 1: The Tutorial Pattern

**What it looks like**

SKILL.md opens with "What is X?", defines terms, walks through a beginner workflow, and closes with "Next steps." It reads like a blog post or onboarding doc.

**Why it fails**

Claude's training includes most published tutorials, official documentation, and introductory guides for every major domain. A skill that recaps this content provides zero knowledge delta. On skill-judge D1, it will score 4-8/20. On D2, it will score 4-6/15 because it transfers no thinking patterns, only facts Claude already has.

**Diagnostic test**

Search your SKILL.md for these phrases:
- "X is a..."
- "To get started..."
- "The following steps..."
- "For more information, see..."
- Any sentence that defines a term or concept

If you find more than 2-3 of these, you have the Tutorial Pattern.

**Fix**

Delete every definition and introductory paragraph. Replace them with:
- The decision you make that beginners get wrong
- The edge case the documentation doesn't cover
- The failure mode that only surfaces in production

Example replacement:
- Instead of: "A playbook is a structured response procedure for security incidents."
- Write: "Playbooks fail at the branch points — the places where the procedure says 'if X, do Y' but doesn't say how to determine whether X is true. Every NEVER item should be about a branch point failure, not a general warning."

---

## Pattern 2: The Dump Pattern

**What it looks like**

SKILL.md contains every note, link, checklist, decision tree, script snippet, and passing thought the author ever had about the domain. It is 600-900 lines. Sections are comprehensive. Nothing is missing. Nothing is compressed.

**Why it fails**

Every skill activation loads the full SKILL.md into context. A 700-line skill costs 700 lines of context on every trigger — whether the user needed 50 lines or all 700. The cognitive compression that makes expert knowledge valuable is absent: you have the raw material but not the insight. On skill-judge, it will score 4-8/20 on D1 (volume without delta), 4-8/15 on D5 (progressive disclosure failure), and likely fail D7 (pattern recognition) if sections aren't structured.

**Diagnostic test**

- Line count over 500? Likely Dump Pattern.
- Does every section have roughly equal length? Dump Pattern.
- Are there 3+ tables of reference data that never change? Dump Pattern.
- Could you cut 40% of the content and lose nothing an expert would miss? Dump Pattern.

**Fix**

1. Apply the knowledge delta scan: mark [E], [A], [R] on every paragraph.
2. Delete all [R] content.
3. For [A] content: cut by 60%, keep only the trigger/reminder phrases.
4. For [E] content that is deep reference material (tables, schemas, examples): move to `references/` files with loading triggers.
5. What remains in SKILL.md should be decision frameworks and heuristics only.

---

## Pattern 3: The Orphan References Pattern

**What it looks like**

The skill has a `references/` directory with 3-5 well-written, detailed files. SKILL.md ends with a "Reference Docs" section listing them. When Claude activates the skill, it reads SKILL.md, sees the list, and does not load the files — because there is no conditional trigger telling it to.

**Why it fails**

Claude does not speculatively load files referenced in a list. It loads files only when explicitly instructed by a conditional in a decision tree or workflow step. A references/ directory without loading triggers is dead content — it wastes disk space, misleads the author into thinking depth is covered, and results in a skill that appears complete but behaves as if the reference files don't exist.

**Diagnostic test**

Look at every reference to a `references/` file in SKILL.md:
- Is it in a decision tree row with a conditional ("Load X when Y")?
- Is it in a workflow step with a conditional ("If scenario Z, load references/X.md")?

If it is only in a list, table, or footer without a conditional trigger, it is an orphaned reference.

**Fix**

For each reference file, identify the specific scenario that warrants loading it:
- "Load `references/scoring-rubric.md` when detailed rubric for any single dimension is needed"
- "Load `references/failure-patterns.md` when diagnosing a structural failure"

Add these as rows in a decision tree or as conditional steps in a workflow. If you cannot identify a specific scenario, delete the reference file — it is not needed.

---

## Scoring Impact of Each Pattern

| Pattern | D1 Impact | D5 Impact | Other |
|---------|-----------|-----------|-------|
| Tutorial | -8 to -12 | none | D2 -6, D8 -4 |
| Dump | -8 to -12 | -8 to -12 | D7 -4 |
| Orphan References | none | -8 to -12 | D8 -4 |

A skill with all three patterns simultaneously will score below 60/120 (F grade) regardless of how professional it looks.
