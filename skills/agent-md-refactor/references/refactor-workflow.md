# Refactor Workflow — Agent MD Refactor

## Pre-Flight: Platform Check (Do This First)

Before any restructuring, identify the target platform(s).

```
Does this file serve Claude Code exclusively?
  YES → progressive disclosure (linked files) is valid
  NO  → keep flat; only prune and reorganize within single file
  BOTH → create Claude Code version + separate flat version
```

See [anti-patterns-catalog.md](anti-patterns-catalog.md) for the full platform compatibility matrix.

---

## Phase 1: Contradiction Scan

Read the entire file before touching anything. Map:
- Line numbers of each rule
- Scope of each rule (always / when / if)
- Any two rules that could conflict on the same codebase action

**Output to user (if contradictions found):**
```
Contradiction found:
  Line 12: "Use semicolons"
  Line 187: "No semicolons in test files"

Q: Is the second rule intentional (tests use different style) or a copy-paste error?
```

Do not proceed past Phase 1 until contradictions are resolved.

---

## Phase 2: Essentials Extraction

Apply the "every task" test: if an instruction only matters for 30% of tasks, it belongs in a linked file, not root.

**Root file keeps:**
- Project identity (1 sentence)
- Non-default commands (build, test, typecheck — only if non-standard)
- Package manager (only if not npm)
- Hard overrides (things that MUST take precedence over agent defaults)
- Rules that apply to 100% of tasks

**Root file target:** Under 50 lines.

---

## Phase 3: Categorization

Group by WHEN they are needed, not by WHAT they are about.

**Effective grouping:** `testing.md` (needed when writing or modifying tests)
**Ineffective grouping:** `style-and-conventions-and-formatting-and-naming.md` (too broad)

**Sizing rule:** 3–6 linked files maximum. If you have more than 6, merge the least-referenced topics.

---

## Phase 4: Deletion Triage

Three-bucket sort for each candidate instruction:

| Bucket | Criterion | Action |
|--------|-----------|--------|
| DELETE | Universal default — agent already knows | Remove |
| KEEP | Domain-specific or non-obvious | Keep |
| ESCALATE | Unclear if project-specific or generic | Ask user |

**Never delete without user confirmation if the instruction:**
- Contains a specific library name
- References a project-internal pattern (e.g., "use our AuthContext hook")
- Has a non-obvious rationale embedded in it

---

## Phase 5: Link Validation

After creating linked files:
1. Every file referenced from root must exist
2. No linked file references another linked file (depth 2+ = invisible)
3. Root file links use relative paths (not absolute)
4. Verify link syntax matches target platform (Markdown `[text](path)` for Claude Code)

---

## Execution Checklist

```
[ ] Platform identified — confirm linked files are valid for this platform
[ ] Full file read before any changes
[ ] All contradictions surfaced to user and resolved
[ ] Root file under 50 lines
[ ] 3–6 linked files (not more)
[ ] No linked file references another linked file
[ ] Deletion candidates confirmed with user for domain-specific rules
[ ] All links validated (files exist, paths correct)
[ ] No instruction lost without explicit user approval
```
