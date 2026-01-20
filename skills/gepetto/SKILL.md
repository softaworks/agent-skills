---
name: gepetto
description: Creates detailed, sectionized implementation plans through research, stakeholder interviews, and multi-LLM review. Use when planning features that need thorough pre-implementation analysis.
---

# Gepetto

Orchestrates a multi-step planning process: Research → Interview → Spec Synthesis → Plan → External Review → Sections

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
| all sections complete | resume | Step 15 (ralph-loop prompt) |
| + claude-ralph-loop-prompt.md | resume | Step 16 (ralphy PRD) |
| + claude-ralphy-prd.md | complete | Done |

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
STEP {N}/18: {STEP_NAME}
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

### 14. Write Section Files

See [section-splitting.md](references/section-splitting.md)

For each section defined in the manifest:
1. Read index.md to get section info
2. Write `section-NN-<name>.md` with implementation details from `claude-plan.md`
3. Mark TODO complete
4. Continue until all sections are written

**IMPORTANT: Each section file must be completely self-contained.** The implementer should NOT need to reference any other document.

### 15. Generate Ralph-Loop Prompt (Optional Integration)

Create `<planning_dir>/claude-ralph-loop-prompt.md` for optional ralph-loop integration.

**This file embeds all section content inline** so users who want autonomous execution can run a single command:
```
/ralph-loop @<planning_dir>/claude-ralph-loop-prompt.md --completion-promise "COMPLETE" --max-iterations 100
```

**File structure:**
```markdown
You are implementing a feature based on a spec-forge plan.

## Your Mission

Read the planning documents and implement ALL sections in dependency order.

## Planning Documents

### Section Index (dependencies and order)

{EMBED: full content of sections/index.md here}

### Section Files

---
## section-01-name.md
---
{EMBED: full content of section-01-name.md}

---
## section-02-name.md
---
{EMBED: full content of section-02-name.md}

{... repeat for all sections ...}

## Execution Rules

1. Read the index.md to understand the dependency graph
2. Execute sections in the correct order (respect dependencies)
3. For each section:
   - Implement all requirements
   - Verify acceptance criteria are met
   - Run any tests mentioned
   - Only move to next section when current is complete
4. Track progress by creating planning/PROGRESS.md with completed sections

## On Completion

When ALL sections are implemented and verified:
- Update planning/PROGRESS.md with final status
- Output <promise>ALL-SECTIONS-COMPLETE</promise>

If blocked on any section after multiple attempts:
- Document the blocker in planning/PROGRESS.md
- Output <promise>BLOCKED</promise>
```

**Important:** Replace `{EMBED: ...}` placeholders with actual file contents when writing.

### 16. Generate Ralphy PRD (External CLI Integration)

Create `<planning_dir>/claude-ralphy-prd.md` for integration with [Ralphy](https://github.com/michaelshimeles/ralphy) and similar task-based AI CLI runners.

Unlike ralph-loop (which embeds everything in a single prompt), Ralphy iterates through a checkbox task list and relies on the AI to read referenced files for context.

**File structure:**

```markdown
# Implementation PRD

This PRD was generated by Gepetto. Each task references a detailed section file.

**Before running:** Ensure you're in the project root directory where `sections/` is accessible.

## How to Use

```bash
# With Ralphy CLI
ralphy --prd <planning_dir>/claude-ralphy-prd.md

# Or copy to project root as PRD.md
cp <planning_dir>/claude-ralphy-prd.md ./PRD.md
ralphy
```

## Context

For each task below, read the corresponding section file in `sections/` for:
- Background and requirements
- Implementation details
- Acceptance criteria
- Files to create/modify

## Tasks

- [ ] Section 01: {section_name} - Read sections/section-01-{name}.md for details
- [ ] Section 02: {section_name} - Read sections/section-02-{name}.md for details
- [ ] Section 03: {section_name} - Read sections/section-03-{name}.md for details
{... one task per section from the SECTION_MANIFEST ...}
```

**Rules for generating:**
1. Parse `sections/index.md` to get SECTION_MANIFEST
2. Create one checkbox task per section
3. Task description should include the section name and reference the section file
4. Keep task descriptions concise - the detail is in the section files

### 17. Final Status

Verify all files were created successfully:
- All section files from SECTION_MANIFEST
- `claude-ralph-loop-prompt.md`
- `claude-ralphy-prd.md`

### 18. Output Summary

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
