---
name: naming-analyzer
description: Analyze and improve variable, function, class, and API names in any codebase. Triggers on: "review my naming", "are these names good", "rename suggestions", "naming conventions", "misleading names", "confusing variable names", "improve readability". Identifies semantic problems — not just style violations — and flags serialization-boundary renames that require deprecation before changing.
---

## Mindset

**Names are contracts, not labels.** A public function name is a promise to all callers; a DB column name is a promise to the schema. Renaming is cheap inside a function body, expensive at an API boundary, and potentially breaking at a serialization boundary. Always scope your analysis to blast radius first.

**Misleading names are bugs, vague names are debt.** A function named `getUser` that mutates state causes real defects. A variable named `data` causes confusion tax — it's worth renaming but not urgent.

**The reader's mental model is the measure.** A name is good when the reader can predict behavior without reading the body. Test by reading only signatures in a file — they should tell a coherent story.

**Scope determines acceptable brevity.** A 1-line lambda can use `x`; a module-level exported function cannot use `proc`. The longer the scope, the more the name must earn its place.

**Consistency beats perfection.** A codebase that uniformly uses `Manager` everywhere is better than a half-migrated one. Flag convention violations only when the inconsistency is within the same module or PR scope.

## Navigation

**Use this skill when**:
- A user asks about naming quality in a specific file, module, or PR
- Names in a diff are ambiguous, inconsistent, or misleading
- A refactor has produced names that no longer match behavior
- Setting up naming conventions for a new project

**Do NOT use this skill when**:
- The user wants a linter configured (that's a tooling task, not analysis)
- All names are already idiomatic and no issues are apparent — silence is correct here
- The naming is unusual but internally consistent with domain language (e.g., physics simulations using single-letter variable names is standard)

**Quick triage:**
```
Is the name actively misleading (wrong behavior implied)?
├─ Yes → CRITICAL: flag immediately, suggest rename + verify no serialization boundary
└─ No → Is it at a public API/serialization boundary?
    ├─ Yes → HIGH caution: suggest rename only with deprecation plan
    └─ No → Is it vague/abbreviated in a wide scope?
        ├─ Yes → MEDIUM: suggest rename, safe to apply via IDE refactor
        └─ No → Minor style: note it, don't block the review
```

## Philosophy

Names are the primary communication channel between the author's intent and the reader's understanding. Every naming suggestion must improve that channel without breaking the contracts that depend on it. Treat serialization boundaries as immutable until a migration plan exists.

## NEVER

- **NEVER suggest renaming a serialized field name without flagging the deprecation requirement** — JSON keys, DB column names, proto fields, Redux action strings, and env var names are consumed by external systems that cannot be updated atomically. A rename without a deprecation alias causes runtime breakage in production.

- **NEVER rename a framework lifecycle hook or magic method to "improve clarity"** — `__init__`, `componentDidMount`, `middleware`, `beforeSave` are called by reflection or convention; renaming them silently breaks behavior without any compile error.

- **NEVER flag single-letter names in math/physics/ML code as issues** — `W`, `b`, `X`, `y`, `σ` are the established notation for weights, biases, matrices, targets, and activations. Renaming them to `weightMatrix` destroys correspondence with the paper being implemented.

- **NEVER suggest generic replacements for vague names** — replacing `data` with `responseData` is barely better; push for domain-specific names (`invoiceLineItems`, `authTokenPayload`). A suggestion that is itself vague adds no value.

- **NEVER auto-apply renames to generated code** — files named `*.generated.ts`, `*_pb2.py`, `*.g.dart`, or anything in a `generated/` directory are overwritten on the next build cycle. Flag the generator template instead.

- **NEVER suggest `Manager`, `Helper`, `Utils`, or `Processor` as improvements** — these are already the problem. They are dumping-ground names that signal missing abstraction, not better names.

- **NEVER recommend renaming across repos in a single suggestion** — cross-repo renames require coordinated deploys. Flag the dependency and stop; the human must orchestrate the migration.

## Analysis Protocol

### Step 1: Classify by blast radius before evaluating quality

1. Read the name in context — what does the surrounding code actually do?
2. Check: is this name used at a serialization boundary? (See `references/safe-rename-checklist.md`)
3. Classify: misleading / vague / style-only / fine

### Step 2: Apply semantic tests

- **CQS test**: Does the name imply read-only but the body mutates state? → Misleading
- **Abstraction leak test**: Does the name reveal the implementation layer the caller shouldn't see? → Refactor
- **Scope-length heuristic**: Is the abbreviation acceptable for this scope? → See `references/semantic-analysis-frameworks.md`
- **Newspaper test**: Reading only signatures in the file, does the module's purpose emerge?

### Step 3: Report with severity + safety

```markdown
## [CRITICAL | HIGH | MEDIUM | MINOR] — <current name>

**Location**: file:line
**Issue**: <what is wrong semantically, not just stylistically>
**Serialization boundary**: [YES — requires deprecation] | [NO — safe to rename]
**Suggested name**: <specific domain-appropriate name>
**Why**: <non-obvious reason — not "it's clearer">
```

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Renamed a field and API consumers break silently | Serialization boundary missed; JSON key was load-bearing | Revert; add old name as alias with deprecation warning; communicate to consumers before removal |
| Renamed a method and tests pass but runtime fails | Framework uses the old name via reflection (Django signals, SQLAlchemy events, Flask routes) | Check for decorator registration or string-based dispatch; restore old name or update registration |
| Suggested name is already used elsewhere in the codebase | Didn't grep before suggesting | Search for the proposed name before recommending; collision is worse than the original |
| User accepts rename but it makes diffs unreadable | Name is too long for the diff hunk to provide context | Prefer shorter-but-specific over long-and-exhaustive for frequently-diffed code |
| Renaming `Manager` class creates 20 sub-issues | The class itself is the problem, not its name | Flag the design smell; recommend decomposition before naming |

## References

- `references/safe-rename-checklist.md` — Pre-rename safety checks, framework-protected names, deprecation patterns
- `references/semantic-analysis-frameworks.md` — CQS test, abstraction leak detection, scope-length heuristics, anti-pattern catalog
