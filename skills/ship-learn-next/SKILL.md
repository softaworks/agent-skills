---
name: ship-learn-next
description: "Extract actionable learning reps from any educational content — YouTube transcripts, articles, tutorials, or course notes. Produces a three-part plan: what to Ship (build now to prove understanding), what to Learn (specific gaps to fill), and what to Do Next (next learning step). Use when you have consumed content and want concrete next actions, not a summary. Triggers: make this actionable, turn this into a plan, what should I build from this, learning plan, extract takeaways."
allowed-tools:
  - Read
  - Write
---

## Mindset

**Reps reveal truth; plans reveal preferences.** A user's plan reflects what they wish were true. Their first rep reveals what is actually true. Design Rep 1 specifically to surface the gap.

**Scope is the enemy of rep 1.** Most people size their first rep at "learning the skill" rather than "producing one output." A rep that produces zero artifacts teaches zero. The practitioner question is: what is the smallest possible artifact that would falsify or confirm the advice?

**Content type determines extraction strategy.** YouTube speakers bury technique inside story; extract the behavior, not the anecdote. Articles front-load argument and back-load method; read the how-to sections first. Courses are 20% essential, 80% depth; identify the 20% before building the plan.

**Reflection without measurement drifts to narrative.** Users will say "it went okay" unless prompted for specific numbers (sent/opened/responded, shipped/unshipped, score/10). Build measurement into success criteria at design time, not after.

**The second rep is worth more than the first plan.** The plan is a hypothesis. Rep 2 is the first iteration with evidence. Don't over-architect reps 3-5 before the user has shipped once.

---

## Navigation

**Use this skill when**:
- User provides learning content (transcript, article, notes, course) and wants to act on it
- User says "make this actionable", "turn this into a plan", "I watched/read X, now what?"
- User wants to build a skill through practice, not study
- User has a goal but hasn't started shipping toward it

**Do NOT use this skill when**:
- User wants a reading list or course recommendations (this is anti-pattern territory)
- User wants a study schedule (redirect: study schedules are for exams, reps are for skills)
- User is in mid-rep and needs help executing (use appropriate domain skill instead)
- No learning content is provided — ask for it before proceeding

**Ambiguous input decision tree**:
```
User provides content → Read it, extract lessons, proceed
User describes content without providing it → Ask for the file/text
User has a goal but no content → Ask: "What advice/content are you drawing this from?"
User has both content AND a vague goal → Clarify the goal before designing Rep 1
```

---

## Philosophy

The bottleneck is never content — it's reps. Every rep produces more usable learning than any amount of consumption, because the artifact surfaces what the advice actually requires vs. what the user imagined it required.

---

## NEVER

- NEVER design Rep 1 that takes longer than 7 days — because urgency is the mechanism; longer reps let the user exit the loop before the feedback lands, and the plan dies.
- NEVER make the quest goal a learning outcome ("understand cold email") — because learning outcomes have no artifact and cannot fail, making reflection impossible; goals must produce observable outputs.
- NEVER list resources beyond what blocks Rep 1 — because every resource added is an invitation to consume instead of ship, which is the exact behavior this framework exists to break.
- NEVER generate reps 3-5 with full detail before rep 1 ships — because detailed future reps are a comfort object that substitutes for the discomfort of starting; they also become wrong the moment rep 1 reveals real constraints.
- NEVER accept "this week" as a deadline — because it's a non-commitment; always resolve to a specific day and optionally time, which surfaces whether the user has actually blocked time or is optimistically planning.
- NEVER skip the reflection structure — because the LEARN phase is where the framework's compounding value lives; a rep without structured reflection is just a task, not a learning cycle.
- NEVER let a quest contain more than ONE primary skill being practiced — because skill isolation is what makes reps measurable; multi-skill quests produce ambiguous feedback ("did I fail at writing or at research?").

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| User returns after rep 1 with "it went fine, nothing to reflect on" | Reflection prompts were too open-ended; no measurement criterion was embedded | Ask for the specific number (emails sent, responses received, score/10, artifacts produced) — vague reports indicate the success criteria weren't concrete enough |
| Rep 1 isn't shipped after 2+ weeks | Rep was sized too large, or user had an unacknowledged prerequisite (tool, permission, audience) | Diagnose: "What specifically stopped you?" then cut the rep in half or isolate the prerequisite as a mini-rep-0 |
| Content has no actionable advice — it's all theory | Source is a thought leadership piece or overview, not a practitioner guide | Reframe: what does the user already do that this content comments on? Design a rep around their existing behavior, annotated by the content |
| User wants to plan reps 6-20 before shipping rep 1 | Anxiety disguised as planning; planning feels safer than shipping | Name it directly: "Planning reps 6-20 is a way to avoid rep 1. What's stopping you from starting rep 1 today?" |
| Quest goal shifts between reps | User is discovering a more interesting adjacent problem | Acceptable after rep 2+; before that, preserve the original goal so the first rep has a fair test |

---

## Workflow

### 1. Ingest the content
Read the file provided. If no file: ask for it. Do not proceed without source material.

See [references/content-extraction.md](references/content-extraction.md) for extraction patterns by content type.

### 2. Extract lessons (actionable only)

Three-filter test for each lesson:
1. **Behavior test**: Is this something the user must *do differently*, not just *know*?
2. **Rep test**: Can this be practiced in a 1-7 day rep?
3. **Artifact test**: Does practicing it produce something observable?

Drop anything that fails filter 1. Downgrade to "resources" anything that fails filters 2-3.

### 3. Define the quest

Ask the user: "In 4-8 weeks, what would you have **shipped** that would make this content feel worth your time?"

Push until you get: a specific artifact + a number + a timeframe.
- Bad: "Get better at sales"
- Good: "Book 3 discovery calls from cold outreach in 6 weeks"

### 4. Size Rep 1

Rep 1 must:
- Produce ONE artifact (not a list of tasks)
- Ship in 1-7 days
- Require only what the user already has access to
- Be embarrassingly smaller than the quest goal

Ask: "What's the smallest version of this that would still teach you something real?"

Use the domain sizing table in [references/rep-templates.md](references/rep-templates.md) if the user's domain is listed.

### 5. Build the plan

Use templates from [references/rep-templates.md](references/rep-templates.md).

Resolve every deadline to a specific day. Replace "this week" with "by [day]".

### 6. Save the plan

Filename: `Ship-Learn-Next Plan - [Quest Title].md`
Quest title: 3-6 words, outcome-focused (not topic-focused).

Always save before presenting. Then show the user Rep 1 only. Ask: "What day will you ship Rep 1?"

### 7. Close

After showing Rep 1, ask exactly two questions:
1. "What day will you ship Rep 1?"
2. "What's the one thing most likely to stop you — and how will you handle it?"

Do not ask for a commitment on the full quest. Commitment on rep 1 is sufficient.
