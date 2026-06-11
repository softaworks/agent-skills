---
name: codex
description: Use when the user asks to run Codex CLI (codex exec, codex resume), invokes OpenAI Codex for code analysis, refactoring, automated editing, or multi-step agentic coding workflows. Trigger phrases: "use codex", "run codex", "codex resume", "codex analyze", "codex refactor". Uses GPT-5.2 by default.
---

## Mindset

- **Sandbox discipline first** — the sandbox choice is the highest-stakes decision. Read-only is the safe default; escalate only when the task genuinely cannot complete without writes or network. Never let convenience drive you to `danger-full-access`.
- **Stderr is noise, not signal** — Codex streams thinking tokens to stderr. Suppress with `2>/dev/null` by default; only surface stderr when the user explicitly asks for reasoning traces or when diagnosing a failure.
- **Resume sessions, don't restart them** — re-running `codex exec` from scratch loses accumulated context. If a prior session exists and the user wants to continue, always reach for `resume --last`.
- **Flag placement on resume is load-bearing** — flags between `exec` and `resume` set session-level config; flags after `resume` are task-level. Mixing them silently corrupts behavior.
- **Reasoning effort multiplies cost non-linearly** — `xhigh` can run 5–10× longer than `medium` on hard tasks. Match effort to actual complexity; don't default to max.

## Navigation

**Use this skill when**:
- User says "use codex", "run codex", "codex exec", "codex resume", or "codex analyze/refactor"
- Task requires an agentic coding loop (plan → edit → verify) across multiple files
- User wants to leverage GPT-5.2's SWE-bench-optimized reasoning on a codebase

**Do NOT use this skill when**:
- The user wants Claude Code itself to edit files (no Codex invocation needed)
- Quick single-file edits that Claude can perform directly — Codex overhead isn't worth it
- User hasn't confirmed `codex --version` works (unresolved install errors will silently fail)

**Sandbox selection** (most common ambiguity):

```
Writing files?
  NO  → read-only
  YES → Network or subprocess needed?
    NO  → workspace-write
    YES → danger-full-access  (ask user first)
```

## Philosophy

Codex is a second reasoning engine, not a shell shortcut. Use it when the problem requires sustained multi-step agency — planning, editing, verifying — that exceeds what a single Claude Code turn can deliver reliably.

## NEVER

- **NEVER use `--sandbox danger-full-access` without explicit user confirmation** — it grants process spawning, arbitrary network access, and filesystem writes with no guardrails; a single bad prompt can modify or exfiltrate files outside the working directory.
- **NEVER omit `--skip-git-repo-check`** — without it, Codex aborts when invoked outside a git root, and the error message is cryptic enough that users assume Codex is broken rather than misconfigured.
- **NEVER pass model or effort flags after `resume --last`** — they appear to be accepted but are silently ignored; the session inherits its original config. Passing them misleads the user into thinking they changed the behavior.
- **NEVER show stderr by default** — thinking tokens flood Claude Code's context window, consuming tokens that degrade subsequent turns. Suppress with `2>/dev/null` unless the user explicitly asks for reasoning traces.
- **NEVER restart a session when `resume --last` exists** — restarting drops accumulated file context, tool call history, and any partial edits Codex was tracking. Resume is almost always correct.
- **NEVER use `xhigh` reasoning on simple tasks** — it can run 5–10× longer and cost significantly more without improving output quality on straightforward changes like formatting or minor bug fixes.
- **NEVER skip `codex --version` when the user reports unexpected behavior** — CLI version mismatches (pre-v0.57.0) silently fall back to older models rather than erroring, making GPT-5.2 features unavailable.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| `codex exec` exits non-zero immediately | Missing `--skip-git-repo-check` outside git root, or CLI not on PATH | Add flag; verify `codex --version` succeeds |
| Resume produces wrong model/effort | Flags placed after `resume` keyword instead of between `exec` and `resume` | Correct flag order: `codex exec [flags] --skip-git-repo-check resume --last` |
| Output is empty or truncated | stderr not suppressed, thinking tokens consumed context budget | Add `2>/dev/null`; if debugging, redirect stderr to a file instead |
| Task completes but no edits appear | `read-only` sandbox used for an edit task | Rerun with `--sandbox workspace-write --full-auto` |
| Cost/time far exceeds expectation | Reasoning effort set to `xhigh` or `high` for a simple task | Drop to `medium` or `low`; verify with `model_reasoning_effort` config |

---

## Running a Task

1. Check `codex --version` if behavior is unexpected (requires v0.57.0+ for GPT-5.2).
2. Ask user for reasoning effort via `AskUserQuestion` (`xhigh` / `high` / `medium` / `low`). Default model: `gpt-5.2`.
3. Select sandbox using the decision tree in **Navigation** above.
4. Assemble the command:
   ```bash
   codex exec \
     -m gpt-5.2 \
     --config model_reasoning_effort="<level>" \
     --sandbox <mode> \
     --full-auto \
     --skip-git-repo-check \
     [-C <DIR>] \
     "your prompt" 2>/dev/null
   ```
5. After completion, offer resume: "You can continue this session by saying 'codex resume'."

## Resuming a Session

```bash
echo "your follow-up prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null
```

All flags go between `exec` and `resume`. Do not add model/effort flags unless the user explicitly overrides them.

## Following Up

After every `codex exec`, use `AskUserQuestion` to confirm next steps or collect clarifications. Restate model, effort, and sandbox when proposing follow-up actions.

---

**Full model/sandbox reference**: `references/model-sandbox-reference.md`
