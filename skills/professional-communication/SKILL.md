---
name: professional-communication
description: Craft, improve, or structure professional written communication for technical contexts — email, async chat, meeting summaries, status updates, and audience-adapted technical explanations. Trigger phrases: "write an email", "draft a message", "help me communicate", "status update", "meeting agenda", "translate this for stakeholders", "improve my message", "how should I phrase this".
allowed-tools: Read, Glob, Grep
---

## Mindset

1. **The recipient's cognitive load is the only metric that matters.** A message is only as good as what the reader does with it. If they have to re-read, ask a clarifying question, or forward it to someone else, the communication failed — regardless of how accurate or thorough it was.

2. **Urgency and importance are almost never self-evident.** Every sender thinks their message is high-priority. Explicit signals ("Decision needed by EOD Friday") outperform implied urgency 100% of the time. The absence of a deadline means "whenever."

3. **Tone debt compounds.** A single passive-aggressive or blame-shifting sentence can permanently change how a reader filters your future messages. Unlike code, communication debt has no automated linter — it requires deliberate reversion.

4. **Medium selection is the first communication decision.** Choosing the wrong medium (chat for a complex decision, email for an urgent blocker) wastes more time than poor wording. Format mismatch signals poor situational awareness to peers and managers.

5. **Precision protects you; vagueness protects no one.** Hedge language ("might," "could," "sort of") reads as uncertainty in technical contexts. Stakeholders interpret ambiguity as risk. Be precise even when the situation is uncertain — state the uncertainty explicitly instead.

## Navigation

**Use this skill when**:
- Drafting or improving any written professional message (email, chat, Slack/Teams, async update)
- Adapting technical content for non-technical audiences (executives, clients, product)
- Structuring meeting agendas, summaries, or post-mortems
- Handling escalations, conflict-adjacent communications, or sensitive announcements
- The user says "help me say this," "is this too harsh," "how do I ask for X," or "translate this"

**Do NOT use this skill when**:
- The task is a difficult conversation requiring emotional intelligence — use `feedback-mastery` instead
- The output is formal legal, HR, or compliance documentation — those require domain-specific review beyond communication framing
- The user needs speech/presentation coaching (different register, different skill)

**Quick disambiguation**:
- Feedback to a colleague → `feedback-mastery`
- Written message, update, or audience translation → this skill
- Both → use this skill first, then flag `feedback-mastery` for delivery coaching

## Philosophy

Professional communication is not about demonstrating expertise — it is about creating the conditions for the reader to act correctly. Every structural choice (subject line, bullet vs. prose, opening sentence) is either reducing or adding to the reader's work.

## NEVER

- **NEVER open with context before stating the ask** — recipients scan for what they need to do, not what led to it. Burying the request at the bottom of a long context section guarantees it gets missed or deferred. Lead with the ask; follow with the rationale.

- **NEVER use a vague subject line** — "Quick question" or "Follow-up" forces the recipient to open the email to know whether it's urgent. This creates anxiety and delays action. Subject lines are pre-decisions: "API rate limit approval needed by Thursday" gives the reader everything before they open.

- **NEVER send a "wall of text" as a chat message** — prose paragraphs in Slack/Teams signal that you didn't consider the reader's context. Chat is a scanning medium; documents are a reading medium. Long explanations belong in a linked document, not a thread.

- **NEVER mark something urgent without stating the consequence of inaction** — "URGENT" without "if we don't decide by 3pm, the deploy is blocked until Monday" is noise. Stakeholders ignore unexplained urgency signals; they respond to explicit impact.

- **NEVER write in passive voice when accountability matters** — "The bug was missed" distributes blame diffusely and signals defensiveness. "QA missed the bug in the payment flow" is harder to write but faster to resolve — it's clear who needs to be in the post-mortem. Passive voice in incident communications is a red flag.

- **NEVER assume a technical peer wants more detail** — over-explanation to a peer signals distrust of their competence. If they need more, they'll ask. Default to the conclusion; offer depth if asked. This is the reverse of non-technical audience rules.

- **NEVER continue an async thread past 3 exchanges without offering a sync** — ping-pong past 3 rounds means the problem has ambiguity that text cannot resolve. Offering a 15-minute call is not a failure of async; it is the correct escalation path. Continuing to type is ego protection, not communication.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| No response after 48h | No explicit ask, unclear deadline, or wrong channel | Resend with explicit action request in the first sentence; switch medium if needed |
| Reply asks clarifying questions you already answered | Information was buried in the middle; reader scanned and missed it | Restructure: ask/decision first, context second; use bold to surface key data |
| Message perceived as aggressive or blame-y | Passive constructions + implicit accusations ("someone missed this") | Rewrite to specific facts + forward-looking action: what happened, what we'll do |
| Executive asks to "simplify" after reading your update | Technical depth exceeded their decision-making need | Strip all implementation detail; restate as: business impact, risk, decision needed |
| Message went to wrong audience (e.g., escalated too high) | Urgency misread medium; no escalation check | Send an immediate correction with explicit framing: "This was meant for [team]; forwarding to correct channel now" |

## How to Draft Any Message

1. **Identify the output type**: decision request / status update / FYI / escalation / explanation. Different types have different templates — see `references/email-templates.md`.
2. **State the ask or key fact in the first sentence.** No preamble.
3. **Apply audience calibration**: engineering peer → technical precision; manager → impact + timeline; executive → decision needed + risk if none; customer → plain language + what it means for them.
4. **Apply the "So What?" test** to every paragraph: if a paragraph doesn't change what the reader does or understands, cut it.
5. **Check medium fit**: real-time urgency → call; complex decision → email + doc; quick coordination → chat.

## References

- `references/email-templates.md` — Ready-to-use templates by message type (status update, escalation, FYI, request)
- `references/meeting-structures.md` — Agenda and summary formats for standups, retros, architecture reviews, post-mortems
- `references/jargon-simplification.md` — Technical-to-plain-language translations by domain
- `references/remote-async-communication.md` — Async-first principles, channel selection matrix, time zone norms; **load this when the communication is cross-timezone or fully async**

## Companion Skills

- `feedback-mastery` — Difficult conversations, delivering critical feedback, managing conflict
