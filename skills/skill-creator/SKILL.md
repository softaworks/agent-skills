---
name: skill-creator
description: Create high-quality SKILL.md files that pass skill-judge evaluation. Use when authoring a new skill from scratch, deciding what expert knowledge to encode, structuring SKILL.md sections (Mindset/Navigation/Philosophy/NEVER/When-Things-Go-Wrong), writing descriptions that trigger activation, calibrating knowledge delta, or diagnosing why a draft skill scores poorly. Triggers on phrases like "create a new skill", "write a SKILL.md", "help me author a skill", "what should go in my skill", "how do I write a good skill".
---

# Skill Creator

Build skills that pass production — not just skills that look good on paper.

---

## Mindset

1. **Description first, body second — always.** The description is the only thing Claude reads before deciding to activate a skill. A perfect body with a vague description is an invisible skill. Start every skill session by nailing the description; everything else is secondary.
2. **You are writing for Claude, not for a human.** Humans need context, background, definitions. Claude does not. Every line should be a decision framework, a non-obvious heuristic, or a practitioner-only edge case — not an explanation of what the domain is.
3. **Knowledge delta is the only currency.** Ask for every paragraph: "Does Claude already know this?" If yes, delete it. Claude's training covers documentation, tutorials, and best practices. What it lacks is the earned judgment that comes from repeated failure in a specific domain.
4. **The NEVER list is half the skill.** Expert knowledge is as much about what to avoid as what to do. A skill without a NEVER section is missing 50% of its value. Each NEVER item must name the specific action AND its non-obvious consequence — not a warning, a fact.
5. **Progressive disclosure is not optional.** SKILL.md under 500 lines, references/ for depth. But a reference file with no loading trigger in SKILL.md is dead content. Wire it explicitly or don't create it.

---

## Navigation

**Use this skill when**:
- Authoring a SKILL.md file from scratch
- Identifying what expert knowledge is worth encoding vs. what Claude already knows
- Deciding what goes in SKILL.md body vs. references/
- Writing a description that reliably triggers activation
- Diagnosing a draft skill that scores poorly on skill-judge

**Do NOT use this skill when**:
- Evaluating an existing skill for quality (use skill-judge)
- Refactoring bloated plugin instruction files (use agent-md-refactor)
- Wiring a skill into a plugin manifest (use plugin-forge)

**Decision tree — what to do first**:

| User starts with... | First action |
|---------------------|-------------|
| "I want to create a skill about X" | Ask: what does a practitioner know about X that took years to learn? Start there. |
| Existing notes / docs / spec to convert | Run knowledge delta scan — mark [E] expert, [A] activation-ok, [R] redundant — before writing a single line of SKILL.md |
| A draft SKILL.md that scored below B on skill-judge | Load [`references/antipatterns.md`](references/antipatterns.md) — identify which of the three failure patterns the draft matches |
| A skill that never activates despite good content | Description problem — rewrite description before touching the body |

---

## Philosophy

A skill is a compressed expert brain, not a tutorial. The moment you find yourself explaining what something is, stop — that belongs in documentation, and Claude already read the documentation. The question is never "is this correct?" It is always "would a domain expert say this captures knowledge that took years to earn?"

The test: would someone who has done this work for five years, reading your SKILL.md, say "yes — that captures the hard-won judgment I couldn't find anywhere else"? If the answer is "it's good but I could have read this from the docs", the skill fails.

---

## NEVER

- **NEVER start writing SKILL.md content before the description field is finalized** — the description drives skill activation; if it doesn't reliably trigger on the right phrases, no amount of body quality saves it. A skill that never activates has zero value regardless of its score.
- **NEVER include a README.md with content that duplicates SKILL.md** — the agent reads SKILL.md exclusively; README.md is for humans browsing a repo. Duplicate content means you'll maintain two versions that diverge, and the agent always gets the one you last edited.
- **NEVER add a references/ file without a MANDATORY loading trigger in SKILL.md** — files in references/ are only loaded when SKILL.md explicitly tells Claude to load them via a decision tree or workflow step. A list of references at the bottom without "load X when Y" instructions is Pattern 3 (Orphan References) — the files are never read.
- **NEVER write a NEVER item without a specific non-obvious consequence** — "NEVER do X" with no reason is useless because Claude doesn't know why to avoid it and can't weigh it against competing considerations. The consequence must be non-obvious: something that a reasonable person would not infer without domain experience.
- **NEVER create a skill by wrapping official documentation** — Claude's training already covers official docs, README files, and tutorials. Wrapping them adds tokens without adding knowledge delta. Provide practitioner judgment: what goes wrong, what edge cases kill you, what the docs don't say.
- **NEVER write a description without WHAT, WHEN, and trigger KEYWORDS** — descriptions that describe but don't trigger fail in production. The WHEN clause ("Use when...") is mandatory. Domain-specific trigger phrases ("incidents", "playbooks", "deploy", etc.) must appear verbatim so the routing matches natural user phrasing.
- **NEVER mistake length for quality** — a 50-line skill with pure expert knowledge outperforms a 400-line skill with 70% redundancy. Long skills pay a context cost on every activation. Every line must earn its tokens.

---

## Workflow: Building a Skill from Scratch

### Step 1 — Identify the knowledge worth encoding

