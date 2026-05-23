# Memory Protocol Skill

Gives any AI agent a persistent, structured memory using a single Markdown file (`agent-memory.md`). Defines when to read memory, how to write new entries, rules for keeping it clean, and a `/dream` consolidation procedure for when the file grows too large.

## Purpose

Long-running agents lose context between sessions. This skill solves that by:

- Reading memory before answering domain-specific questions
- Writing structured entries after significant tasks
- Replacing stale entries instead of appending duplicates
- Consolidating the file when it exceeds 200 lines via `/dream`

## When to Use This Skill

Activate when the agent:

- Receives a thematic question ("how does X work in this project?")
- Completes a significant task (new feature, debug session, config change)
- Is asked to remember something
- Encounters `/dream` command

**Activation keywords**: "remember", "what do you know about", "update memory", "/dream", any domain-specific question the agent might already know the answer to

## Memory File Location

Default path (adapt to your vault/project structure):
```
/data/obsidian-vault/ProjectName/agent-memory.md
```

## Entry Format

```markdown
### YYYY-MM-DD - Title
- Scope: user | project | session | team
- Content: ...
- Source: observation
- Expires: permanent
```

## The /dream Command

When `agent-memory.md` exceeds **200 lines**:

1. Read the full file
2. Group entries by topic, remove outdated duplicates
3. Save a snapshot of the old version to `Memory/dream-YYYY-MM-DD.md`
4. Write a condensed `agent-memory.md` (target: 50–70 lines)

This prevents context window bloat without losing historical data.

## Rules

- **Replace, don't append**: If a newer fact supersedes an old entry on the same topic, edit the file
- **Never store**: API keys, tokens, passwords, PII
- **Be concrete**: Entries should be actionable in a future session, not vague notes
