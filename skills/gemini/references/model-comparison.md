# Gemini Model Comparison Reference

## Model Selection Matrix

| Model | Latency | Cost (input) | Context | Best When |
|-------|---------|--------------|---------|-----------|
| `gemini-3-pro-preview` | Medium | $2-4/M | 1M / 64k out | Complex reasoning, coding, agentic tasks, default choice |
| `gemini-3-flash` | Sub-second | Lower | 1M / 64k out | Speed-critical, distilled from 3 Pro, TPU-optimized |
| `gemini-2.5-pro` | Medium | Mid | 1M / 65k out | Legacy: mature stability, thinking mode |
| `gemini-2.5-flash` | Fast | $0.15/M | 1M / 65k out | Legacy: cost-optimized, high-volume, thinking mode |
| `gemini-2.5-flash-lite` | Fastest | Lowest | 1M / 65k out | Legacy: maximum throughput, minimal analysis depth needed |

## Decision Tree: Which Model to Use?

```
Is the task speed-critical (CI gate, user-facing latency)?
  YES → gemini-3-flash
  NO → Is cost a primary constraint (high-volume batch)?
    YES → gemini-2.5-flash
    NO → gemini-3-pro-preview (default)
```

## Approval Mode Matrix

| Mode | Interactive TTY | Background/Claude Code | Auto-edits | When to use |
|------|----------------|----------------------|------------|-------------|
| `default` | Safe | HANGS INDEFINITELY | No | Interactive terminal ONLY |
| `auto_edit` | Safe | Risky (may hang on non-edit prompts) | Yes | Supervised code review with edits |
| `yolo` | Safe | Safe | Yes | All background/automated tasks — required |

## Gemini 3 Pro Benchmarks

- SWE-bench: 76.2% (state-of-the-art)
- GPQA Diamond: 91.9%
- WebDev Arena Elo: 1487
- 35% improvement over Gemini 2.5 Pro on software engineering tasks
- Knowledge cutoff: January 2025

## CLI Version Requirements

- Gemini 3 model support: v0.16.0+
- Check version: `gemini --version`
- Google Cloud credentials must be configured
