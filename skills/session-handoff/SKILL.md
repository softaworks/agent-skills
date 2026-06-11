---
name: session-handoff
description: "Creates and resumes comprehensive handoff documents for seamless AI agent session transfers. Use when: user says 'create handoff', 'save state', 'context is getting full', 'I need to pause', 'resume from handoff', 'continue where we left off', 'load context'; OR proactively after 5+ file edits, complex debugging, or architecture decisions. Solves context-exhaustion continuity failures in long-running agent work."
---

## Mindset

Handoffs fail not because they're incomplete — they fail because the *resuming* agent cannot reconstruct **intent and momentum**, only facts. A list of changed files is not a handoff. The document must answer: "What was I *trying to do* and why does it matter right now?"

Three practitioner truths:
- The most important section is "Decisions Made and Why" — not "Next Steps". Resuming agents reconstruct next steps from decisions; they cannot reconstruct decisions from next steps.
- Staleness is asymmetric: a handoff that's 2 hours old in an active repo is more dangerous than one that's 2 weeks old in a quiet one. Always check git delta, not wall clock.
- The agent writing the handoff is context-rich and will underspecify because things feel obvious. Write for an agent that knows nothing except what you write.

## Navigation

**Use this skill when**:
- User says: "create handoff", "save state", "context getting full", "I need to pause", "resume from", "continue where we left off"
- Context window is visibly large (10+ tool calls, 5+ file edits, complex debug chains)
- A major decision or architecture choice was just made
- Resuming work from a previous session or different machine

**Do NOT use this skill when**:
- The task will complete in the current session — handoffs for trivial tasks add noise
- No actual work has been done yet (handoff would be empty, misleading)
- User asked to *save to memory* (MEMORY.md) rather than handoff — these are different tools

**Ambiguous case — CREATE vs RESUME**:
- If user says "create handoff" → CREATE workflow
- If user says "resume" / "load" / "continue" → RESUME workflow
- If user provides a file path → RESUME workflow, load that file

## Philosophy

A handoff is not documentation — it is a **cognitive transplant**. Every word should close an ambiguity gap, not describe what is already visible in the codebase.

## NEVER

- NEVER write "continue implementing X" as a next step without specifying the exact file, function, and the decision boundary where you stopped — because a resuming agent will start from the beginning of X rather than the midpoint.
- NEVER include secrets, tokens, API keys, or passwords in handoff documents — they are stored in `.claude/handoffs/` which may be committed; validate with `validate_handoff.py` before finalizing.
- NEVER skip the "Decisions Made" section because "it's obvious from the code" — the rationale for a decision is never recoverable from the code itself, only its outcome is.
- NEVER resume from a handoff without running `check_staleness.py` first — a STALE handoff with an incorrect assumed branch is worse than no handoff (the resuming agent will confidently pursue a superseded plan).
- NEVER create a handoff chain longer than 3 links without pruning — resuming agents reading 4+ chained handoffs will synthesize a corrupted composite context that contradicts itself.
- NEVER omit the "What Is Blocked / Unresolved" section — unexplained blocks are the #1 cause of resuming agents re-attempting the same failed approach.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Resuming agent heads in wrong direction | Next steps were listed without the decision context behind them | Read "Decisions Made" section; reconstruct intent before acting |
| Validation score below 70 | `[TODO: ...]` stubs left unfilled, or key sections empty | Fill all TODO markers; "Current State" and "Decisions Made" are mandatory |
| `check_staleness.py` reports VERY_STALE | Many commits since handoff; branch may have diverged | Do NOT resume — create fresh handoff from current state instead |
| Chained handoffs contradict each other | Older handoff assumed X; newer handoff changed course without noting it | Read newest handoff only; treat it as authoritative; mark prior handoffs superseded |
| Secrets detected by validator | Credentials were pasted inline rather than referenced by path | Remove secrets, replace with vault/env reference, re-validate |

---

## CREATE Workflow

### Step 1: Generate scaffold

```bash
python scripts/create_handoff.py [task-slug]
# Chaining from prior handoff:
python scripts/create_handoff.py "auth-part-2" --continues-from 2024-01-15-auth.md
```

Script auto-fills: timestamp, project path, git branch, recent commits, modified files.

### Step 2: Fill mandatory sections

Open the generated file. These sections are **mandatory** — a handoff without them is invalid:

1. **Current State Summary** — one paragraph: what is working, what is not, where execution stopped
2. **Decisions Made and Why** — each decision with its rationale; not just the outcome
3. **What Is Blocked / Unresolved** — anything stalled and the last approach tried
4. **Immediate Next Steps** — file + function + exact stopping point for each action item

Template structure: [references/handoff-template.md](references/handoff-template.md)

### Step 3: Validate

```bash
python scripts/validate_handoff.py <handoff-file>
```

Do not finalize if: any `[TODO: ...]` remains, secrets detected, score < 70.

### Step 4: Confirm to user

Report: file location, validation score, first next-step action item.

---

## RESUME Workflow

### Step 1: Find and assess handoffs

```bash
python scripts/list_handoffs.py
python scripts/check_staleness.py <handoff-file>
```

Staleness levels: **FRESH** → resume safely | **SLIGHTLY_STALE** → review changes first | **STALE** → verify carefully | **VERY_STALE** → create fresh handoff instead.

### Step 2: Load and verify

Read the handoff completely. If chained, read the most recent only — use predecessor links only to resolve specific gaps.

Full resume checklist: [references/resume-checklist.md](references/resume-checklist.md)

Priority checks:
1. Git branch matches expected branch from handoff
2. Blockers listed — have they been resolved externally?
3. Referenced files still exist and match expected state

### Step 3: Begin from intent, not steps

Start from "Decisions Made" to reconstruct *why* the work matters, then execute "Immediate Next Steps" item #1.

### Step 4: Maintain or chain

- Mark completed items in "Pending Work" as you go
- After substantial progress: create new handoff with `--continues-from` to chain; keep chain ≤ 3 links deep

---

## Storage

Location: `.claude/handoffs/`
Naming: `YYYY-MM-DD-HHMMSS-[slug].md`

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `create_handoff.py [slug] [--continues-from <file>]` | Scaffold new handoff |
| `list_handoffs.py [path]` | List available handoffs |
| `validate_handoff.py <file>` | Check completeness, quality, secrets |
| `check_staleness.py <file>` | Assess if context is still current |
