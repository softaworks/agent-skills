# Codex CLI — Model & Sandbox Reference

## Model Comparison Table

| Model | Best for | Context | Pricing (in/out per M) |
|-------|----------|---------|------------------------|
| `gpt-5.2-max` | Ultra-complex reasoning, deep architectural analysis | 400K / 128K | $1.25 / $10.00 |
| `gpt-5.2` ⭐ | Flagship — software engineering, agentic coding | 400K / 128K | $1.25 / $10.00 |
| `gpt-5.2-mini` | Cost-efficient; 4× usage headroom | 400K / 128K | $0.25 / $2.00 |
| `gpt-5.1-thinking` | Ultra-complex reasoning; runs ~2× slower on hardest tasks | 400K / 128K | varies |

**Cached input discount**: 90% off ($0.125/M) for repeated context; cache lasts up to 24 hours.

## Reasoning Effort Levels

| Level | When to use |
|-------|-------------|
| `xhigh` | Deep problem analysis, complex multi-file reasoning |
| `high` | Refactoring, architecture, security analysis, performance |
| `medium` | Feature additions, bug fixes, code organization |
| `low` | Quick fixes, formatting, simple documentation changes |

## Sandbox Mode Decision Tree

```
Does the task require writing files?
├── NO  → --sandbox read-only          (analysis, review, Q&A)
└── YES → Does it require network or process spawning?
          ├── NO  → --sandbox workspace-write   (edits, refactors)
          └── YES → --sandbox danger-full-access (install deps, run tests, CI)
```

## Quick Reference Command Table

| Use case | Sandbox | Key flags |
|----------|---------|-----------|
| Read-only review/analysis | `read-only` | `--sandbox read-only 2>/dev/null` |
| Apply local edits | `workspace-write` | `--sandbox workspace-write --full-auto 2>/dev/null` |
| Network or broad access | `danger-full-access` | `--sandbox danger-full-access --full-auto 2>/dev/null` |
| Resume recent session | Inherited | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` |
| Run from another directory | Match task | `-C <DIR>` plus other flags `2>/dev/null` |

## Resume Session Rules

- Resume syntax: `echo "your prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null`
- All flags go **between** `exec` and `resume`
- Do NOT pass model/effort flags on resume unless user explicitly requests — session inherits originals
- `--skip-git-repo-check` is always required, even on resume

## CLI Version Requirements

- Requires Codex CLI **v0.57.0+** for GPT-5.2 support
- Check: `codex --version`
- Switch model mid-session: `/model` slash command inside Codex session
- Default config: `~/.codex/config.toml`
