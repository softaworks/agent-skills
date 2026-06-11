# Mindset / Navigation / Philosophy — Skill Header Template

**Canonical standard for the opening sections of all agent-toolkit skills.**

These three sections come FIRST in every `SKILL.md`, before any workflow content, quick-reference tables, or technical reference material. They are not optional boilerplate — they are the load-bearing contract between the skill and the agent that activates it.

---

## Why Three Sections

Skills are activated by agents making autonomous routing decisions. Without explicit guidance, agents over-trigger on superficial keyword matches, under-trigger on ambiguous phrasing, and default to novice-level judgment when domain expertise is what the user actually needs. These three sections address each failure mode directly:

| Section | Failure it prevents | What it provides |
|---|---|---|
| **Mindset** | Generic, novice-quality output | Expert stances and hard-won heuristics |
| **Navigation** | Wrong-context activation | Explicit when-to-use and when-NOT-to-use gates |
| **Philosophy** | Inconsistent decisions across the workflow | One overarching principle that resolves all trade-offs |

---

## Section 1: Mindset

**Purpose:** Communicate what distinguishes expert thinking from novice thinking in this domain. These are not definitions — they are the stances an expert holds reflexively, things that took years of practice to internalize.

**Format rules:**
- 3–5 bullet heuristics, each starting with a bold "expert stance" phrase
- Each bullet should read like a hard-won lesson, not a textbook summary
- Do not pad to reach 5 bullets — 3 sharp heuristics beat 5 generic ones
- Do not use sub-bullets; each heuristic stands alone

**Fill-in template:**

```markdown
## Mindset

- **[Expert stance phrase]** — [One to two sentences explaining why novices get this wrong and what the expert sees instead.]
- **[Expert stance phrase]** — [One to two sentences explaining the counterintuitive insight or priority inversion an expert applies.]
- **[Expert stance phrase]** — [One to two sentences on what the expert refuses to do or what trap they have learned to recognize immediately.]
- **[Expert stance phrase]** — [Optional: a constraint or quality bar that experts enforce that novices skip.]
- **[Expert stance phrase]** — [Optional: a systemic or long-term perspective that novices miss because they are focused on the immediate task.]
```

---

## Section 2: Navigation

**Purpose:** Tell the agent exactly when to activate this skill and — equally important — when NOT to activate it. Skills that never specify exclusion criteria get triggered in wrong contexts, producing off-target output and consuming context budget on irrelevant material.

**Format rules:**
- Include a "Use when" list with concrete trigger phrases or conditions
- Include a "Do not use when" list — this is mandatory, not optional
- Include a short decision tree or disambiguation block for the ambiguous middle cases
- The "do not use when" cases must be specific enough to be actionable (not "when the topic is unrelated")

**Fill-in template:**

```markdown
## Navigation

**Use this skill when:**
- [Specific trigger phrase or condition — e.g., "user asks to design a component library"]
- [Another trigger — e.g., "user mentions tokens, theming, or visual consistency"]
- [Another trigger — name the verbs, nouns, or intent signals that indicate this skill]

**Do not use this skill when:**
- [Exclusion case — e.g., "user wants a single one-off component, not a system"]
- [Exclusion case — e.g., "scope is a bug fix or refactor, not new design work"]
- [Exclusion case — the adjacent skill that covers this instead, and when to hand off to it]

**Ambiguous inputs — quick decision tree:**
- If the request mentions [signal A] → [route or action]
- If the request mentions [signal B] → [route or action]
- If unclear → [default behavior or clarifying question to ask]
```

---

## Section 3: Philosophy

**Purpose:** State the one core principle that drives every decision in this skill's domain. When two approaches are in tension, this principle is what breaks the tie. It is not a list of values — it is a single governing idea expressed in 1–3 sentences.

**Format rules:**
- Prose only — no bullet lists, no headers, no tables
- 1–3 sentences maximum
- Must be opinionated enough to actually resolve trade-offs
- Avoid generic platitudes ("quality matters", "keep it simple") — the statement must be specific enough that it would lead to a different decision than the opposite stance would

**Fill-in template:**

```markdown
## Philosophy

[One to three sentences stating the governing principle of this skill's domain. This should be specific enough that a reader could use it to resolve a trade-off — e.g., it should tell you whether to favor flexibility or convention, speed or correctness, user control or sensible defaults. It is not a mission statement; it is a decision rule.]
```

---

## Placement in SKILL.md

The three sections appear immediately after the frontmatter and the skill's one-line description, before any workflow, process, or reference content:

```markdown
---
name: skill-name
description: One sentence. Trigger phrases. When to use.
---

# Skill Title

Brief description of what the skill does.

## Mindset

...

## Navigation

...

## Philosophy

...

---

## [First workflow or reference section]
```

Do not insert quick-reference tables, "How It Works" sections, or script documentation before the three header sections. Agents read top-to-bottom — if stance and routing gates are buried below workflow prose, they are already past the activation decision by the time they encounter them.

---

## Worked Example 1: Design Skill (creative domain)

