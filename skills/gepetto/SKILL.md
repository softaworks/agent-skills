---
name: gepetto
description: Creates detailed, sectionized implementation plans through research, stakeholder interviews, and multi-LLM review. Use when planning a feature, refactor, or system that needs thorough pre-implementation analysis before coding begins. Trigger phrases: "make a plan", "plan this out", "help me plan", "create an implementation plan", "I need to think through", "architect this".
---

# Gepetto

Orchestrates a multi-step planning process: Research → Interview → Spec Synthesis → Plan → External Review → Sections

## Mindset

1. **You are the architect, not a transcriptionist.** The user's spec is a starting point — your job is to surface what they haven't thought about yet: failure modes, scaling inflection points, security implications, operational costs. A plan that only restates the spec is worthless.

2. **Sections are contracts, not outlines.** Each section file must be so self-contained that a developer with zero context could implement it correctly. If a section requires reading another document to understand, rewrite it.

3. **External review is adversarial by design.** Gemini and Codex are not validators — they are red teamers. Weight their critiques seriously; integrate at least one substantive finding from each reviewer or explicitly document why you rejected it.

4. **Resume fidelity beats speed.** Gepetto writes intermediate files precisely so work survives interruption. Never skip writing a step's output file even if you believe you'll complete the workflow in one session — the user may interrupt, context may compact, or a subagent may fail.

5. **The interview is the highest-leverage step.** Bad interview → bad spec → bad plan → wasted sections. Spend more time here than feels comfortable. Ask the follow-up question, not just the surface question.

---

## Navigation

### Use Gepetto when:
- Building something that will take more than one session to implement
- The requirements are ambiguous, contradictory, or incomplete
- Multiple architectural approaches are viable and the tradeoffs matter
- The user wants autonomous implementation via ralph-loop or Ralphy afterward
- A feature touches multiple layers (DB, API, UI, infra) and coordination matters
- Technical risk is high enough that an external review catch is worth the time

### Do NOT use Gepetto when:
- The task is a single-file edit or a bug fix with a known cause — just fix it
- The user said "just do it" or "go ahead and implement" — they want code, not a plan
- The spec is already a detailed implementation plan — start coding or use a simpler skill
- Time is critical and the user explicitly wants the fastest path to working code
- The feature is a trivial CRUD endpoint or boilerplate scaffold with no novel decisions
- The codebase has a strong, opinionated framework that answers all design questions

### Decision tree:

```
Is the work completable in < 30 minutes of focused implementation?
  YES → Skip Gepetto, implement directly
  NO  → Is the design space genuinely open (multiple valid architectures)?
          NO  → Is a plan needed for coordination / review / autonomous execution?
                  NO  → Skip Gepetto, implement directly
                  YES → Run Gepetto
          YES → Run Gepetto
```

---

## Philosophy

A plan that takes one hour to write and saves five hours of re-implementation is the best investment in software. Gepetto exists because the cost of unclear requirements is always paid — either up front in planning or later in rework. Make the user pay it consciously, up front, with full information.

---

## NEVER

- **NEVER skip the interview to save time.** The interview is where hidden requirements surface. A plan built without it encodes the author's assumptions, not the user's needs. Every skipped interview results in at least one surprise rework in the sections phase.

- **NEVER have subagents write intermediate files directly.** Subagents write in parallel and race. If two subagents both write `claude-research.md`, the last writer wins and findings are lost. All file writes belong to the main context after collecting subagent results.

- **NEVER integrate all external reviewer suggestions uncritically.** Gemini and Codex optimize for generic best practices, not for the user's constraints. A suggestion to "add Redis for caching" may be architecturally correct but operationally wrong for a solo developer with no Redis budget. Document what you rejected and why — silence implies you didn't read the review.

- **NEVER create section files without writing `sections/index.md` first.** The SECTION_MANIFEST in `index.md` is the authoritative list; everything else is derived from it. Writing section files before the manifest means you have no ground truth for resume detection or for ralph-loop orchestration.

