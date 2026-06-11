---
name: daily-meeting-update
description: "Interactive daily standup/meeting update generator. Use when user says 'daily', 'standup', 'scrum update', 'status update', 'what did I do yesterday', 'prepare for meeting', 'morning update', 'team sync', 'async update', or 'remote standup'. Pulls activity from GitHub, Jira, and Claude Code session history. Conducts interview (yesterday, today, blockers, discussion topics) and generates formatted update for sync meetings, async Slack posts, or standup bots."
user-invocable: true
---

# Daily Meeting Update

Generate a daily standup/meeting update through an **interactive interview**. Never assume tools are configured — ask first.

---

## Mindset

1. **Tools surface what happened; the interview captures why it matters.** A merged PR without context ("I was blocked waiting for this") is noise. Always interview, even when you have full tool data.
2. **The Topics for Discussion question is highest-signal.** It captures cross-team dependencies, architectural decisions, and team-wide risks that no tool can detect. It's the one question you cannot skip.
3. **Async ≠ fewer questions — async updates are read without you present.** A vague sync standup is forgiven because teammates can ask. A vague async post blocks people for hours. Async format requires more precision, not less.
4. **One missed blocker cascades.** If a user is waiting on someone outside their team, that handoff won't happen unless stated explicitly. Surface it, name names, suggest the next action.
5. **Consent before access.** The user's repo list may include client work, personal projects, or sensitive branches they do not want surfaced in a standup. Always ask which repos; never enumerate everything visible.

---

## Navigation

### Use this skill when:
- User says "daily", "standup", "scrum", "morning update", "status update", "team sync"
- User asks "what did I do yesterday" or "help me prepare for my meeting"
- User needs an async Slack post, standup bot answer, or remote team update
- User is catching up after missed days (cover multiple days in "yesterday")

### Do NOT use this skill when:
- User wants a project status report (different scope — weekly/monthly, audience is leadership)
- User wants a written retrospective or sprint review
- User is asking about a specific ticket/PR status (use Jira/GitHub tools directly)

### Sync vs Async Decision Tree

```
Is the standup happening live (video/in-person/phone)?
├─ YES → Use full Markdown template (Phases 1→2→3 below)
│        Keep to <12 bullets; audience can ask follow-ups live
└─ NO  → Is it posted to Slack/chat?
          ├─ YES → Use chat format (bold headers, tag names, 4-6 lines)
          │        → See references/async-remote-patterns.md
          └─ NO  → Standup bot (Geekbot, Standuply)?
                    ├─ YES → Full sentences per prompt, no bullets
                    └─ NO  → Email/wiki → Full Markdown with links section
```

---

## Philosophy

The standup update is a coordination tool, not a progress report. Its job is to unblock teammates, surface dependencies before they become delays, and focus collective attention on what matters today — not to prove productivity.

---

## Workflow

```
Phase 1: DETECT & OFFER INTEGRATIONS
  ↓ Check Claude Code history, gh CLI, jira CLI (silently)
  ↓ Ask user which repos/integrations to pull (consent required)
  ↓ Pull data NOW — before interview, not during

Phase 2: INTERVIEW (with insights)
  ↓ Show pulled data as context for each question
  ↓ Q1: Yesterday (with tool data as prompt)
  ↓ Q2: Today (with Jira tickets as suggestions)
  ↓ Q3: Blockers
  ↓ Q4: Topics for Discussion (NEVER skip)

Phase 3: GENERATE UPDATE
  ↓ Combine interview answers + tool data
  ↓ Format for meeting type (sync/async/bot)
  ↓ Present to user
```

---

## Phase 1: Detect & Offer Integrations

Detect silently (suppress all errors). Full detection commands: `references/integration-details.md`

| Integration | Quick Detection |
|-------------|-----------------|
| Claude Code History | `~/.claude/projects/*/*.jsonl` exists |
| GitHub CLI | `gh auth status` succeeds |
| Jira CLI | `jira` command exists |
| Atlassian MCP | `mcp__atlassian__*` tools available |
| Git | Inside a git repository |

**For each detected integration:** Ask user if they want it pulled and which repos/projects to include. Never pull without explicit approval.

**Claude Code History:** Run `scripts/claude_digest.py --format json`, then present sessions via `AskUserQuestionTool` with `multiSelect: true` so user can exclude personal projects.

**If any integration fails:** Skip silently and proceed. No integration is required — the interview works without them.

Full pull commands, error handling: `references/integration-details.md`

---

## Phase 2: Interview (with Insights)

> In Claude Code: use `AskUserQuestionTool` for structured questions with options.

Show pulled data as context before asking each question — this triggers memory ("I see you merged PR #123, anything else?").

### Q1: Yesterday
Show tool data first, then: *"Anything else you worked on since the last standup that I missed?"*

If no data pulled: *"What did you work on yesterday/since last standup?"*

### Q2: Today
*"What will you work on today?"*

If Jira data pulled, suggest open tickets assigned to user as options.

### Q3: Blockers
*"Any blockers or impediments?"* → If yes, follow up for details and who needs to act.

### Q4: Topics for Discussion ← NEVER SKIP
*"Anything to bring up at the end of the daily?"* Examples: technical decision needing input, cross-team alignment, prioritization question, announcement.