**Skill:** `design-system-starter`

```markdown
## Mindset

- **Tokens before components** — Novices reach for a Button component; experts reach for the color and spacing contract first. A component built on ad-hoc values is a component that breaks the moment the brand evolves.
- **Consistency is a feature, not a constraint** — The value of a design system compounds only when deviation requires a deliberate exception. Every one-off shortcut is debt owed to the next designer who inherits the codebase.
- **Accessibility is load-bearing, not decorative** — Contrast ratios and focus states are not a checklist appended at the end; they are structural decisions that determine whether the component architecture is valid. Design for the constraint first.
- **The system serves the product, not the other way around** — A design system that blocks shipping is worse than no design system. Scope aggressively: establish the 20% of tokens and components that cover 80% of surfaces, then expand.

## Navigation

**Use this skill when:**
- User asks to create, establish, or audit a design system or component library
- User mentions design tokens, theming, color contracts, or spacing scales
- User wants to enforce visual consistency across a multi-surface product
- User asks for dark mode architecture or brand-level theming

**Do not use this skill when:**
- User wants a single component or a one-off UI element — use `react-dev` or `mui` instead
- User is refactoring or debugging an existing component, not architecting a system
- User wants a static mockup or prototype — this skill produces production-grade architecture, not wireframes
- The product has one screen and no foreseeable reuse — over-engineering costs more than it saves

**Ambiguous inputs — quick decision tree:**
- If user says "component library" with no mention of tokens or theming → clarify whether they want a full system or a set of isolated components
- If user says "design system" for a solo/prototype project → proceed but scope to minimal tokens + 3–5 components, flag when to stop
- If unclear → ask: "Are you building something reusable across multiple surfaces, or is this for a single product?"

## Philosophy

A design system is a bet that the cost of the constraints it imposes now is lower than the cost of the inconsistency it prevents later. Every architectural decision in this skill optimizes for the long-term maintainability of that bet — not for the fastest path to a visible result.
```

---

## Worked Example 2: Technical Skill (API integration domain)

**Skill:** `openapi-to-typescript`

```markdown
## Mindset

- **The spec is the source of truth, not the implementation** — If the OpenAPI spec says a field is optional but the server always returns it, the spec is what you type against. The server can change; the contract should not.
- **Generate, do not hand-write** — Hand-written types drift. The moment a developer manually edits a generated type, that type becomes a maintenance liability. Generate, validate, regenerate.
- **Discriminated unions over optional fields** — A response type with five optional fields and no discriminant is not a type; it is a guess. Push back on schemas that conflate multiple response shapes into a single flat object.
- **Treat 4xx and 5xx as first-class types** — Error responses are not exceptions to be caught; they are values to be typed. A client that does not model error shapes will produce runtime surprises that a type system could have caught at build time.
- **Version the contract, not the workaround** — When the API changes, update the spec and regenerate. Do not add conditional logic to paper over a breaking change in the generated types.

## Navigation

**Use this skill when:**
- User has an OpenAPI (2.x or 3.x) or Swagger spec and wants TypeScript types
- User asks to generate a typed API client from a spec file
- User wants to validate that their TypeScript client matches a remote API contract
- User mentions `openapi-typescript`, `swagger-codegen`, or `orval` in context

**Do not use this skill when:**
- User is writing a REST client by hand with no spec — use `react-dev` patterns instead
- The spec is internal and already has a generated SDK maintained by another team — consume that SDK, do not regenerate
- User wants GraphQL types — different toolchain, different skill
- User wants to *write* an OpenAPI spec from scratch — this skill consumes specs, it does not author them

**Ambiguous inputs — quick decision tree:**
- If user pastes a JSON/YAML blob → check for `openapi:` or `swagger:` key; if present, proceed; if absent, ask what format it is
- If user says "generate types for my API" with no spec → ask for the spec URL or file before proceeding
- If the spec has no `components/schemas` → warn that output will be limited to endpoint-level types only

## Philosophy

Type safety at the API boundary is only as strong as the discipline to keep the generated types current. This skill treats regeneration as a routine operation and manual type editing as a red flag — the goal is a workflow where the TypeScript compiler enforces the API contract automatically, without ongoing human maintenance.
```

---

## Common Mistakes to Avoid

**In Mindset:**
- Listing definitions ("Tokens are reusable values") instead of stances ("Tokens before components")
- Padding with obvious advice that applies to any domain ("test your work", "read the docs")
- Exceeding 5 bullets — more heuristics signal less curation

**In Navigation:**
- Omitting the "do not use when" block — this is the most common and most costly omission
- Writing exclusions too vaguely ("when not relevant") — name the adjacent skill or the specific condition
- Skipping the ambiguous-inputs block — ambiguity is where wrong-context activation happens most

**In Philosophy:**
- Writing a list formatted as prose ("First do X, then Y, then Z")
- Using generic language that would be true for any skill ("quality matters", "think about the user")
- Stating a process instead of a principle — philosophy answers "why", not "how"