- **NEVER produce a section file that says "see claude-plan.md for details."** Section files are implementation contracts. If the implementer must cross-reference the main plan, the section is incomplete. Duplicate context aggressively — it is cheap compared to a developer making wrong assumptions.

- **NEVER ask yes/no questions in the interview.** "Is authentication required?" gives you a one-bit answer. "What happens when a user's session expires mid-transaction?" forces the user to think through the edge case. The difference is a section on session recovery versus a silent data loss bug.

- **NEVER run Gepetto on an already-in-progress implementation without first checking for existing planning files.** Overwriting `claude-plan.md` on a partial implementation destroys the resume chain. Always scan for existing files and enter resume mode if any are found.

---

## When Things Go Wrong

| Scenario | Diagnosis | Recovery |
|----------|-----------|----------|
| External reviewer CLI not found | gemini/codex not installed or not on PATH | Skip that reviewer, note in output, proceed with one review or zero; document in integration notes |
| Subagent times out during section writing | Large plan or slow model | Re-run only missing sections — check SECTION_MANIFEST against existing files and launch Tasks only for gaps |
| User edits claude-plan.md mid-workflow | Plan content diverged from spec/interview | Re-read the edited plan before step 13; the user's edits are authoritative, do not revert them |
| Interview produces contradictory requirements | User said X in Q3 and not-X in Q7 | Surface the contradiction explicitly before writing the spec; ask the user to resolve it |
| Sections index and section files are out of sync | Manual file deletion or rename | Re-parse SECTION_MANIFEST and treat manifest as truth; regenerate only missing files |
| ralph-loop fails to find SECTION_MANIFEST | `<!-- SECTION_MANIFEST` block missing or malformed | Regenerate `sections/index.md` with the correct block format starting at line 1 |

For multi-day implementations spanning sessions, use session-handoff after each section phase to ensure the resuming agent can reconstruct intent without re-reading all planning files.

---

## CRITICAL: First Actions

**BEFORE anything else**, do these in order:

### 1. Print Intro

Print intro banner immediately:
```
═══════════════════════════════════════════════════════════════
GEPETTO: AI-Assisted Implementation Planning
═══════════════════════════════════════════════════════════════
Research → Interview → Spec Synthesis → Plan → External Review → Sections

Note: GEPETTO will write many .md files to the planning directory you pass it
```

### 2. Validate Spec File Input

**Check if user provided @file at invocation AND it's a spec file (ends with `.md`).**

If NO @file was provided OR the path doesn't end with `.md`, output this and STOP:
```
═══════════════════════════════════════════════════════════════
GEPETTO: Spec File Required
═══════════════════════════════════════════════════════════════

This skill requires a markdown spec file path (must end with .md).
The planning directory is inferred from the spec file's parent directory.

To start a NEW plan:
  1. Create a markdown spec file describing what you want to build
  2. It can be as detailed or as vague as you like
  3. Place it in a directory where gepetto can save planning files
  4. Run: /gepetto @path/to/your-spec.md

To RESUME an existing plan:
  1. Run: /gepetto @path/to/your-spec.md

Example: /gepetto @planning/my-feature-spec.md
═══════════════════════════════════════════════════════════════
```
**Do not continue. Wait for user to re-invoke with a .md file path.**

### 3. Setup Planning Session

Determine session state by checking existing files:

1. Set `planning_dir` = parent directory of the spec file
2. Set `initial_file` = the spec file path
3. Scan for existing planning files:
   - `claude-research.md`
   - `claude-interview.md`
   - `claude-spec.md`
   - `claude-plan.md`
   - `claude-integration-notes.md`
   - `claude-ralph-loop-prompt.md`
   - `claude-ralphy-prd.md`
   - `reviews/` directory
   - `sections/` directory

4. Determine mode and resume point:

