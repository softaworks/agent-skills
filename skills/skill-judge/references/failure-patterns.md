# Common Failure Patterns in Skill Design

Nine patterns observed across skill audits. Each has a signature symptom, root cause, and targeted fix.

---

## Pattern 1: The Tutorial
**Symptom**: Explains what PDF is, how Python works, basic library usage
**Root cause**: Author assumes Skill should "teach" the model
**Fix**: Claude already knows this. Delete all basic explanations. Focus on expert decisions, trade-offs, anti-patterns.

---

## Pattern 2: The Dump
**Symptom**: SKILL.md is 800+ lines with everything included
**Root cause**: No progressive disclosure design
**Fix**: Core routing and decision trees in SKILL.md (<300 lines ideal). Detailed content in `references/`, loaded on-demand.

---

## Pattern 3: The Orphan References
**Symptom**: References directory exists but files are never loaded
**Root cause**: No explicit loading triggers — just a list at the bottom
**Fix**: Add "MANDATORY - READ ENTIRE FILE" at workflow decision points. Add "Do NOT Load" to prevent over-loading.

---

## Pattern 4: The Checkbox Procedure
**Symptom**: Step 1, Step 2, Step 3... mechanical procedures
**Root cause**: Author thinks in procedures, not thinking frameworks
**Fix**: Transform into "Before doing X, ask yourself..." Focus on decision principles, not operation sequences.

---

## Pattern 5: The Vague Warning
**Symptom**: "Be careful", "avoid errors", "consider edge cases"
**Root cause**: Author knows things can go wrong but hasn't articulated specifics
**Fix**: Specific NEVER list with concrete examples and non-obvious reasons: "NEVER use X because [specific problem that takes experience to learn]"

---

## Pattern 6: The Invisible Skill
**Symptom**: Great content but skill rarely gets activated
**Root cause**: Description is vague, missing keywords, or lacks trigger scenarios
**Fix**: Description must answer WHAT, WHEN, and include KEYWORDS.

```
BAD:  "Helps with document tasks"
GOOD: "Create, edit, and analyze .docx files. Use when working with
       Word documents, tracked changes, or professional document formatting."
```

---

## Pattern 7: The Wrong Location
**Symptom**: "When to use this Skill" section in body, not in description
**Root cause**: Misunderstanding three-layer loading — body loads AFTER triggering decision
**Fix**: Move all triggering information to description field. Body is only loaded after skill is already selected.

---

## Pattern 8: The Over-Engineered
**Symptom**: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, CONTRIBUTING.md alongside SKILL.md
**Root cause**: Treating Skill like a software project
**Fix**: Delete all auxiliary files. Only include what Agent needs for the task. No documentation about the Skill itself.

---

## Pattern 9: The Freedom Mismatch
**Symptom**: Rigid scripts for creative tasks; vague guidance for fragile operations
**Root cause**: Not considering task fragility when designing constraints
**Fix**:
- High freedom for creative tasks (principles, not steps)
- Low freedom for fragile ops (exact scripts, no parameters)
