# Anti-Patterns Catalog — Agent MD Refactor

## Category 1: Root File Bloat

### Chronological accumulation drift
Every sprint someone adds 3 lines to CLAUDE.md. After 6 months it's 800 lines. No single section looks unreasonable in isolation — the problem is additive.
**Signal:** Lines added > lines removed over last 10 commits.

### Defensive over-specification
Teams write walls of rules after a single bad incident. "Always check if file exists before reading" appears because an agent once deleted a file. The rule now burns tokens on every task even when irrelevant.
**Signal:** Instructions that read like post-mortems ("Never again X").

### Platform-agnostic instructions in platform-specific files
CLAUDE.md written for Claude Code containing Copilot-style slot-fill patterns. The instruction format doesn't match the agent runtime.
**Signal:** Instructions that reference `<SLOT>`, `{{variable}}`, or step-by-step wizard patterns.

---

## Category 2: Structural Errors

### False modularity — splitting without linking
Files created in `.claude/` but root file never references them. Agent never reads them.
**Signal:** `.claude/*.md` files with zero inbound links from root.

### Cross-file contradiction via copy-paste
`testing.md` says "mock all external calls." `architecture.md` says "prefer integration tests." Both were copied from different projects.
**Signal:** Two linked files with semantically opposite rules.

### Depth-first file structure
```
.claude/
  backend/
    api/
      rest/
        conventions.md   ← agent never reaches this
```
Agents follow links one level at a time. Anything beyond depth 2 is effectively invisible.
**Signal:** Any linked file that is itself a directory index pointing to more files.

---

## Category 3: Content Quality Failures

### Rule without context = ignored rule
"Use functional components only" — but WHY? When an agent encounters a class component in existing code, it doesn't know if refactoring it is in scope.
**Signal:** Rules with no rationale and no scope boundary.

### Instruction-as-aspiration
"Write maintainable, well-tested, performant code" belongs in a team handbook, not an agent instruction file. Agents need executable conditions, not values.
**Signal:** Any rule where compliance cannot be verified by inspection.

### Stale command blocks
```
npm run dev
```
Project switched to pnpm 4 months ago. Agent runs the wrong command. No error visible in output (just wrong behavior).
**Signal:** Commands that don't match package.json scripts or Makefile targets.

---

## Category 4: Refactor Execution Errors

### Refactoring without reading the full file first
Splitting on first scan misses contradictions that only appear when you see instruction A on line 12 and its contradiction on line 340. Always read complete before splitting.

### Over-categorizing
Eight linked files for a 200-line AGENTS.md. Now the agent reads 8 files to find one rule. You've increased context cost, not reduced it.
**Threshold:** One linked file per ~150 lines of original content is reasonable.

### Losing provenance on deletions
Flagging "Write clean code" for deletion is safe. Flagging a domain-specific constraint ("never use mutable default arguments in Python config objects") because it "sounds like best practices" destroys institutional knowledge.
**Rule:** Only delete instructions that are universal defaults. When in doubt, keep.

---

## Platform Compatibility Matrix

| Platform | Root File | Linked Files Followed? | Max Depth | Notes |
|----------|-----------|------------------------|-----------|-------|
| Claude Code | CLAUDE.md | Yes (explicit Read) | Unlimited | Agent actively follows links |
| Claude.ai Projects | Project Knowledge | No — flat only | 1 | All instructions must be in one file |
| GitHub Copilot | COPILOT.md (or .github/copilot-instructions.md) | No | 1 | Single file, no linking |
| Cursor | .cursorrules | No | 1 | Flat JSON or markdown |
| Aider | .aider.conf | No | 1 | Config file, not linked docs |
| Devin | DEVIN.md | Limited | 2 | Partial link following |
| OpenHands | .openhands_instructions | No | 1 | Flat only |

**Critical implication:** Progressive disclosure (linked files) only works for Claude Code. For all other platforms, all instructions must remain in the root file — splitting actively breaks them.
