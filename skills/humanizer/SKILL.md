---
name: humanizer
version: 3.0.0
description: "Strip AI writing fingerprints from any text: removes 24 documented patterns (hedge-and-hedge, em-dash overuse, the tapestry cluster, false-profound closers, promotional language inflation). Use when text sounds robotic, obviously AI-generated, or when told this sounds like ChatGPT. Triggers: humanize this, remove AI patterns, make this sound natural, too corporate, too stiff. Distinct from writing-clearly-and-concisely which edits human prose; this skill targets AI-generated artifacts."
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# Humanizer: Remove AI Writing Patterns

## Mindset

**Pattern removal is not the goal — voice is.** Sterile text with zero AI-isms is still obviously not human. The job is making writing feel like a real person wrote it with intent.

**Specificity beats neutrality every time.** "The company plans to open two more locations next year" is more human than "The future looks bright." Real humans have specific information and share it.

**Rhythm reveals AI origin more than word choice.** Same-length sentences with identical structure feel algorithmic even when every word is "clean." Read output aloud — if it sounds metronomic, it failed.

**AI writing hedges structurally, not just lexically.** The pattern "It is worth noting that X, which Y, thereby Z" is three separate hedges baked into sentence structure. Fix the architecture, not just the vocabulary.

**The most dangerous output is "clean but soulless."** No opinions, no uncertainty, no first-person, neutral reporting of everything — this reads like a press release and is just as obviously generated.

---

## Navigation

**Use this skill when:**
- Text feels robotic, corporate, or AI-generated even if you can't name why
- You spot specific AI vocabulary: "delve", "tapestry", "pivotal", "showcase", "underscore", "vibrant", "testament", "landscape" (abstract), "interplay", "intricate"
- Writing uses em dashes every other sentence
- Every paragraph ends with a vague optimistic statement
- You see "Not only X but Y" or "It's not just A, it's B" patterns
- Bullet lists all start with "**Bold Header:** then explanation"
- Text contains "I hope this helps" or "Certainly!" (chatbot artifacts left in)
- Writing uses "serves as" or "stands as" instead of "is"

**Do NOT use this skill when:**
- The text is already spare and direct — over-editing introduces new problems
- The AI-ish tone is intentional (formal legal, regulatory, academic)
- You need to add content; this skill edits, it doesn't research

**Quick decision tree:**

```
Is there actual content/information in the text?
├── NO → Ask for source material first; humanizer can't fabricate facts
└── YES → Does it read naturally aloud?
    ├── YES → Light pass only; focus on rhythm variation
    └── NO → Full pass; start with structural issues before word-level fixes
        ├── Structure problems? → Fix sentence architecture first
        └── Word problems only? → Swap vocab, then check rhythm
```

---

## Philosophy

AI writes toward the statistical center — the most likely phrasing that applies to the widest cases. Humanizing means pushing away from center: toward the specific, the opinionated, the slightly imperfect. A human wrote this. Show it.

---

## NEVER

- **NEVER remove hedging without replacing it with an actual stance** — "may affect outcomes" is fine; deleting uncertainty and leaving nothing is dishonest.

- **NEVER flatten all sentence variation in the opposite direction** — making every sentence short and punchy is just a different kind of rhythm problem. Mix 8-word and 30-word sentences deliberately.

- **NEVER add first-person ("I") unless the context clearly supports it** — injecting "I" into a company blog post or product description reads as wrong as the original AI tone.

- **NEVER swap AI vocabulary for equally abstract vocabulary** — replacing "vibrant ecosystem" with "dynamic environment" accomplishes nothing. The fix is specificity: "23 active contributors pushing daily."

- **NEVER strip boldface from genuine technical terms** — the target is *mechanical* boldface decoration, not all emphasis. API method names, warnings, and genuinely key terms warrant bold.

- **NEVER rewrite so aggressively that factual claims change** — changing "the project was successful" to "the project exceeded targets" invents a claim. Stick to what the original actually asserted.

- **NEVER output a "Changes made" section unless explicitly requested** — it proves the text was edited by an AI. The output should stand alone.

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|--------------|----------|
| Output still sounds AI even after full pass | Sentence rhythm unaddressed — word swaps without structural changes | Read aloud; find the metronomic sections; manually vary sentence length |
| Rewrites lose important nuance or context | Over-editing; removing specificity along with fluff | Restore original claims; edit for tone only, not content |
| Text feels "cleaned up" but has no voice | Removed patterns without adding personality | Add one concrete detail, one opinion, or one moment of acknowledged complexity |
| User says "too casual now" | Overcorrected toward first-person/informal | Return to third-person; vary rhythm without adding personality markers |
| Promotional text keeps regenerating AI patterns | Wrote new content instead of editing; LLM defaults | Work sentence-by-sentence; don't let model rewrite from scratch |

---

## Workflow

**Step 1 — Structural scan (do first):**
- Sentence rhythm: are lengths uniform? Fix before word-level edits.
- Paragraph endings: do they vague-out into optimism? Replace with specifics.
- Lists: are they "**Header:** body" format? Collapse to prose.
- Heading case: Title Case In Every Word? → Sentence case only.

**Step 2 — Pattern pass (load reference if needed):**
Load `references/patterns.md` for the full 24-pattern catalog with before/after examples.

Priority order (most to least detectable):
1. Chatbot artifacts (leave "I hope this helps", "Certainly!")
2. AI vocabulary words (delve, tapestry, pivotal, showcase, vibrant, testament)
3. Copula avoidance (serves as → is, boasts → has)
4. Vague attributions (Experts say → name the expert + source)
5. Inflated significance (pivotal moment, marks a shift, evolving landscape)
6. Em dash overuse (more than 1 per 200 words is likely AI)
7. Negative parallelisms (Not only X but Y)
8. Rule of three (forced triads)
9. Generic conclusions (future looks bright → specific next action)

**Step 3 — Voice check:**
- Does any sentence express an opinion, uncertainty, or specific feeling?
- Does rhythm vary when read aloud?
- Is there at least one concrete specific (number, name, date, product feature)?

If all three are no — the output is clean but soulless. Add one element from Step 3 before finishing.

---

## Output Format

Provide the humanized text only. No preamble ("Here is the rewritten version:"), no summary of changes, no closing offer to revise further — these are themselves AI writing patterns.

Exception: if the user explicitly asks "what did you change?", provide a brief bulleted list.

---

## Reference

**`references/patterns.md`** — Full 24-pattern catalog with before/after examples for all documented AI writing signals. Load this when you need specific examples or are working on a particular pattern type.
