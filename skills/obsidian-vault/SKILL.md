---
name: obsidian-vault
description: |
  Use this skill before any read or write operation on an Obsidian vault.
  Defines the two-layer architecture (Raw vs Wiki), frontmatter rules,
  search strategy, and the three-stage pipeline for vault maintenance.
triggers:
  - save to obsidian
  - find in notes
  - search the vault
  - add to vault
  - organize notes
  - update index
---

# Obsidian Vault Architecture

## Two Layers — Strict Separation

### Raw Layer (your write zone)

Folders: `Inbox/`, `Reports/`, `Тренды/`, `Sessions/`, `Knowledge/`

- All files must have `type: raw_material` in frontmatter
- No horizontal cross-links between Raw files
- Source of truth for input data

### Wiki Layer (read-only for most agents)

Folder: `Wiki/`

- Contains atomic synthesis notes (`type: summary`)
- The semantic knowledge base — always search here first
- Written **only** by the Wiki Compiler agent (`/compile_wiki`)
- **NEVER write to `Wiki/` directly** — if asked, redirect to Wiki Compiler

---

## Search Strategy

Always search Wiki first, then Raw if needed:

```bash
# Priority 1 — semantic layer
grep -ril "TOPIC" /data/obsidian-vault/ProjectName/Wiki --include="*.md"

# Priority 2 — raw sources (only if Wiki insufficient)
grep -ril "TOPIC" /data/obsidian-vault/ProjectName/Reports --include="*.md"
```

---

## Frontmatter (Raw Layer)

Every Raw file must have:

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

**Tag rules:**
- Use underscores, no spaces: `skin_care` not `skin care`
- No pure numbers: `year2026` not `2026`
- 3–7 tags per file
- Check `_TEMPLATE.md` Master Tag Dictionary before creating new tags
- Add new tags to `_TEMPLATE.md` when you create them

---

## Three-Stage Pipeline

| Stage | Responsible | Scope |
|-------|------------|-------|
| 1. Librarian | `agents/obsidian-librarian.md` | Inbox/ + Raw folders: frontmatter, tags, routing |
| 2. Wiki Compiler | `agents/compiler-agent.md` | Wiki/: synthesize → Sapling notes |
| 3. Semantic Linker | `src/semantic_linker.ts` | Wiki/ only: horizontal semantic links |

**Rule**: each stage works only in its own zone.

---

## File Routing (from Inbox)

- Session notes, chat logs → `Sessions/`
- YouTube research, media transcripts → `Тренды/`
- Reports, analysis, articles → `Reports/`
- Instructions, guides, setup docs → `Knowledge/`

After routing, update `_INDEX.md`:
```
- [[FileName]] — brief description (date, main tags)
```

---

## Absolute Prohibitions

- ❌ Never create files in `Wiki/` — that's Wiki Compiler's job
- ❌ Never use `type: summary` — only `raw_material`
- ❌ Never add cross-links between Raw files
- ❌ Never modify tags of already-tagged files
- ❌ Never delete files — move to `Archive/` instead
