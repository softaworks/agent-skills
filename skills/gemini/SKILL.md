---
name: gemini
description: Use when the user asks to run Gemini CLI, needs big context (>200k tokens) analysis, wants a second-model code review, or says "use Gemini", "run Gemini", "Gemini review", "analyze with Gemini". Invokes gemini-3-pro-preview by default for state-of-the-art reasoning and 1M-token context.
---

# Gemini Skill

## Mindset

- **Approval mode is the only true footgun.** Every hung Gemini process in the wild traces to `--approval-mode default` in a non-TTY shell. Before running any command, ask: is this an interactive terminal? If uncertain, assume no.
- **Model selection is a cost/speed/quality triangle, not a quality ladder.** `gemini-3-flash` is distilled from `gemini-3-pro` — for pure speed it beats Pro; it is not a "worse" model, it's a different trade-off.
- **Large context degrades with vague prompts.** A 1M-token codebase fed a generic "review this" prompt produces generic output. Structured enumeration (numbered focuses, explicit output format) is what unlocks Gemini's context advantage.
- **Sessions are ephemeral.** Gemini CLI has no built-in resume. Do not promise continuity across invocations; plan prompts to be self-contained or explicitly carry forward prior findings.
- **`--include-directories` is opt-in scope, not filtering.** It adds directories to the workspace; it does not restrict Gemini from reading the cwd. Misunderstanding this causes unintended file access when the cwd is a large repo.

## Navigation

**Use this skill when**:
- User explicitly mentions Gemini or asks to "run Gemini"
- Task context exceeds ~200k tokens (entire codebases, large doc sets)
- User wants a second-model opinion on code or architecture
- Speed-critical or cost-optimized large-context batch analysis is needed

**Do NOT use this skill when**:
- Task fits Claude's own context window — adding Gemini is latency with no benefit
- User wants a conversational back-and-forth — Gemini CLI is one-shot or interactive terminal only, not a chat loop inside Claude
- No Gemini CLI is installed (`gemini --version` fails) — verify first, do not assume

**Ambiguous input decision tree**:
```
User says "review this codebase"
  → Fits in Claude context? → Handle directly, no Gemini needed
  → Too large or user said "use Gemini"? → Invoke this skill
    → Interactive terminal confirmed? → approval-mode default or auto_edit
    → Background / Claude Code tool call? → approval-mode yolo (required)
```

## Philosophy

Gemini CLI is a force-multiplier for context scale, not a replacement for precise prompting. The skill's job is to translate user intent into a safe, structured Gemini invocation — correct approval mode, right model for the trade-off, explicit prompt structure — and surface the output cleanly.

## NEVER

- NEVER use `--approval-mode default` in a non-interactive shell — it blocks waiting for TTY input that never arrives; the process idles at 0% CPU for hours consuming quota.
- NEVER omit `--approval-mode yolo` when running inside Claude Code tool calls — Claude Code Bash is never a TTY; `default` always hangs here.
- NEVER pass a vague free-form prompt to a large context invocation — Gemini will summarize rather than analyze; always enumerate focus areas and specify the output format you need.
- NEVER assume `--include-directories` limits scope — it expands scope; if you add a large external directory, Gemini will read it in addition to cwd, not instead of it.
- NEVER skip `gemini --version` before first use — v0.16.0+ is required for Gemini 3 model names; earlier versions silently fall back or error on unknown model IDs.
- NEVER run without a timeout on tasks >5 min estimated — even with `yolo`, network issues can stall the process; `timeout 300 gemini ...` is the safety net.
- NEVER promise users they can resume a Gemini session — CLI sessions are one-shot unless explicitly opened with `-i`; carry forward findings manually in follow-up prompts.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Process running 20+ min, 0% CPU, stat 'S' | `--approval-mode default` in non-TTY | `pkill -9 -f "gemini.*gemini-3"` then re-run with `--approval-mode yolo` |
| `Unknown model` error | CLI version < 0.16.0 | `gemini --version`; upgrade to v0.16.0+ |
| Generic / shallow output on large codebase | Vague prompt | Restructure with numbered focus areas and explicit output format (see references/prompt-patterns.md) |
| Out-of-memory / truncated output | Context too large for single pass | Switch to `gemini-3-flash`; use `--include-directories` to narrow scope; break into sub-analyses |
| `auto_edit` mode hangs mid-run | Non-edit approval prompt triggered | Kill process; switch to `yolo` for background or `default` for interactive |

---

## Running a Task

**Step 1 — Verify CLI is available**
```bash
gemini --version   # must be v0.16.0+
```

**Step 2 — Select model** (ask user or default to Pro)

See `references/model-comparison.md` for full matrix. Quick rule:
- Speed-critical → `gemini-3-flash`
- Cost-optimized batch → `gemini-2.5-flash`
- Everything else → `gemini-3-pro-preview`

**Step 3 — Determine approval mode**

| Execution context | Approval mode |
|-------------------|---------------|
| Interactive terminal (confirmed TTY) | `default` or `auto_edit` |
| Background / Claude Code Bash tool | `yolo` (required) |
| Unknown / uncertain | `yolo` (safe default) |

**Step 4 — Assemble and run**

Background (standard):
```bash
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Perform a comprehensive code review. Focus on:
   1. Security vulnerabilities
   2. Performance issues
   3. Code quality
   Return findings as: [File:Line] Severity — Issue — Fix"
```

Background with safety timeout:
```bash
timeout 300 gemini -m gemini-3-pro-preview --approval-mode yolo "..."
```

Interactive with initial prompt:
```bash
gemini -m gemini-3-pro-preview -i "Review auth system" --approval-mode auto_edit
```

Multi-directory:
```bash
gemini -m gemini-3-pro-preview --approval-mode yolo \
  --include-directories /path/to/backend \
  --include-directories /path/to/frontend \
  "Analyze cross-service API contracts"
```

**Step 5 — After completion**

Inform user: "Gemini analysis complete. For follow-up, start a new Gemini session carrying forward the key findings — there is no built-in resume."

---

## References

- `references/model-comparison.md` — Full model matrix, decision tree, approval mode matrix, benchmarks
- `references/prompt-patterns.md` — Structured prompt templates for code review, architecture review, onboarding, hung-process recovery

Load these when: user asks for model details, benchmark numbers, prompt templates, or troubleshooting scripts.
