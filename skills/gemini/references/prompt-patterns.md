# Gemini Prompt Patterns Reference

## Effective Prompt Structure for Large Context

Gemini processes large context most reliably when prompts are structured with explicit enumeration. Free-form questions on a 1M-token codebase tend to produce generic results.

### Code Review Template
```bash
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Perform a focused code review. Return findings as a numbered list, each with:
   - File and line reference
   - Severity (Critical/High/Medium/Low)
   - Issue description
   - Suggested fix

   Focus areas:
   1. Security vulnerabilities (OWASP Top 10)
   2. Performance bottlenecks
   3. Error handling gaps
   4. Untested edge cases"
```

### Architecture Review Template
```bash
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Review this architectural plan. Structure your response as:
   RISKS: [list with severity]
   GAPS: [missing components or integrations]
   ALTERNATIVES: [2-3 alternative approaches with trade-offs]
   VERDICT: [go/no-go with conditions]"
```

### Codebase Onboarding Template
```bash
gemini -m gemini-3-pro-preview --approval-mode yolo \
  "Analyze this codebase and produce an onboarding guide:
   1. High-level architecture (components and their responsibilities)
   2. Key design patterns used
   3. Data flow for the main use case
   4. Known technical debt or TODO items
   5. How to run and test locally"
```

## Multi-Directory Analysis

```bash
gemini -m gemini-3-pro-preview --approval-mode yolo \
  --include-directories /path/to/backend \
  --include-directories /path/to/frontend \
  "Analyze cross-service dependencies and API contracts"
```

## Timeout Safety Patterns

```bash
# 5-minute timeout (most tasks)
timeout 300 gemini -m gemini-3-pro-preview --approval-mode yolo "..."

# 10-minute timeout (full codebase analysis)
timeout 600 gemini -m gemini-3-pro-preview --approval-mode yolo "..."
```

## Hung Process Recovery

```bash
# Detect hung process
ps aux | grep -E "gemini.*gemini-[23]" | grep -v grep
# Hung = 20+ min runtime, 0% CPU, state 'S', no network connections

# Check network activity (0 = hung)
lsof -p <PID> 2>/dev/null | grep -E "(TCP|ESTABLISHED)" | wc -l

# Kill and restart
pkill -9 -f "gemini.*gemini-3-pro-preview"
# Then re-run with --approval-mode yolo
```
