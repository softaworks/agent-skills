---
name: presentation-to-audience
description: Use when designing a presentation's narrative structure, calibrating content to audience type, planning opening and closing strategy, or preparing for hostile Q&A. Trigger phrases: "structure my presentation", "who is my audience", "what should I open with", "how do I handle questions", "is this the right narrative", "executive deck", "technical pitch", "board presentation". Covers narrative arc, audience calibration, and delivery design — NOT slide mechanics (use marp-slide for Marp syntax, layout, export).
---

# Presentation to Audience

## Mindset

1. **The deck is not the presentation — the audience's decision is.** Every structural choice flows backward from one question: what does this audience need to decide or believe when they leave? Content that doesn't serve that decision is decoration, regardless of how accurate or interesting it is.
2. **Narrative arc is a trust instrument, not an organizational preference.** Choosing the wrong arc for an audience type doesn't just reduce clarity — it actively destroys credibility. Technical audiences who see vision-first assume you haven't done the work. Exec audiences who see data-first assume you can't synthesize.
3. **The opening is your highest-leverage 30 seconds.** Audiences form a listening posture in the first 30 seconds and rarely revise it. An agenda slide in that window tells them the session is procedural; a sharp problem statement tells them this will matter to them. You don't recover from a procedural opening.
4. **Q&A is not separate from the presentation — it is a continuation of the narrative.** Hostile questions are attempts to redirect the narrative to a frame you didn't choose. The bridge technique exists precisely because answering on the questioner's terms cedes that frame permanently.
5. **Cognitive load is not a preference, it is physics.** Audiences literally cannot read text and listen to speech simultaneously; the two tasks compete for the same language-processing hardware. A slide that requires reading is a slide that is not being heard.

## Navigation

**Use this skill when**:
- Designing the structure and argument flow of a presentation from scratch
- Adapting existing content to a specific audience type (exec, technical, hostile, mixed)
- Choosing which narrative arc fits the situation
- Planning opening statements, closing calls to action, or Q&A strategy
- The user says a deck "isn't landing" or "feels flat" without a clear Marp syntax issue

**Do NOT use this skill when**:
- The request is purely about slide layout, Marp syntax, theme selection, or export — use `marp-slide` instead
- The user wants to write prose (a report, doc, or email) — use `writing-clearly-and-concisely`
- The request is about speaker delivery mechanics (pacing, voice, body language) — out of scope for both skills

**Audience type → arc selection decision tree**:

```
What is the audience's primary posture?

  TECHNICAL (skeptical, evidence-driven, peer reviewers)
  └─ Use: Problem → Solution → Proof
     Reason: credibility is earned through methodology, not vision;
             leading with vision reads as sales, not substance

  EXECUTIVE (time-constrained, synthesis-driven, decision authority)
  └─ Use: Vision → Gap → Path
     Reason: execs decide first, validate later; leading with data
             forces them to synthesize — your job, not theirs

  HOSTILE / SKEPTICAL (pre-opposed, adversarial, or politically misaligned)
  └─ Use: Situation → Complication → Resolution (McKinsey SCR)
     Reason: agreeing on the situation first creates common ground
             before you introduce the complication they may dispute;
             jumping to your solution without shared context triggers
             immediate counter-argument reflex

  MIXED (unknown or multi-stakeholder)
  └─ Default to Situation → Complication → Resolution
     Reason: SCR is the only arc that doesn't require you to assume
             the audience's existing belief set; it builds the shared
             frame before asserting anything
```

## Philosophy

A presentation is a structured argument delivered in real time to people with limited attention and competing priors. Its job is not to show everything you know — it is to move the audience from their current belief or decision state to the one you need them to reach. Every slide either serves that movement or slows it down.

## NEVER

