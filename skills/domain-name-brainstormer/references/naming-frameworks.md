# Domain Naming Frameworks Reference

## Phonaesthetic Scoring (apply to every candidate)

Rate each name 1–3 on each axis; discard anything scoring ≤5 total:

| Axis | 1 (weak) | 2 (ok) | 3 (strong) |
|------|----------|--------|------------|
| **Plosive density** | no plosives | 1 plosive | 2+ plosives (b, d, k, p, t) — "snap" factor |
| **Vowel-consonant rhythm** | CCCC or VVVV clusters | minor cluster | alternating VC/CV pattern |
| **Stress on first syllable** | stress buried mid-word | borderline | naturally front-stressed |
| **Back-of-mouth resonance** | flat, nasal-heavy | mixed | rounded vowels (o, oo, u) give trust feel |
| **Brevity** | 4+ syllables | 3 syllables | 1–2 syllables |

Examples: "Stripe" (3+3+3+2+3=14), "Notion" (2+3+3+2+3=13), "Figma" (3+3+2+2+3=13).

## Trademark Risk Tiers

Before presenting a name, mentally classify it:

- **Tier 1 (low risk)**: Invented/portmanteau with no dictionary root — "Zuora", "Twilio". These clear trademark search most often.
- **Tier 2 (medium)**: Dictionary word applied out-of-field — "Stripe" (payments ≠ stripe patterns). Registerable but must verify class overlap.
- **Tier 3 (high risk)**: Common word in same field — "FastSend" for a shipping tool. Highly likely someone already holds Class 38/42 mark.
- **Tier 4 (instant reject)**: Sounds like or contains letters from a famous mark — "Goooglebox", "Facebooks". USPTO rejection guaranteed.

Surface risk tier in your output: if Tier 3 or 4, say so explicitly and suggest a portmanteau alternative.

## TLD Selection Decision Tree

```
Is audience global non-tech?
  YES → .com only (no exceptions; audience doesn't understand TLD nuance)
  NO → continue

Is product developer-facing?
  YES → .dev first, .io second
  NO → continue

Is AI/ML the core product, not just a feature?
  YES → .ai (but budget $60-100/yr; Anguilla registrar)
  NO → continue

Is it a mobile app with no web identity?
  YES → .app (Google Registry, requires HTTPS enforced by registry)
  NO → .com or category TLD (.design, .health, .legal etc.)
```

## Word Construction Patterns (ranked by distinctiveness)

1. **Portmanteau** — merge two words, drop overlapping phonemes: "Pinterest" (pin + interest), "Instagram" (instant + telegram). Highest trademark clearance rate.
2. **Clipped compound** — take the first 3-4 chars of each word: "FedEx" (Federal + Express). Works best when both roots are widely known.
3. **Back-formation** — treat the domain as a verb: "Slack", "Zoom", "Figma". Requires invented or repurposed word.
4. **Latinate root** — add -ly, -fy, -io, -era suffix to a concrete concept: "Clarity", "Notify", "Zapier". Medium distinctiveness.
5. **Pure dictionary word (out-of-field)** — high risk of .com squatting; requires premium budget.

## The "Radio Test"

Imagine someone says your domain name on a podcast with no visual aid. Ask:
1. Can the listener spell it correctly on first attempt?
2. Is there zero ambiguity on where the word boundaries are?
3. Does the TLD sound natural when spoken aloud? ("dot-dev" — yes; "dot-xyz" — weird pause)

If any answer is NO, flag it in output with "fails radio test — consider [alternative]".

## Squatter Pattern Recognition

Names that are almost certainly parked or premium-priced:
- Single common English word + .com (>99% taken)
- Two-word compound describing a common business activity + .com (>95% taken)
- Any 3-letter .com (all registered since ~2000)
- Any 4-letter pronounceable .com (>98% taken)
- Country-code hacks (.ly, .me, .io used as word suffix) — legal risk if country policy changes

Always offer a .io or .dev fallback when suggesting these patterns.

## Negative Space Naming

Some of the strongest brand names describe what the product *removes*, not what it does:
- "Notion" (implies disorder removed)
- "Calm" (implies anxiety removed)
- "Clear" (implies confusion removed)

This pattern tends to produce available, trademark-clear names because it's indirect. Use when the product solves a pain point (vs. adds a feature).