Before writing anything, answer these questions:
- What does an expert in this domain know that took years (not hours) to learn?
- What are the common mistakes practitioners make that aren't obvious from documentation?
- What decision frameworks do experts use that they couldn't easily articulate if asked?
- What are the top 5 things an expert would never do, and WHY (specifically)?

If you can't answer these, the skill isn't ready to write yet.

### Step 2 — Write the description (before anything else)

A valid description answers all three:
- **WHAT**: what does this skill help with?
- **WHEN**: what situations trigger its use? Include a "Use when..." clause.
- **KEYWORDS**: what domain-specific terms would a user naturally say?

Template:
```
[Action verbs covering the core function]. Use when [specific trigger scenario 1], [trigger scenario 2], or [trigger scenario 3]. Triggers on phrases like "[natural phrase 1]", "[natural phrase 2]", "[domain term]".
```

Test: read your description and ask "would someone asking '[trigger phrase]' get routed here?" If not, rewrite.

### Step 3 — Knowledge delta scan on your raw material

If converting notes, docs, or a draft:
- Mark each paragraph **[E] Expert** — Claude genuinely doesn't know this
- Mark each paragraph **[A] Activation** — Claude knows but brief reminder is useful
- Mark each paragraph **[R] Redundant** — Claude definitely knows this

Target ratio: >70% E, <20% A, <10% R. Delete all R content before writing SKILL.md.

### Step 4 — Structure the body

Use the canonical pattern: **Mindset → Navigation → Philosophy → NEVER → Workflow/Process → When Things Go Wrong**

| Section | What it contains | Common mistake |
|---------|-----------------|----------------|
| Mindset | 4-6 numbered principles that transfer expert thinking patterns — not facts, not procedures | Making it a list of tips instead of a compressed worldview |
| Navigation | Use/Don't Use cases + decision tree for ambiguous inputs | Forgetting the "Do NOT use when" clause — causes cross-skill routing errors |
| Philosophy | 2-4 sentences: the organizing insight that makes the other sections coherent | Writing a mission statement instead of a practitioner truth |
| NEVER | 5-7 items: specific action + specific non-obvious consequence | Writing 3 obvious warnings instead of 5 practitioner-only failure modes |
| Workflow/Process | Step-by-step with decision points — use tables and checklists | Prose descriptions instead of structured steps |
| When Things Go Wrong | Table: Symptom → Likely Cause → Fix | Missing — this is the section most likely to be omitted |

### Step 5 — Wire references/ correctly

If deep reference material exists or is needed:
1. Create `references/<filename>.md`
2. In SKILL.md, add an explicit conditional: "Load `references/<filename>.md` when [specific scenario]"
3. The trigger must appear in a decision tree or workflow step — not in a "see also" footer

### Step 6 — Run the self-test

Before submitting for skill-judge review, ask:
- Does the description include WHAT + WHEN + keywords?
- Is SKILL.md under 500 lines?
- Does every NEVER item state the specific non-obvious consequence?
- Are all references/ files wired to loading triggers (not just listed)?
- Does the Mindset section transfer thinking patterns, not just facts?
- Would a domain expert say "yes, this captures what took me years to learn"?

Scoring this yourself against skill-judge's 8 dimensions before review catches 80% of issues.

---

## The Three Failure Patterns to Avoid

Load [`references/antipatterns.md`](references/antipatterns.md) for full detail on these patterns. Summary:

| Pattern | What it looks like | Why it fails |
|---------|-------------------|-------------|
| Tutorial Pattern | SKILL.md explains what the domain is, walks through basics, defines terms | Everything in it is in Claude's training; zero knowledge delta; skills scores F on D1 |
| Dump Pattern | SKILL.md is every note, link, checklist, and thought you ever had about the topic | 500+ lines, <30% expert content; context cost is massive; no compression of wisdom |
| Orphan References Pattern | references/ directory exists with detailed files, nothing in SKILL.md points to them conditionally | Reference files are never loaded; effectively invisible; wastes disk and misleads authors |

---

## When Things Go Wrong

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Skill never activates even though content is relevant | Description missing WHEN clause or domain trigger keywords | Rewrite description: add "Use when...", add 2-3 verbatim trigger phrases users would say |
| Skill activates for the wrong tasks | Description is too broad — WHAT clause describes too many scenarios | Add "Do NOT use when..." clause to description; tighten the WHEN clause |
| Skill scored below C on skill-judge D1 (Knowledge Delta) | Body contains basics Claude knows — tutorials, definitions, documentation rewrites | Run knowledge delta scan (Step 3); delete all [R] content; replace with practitioner edge cases |
| NEVER items scored 1-3/15 by skill-judge D3 | NEVER items are vague warnings without specific consequences | Rewrite each: "NEVER [specific action] — [specific non-obvious consequence that only practitioners know]" |
| References/ files exist but are never loaded | No conditional loading triggers in SKILL.md body | Add decision tree rows or workflow steps that say exactly when to load each file |
| Skill looks complete but domain expert says "this is too basic" | Knowledge delta not sourced from actual practitioner experience | Interview a practitioner or draw on first-hand failure modes; replace textbook knowledge with scar tissue |
| Draft is over 500 lines | Mixed SKILL.md + reference content into one file | Move deep reference material to references/ files with loading triggers; keep SKILL.md to decision frameworks only |
