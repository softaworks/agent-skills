---
name: writing-clearly-and-concisely
description: Use when writing or editing prose for humans — documentation, commit messages, error messages, explanations, reports, API copy, UI text, READMEs. Trigger phrases: "write clearly", "edit for clarity", "too wordy", "make this concise", "sounds like AI", "clean up this text".
---

## Mindset

Expert writers know what novices don't:

1. **The first draft is always upstream of the real problem.** Weak prose is almost never a word-choice problem — it's a structure problem dressed up as a vocabulary problem. Reordering the sentence often beats replacing the words.
2. **Vagueness is a tax on the reader.** Every abstract noun (leverage, impact, ensure, facilitate) forces the reader to mentally insert the concrete thing you omitted. Name the thing.
3. **The edit loop has a direction.** Start with structure (is the argument sequenced?), then paragraphs (one idea each?), then sentences (active, positive, short?), then words. Editing words before fixing structure is wasted effort.
4. **LLMs regress to the statistical mean.** The most-likely-next-token is always a blurry paraphrase of thousands of prior documents. The result is simultaneously less specific and more exaggerated — generic praise that could describe any subject. The antidote is specificity, not elegance.
5. **Omission is a writing choice, not a failure.** "Omit needless words" means cut concepts, not just syllables. If a sentence says what the previous sentence implied, delete it.

## Navigation

**Use this skill when:**
- Writing any prose a human will read (docs, READMEs, commit messages, error messages, UI copy, PR descriptions, reports, emails)
- Editing to reduce wordiness, cut AI-sounding phrases, or improve clarity
- The draft sounds promotional, hedging, or generic

**Do NOT use this skill when:**
- Writing code comments that follow language-specific conventions (those have their own norms)
- Translating between languages (different skill domain)
- Creating purely structured output (JSON, YAML, tables with no prose)

**Quick triage:** Does the output contain sentences a human will read? Use this skill. Does it contain only code or data? Skip it.

## Philosophy

Write to transfer a specific idea from your head into the reader's head with minimum friction. Every word that doesn't serve that transfer is overhead. Every abstraction that could be a concrete noun is a missed opportunity.

## NEVER

- **NEVER end a sentence with a participial "-ing" analysis phrase** ("ensuring reliability", "highlighting its importance", "reflecting its legacy") — these phrases perform analysis without doing it. The "highlighting" is a claim, not a fact; it adds zero information.
- **NEVER open a conclusion with "In summary", "In conclusion", or "Overall"** — because it signals the reader that you are about to repeat yourself. If the structure was clear, the summary is redundant. If the structure was unclear, the summary doesn't fix it.
- **NEVER use "it's important to note/remember/consider"** — because this construction hedges instead of asserting. If the fact is important, state it. If it needs a qualifier, attach the qualifier directly to the claim.
- **NEVER write "Despite its [positive], [subject] faces challenges"** — this formula is the LLM equivalent of a five-paragraph essay conclusion. It signals a canned structure, not a real argument. If there are challenges, state them without the rhetorical frame.
- **NEVER use promotional-positive stacking** (groundbreaking, seamless, robust, cutting-edge, enduring legacy, nestled, boasts) — because these words describe how you want the reader to feel about the subject, not what the subject actually does. They erode credibility.
- **NEVER substitute abstract nouns for verbs** ("provide assistance" → "help", "make a decision" → "decide", "give consideration to" → "consider") — nominalizing verbs buries the action and adds syllables without meaning.
- **NEVER add a "challenges and future prospects" section as a formula** — this structure signals the writer ran out of facts and is padding. If you have a real forward-looking claim with evidence, state it in-line.

## 3-Pass Editing Procedure

Run passes in this order — structure before sentences before words:

**Pass 1 — Structure (paragraph level)**
- Does each paragraph have exactly one idea?
- Is the most important information first (inverted pyramid)?
- Delete any paragraph that only restates a previous one.

**Pass 2 — Sentences**
- Convert passive to active: find "is/are/was/were [verb]ed by" → flip subject and object.
- Positive form: "not many" → "few", "did not remember" → "forgot".
- Break any sentence over ~25 words into two.

**Pass 3 — Words**
- Replace every puffery word (pivotal, crucial, vital, testament, leverages, ensures) with the specific word or delete the sentence.
- Delete "very", "really", "quite", "rather".
- Replace "-ing" phrase tails with declarative clauses or delete them.

## Before / After Examples

**Superficial analysis tail (AI tell):**
Before: `The new API supports OAuth 2.0, reflecting the team's commitment to security best practices.`
After: `The new API supports OAuth 2.0.`
Why: "reflecting the team's commitment" is unattributed narration, not information.

**Passive + puffery:**
Before: `Significant performance improvements were delivered by the refactor, ensuring a more seamless user experience.`
After: `The refactor cut median response time from 420 ms to 85 ms.`
Why: Named the actual outcome; eliminated passive voice and the empty "-ing" tail.

**Needless preamble:**
Before: `It is important to note that this setting only applies when the feature flag is enabled.`
After: `This setting only applies when the feature flag is enabled.`
Why: "It is important to note that" contributes no content.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Edited text sounds clinical/cold | Correct grammar, wrong register — cut too many hedges without considering audience | Restore one hedge per paragraph where uncertainty is real; match sentence length to conversational tone |
| Text is shorter but still unclear | Fixed word count, not structure — sentences were trimmed, not reorganized | Run Pass 1 again: check whether each paragraph has exactly one main claim |
| Draft still sounds like AI after edits | Surface edits only — swapped puffery words but kept abstract nouns and "-ing" tails | Identify the concrete subject/object/verb; delete the frame around it |
| Reader says "too terse, needs context" | Over-application of concision to background explanation | Restore the sentence that answers "why does this matter", not the one that restates what was already said |

## Reference Files

Load only what you need — one file covers most tasks:

| Need | File | ~Tokens |
|------|------|---------|
| Active voice, positive form, concision, paragraph structure | `elements-of-style/03-elementary-principles-of-composition.md` | 4,500 |
| Grammar, possessives, comma rules | `elements-of-style/02-elementary-rules-of-usage.md` | 2,500 |
| Word choice, commonly misused terms | `elements-of-style/05-words-and-expressions-commonly-misused.md` | 4,000 |
| Full AI pattern catalog (Wikipedia field-tested) | `references/signs-of-ai-writing.md` | load only when auditing for AI tells |

**Context-tight fallback:** Write the draft using the 3-pass procedure above, then dispatch a subagent with the draft and only the one reference file needed for the specific issue.
