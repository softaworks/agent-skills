---
name: game-changing-features
description: "Structured opportunity analysis to surface 10x product leverage points — maps features against user pain tiers, competitive white space, and leverage-multiplier categories (network effects, automation, data moats). Use when deciding what to build next, evaluating feature ROI, or preparing a product strategy pitch. Outputs a prioritized opportunity matrix with rationale. Triggers: what should we build, game-changing feature, highest leverage improvement, product strategy, 10x opportunity."
---

# 10x Feature Strategy

## Mindset

1. **The feature that changes everything is rarely the most-requested one.** Users request solutions to symptoms; the 10x move solves the underlying job. Look one level above what users ask for.

2. **Small changes at high-frequency moments beat large changes at rare moments.** A 3-second save on a daily action compounds to 18 minutes/week. A major new feature used once a month might deliver less value. Always check frequency before estimating impact.

3. **Defensibility is the hidden dimension of feature scoring.** A feature that's easy to copy gives you 6 months. A feature that gets better with usage data, network effects, or user-generated content gives you years. Weight defensibility heavily in bets.

4. **The "obviously good" idea is often the wrong one.** If the team immediately agrees it's a great idea, it's probably already on the competitor's roadmap. The best bets feel slightly uncomfortable — plausible but not obvious.

5. **Activation beats retention beats acquisition — always audit in this order.** Most teams chase acquisition features when the product is bleeding users at activation. Diagnosing which stage is broken first prevents shipping the wrong 10x feature.

## Navigation

**Use this skill when**:
- User wants strategic product thinking about what to build
- User asks for "10x", "game-changing", "highest-leverage", or "what should we build next"
- User needs to prioritize a feature backlog from a value lens
- User wants to find quick wins with outsized impact

**Do NOT use this skill when**:
- User needs implementation plans or architecture (use `implementation-blueprint`)
- User has already chosen a feature and needs a spec (use `dev-spec`)
- User wants to stress-test a specific idea (use `critical-brainstorm`)
- User asks a quick "what feature should I add" question expecting a single answer in chat — answer directly without full session workflow

**Quick calibration**:
- If the user provides a product name and wants strategic analysis → run the full 5-step session, write output to `.claude/docs/ai/<product>/10x/session-N.md`
- If the user asks a bounded question ("what's one quick win for our onboarding?") → answer in chat, no file write needed

## Philosophy

The goal is not to generate the longest feature list — it is to identify the one or two moves that change the product's trajectory. Every hour spent on a good-but-not-great feature is an hour not spent on the transformative one. Ruthless prioritization is the product.

## NEVER

- NEVER present a feature list without explicit stack-ranking — because an un-ranked list shifts the prioritization burden back to the team, which is the exact problem this skill exists to solve.
- NEVER call a feature "10x" without specifying *what metric* it 10x's — because "10x better" without a denominator is motivational language, not strategy, and it misleads the team about the actual bet they're making.
- NEVER include a feature idea that maps to "better UX" or "improved performance" without naming the specific interaction being changed — because vague ideas survive roadmap review without ever getting built or killed; they become permanent backlog debt.
- NEVER score features on feasibility before scoring them on impact — because low feasibility scores kill transformative ideas before the team can find creative paths to ship them at reduced scope.
- NEVER recommend a collaboration feature without first checking if the product's user base actually has teammates — because collaboration features in solo-use products have near-zero adoption and create the illusion of strategy without value.
- NEVER output a session without at least one "Do Now" item that can ship in under 2 weeks — because sessions that produce only long-term bets are perceived as impractical and get shelved; an immediate win buys credibility for the bigger bets.
- NEVER skip the activation/retention/acquisition diagnostic — because shipping an acquisition feature when users churn at onboarding is the single most common way product teams waste a full quarter on the wrong lever.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| All ideas feel incremental, nothing feels 10x | Anchoring to current product shape; thinking in features not outcomes | Reframe: ask "what would make a user cancel a competitor to switch to us?" then reverse-engineer features from that answer |
| Team rejects the top-ranked ideas as "too risky" | Feasibility was scored too early in the process; ideas not paired with risk mitigations | Re-evaluate with explicit "reduced scope" path: what's the smallest version that tests the hypothesis? |
| User provides no context about the product | Can't research without a starting point | Ask exactly two questions: (1) What does the product do in one sentence? (2) Who is the primary user and what is their job? Then proceed. |
| Output feels like a generic product advice column | Skill applied without reading the actual codebase or product | Stop and read: check existing feature list, recent commits, support tickets or feedback if available. Ground every idea in observed evidence. |

---

## Workflow

### Step 1: Diagnose the growth stage first

Before ideating, determine where the product is bleeding value:
- **Activation problem**: Users sign up but don't reach the "aha moment"
- **Retention problem**: Users activate but churn within 30-90 days
- **Expansion problem**: Users stay but don't deepen usage or upgrade
- **Acquisition problem**: Hard to bring new users in

Features that fix the actual bottleneck outperform features that improve a healthy stage. If you can't diagnose, ask the user for churn timing data.

### Step 2: Understand current value (from the product, not from memory)

Read the codebase or product description. Document:
- What is the core action users take most?
- Where do users spend the most time?
- What does the product track or know about users that it doesn't surface?

### Step 3: Generate ideas across three scales

- **Massive** (transformative, 3+ months): Opens new markets, new user segments, or fundamentally new capabilities
- **Medium** (force multiplier, 1-2 months): Makes the core action dramatically faster/easier or turns casual users into power users
- **Small gems** (disproportionate value, <2 weeks): Single interactions that eliminate daily friction or anxiety

For each scale, sweep all 10 opportunity categories → see [references/opportunity-categories.md](references/opportunity-categories.md)

### Step 4: Score on impact before feasibility

For each idea, score in this order:
1. Impact (how much more valuable does this make the product?)
2. Reach (what % of users benefit?)
3. Frequency (how often does the user encounter this value?)
4. Defensibility (does this compound over time or is it copyable in 6 months?)
5. Feasibility (only after scoring the above four)

### Step 5: Stack rank and write output

Produce a prioritized list with at least one item in each tier: Do Now / Do Next / Strategic Bets / Backlog.

Write full sessions to `.claude/docs/ai/<product>/10x/session-N.md` using the template in [references/opportunity-categories.md](references/opportunity-categories.md).

For quick single-question responses, answer in chat without file output.
