---
name: agent-md-refactor
description: Refactor bloated AGENTS.md, CLAUDE.md, COPILOT.md, or similar agent instruction files. Splits monolithic files into organized, linked documentation using progressive disclosure. Use when: "refactor my AGENTS.md", "my CLAUDE.md is too long", "split my agent instructions", "organize my agent config", "progressive disclosure for my instructions", "clean up my CLAUDE.md".
license: MIT
---

# Agent MD Refactor

---

## Mindset

**Platform determines structure.** Progressive disclosure (linked files) only works for Claude Code. Claude.ai Projects, Copilot, Cursor, and Aider all ignore linked files — splitting them actively breaks those setups. Confirm platform before touching anything.

**Read the entire file before splitting.** Contradictions between line 12 and line 340 are invisible if you scan and split incrementally. A contradiction you miss becomes an agent inconsistency you can't debug later.

**Deletion destroys institutional knowledge.** "Write clean code" is safe to delete. "Never use mutable default arguments in our config loader" looks like generic advice but encodes a real incident. Only delete universally-obvious defaults — when in doubt, keep.

**The "every task" test is the only categorization rule that matters.** If an instruction only applies to 30% of tasks, it doesn't belong in the root file. Not "is it important" — is it relevant to 100% of tasks.

**Over-splitting is worse than not splitting.** Eight linked files for a 200-line source forces the agent to open 8 files to find one rule. More context cost, not less. Target 3–6 linked files maximum.

---

## Navigation

**Use this skill when:**
- "refactor my AGENTS.md / CLAUDE.md / COPILOT.md"
- "my agent instructions are too long"
- "split my agent instructions into files"
- "progressive disclosure for my agent config"
- "clean up / organize my CLAUDE.md"

**Do NOT use this skill when:**
- The file is already under 80 lines — pruning and editing is faster than restructuring
- The platform is Claude.ai Projects, Copilot, Cursor, or Aider — linked files don't work there; offer prune-only instead
- The user wants to write new instructions from scratch — this skill refactors, it doesn't author

**Platform decision tree:**
```
What platform(s) does this file serve?
├── Claude Code only           → full progressive disclosure (linked files valid)
├── Claude.ai Projects only    → flat only; prune and reorganize, no splitting
├── Copilot / Cursor / Aider   → flat only; splitting breaks it
└── Multiple platforms         → create separate files per platform, or keep flat
```

---

## Philosophy

Agent instruction files are not documentation — they are compiler inputs. Every byte costs inference tokens on every task. The goal is maximum signal density at minimum size: root file carries only what every task needs, linked files carry the rest, and anything a competent agent already knows gets deleted.

---

## NEVER

- **NEVER split files before confirming platform** — linked files are silently ignored on Claude.ai Projects, Copilot, Cursor, and Aider; splitting a multi-platform file breaks all non-Claude-Code users without any error message.

- **NEVER delete instructions that contain project-specific nouns** — library names, internal hook names, team-specific patterns, and incident-derived rules all look like "generic best practices" to an outside reader but encode irreplaceable context. Only delete instructions that could appear verbatim in any project.

- **NEVER create linked files that link to more linked files** — agents follow links from root, then read the target file. They do not recursively follow links inside linked files. Any instruction buried at depth 2+ is effectively invisible, creating a false sense of organization with zero functional benefit.

- **NEVER merge contradicting instructions without user confirmation** — two conflicting rules might both be intentional (e.g., "use semicolons" in source, "no semicolons" in test files). Silently picking one invalidates half the project's convention history.

- **NEVER apply progressive disclosure to a file under 80 lines** — the overhead of maintaining links and multiple files exceeds the context savings. Small files should be pruned, not split.

- **NEVER categorize by topic noun instead of task trigger** — `style-and-conventions.md` is organized around what the content is; `code-review.md` is organized around when it is needed. Agents retrieve context when starting a task — trigger-based grouping matches how they actually read.

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Agent stops following linked files | Platform is Claude.ai Projects or Copilot — linked files are not followed | Flatten back to single file; use section headers instead |
| Linked file exists but agent never reads it | No link in root file pointing to it, or link at depth 2+ | Add explicit link from root; never nest links |
| Refactored file loses a critical constraint | Domain-specific rule deleted as "obvious" | Restore from git history; add to deletion triage checklist — confirm all project-noun rules with user |
| Root file creep returns after 2 months | No process to prevent additive drift | Add line-count gate to CI or README: "Root file must stay under 50 lines" |
| Split created contradictions that didn't exist before | Copy-paste from different source contexts during categorization | Re-read both files; surface conflict to user before finalizing |

---

## Quick Process

Full workflow detail: [references/refactor-workflow.md](references/refactor-workflow.md)
Anti-patterns catalog + platform compatibility matrix: [references/anti-patterns-catalog.md](references/anti-patterns-catalog.md)

**Five-phase summary:**

1. **Platform check** — confirm linked files are valid for this target
2. **Full read + contradiction scan** — read complete file; surface all conflicts to user before touching anything
3. **Essentials extraction** — apply "every task" test; root file target under 50 lines
4. **Categorize by task trigger** — 3–6 linked files max; group by WHEN needed, not WHAT topic
5. **Deletion triage** — three buckets: DELETE (universal defaults), KEEP (domain-specific), ESCALATE (ask user)