| Files Found | Mode | Resume From |
|-------------|------|-------------|
| None | new | Step 4 |
| research only | resume | Step 6 (interview) |
| research + interview | resume | Step 8 (spec synthesis) |
| + spec | resume | Step 9 (plan) |
| + plan | resume | Step 10 (external review) |
| + reviews | resume | Step 11 (integrate) |
| + integration-notes | resume | Step 12 (user review) |
| + sections/index.md | resume | Step 14 (write sections) |
| all sections complete | resume | Step 15 (execution files) |
| + claude-ralph-loop-prompt.md + claude-ralphy-prd.md | complete | Done |

5. Create TODO list with TodoWrite based on current state

Print status:
```
Planning directory: {planning_dir}
Mode: {mode}
```

If resuming:
```
Resuming from step {N}
To start fresh, delete the planning directory files.
```

---

## Logging Format

```
═══════════════════════════════════════════════════════════════
STEP {N}/17: {STEP_NAME}
═══════════════════════════════════════════════════════════════
{details}
Step {N} complete: {summary}
───────────────────────────────────────────────────────────────
```

---

## Workflow

### 4. Research Decision

See [research-protocol.md](references/research-protocol.md).

1. Read the spec file
2. Extract potential research topics (technologies, patterns, integrations)
3. Ask user about codebase research needs
4. Ask user about web research needs (present derived topics as multi-select)
5. Record which research types to perform in step 5

### 5. Execute Research

See [research-protocol.md](references/research-protocol.md).

Based on decisions from step 4, launch research subagents:
- **Codebase research:** `Task(subagent_type=Explore)`
- **Web research:** `Task(subagent_type=Explore)` with WebSearch

If both are needed, launch both Task tools in parallel (single message with multiple tool calls).

**Important:** Subagents return their findings - they do NOT write files directly. After collecting results from all subagents, combine them and write to `<planning_dir>/claude-research.md`.

Skip this step entirely if user chose no research in step 4.

### 6. Detailed Interview

See [interview-protocol.md](references/interview-protocol.md)

Run in main context (AskUserQuestion requires it). The interview should be informed by:
- The initial spec
- Research findings (if any)

### 7. Save Interview Transcript

Write Q&A to `<planning_dir>/claude-interview.md`

### 8. Write Initial Spec (Spec Synthesis)

Combine into `<planning_dir>/claude-spec.md`:
- **Initial input** (the spec file)
- **Research findings** (if step 5 was done)
- **Interview answers** (from step 6)

This synthesizes the user's raw requirements into a complete specification.

### 9. Generate Implementation Plan

Create detailed plan → `<planning_dir>/claude-plan.md`

**IMPORTANT**: Write for an unfamiliar reader. The plan must be fully self-contained - an engineer or LLM with no prior context should understand *what* we're building, *why*, and *how* just from reading this document.

### 10. External Review

See [external-review.md](references/external-review.md)

Launch TWO subagents in parallel to review the plan:
1. **Gemini** via Bash
2. **Codex** via Bash

Both receive the plan content and return their analysis. Write results to `<planning_dir>/reviews/`.

### 11. Integrate External Feedback

Analyze the suggestions in `<planning_dir>/reviews/`.

You are the authority on what to integrate or not. It's OK if you decide to not integrate anything.

**Step 1:** Write `<planning_dir>/claude-integration-notes.md` documenting:
- What suggestions you're integrating and why
- What suggestions you're NOT integrating and why

**Step 2:** Update `<planning_dir>/claude-plan.md` with the integrated changes.

### 12. User Review of Integrated Plan

Use AskUserQuestion:
```
The plan has been updated with external feedback. You can now review and edit claude-plan.md.

If you want Claude's help editing the plan, open a separate Claude session - this session
is mid-workflow and can't assist with edits until the workflow completes.

When you're done reviewing, select "Done" to continue.
```

Options: "Done reviewing"

Wait for user confirmation before proceeding.

### 13. Create Section Index

See [section-index.md](references/section-index.md)

Read `claude-plan.md`. Identify natural section boundaries and create `<planning_dir>/sections/index.md`.

**CRITICAL:** index.md MUST start with a SECTION_MANIFEST block. See the reference for format requirements.

