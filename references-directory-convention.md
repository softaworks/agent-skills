# References Directory Convention

## Purpose

The `references/` directory holds supplementary content that a skill loads on demand rather than on every invocation. It exists to keep `SKILL.md` focused and concise while still making deep reference material available when needed.

## When to Use references/

Create a `references/` directory when:

- The skill's `SKILL.md` would exceed 300 lines if all content were inlined.
- Content is only needed for a subset of task types (e.g., a lookup table used only during threat enrichment, not during triage).
- Reference material is stable and unlikely to change with every skill revision (e.g., field mappings, taxonomy tables, error code lists).

Do NOT create a `references/` file just to be tidy. If the content is always needed for the skill to work correctly, it belongs in `SKILL.md` directly.

## File Naming

- Use kebab-case for all reference file names.
- Use the `.md` extension.
- Name files after their content, not their audience.

Good:

```
references/field-mapping-table.md
references/severity-levels.md
references/alert-triage-workflow.md
```

Bad:

```
references/ref1.md
references/Agent_Reference.md
references/extra_stuff.md
```

## Writing Loading Triggers

Loading triggers are instructions inside `SKILL.md` that tell the agent when to read a specific reference file. Every loading trigger must be:

1. Clearly marked as mandatory or conditional.
2. Tied to a specific task or condition — never vague.
3. Placed near the task description it governs, not at the bottom of the file.

### Mandatory Trigger Format

Use this format when the reference must always be read before a specific task:

```
MANDATORY — read references/field-mapping-table.md before proceeding with alert normalization.
```

### Conditional Trigger Format

Use this format when the reference is only needed under certain conditions:

```
If the alert source is "Crowdstrike", read references/crowdstrike-field-map.md before mapping fields.
```

Do not write triggers that say "read this for more information" — that is browsing guidance, not an execution instruction.

## Writing "Do NOT Load" Guidance

When a reference file exists but should not be loaded outside its specific context, say so explicitly in `SKILL.md`:

```
Do NOT load references/full-taxonomy-table.md during triage. Only load it during classification tasks.
```

This prevents the agent from loading reference files speculatively or out of order.

## Always-Loaded vs On-Demand Content

| Content Type | Where It Lives |
|---|---|
| Skill purpose and scope | `SKILL.md` |
| Core workflow steps | `SKILL.md` |
| Output format requirements | `SKILL.md` |
| Key rules and constraints | `SKILL.md` |
| Lookup tables (large) | `references/` |
| Field mapping tables | `references/` |
| Taxonomy or classification lists | `references/` |
| Sub-workflows for specific task types | `references/` |
| Error code reference tables | `references/` |

The rule: if the agent cannot start a task correctly without reading it, it goes in `SKILL.md`. If the agent only needs it mid-task for a specific subtask, it goes in `references/`.

## Good vs Bad Progressive Disclosure Structure

### Bad — Everything Inlined

```
SKILL.md (620 lines)
  - Skill purpose (10 lines)
  - Core workflow (40 lines)
  - Full ATT&CK technique list (200 lines)
  - All severity mappings for 8 platforms (180 lines)
  - Error handling for 60 edge cases (190 lines)
```

The agent reads all 620 lines on every invocation, even when it only needs the core workflow.

### Good — Progressive Disclosure

```
SKILL.md (90 lines)
  - Skill purpose (10 lines)
  - Core workflow (40 lines)
  - Loading triggers pointing to references/ (5 lines)
  - Output format (15 lines)
  - Key rules (20 lines)

references/
  attack-technique-list.md     (200 lines — loaded during classification)
  severity-platform-map.md     (180 lines — loaded during severity scoring)
  edge-case-error-handling.md  (190 lines — loaded when errors are encountered)
```

The agent reads `SKILL.md` every time, then reads only the reference files relevant to the current task.

## Directory Layout Example

```
my-skill/
  SKILL.md
  references/
    field-mapping-table.md
    severity-levels.md
    alert-triage-workflow.md
```

Reference files have no required internal structure, but they should start with a one-line purpose statement so the agent can confirm it loaded the right file.
