---
name: domain-name-brainstormer
description: Brainstorm and evaluate domain name candidates using phonaesthetics, trademark risk tiers, and TLD selection frameworks. Use when naming a startup, product, or brand — outputs a scored shortlist with radio-test results. Trigger phrases: "suggest domain names", "help me name my", "find a domain for", "domain brainstorm", "domain candidates".
---

# Domain Name Brainstormer

## Mindset

- **Distinctiveness is the primary constraint, not descriptiveness.** Generic descriptive names (.com almost certainly taken, trademark unregisterable). The best names are invented or out-of-field.
- **Phonaesthetics predict memorability better than meaning.** A name that "snaps" when spoken (plosive consonants, front-stressed, 1–2 syllables) survives word-of-mouth better than a perfectly descriptive one.
- **TLD choice signals audience, not just availability.** .com signals mainstream/trust; .dev signals developer tool; .ai signals the AI is the product (not a feature). Picking the wrong TLD causes brand positioning damage, not just aesthetics.
- **Most "good" .coms are taken or premium-priced.** The real deliverable is a shortlist that maximizes likelihood of availability — invented words, portmanteaus, out-of-field vocabulary.
- **Trademark risk is non-negotiable to surface.** A creative name that infringes Class 42 (software/SaaS) is worse than no name — it causes forced rebrand after launch.

## Navigation

**Use this skill when**: user needs domain name candidates for a startup, product, personal brand, or side project; user wants to evaluate name options they already have; user needs TLD guidance.

**Do NOT use this skill when**: user needs live availability checking (Claude has no WHOIS/DNS access — that is always the user's next step at a registrar); user needs legal trademark clearance (surface risk tier, but defer to trademark attorney for Tier 2+).

**Ambiguous input decision tree**:
```
Is the product category clear?
  NO → ask: "What does it do and who is the primary user?"
  YES → Is the target audience global non-tech?
          YES → constrain output to .com only
          NO → use TLD decision tree (see references/naming-frameworks.md)
```

## Philosophy

Strong domain names are invented assets, not discovered ones. The workflow is: generate phonaesthetically strong candidates → score them → eliminate trademark risk → output a ranked shortlist with radio-test results. Availability is the user's verification step, never Claude's claim.

## NEVER

- NEVER present any domain as available, registered, or taken — Claude has no WHOIS, DNS, or registrar access. Say "candidate" not "available".
- NEVER suggest single common English words on .com without flagging "almost certainly taken or premium-priced ($500–$50,000+)" — these look like options but are traps that waste the user's time.
- NEVER skip trademark risk classification — a name that infringes an existing SaaS trademark causes forced rebrand after launch, which costs orders of magnitude more than the domain.
- NEVER recommend hyphens as a "workaround" for taken names — hyphens fail the radio test completely (users say "go to code dash box dot com?" and navigate wrong), and they signal spam to email filters.
- NEVER suggest names with embedded numbers as primary choices — "4ward", "2fast" — they fail the radio test (is it the digit or the word?) and look amateurish on business cards.
- NEVER recommend .xyz as a serious primary TLD to non-tech audiences — it carries strong spam/scam association from bulk registrations; it signals "cheap placeholder" to anyone over 30.
- NEVER recommend country-code hacks (.ly, .me as word suffixes) as a primary domain without flagging country policy risk — Libya (.ly) has blocked/revoked domains for content violations; Bit.ly would be inaccessible if repeated.

## Output Format

For each session, produce:

**1. Analysis** (2–3 lines): category, audience, naming constraints surfaced.

**2. Candidates table** (10–15 names):
| Candidate | Pattern | Phonaesthetic Score /15 | Trademark Risk | Radio Test |
|-----------|---------|------------------------|----------------|------------|
| stripe.dev | dictionary/out-of-field | 14 | Tier 2 — verify class | PASS |

**3. Top 3 with reasoning**: why each works across distinctiveness, memorability, and brand fit.

**4. Next steps** (always): "Verify candidates at Namecheap/GoDaddy/Porkbun. Check trademark at USPTO TESS (tess.uspto.gov) for Tier 2+ names."

## Naming Frameworks

See `references/naming-frameworks.md` for:
- Phonaesthetic scoring rubric (5 axes)
- Trademark risk tier definitions (Tier 1–4)
- TLD selection decision tree
- Word construction patterns ranked by distinctiveness
- Radio test protocol
- Squatter pattern recognition
- Negative space naming technique

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| User says "all my candidates are taken" | Suggestions leaned on common words + .com | Pivot to portmanteau/invented words; offer .io/.dev alternatives; ask what budget they have for premium .com |
| User wants a .com of a two-word phrase | Almost certainly parked or $1,000+ | Acknowledge directly; generate portmanteau alternatives + offer .io/.dev at $10–15/yr |
| User has a name and wants domain variants | Don't re-brainstorm — evaluate the name they have | Run phonaesthetic score + trademark risk + radio test on their name; suggest TLD variants |
| User wants to know if a specific domain is available | Claude cannot check | Say clearly: "I can't check availability — go to porkbun.com or namecheap.com and search directly." |
| User's project is AI-related and they want .ai | Surface cost ($60–100/yr, Anguilla registry) and policy risk | Recommend .ai only if AI is the core product, not a feature; offer .dev as fallback |
