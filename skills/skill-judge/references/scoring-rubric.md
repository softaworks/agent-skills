# Scoring Rubric — Full Dimension Details

## D1: Knowledge Delta (20 points) — THE CORE DIMENSION

| Score | Criteria |
|-------|----------|
| 0-5 | Explains basics Claude knows (what is X, standard library tutorials) |
| 6-10 | Mixed: some expert knowledge diluted by obvious content |
| 11-15 | Mostly expert knowledge with minimal redundancy |
| 16-20 | Pure knowledge delta — every paragraph earns its tokens |

**Red flags** (instant score ≤5):
- "What is [basic concept]" sections
- Step-by-step tutorials for standard operations
- Generic best practices ("write clean code", "handle errors")
- Definitions of industry-standard terms

**Green flags**:
- Decision trees for non-obvious choices ("when X fails, try Y because Z")
- Trade-offs only an expert would know
- Edge cases from real-world experience
- "NEVER do X because [non-obvious reason]"

**Knowledge classification**:
- **[E] Expert**: Claude genuinely doesn't know — keep
- **[A] Activation**: Claude knows but brief reminder is useful — keep if brief
- **[R] Redundant**: Claude definitely knows — delete

Good ratio: >70% Expert, <20% Activation, <10% Redundant

---

## D2: Mindset + Appropriate Procedures (15 points)

| Score | Criteria |
|-------|----------|
| 0-3 | Only generic procedures Claude already knows |
| 4-7 | Has domain procedures but lacks thinking frameworks |
| 8-11 | Good balance: thinking patterns + domain-specific workflows |
| 12-15 | Expert-level: shapes thinking AND provides procedures Claude wouldn't know |

**Valuable thinking patterns look like**:
```markdown
Before [action], ask yourself:
- **Purpose**: What problem does this solve? Who uses it?
- **Constraints**: What are the hidden requirements?
```

**Valuable domain procedures look like** (non-obvious ordering, easy-to-miss steps):
```markdown
OOXML workflow: unpack → edit XML → validate → pack
MUST recalculate formulas after editing (not before)
```

**Redundant generic procedures** (skip these): "Step 1: Open file, Step 2: Edit, Step 3: Save"

---

## D3: Anti-Pattern Quality (15 points)

| Score | Criteria |
|-------|----------|
| 0-3 | No anti-patterns mentioned |
| 4-7 | Generic warnings ("avoid errors", "be careful") |
| 8-11 | Specific NEVER list with some reasoning |
| 12-15 | Expert-grade anti-patterns with WHY — things only experience teaches |

Expert anti-pattern structure: `NEVER [specific action] because [non-obvious consequence]`

Test: Would an expert say "yes, I learned this the hard way"? Or "this is obvious to everyone"?

---

## D4: Specification Compliance (15 points)

| Score | Criteria |
|-------|----------|
| 0-5 | Missing frontmatter or invalid format |
| 6-10 | Has frontmatter but description is vague or incomplete |
| 11-13 | Valid frontmatter, description has WHAT but weak on WHEN |
| 14-15 | Perfect: WHAT + WHEN + trigger KEYWORDS |

**Description must answer THREE questions**:
1. **WHAT**: What does this Skill do?
2. **WHEN**: In what situations? ("Use when...", "When user asks for...")
3. **KEYWORDS**: File extensions, domain terms, action verbs

The brutal truth: A Skill with perfect content but poor description is useless — it never gets activated.

**Description quality checklist**:
- [ ] Lists specific capabilities (not just "helps with X")
- [ ] Includes explicit trigger scenarios
- [ ] Contains searchable keywords
- [ ] Specific enough Agent knows EXACTLY when to use it

---

## D5: Progressive Disclosure (15 points)

| Score | Criteria |
|-------|----------|
| 0-5 | Everything dumped in SKILL.md (>500 lines, no structure) |
| 6-10 | Has references but unclear when to load them |
| 11-13 | Good layering with MANDATORY triggers present |
| 14-15 | Perfect: decision trees + explicit triggers + "Do NOT Load" guidance |

Three layers:
- Layer 1 — Metadata (always in memory): name + description, ~100 tokens
- Layer 2 — SKILL.md Body (loaded after triggering): ideal <500 lines
- Layer 3 — Resources (loaded on demand): no limit

**Good loading trigger** (embedded in workflow):
```markdown
**MANDATORY - READ ENTIRE FILE**: Before proceeding, read
[`scoring-rubric.md`](references/scoring-rubric.md) completely.
**Do NOT load** `failure-patterns.md` for this task.
```

**Bad loading trigger** (just listed at bottom): `- scoring-rubric.md - for scoring`

---

## D6: Freedom Calibration (15 points)

| Score | Criteria |
|-------|----------|
| 0-5 | Severely mismatched (rigid scripts for creative tasks, vague for fragile ops) |
| 6-10 | Partially appropriate, some mismatches |
| 11-13 | Good calibration for most scenarios |
| 14-15 | Perfect freedom calibration throughout |

| Task Type | Should Have | Example Skill |
|-----------|-------------|---------------|
| Creative/Design | High freedom (principles) | frontend-design |
| Code review | Medium freedom (prioritized list) | code-review |
| File format ops | Low freedom (exact scripts) | docx, xlsx, pdf |

Test: "If Agent makes a mistake, what's the consequence?" High consequence → Low freedom.

---

## D7: Pattern Recognition (10 points)

| Pattern | ~Lines | Key Characteristics | When to Use |
|---------|--------|---------------------|-------------|
| **Mindset** | ~50 | Thinking > technique, strong NEVER list | Creative tasks requiring taste |
| **Navigation** | ~30 | Minimal SKILL.md, routes to sub-files | Multiple distinct scenarios |
| **Philosophy** | ~150 | Two-step: Philosophy → Express | Art/creation requiring originality |
| **Process** | ~200 | Phased workflow, checkpoints | Complex multi-step projects |
| **Tool** | ~300 | Decision trees, code examples | Precise operations on specific formats |

| Score | Criteria |
|-------|----------|
| 0-3 | No recognizable pattern, chaotic structure |
| 4-6 | Partially follows a pattern |
| 7-8 | Clear pattern with minor deviations |
| 9-10 | Masterful application of appropriate pattern |

---

## D8: Practical Usability (15 points)

| Score | Criteria |
|-------|----------|
| 0-5 | Confusing, incomplete, contradictory, or untested guidance |
| 6-10 | Usable but with noticeable gaps |
| 11-13 | Clear guidance for common cases |
| 14-15 | Comprehensive coverage including edge cases and error handling |

**Check for**:
- Decision trees: For multi-path scenarios, is there clear guidance on which path to take?
- Code examples: Do they actually work? Or pseudocode that breaks?
- Error handling: What if the main approach fails? Fallbacks provided?
- Edge cases: Unusual but realistic scenarios covered?
- Actionability: Can Agent immediately act, or needs to figure things out?

**Good usability** (decision tree + fallback):
```markdown
| Task | Primary Tool | Fallback | When to Use Fallback |
|------|-------------|----------|----------------------|
| Read text | pdftotext | PyMuPDF | Need layout info |
```
