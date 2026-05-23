# Obsidian Vault Skill

A two-layer knowledge architecture for Obsidian vaults used with AI agents. Enforces strict separation between raw input data and synthesized Wiki notes, preventing agents from accidentally writing to the semantic layer.

## Purpose

AI agents working with Obsidian tend to mix raw data and synthesized knowledge. This skill establishes:

- **Raw Layer** (`Reports/`, `Тренды/`, `Sessions/`, `Knowledge/`, `Inbox/`) — source material with `type: raw_material`
- **Wiki Layer** (`Wiki/`) — atomic synthesis notes with `type: summary`, written only by a dedicated Wiki Compiler step

## When to Use This Skill

Activate when the agent needs to:

- Search for information in the vault
- Save a note or report to the vault
- Process files from an Inbox folder
- Understand the vault architecture before writing any files

**Activation keywords**: "save to obsidian", "find in notes", "search the vault", "add to vault", "organize notes"

## Architecture

```
vault/
├── Wiki/          ← SEMANTIC LAYER — synthesis notes only. Read-only for most agents.
├── Reports/       ← Raw Layer: reports, articles, research
├── Тренды/        ← Raw Layer: trend analysis, YouTube transcripts
├── Sessions/      ← Raw Layer: session notes, AI chat logs
├── Knowledge/     ← Raw Layer: instructions, guides, setup docs
├── Inbox/         ← Raw Layer: incoming unprocessed files
├── Memory/        ← Agent memory snapshots
├── _INDEX.md      ← Master index, update after every file change
└── _TEMPLATE.md   ← Frontmatter template + Master Tag Dictionary
```

## Three-Stage Pipeline

For cron or manual vault maintenance:

| Stage | File | Scope |
|-------|------|-------|
| 1. Librarian | `agents/obsidian-librarian.md` | All folders except `Wiki/` — frontmatter, tags, routing |
| 2. Wiki Compiler | `agents/compiler-agent.md` | `Wiki/` — synthesize raw data into Sapling notes |
| 3. Semantic Linker | `src/semantic_linker.ts` | `Wiki/` only — horizontal semantic links |

## Frontmatter Format (Raw Layer)

```yaml
---
title: "Human readable title"
date: YYYY-MM-DD
category: cosmetology | psychology | business | development
tags: [tag1, tag2, tag_with_underscore]
type: raw_material
semantic_weights:
---
```

## Key Rules

- Wiki Layer is **read-only** for all agents except Wiki Compiler
- Only `type: raw_material` is written to Raw Layer
- Horizontal links exist **only** within Wiki Layer
- Raw files are isolated — no cross-links between Raw files
- Every file gets frontmatter; update `_INDEX.md` after any change
