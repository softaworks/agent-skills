# Humanizer PL

A Claude Code skill that removes signs of AI-generated writing from **Polish** text —
the Polish-language companion to the [humanizer](../humanizer/) skill.

Polish AI text has its own tells that an English-oriented humanizer misses: English
punctuation calques (em dashes instead of the Polish en dash, `"English"` instead of
`„Polish"` quotation marks, commas after sentence-initial adverbials), syntactic
calques (*zaadresować problem*, *dedykowany dla*, *wydaje się być*), and a distinct
set of overused phrases (*w dzisiejszym dynamicznie zmieniającym się świecie*, *warto
zauważyć, że*, *kluczowy*, *kompleksowy*, *podsumowując*).

## What's inside

- **`SKILL.md`** — the working editor instructions: pattern catalog with before/after
  examples, a fix process, and Polish typography normalization rules.
- **`signs-of-ai-writing-pl.md`** — a comprehensive, sourced field guide to AI-writing
  markers in Polish (the Polish counterpart of Wikipedia's *Signs of AI writing*),
  compiled from:
  - Polish academic research on LLM-generated Polish (error typology of ChatGPT
    matura essays, the PolEval 2025 "Śmigiel" detection shared task, CEAID benchmark,
    stylometry studies);
  - Polish Wikipedia community practice (fabricated references, `utm_source=chatgpt.com`
    trails, Markdown artifacts in wikitext);
  - Polish SEO/copywriting guides and phrase scanners (~120 documented phrases);
  - AI-detector documentation covering Polish (JSA, plagiat.pl, and others) and their
    false-positive caveats;
  - teachers', examiners' and social-media users' observations.

## When to use

- Editing or reviewing Polish text that was drafted with AI assistance
- Making Polish copy sound natural before publication
- Fixing Polish typography that LLMs get wrong (quotes, dashes, commas, Title Case)
- Reviewing Polish text for AI-writing red flags (with appropriate caution — see the
  "Nieskuteczne wskaźniki" section of the field guide before accusing anyone)

## Usage

In Claude Code:

```
/humanizer-pl

[paste your Polish text here]
```

Or simply ask: *"odchudź ten tekst z artefaktów AI"* / *"humanize this Polish text"*.

## Installation

**Claude Code:**

```bash
cp -r skills/humanizer-pl ~/.claude/skills/
```

**claude.ai:** add the skill to project knowledge or paste `SKILL.md` contents into
the conversation.

## Key principles

1. **Accumulation, not single markers** — one *kluczowy* means nothing; five AI-phrases
   in one paragraph is a red flag.
2. **Typography is mechanical** — Polish quotes, dashes and comma rules are always
   fixed, regardless of authorship.
3. **Never polish a hallucination** — unverifiable statistics and suspicious citations
   get flagged `[DO WERYFIKACJI]`, not paraphrased into smoother hallucinations.
4. **Don't fabricate soul** — fake personal anecdotes are a worse artifact than none.

## Credits

- Structure and universal markers adapted from
  [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
  (WikiProject AI Cleanup, CC BY-SA 4.0)
- Approach modeled on the [humanizer](../humanizer/) skill (original by
  [@blader](https://github.com/blader/humanizer))
- Polish-language research: see the source list at the end of
  `signs-of-ai-writing-pl.md`