Write `index.md` before proceeding to section file creation.

### 14. Write Section Files — Parallel Subagents

See [section-splitting.md](references/section-splitting.md)

**Launch parallel subagents** - one Task per section for maximum efficiency:

1. First, parse `sections/index.md` to get the SECTION_MANIFEST list
2. Then launch ALL section Tasks in a single message (parallel execution):

```
# Launch all in ONE message for parallel execution:

Task(
  subagent_type="general-purpose",
  prompt="""
  Write section file: section-01-{name}

  Inputs:
  - <planning_dir>/claude-plan.md
  - <planning_dir>/sections/index.md

  Output: <planning_dir>/sections/section-01-{name}.md

  The section file must be COMPLETELY SELF-CONTAINED. Include:
  - Background (why this section exists)
  - Requirements (what must be true when complete)
  - Dependencies (requires/blocks)
  - Implementation details (from the plan)
  - Acceptance criteria (checkboxes)
  - Files to create/modify

  The implementer should NOT need to reference any other document.
  """
)

Task(
  subagent_type="general-purpose",
  prompt="Write section file: section-02-{name} ..."
)

Task(
  subagent_type="general-purpose",
  prompt="Write section file: section-03-{name} ..."
)

# ... one Task per section in the manifest
```

Wait for ALL subagents to complete before proceeding.

### 15. Generate Execution Files — Subagent

**Delegate to subagent** to reduce main context token usage:

```
Task(
  subagent_type="general-purpose",
  prompt="""
  Generate two execution files for autonomous implementation.

  Input files:
  - <planning_dir>/sections/index.md (has SECTION_MANIFEST)
  - <planning_dir>/sections/section-*.md (all section files)

  OUTPUT 1: <planning_dir>/claude-ralph-loop-prompt.md
  For ralph-loop plugin. EMBED all section content inline.

  Structure:
  - Mission statement
  - Full content of sections/index.md
  - Full content of EACH section file (embedded, not referenced)
  - Execution rules (dependency order, verify acceptance criteria)
  - Completion signal: <promise>ALL-SECTIONS-COMPLETE</promise>

  OUTPUT 2: <planning_dir>/claude-ralphy-prd.md
  For Ralphy CLI. REFERENCE section files (don't embed).

  Structure:
  - PRD header
  - How to use (ralphy --prd command)
  - Context explanation
  - Checkbox task list: one "- [ ] Section NN: {name}" per section

  Write both files.
  """
)
```

Wait for subagent completion before proceeding.

### 16. Final Status

Verify all files were created successfully:
- All section files from SECTION_MANIFEST
- `claude-ralph-loop-prompt.md`
- `claude-ralphy-prd.md`

### 17. Output Summary

Print generated files and next steps:
```
═══════════════════════════════════════════════════════════════
GEPETTO: Planning Complete
═══════════════════════════════════════════════════════════════

Generated files:
  - claude-research.md (research findings)
  - claude-interview.md (Q&A transcript)
  - claude-spec.md (synthesized specification)
  - claude-plan.md (implementation plan)
  - claude-integration-notes.md (feedback decisions)
  - reviews/ (external LLM feedback)
  - sections/ (implementation units)
  - claude-ralph-loop-prompt.md (for ralph-loop plugin)
  - claude-ralphy-prd.md (for Ralphy CLI)

How to implement:

Option A - Manual (recommended for learning/control):
  1. Read sections/index.md to understand dependencies
  2. Implement each section file in order
  3. Each section is self-contained with acceptance criteria

Option B - Autonomous with ralph-loop (Claude Code plugin):
  /ralph-loop @<planning_dir>/claude-ralph-loop-prompt.md --completion-promise "COMPLETE" --max-iterations 100

Option C - Autonomous with Ralphy (external CLI):
  ralphy --prd <planning_dir>/claude-ralphy-prd.md
  # Or: cp <planning_dir>/claude-ralphy-prd.md ./PRD.md && ralphy
═══════════════════════════════════════════════════════════════
```