### Async/Remote Extra Questions (optional — offer if fully remote or async team)

**Q5: Availability**
*"Any changes to your availability today?"* (late start, focus time, timezone conflicts)
Why: Remote teammates can't see you're AFK. Prevents cascade of blocked DMs.

**Q6: Cross-team dependencies**
*"Are you waiting on anyone outside your team, or does anyone outside your team need something from you?"*
Why: Cross-team blockers stall for days async — no one escalates what isn't named.

Load full async/remote patterns: `references/async-remote-patterns.md`

---

## Phase 3: Generate Update

Format based on meeting type determined in Navigation:

**Sync (Markdown):**
```markdown
# Daily Update - [DATE]

## Yesterday
- [Items from interview + tool data]

## Today
- [Items from interview]

## Blockers
- [Blockers or "No blockers"]

## PRs & Reviews (if GitHub pulled)
- **Opened/Merged/Reviewed:** ...

## Topics for Discussion
- [Topics or "None"]
---
*Links:* [PR/ticket URLs]
```

**Async/Chat (Slack):**
```
*Yesterday:* [2-4 items, plain text]
*Today:* [2-3 items]
*Blockers:* [one sentence, name the blocker and who needs to act]
*FYI:* [discussion topic as thread invitation]
```

Full output templates and Jira section format: `references/integration-details.md`

---

## NEVER

- **NEVER run `gh`, `jira`, or `git log` without asking first** — The user's visible repos may include client work, personal projects, or branches from a confidential feature. Enumerating everything visible is a privacy violation even when technically possible.

- **NEVER skip the Topics for Discussion question** — This is the highest-value question in any standup. Cross-team dependencies, architectural decisions, and process issues only surface if someone asks. Tools cannot detect them. Skipping it is the most common cause of standup meetings that "feel useless."

- **NEVER generate more than 15 bullets total** — Standup updates are read in under 2 minutes. Beyond 15 bullets, teammates skim or skip entirely. If the user has more than 15 items, consolidate by impact: "Resolved 3 auth bugs" not three separate bullets.

- **NEVER include raw ticket/PR numbers without title or summary** — "Fixed PROJ-123" communicates nothing to a teammate reading async. "Fixed PROJ-123: session timeout causing data loss" takes 3 seconds to write and is actually actionable.

- **NEVER assume the current directory is the only project** — Engineers routinely work across 2–5 repos (frontend, backend, infra, shared libs). Defaulting to current directory silently excludes the majority of their work. Always ask.

- **NEVER generate the update before completing all 4 questions** — The blocker or discussion topic revealed in Q3/Q4 often reframes Q1/Q2 ("I merged that PR but it's actually blocking deploy"). Generating early produces an update that misrepresents reality.

- **NEVER use full Markdown headers (`##`) in a Slack/chat async post** — Slack does not render Markdown headings. The output displays as `## Yesterday` literally. Use `*Yesterday:*` (bold inline). Sending malformatted async updates is worse than no update — it signals the user didn't review the output.

- **NEVER treat a missed-day standup the same as a normal one** — If the user skipped Monday's standup, Tuesday's "yesterday" covers 3 days. Ask: "Last time you posted was [day] — shall I cover since then?" and compress multi-day summaries rather than writing 30 bullets.

- **NEVER pull "today's" activity as yesterday** — GitHub/git defaults can include commits from the current morning. A commit made at 8:47am today belongs in "Today", not "Yesterday". Scope all tool queries to `--since="yesterday midnight"` or equivalent, not "last 24h from now."

---

## When Things Go Wrong

| Situation | Expert Response |
|-----------|-----------------|
| User says "I don't remember what I did" | Offer Claude Code digest first; if unavailable, ask: "What meetings did you have? Any PRs you reviewed? Any bugs you looked at even briefly?" — memory is trigger-based, not list-based |
| All integrations fail or unavailable | Proceed with pure interview — no tools required. Note: "Going manual — just answer the 4 questions" |
| User has only 5 minutes | Skip Phase 1 entirely; run Phase 2 verbally ("quick fire: yesterday? today? blockers? discussion?"); generate immediately |
| Async post with a critical blocker | Move blockers to the TOP of the update; add explicit "Action needed from @name by [time]" line; do not bury it in section 3 |
| User works across time zones (their today = team's yesterday) | Confirm the reference period: "Your standup covers work from [user's yesterday start] to now — is that right?" |
| Standup bot asks questions one at a time | Coach user: answer each prompt as a complete sentence; the bot may forward responses verbatim to a different channel |
| User's PR list includes team members' PRs they reviewed | Separate "Reviews done" from "Work opened/merged" — conflating them overstates output |

---

## Quick Reference

| Phase | Action | Tool |
|-------|--------|------|
| 1. Detect & Offer | Silent check → ask consent → pull data | Bash (silent), AskUserQuestionTool |
| 2. Interview | 4 questions with pulled-data context | AskUserQuestionTool |
| 3. Generate | Format for meeting type | Text output |

**Reference files:**
- `references/async-remote-patterns.md` — Slack format, bot format, time-zone edge cases, remote extras
- `references/integration-details.md` — All detection/pull commands, error handling, output templates
