# README Policy

## The Core Test

Before adding any content to `README.md`, ask:

> "Would a human user need this to set up the skill, or does an agent need this to execute a task?"

- If a **human user** needs it to install, configure, or get started: it belongs in `README.md`.
- If an **agent** needs it to understand behavior, follow a workflow, or produce correct output: it belongs in `SKILL.md` or `references/`.

README.md is documentation for humans. SKILL.md is the instruction set for the agent. They must not duplicate each other.

## What README.md Must Contain

README.md should only include content in these four categories:

1. **Installation steps** — how to add the skill to Claude Code, what files to copy, what commands to run.
2. **Configuration** — environment variables, API keys, settings.json entries, file paths that need to be updated.
3. **Quick-start** — a minimal example showing the skill working end-to-end, intended to confirm setup succeeded.
4. **Changelog** — a record of significant changes across versions, for humans tracking upgrades.

If a section does not fit one of these four categories, it does not belong in `README.md`.

## What README.md Must NOT Contain

Do not put any of the following in `README.md`:

- Guidance that duplicates `SKILL.md` — if the skill body already explains how to use a feature, README must not re-explain it.
- Examples that Claude needs to follow during task execution — these are agent instructions and belong in `SKILL.md`.
- Workflow steps, decision logic, or output format rules — these are agent instructions.
- Capability lists intended to help the agent understand what it can do — these belong in `SKILL.md`.
- Reference tables, lookup data, or taxonomy lists — these belong in `references/`.
- Any content written in second-person addressed to "you" where "you" means the agent, not the human reader.

## When to Delete README.md

If a skill has no meaningful installation steps, no configuration requirements, and no environment variables to set, delete the `README.md` entirely.

A README that says only "This skill does X" or "Ask Claude to do Y" adds no value and creates a maintenance burden. Remove it.

Signs a README should be deleted:
- The entire README is a description of what the skill does (that description belongs in `SKILL.md` as the purpose statement).
- The README has no install section or the install section says only "drop the file in the plugins folder."
- The README duplicates the first paragraph of `SKILL.md` word-for-word.
- The README was generated to satisfy a template and contains no real human-facing content.

## README vs SKILL.md — Side by Side

| Content | README.md | SKILL.md |
|---|---|---|
| Installation command | Yes | No |
| API key setup | Yes | No |
| settings.json entry | Yes | No |
| Quick-start invocation example | Yes | No |
| Changelog | Yes | No |
| Workflow steps | No | Yes |
| Output format rules | No | Yes |
| Capability description | No | Yes |
| Examples Claude must follow | No | Yes |
| Loading triggers for references/ | No | Yes |

## Enforcement

When reviewing a skill's files, flag any README.md that:
- Contains a "Usage" section with workflow guidance.
- Contains a "Features" or "Capabilities" section.
- Is longer than the skill's `SKILL.md`.
- Contains language like "Claude will..." or "The agent should..." — these are agent instructions and belong in `SKILL.md`.

Any flagged content should be moved to `SKILL.md` or deleted if it already exists there.