- **NEVER open with an agenda slide** — because it signals a procedural frame before the audience has any reason to care about the content; audiences who see an agenda first assume the session is informational, not decisional, and they disengage before the argument begins. Earn their attention with the sharpest version of the problem or claim first; the structure will be obvious from the content.
- **NEVER use full sentences as bullet points** — because complete sentences compete directly with the speaker's spoken words for the audience's language-processing bandwidth; the audience reads the sentence, hears the speaker say something different, and loses both; use phrase-fragments that are grammatically incomplete without the speaker's voice to complete them.
- **NEVER show a table with more than 5 columns to a live audience** — because column-dense tables require horizontal scanning that is impossible from a projected screen at normal viewing distance; the audience will spend the entire slide attempting to read data they cannot reach, missing everything the speaker says; extract the single number or comparison that actually matters and present it as a chart or a highlighted call-out.
- **NEVER answer the question that was asked if it cedes the narrative frame** — because precise literal answering of hostile questions hands the questioner control of the agenda; use the bridge: acknowledge the question, then pivot to the point your presentation was making; audiences rarely notice and almost never penalize the pivot.
- **NEVER use transitions and animations that don't carry information** — because motion that doesn't signal "this is new" or "this is causally connected" consumes attentional resources the audience needs for comprehension; decorative wipes and fly-ins subtract from the presentation's credibility, especially in technical and executive contexts where restraint signals confidence.
- **NEVER end with "Any questions?" as your last slide** — because the last slide is the last thing the audience remembers; "Any questions?" ends on a procedural placeholder instead of your strongest claim or call to action; put your CTA or top-line conclusion as the final slide and let questions come while it is visible.
- **NEVER use a pie chart with more than 3 segments or any segment under 10%** — because pie charts require angular estimation, which the human visual system performs poorly; audiences cannot distinguish a 12% slice from a 15% slice, and charts with 4+ slices force them to read the legend repeatedly; use a ranked bar chart, which is readable in a single left-to-right pass.
- **NEVER bluff an answer you don't have** — because technical and expert audiences will detect the imprecision immediately, and the credibility loss from one bluffed answer outweighs the gain from appearing knowledgeable; "I don't have that number — I'll send it to you by [specific day]" is the highest-credibility response to a gap.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Audience disengages in the first 3 slides | Opening established context before establishing stakes — they don't yet know why this matters to them | Restructure: lead with the consequence, not the background; the background becomes slide 3, not slide 1 |
| Exec audience keeps asking "but what's the ask?" mid-deck | SCR or Problem-Solution arc used with an exec audience — they want the conclusion first | Reorder: put the recommendation and its decision on slide 2; supporting evidence follows as backup material |
| Technical audience pushes back on methodology before you've shown it | Vision-first arc used with skeptical peers — they inferred you skipped rigor | Switch to Problem → Proof → Solution; lead with data and methodology before the claim |
| Hostile questioner derails the session | Answering on the questioner's terms without bridging; once you accept their frame, the audience adopts it | Bridge immediately on the next question: "That's worth noting — what I'd add is [your point]"; do not attempt to re-answer the previous question |
| "So what?" reaction to data-heavy slides | Data without explicit decision implication — numbers were presented but the consequence was left to the audience to infer | Add a one-line "What this means for [audience]:" below every data slide; make the implication explicit, not implied |
| Presentation feels long even at the right duration | Slides with multiple independent ideas — the audience is experiencing compound cognitive load across ideas, not just slide count | Apply the "so what" test: any slide whose removal wouldn't change the audience's conclusion is a candidate for deletion |
| Q&A runs over and loses the room | No planned stopping mechanism and no return-to-CTA protocol | Close Q&A 2 minutes early with "I want to make sure we leave time for one more thing" and return to your CTA slide; never let Q&A be the last thing the audience experiences |

## Narrative Arc Reference

Load `references/narrative-arcs.md` when:
- The user needs a full structural template for any arc
- The presentation spans more than 20 slides and arc fidelity is in question
- The user has mixed stakeholder types and needs a hybrid structure

## Audience Calibration Reference

Load `references/audience-calibration.md` when:
- The user hasn't identified their audience type and needs diagnostic questions
- The audience includes multiple stakeholder types with conflicting information needs
- The user is presenting cross-functionally (e.g., technical content to a business audience)

## Rehearsal Protocol

Three passes, in order — run each separately, never combined:

**Pass 1 — Read-aloud pass**: Read every bullet fragment aloud as if speaking it. Any phrase that sounds unnatural in speech is a written phrase masquerading as a spoken one. Rewrite it until it sounds like something a person would say.

**Pass 2 — Timing pass**: Time each slide at the intended pace. Any slide under 45 seconds is either too sparse (add a second point) or too obvious (delete it). Any slide over 3 minutes contains more than one idea.

**Pass 3 — Cold-audience pass**: Read each slide assuming the audience has never heard of the topic. Any slide that requires knowledge from outside the deck to understand contains assumed context. Make the context explicit or move it to an earlier slide.

## The "So What" Test

Apply to every slide before finalizing:

> "If I remove this slide, does the audience reach a different conclusion or make a different decision?"

If no: delete the slide.  
If yes: the slide stays, but its title should state the conclusion explicitly, not the topic.

Weak title: "Q3 Customer Churn Data"  
Strong title: "Churn accelerated in Q3 — and the cause is recoverable"

The strong title does the cognitive work so the slide can carry the evidence.
