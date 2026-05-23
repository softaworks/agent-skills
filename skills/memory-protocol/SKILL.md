---
name: memory-protocol
description: |
  Use this skill before thematic answers and after significant tasks.
  Defines how to read, write, and consolidate persistent agent memory
  stored in a structured Markdown file.
triggers:
  - remember
  - what do you know about
  - update memory
  - /dream
---

# Memory Protocol

## Read Before Answering

Before any thematic answer — check if the topic is already known:

```bash
cat /data/obsidian-vault/ProjectName/agent-memory.md
```

For deep search across the full vault:

```bash
grep -ril "TOPIC" /data/obsidian-vault/ --include="*.md"
```

---

## Write After Significant Tasks

After any significant task — update `agent-memory.md` with new facts.

**Entry format:**

```markdown
### YYYY-MM-DD - Title
- Scope: user | project | session | team
- Content: ...
- Source: observation
- Expires: permanent
```

---

## Rules

- **Replace stale entries** on the same topic — don't accumulate duplicates
- **Never save**: API keys, tokens, passwords, PII
- Entries must be concrete and actionable in a future session

---

## /dream — Consolidation

Run when `agent-memory.md` exceeds **200 lines**:

1. Read the full `agent-memory.md`
2. Group entries by topic, remove outdated and duplicate facts
3. Save snapshot of the old version → `Memory/dream-YYYY-MM-DD.md`
4. Write condensed `agent-memory.md` (target: 50–70 lines)
