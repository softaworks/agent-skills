# Async & Remote Team Standup Patterns

## When the Meeting Isn't Real-Time

Many teams run "standups" asynchronously — posted to Slack, a wiki, or a bot. The core 4-question structure still applies, but formatting and tone shift significantly.

---

## Async Update Formats

### Slack / Chat Post (most common)

```
*Yesterday:* Fixed session timeout bug (PR #120 merged), reviewed @alice's payment PR
*Today:* Continue OAuth flow (PROJ-123), unblock @bob on API schema
*Blockers:* Waiting on security sign-off for the OAuth client ID — pinged @infra-team
*FYI:* We should discuss auth token TTL strategy before Wednesday deploy — happy to start a thread
```

**Rules for chat format:**
- Inline bold headers, not Markdown `##` headings (Slack renders `*text*` not `## text`)
- Tag teammates who are involved in blockers or handoffs
- Keep to 4–6 lines; no bullets for Today if items are few
- Discussion topics become threaded FYIs, not a separate section

### Email / Long-form Async (weekly recap hybrid)

Use full Markdown output template — this context loads from SKILL.md Phase 3.

### Standup Bot (Geekbot, Standuply, etc.)

Many bots ask each question one-at-a-time via DM. Coach the user:
- Answer each bot prompt directly from their interview notes
- For "blockers" prompt: full sentence (bots often forward to a manager channel verbatim)
- For "today" prompt: be explicit about ticket IDs since bots often auto-link them

---

## Time-Zone Edge Cases

### User is First to Post (early timezone)

- "Yesterday" window may not overlap with teammates' yesterday
- Clarify: "I'll include anything from the past 24h of my work, not just your team's calendar day"
- Pull GitHub data for last 24h, not "since midnight local"

### User Missed Yesterday's Standup

Decision tree:

```
Did you post anything async yesterday?
├─ Yes → "Reference your async post, add what changed since then"
└─ No  → "Cover 2 days of yesterday (Thu + Fri if Mon standup)"
         → Compress: "Earlier this week: X. Yesterday: Y."
         → Flag the gap explicitly if blockers went unaddressed
```

### Cross-timezone Handoffs

If the user's update will be read by teammates in a different timezone who act on it while the user sleeps:
- Move blockers to the TOP of the update (readers need to act immediately)
- Include explicit handoff notes: "Leaving PROJ-456 at X state — @alice can pick up from branch `feature/xyz`"
- Add a "Needs Action" section if anything requires a teammate decision

---

## Team-Specific Anti-Patterns (Async)

| Situation | Symptom | Fix |
|-----------|---------|-----|
| PM-heavy team | Update becomes a status report with metrics | Keep format terse; metrics belong in a weekly |
| High-meeting culture | User writes update nobody reads | Ask: "Who actually reads this? Format for them." |
| Monorepo team | Commits from 6 people in same repo; user's stand out poorly | Pull by author filter; lead with impact, not repo name |
| Distributed team, no overlap | "Today" items may be stale by time readers see them | Add "by EOD my timezone" estimates on key items |

---

## Formatting Decision Tree: Sync vs Async

```
Is the meeting happening live (video/in-person)?
├─ YES → Use full Markdown template (rendered in meeting tool)
│        Keep to <12 bullets; audience can ask questions live
└─ NO  → Is it posted to Slack/chat?
          ├─ YES → Use chat format (bold headers, no ##, tag names)
          │        Keep to 4–6 lines
          └─ NO  → Is it a bot/form input?
                    ├─ YES → Answer per prompt, full sentences, no bullets
                    └─ NO  → Email/wiki → Full Markdown, add links section
```

---

## Remote-First Standup Extras (Questions 5 & 6)

When teams are fully remote with no watercooler, optionally add:

**Question 5: Availability / Context**
```
"Any changes to your availability today? (late start, early end, off-site, focus time?)"
```
Why this matters: Remote teams can't see you're not at your desk. Heads-up prevents blocked teammates.

**Question 6: Cross-team dependencies**
```
"Are you waiting on anyone outside your team, or does anyone outside your team need something from you?"
```
Why this matters: Cross-team blockers often stall for days in async environments because nobody escalates them.

Only offer these extra questions if the user mentions they're fully remote or the team uses async standups. Don't add them to a normal 15-minute sync standup — it bloats the update.
