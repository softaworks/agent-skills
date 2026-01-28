---
description: Sync root README.md with current skills inventory from skills/ directory
---

# Sync Skills README

Update the root README.md "Available Skills" table with all skills currently in the `skills/` directory. This command scans skills, reads their metadata, categorizes them, and regenerates the table.

## Workflow

### 1. Scan Skills Directory

Use Bash to list all skill directories:

```bash
ls -1 skills/
```

For each skill directory found, proceed to step 2.

### 2. Extract Skill Metadata

For each skill, read the SKILL.md frontmatter to extract:
- `name:` field (skill identifier)
- `description:` field (what the skill does)

Use the Read tool to read `skills/[skill-name]/SKILL.md` and extract the YAML frontmatter between the `---` markers.

**Example:**
```yaml
---
name: codex
description: Use when the user asks to run Codex CLI for code analysis...
---
```

Extract both fields for table generation.

### 3. Categorize Skills

Assign each skill to a category based on its purpose. Use this mapping:

| Category | Emoji | Keywords in name/description |
|----------|-------|------------------------------|
| AI Tools | 🤖 | codex, gemini, perplexity, ai, llm, model |
| Meta | 🔮 | command-creator, plugin-forge, plugin, command |
| Documentation | 📝 | docs, documentation, handoff, requirements, diagram, mermaid, draw, excalidraw, marp, slide, c4-architecture |
| Development | 🛠️ | session, handoff, entropy, development, workflow, database, dependency |
| Design & Frontend | 🎨 | design, frontend, ui, openapi, typescript, system |
| Utilities | 🔧 | domain, meme, web-to-markdown, utility, tool, datadog |
| Planning | 🎯 | plan, planning, spec, forge, gepetto, requirements, clarity, game-changing, features |
| Professional | 👔 | professional, communication, career, soft-skill, feedback, conversation |
| Testing | 🧪 | test, testing, qa, quality |
| Git | 📦 | commit, git, branch, pr, pull-request |

**Categorization logic:**
1. Check the skill name and description (case-insensitive)
2. Match against keywords in the table above
3. Assign to the first matching category
4. If no match, default to "Utilities" (🔧)

### 4. Generate Compact Table

Create a markdown table with this exact format:

```markdown
## 📚 Available Skills

| Category | Skill | Description |
|----------|-------|-------------|
| 🤖 AI Tools | [codex](skills/codex/README.md) | Advanced code analysis with GPT-5.2 |
| 🤖 AI Tools | [gemini](skills/gemini/README.md) | Large-scale review (200k+ context) |
...
```

**Table structure:**
- Column 1: Category emoji + name (e.g., "🤖 AI Tools")
- Column 2: Skill name as markdown link to its README
- Column 3: Short description (max ~50 chars, extracted from SKILL.md description field)

**Sorting:**
- Group by category (AI Tools first, then Meta, Documentation, Design & Frontend, Development, Planning, Professional, Testing, Git, Utilities last)
- Within each category, sort skills alphabetically by name

**Description shortening:**
- If description is longer than 50 characters, create a shortened version
- Keep it concise and action-oriented
- Examples:
  - "Use when the user asks to run Codex CLI for code analysis, refactoring, or automated editing" → "Advanced code analysis with GPT-5.2"
  - "Create comprehensive API handoff documentation for frontend developers after backend implementation" → "API handoff docs for frontend"

### 5. Update README.md

Use the Edit tool to replace the "Available Skills" section in the root README.md.

**Find and replace:**
1. Locate the section starting with `## 📚 Available Skills`
2. Find the end of the table (marked by the next `---` separator or next `##` heading)
3. Replace everything between those markers with the newly generated table

**Important:**
- Preserve the `---` separator after the table
- Do NOT modify other sections (Quick Navigation, Installation, etc.)
- Only replace the table content, keep the section heading

### 6. Report Results

After updating README.md, report to the user:

```
✅ README.md updated successfully

📊 Summary:
- Total skills: [count]
- Categories: [list of categories with counts]
- Skills added/updated: [list if any changes detected]

The Available Skills table in README.md now reflects all skills in the skills/ directory.
```

## Error Handling

**If a skill directory doesn't have SKILL.md:**
- Skip that skill
- Warn the user: "⚠️ Skipped [skill-name]: No SKILL.md found"

**If SKILL.md doesn't have required frontmatter:**
- Skip that skill
- Warn: "⚠️ Skipped [skill-name]: Missing name or description in frontmatter"

**If README.md section not found:**
- Error and stop: "❌ Could not find '## 📚 Available Skills' section in README.md"

## Tools to Use

- **Bash** - List skills directory
- **Read** - Read SKILL.md files for metadata extraction
- **Edit** - Update README.md with new table
- **DO NOT use Grep** - Read files directly for accurate frontmatter parsing

## Success Criteria

- All valid skills from skills/ directory appear in the table
- Skills are correctly categorized with appropriate emojis
- Table maintains compact format (3 columns)
- Descriptions are concise and readable
- README.md is updated without breaking other sections
