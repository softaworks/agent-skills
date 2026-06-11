# Onboarding Guide — agent-toolkit

> Generated from knowledge-graph analysis on 2026-05-31.

## Project Overview

**agent-toolkit** is an opinionated collection of reusable skills, agents, and slash commands for Claude Code and other AI coding agents. It provides packaged instructions and scripts that extend agent capabilities across development, documentation, planning, communication, security review, and professional workflows.

| Field | Value |
|---|---|
| Languages | Markdown, Python, YAML, Shell, TypeScript, JSON, CSS, SQL |
| Frameworks | GitHub Actions |
| Distribution | `npx skills add softaworks/agent-toolkit` |
| Plugin registry | `.claude-plugin/marketplace.json` |

The toolkit contains **61 skills**, **7 agent definitions**, and **7 slash commands**, all packaged to the [Agent Skills](https://agentskills.io/) format and installable individually or as a full marketplace.

---

## Architecture Layers

The project is organized into 7 logical layers:

### 1. Skills Library (`skills/`)

The core of the toolkit. 61 packaged agent skills organized by topic, each in its own subdirectory. Skills span:

- **Development**: `code-review`, `api-design`, `docker-and-containers`, `git-workflow`, `monorepo-workspace`, `dependency-updater`, `testing-strategy`, `security-review`
- **Frontend**: `react-dev`, `react-useeffect`, `design-system-starter`, `mui`, `mermaid-diagrams`, `draw-io`, `excalidraw`, `marp-slide`, `c4-architecture`
- **AI Tools**: `codex`, `gemini`, `perplexity`
- **Communication & Docs**: `crafting-effective-readmes`, `writing-clearly-and-concisely`, `professional-communication`, `feedback-mastery`, `humanizer`, `jira`
- **Planning**: `project-manager`, `requirements-clarity`, `qa-test-planner`, `session-handoff`, `lesson-learned`, `ship-learn-next`
- **Security (NIST 800-61r3)**: `nist-800-61r3-incident-coordinator`, `nist-800-61r3-gap-analyzer`, `nist-800-61r3-maturity-scorer`, `nist-800-61r3-policy-reviewer`, `nist-800-61r3-after-action-reviewer`, `nist-800-61r3-csf-mapper`, `nist-800-61r3-recommendation-auditor`
- **Tooling**: `plugin-forge`, `skill-creator`, `command-creator`, `commit-work`, `agent-md-refactor`
- **Content**: `meme-factory`, `domain-name-brainstormer`, `web-to-markdown`, `presentation-to-audience`, `game-changing-features`

### 2. Agent Definitions (`agents/`)

7 specialized agent definitions for focused, long-running tasks. Each is a markdown system-prompt file:

| Agent | Purpose |
|---|---|
| `general-purpose.md` | General-purpose task agent |
| `ui-ux-designer.md` | UI/UX design critique and wireframing |
| `codebase-pattern-finder.md` | Deep static analysis and pattern detection |
| `mermaid-diagram-specialist.md` | Automated Mermaid diagram generation |
| `communication-excellence-coach.md` | Professional communication coaching |
| `ascii-ui-mockup-generator.md` | ASCII-art UI prototyping |
| `nist-800-61r3-ir-reviewer.md` | Incident response review against NIST 800-61r3 |

### 3. Slash Commands (`commands/`)

7 workflow slash commands for common recurring tasks:

| Command | Purpose |
|---|---|
| `sync-branch.md` | Keep feature branches current with main |
| `codex-plan.md` | Structured implementation planning via GPT |
| `compose-email.md` | Professional email drafting |
| `explain-changes-mental-model.md` | Build a mental model of a diff or PR |
| `explain-pr-changes.md` | Summarize PR changes for reviewers |
| `viral-tweet.md` | Generate engaging tech tweets |
| `sync-skills-readme.md` | Regenerate the skills table in README.md |

### 4. CI/CD Automation (`.github/workflows/`)

4 GitHub Actions workflows maintaining the toolkit automatically:

| Workflow | Purpose |
|---|---|
| `main.yaml` | CI validation on PRs (tests, lint, build checks) |
| `auto-bump.yaml` | Automatic semantic version bump on release |
| `sync-gepetto.yaml` | Sync `gepetto` skill from its upstream source |
| `sync-datadog-cli.yaml` | Sync `datadog-cli` skill from its upstream source |

### 5. Build Tooling (`scripts/`)

2 Python scripts for packaging and distribution:

| Script | Purpose |
|---|---|
| `build_plugins.py` | Packages all skills/agents/commands into `.tgz` bundles for the marketplace |
| `bump_version.py` | Updates semantic version numbers across plugin configuration files |

### 6. Plugin Configuration (`.claude-plugin/`, `.claude/`)

Claude Code-specific wiring:

| File | Purpose |
|---|---|
| `.claude-plugin/marketplace.json` | Central registry: all 56 plugins listed with metadata for `npx`/`/plugin` installation |
| `.claude/commands/add-skill.md` | Internal Claude command to scaffold a new skill into the repo |
| `.claude/commands/sync-skills-readme.md` | Internal Claude command to regenerate the README skills table |

### 7. Project Documentation (root level)

Root-level documentation and templates:

| File | Purpose |
|---|---|
| `README.md` | Main project README with installation instructions and skill catalog |
| `CONTRIBUTING.md` | How to add new skills, naming conventions, submission process |
| `AGENTS.md` | Agent-level instructions for Claude Code working in this repo |
| `CLAUDE.md` | Claude Code project configuration and conventions |
| `error-handling-stub-template.md` | Template for consistent error handling in skills |
| `Mindset-Navigation-Philosophy-template.md` | Philosophical template for skill mindset sections |
| `NEVER-list-template.md` | Template defining hard constraints in skill instructions |
| `references-directory-convention.md` | Convention doc for organizing skill reference files |
| `README-policy.md` | Policy for which skills require a human-facing README |

---

## Key Concepts

### Skill Structure

Every skill follows a consistent 3-part layout:

```
skills/<skill-name>/
  SKILL.md              # Agent instructions (required)
  README.md             # Human documentation (optional, see README-policy.md)
  references/           # Supporting reference material (optional)
    *.md                # Referenced by SKILL.md at runtime
  scripts/              # Executable backing scripts (optional)
    *.py / *.sh
  assets/               # Static assets like templates, CSS (optional)
  templates/            # Reusable code/config templates (optional)
```

The `SKILL.md` is the authoritative file — it is the system prompt the agent receives. `README.md` is for humans. `references/` files are loaded into context by the skill's workflow steps.

### Plugin Format

Each skill, agent, and command is an independent installable plugin. The plugin contract is defined in `.claude-plugin/marketplace.json`. Each entry specifies:
- `id` — unique plugin identifier
- `type` — `skill`, `agent`, or `command`
- `path` — path to the plugin directory
- `name`, `description`, `tags` — marketplace metadata

### Agent Skills vs Slash Commands vs Agents

| Type | What it is | Where it lives | How it's invoked |
|---|---|---|---|
| **Skill** | A reusable task workflow with agent instructions | `skills/<name>/SKILL.md` | `/skill-name` or installed via marketplace |
| **Command** | A focused one-shot workflow shortcut | `commands/<name>.md` | `/<command-name>` |
| **Agent** | A specialized sub-agent for autonomous tasks | `agents/<name>.md` | Invoked by the AI as a subagent |

### NIST 800-61r3 Security Cluster

7 interrelated security skills implement the full NIST 800-61r3 incident response lifecycle. They share a common reference file (`skills/nist-800-61r3-shared/references/csf-element-registry.md`) and are designed to be used in sequence:
1. `nist-800-61r3-incident-coordinator` — Live incident coordination
2. `nist-800-61r3-gap-analyzer` — Identify capability gaps
3. `nist-800-61r3-maturity-scorer` — Score program maturity
4. `nist-800-61r3-policy-reviewer` — Review IR policies
5. `nist-800-61r3-after-action-reviewer` — Post-incident review
6. `nist-800-61r3-csf-mapper` — Map controls to CSF
7. `nist-800-61r3-recommendation-auditor` — Audit recommendations

### Externally-Sourced Skills

Two skills (`gepetto`, `datadog-cli`) are synchronized from external upstream repositories via dedicated GitHub Actions workflows. Do not edit these directly — changes will be overwritten on the next sync.

---

## Guided Tour

Follow these 10 steps to understand the project from the outside in:

### Step 1 — Project Overview
**Read:** `README.md`

Start with the main README to understand what Softaworks Agent Skills is: a curated collection of reusable skills, agents, and slash commands that extend Claude Code and other AI coding assistants. This is the entry point for understanding what's available and how to install it.

### Step 2 — Plugin Marketplace Registry
**Read:** `.claude-plugin/marketplace.json`

The marketplace.json file is the central registry that powers the `/plugin marketplace` command. It lists all 43 skills, 6 agents, and 7 commands with their metadata, enabling one-command installation. Understand this to see the full catalog at a glance.

### Step 3 — Agent Configuration
**Read:** `AGENTS.md`, `CLAUDE.md`

These files define project-level AI agent instructions and conventions. They govern how Claude Code behaves when working in this repository and set the development philosophy for skill creation.

### Step 4 — How Skills Are Structured
**Read:** `skills/session-handoff/SKILL.md`, `skills/session-handoff/README.md`, `skills/session-handoff/scripts/create_handoff.py`

Each skill follows the Agent Skills format: a SKILL.md with agent instructions, an optional README.md for humans, and supporting scripts or references. The `session-handoff` skill is an excellent exemplar — it includes both rich documentation and 4 executable Python scripts showing the complete pattern.

### Step 5 — Core Skill Scripts: Session Handoff
**Read:** `skills/session-handoff/scripts/create_handoff.py`, `skills/session-handoff/scripts/validate_handoff.py`, `skills/session-handoff/scripts/list_handoffs.py`, `skills/session-handoff/scripts/check_staleness.py`

These 4 Python scripts demonstrate the pattern for skills with executable backing code. They provide a full lifecycle for managing AI session context: create, list, validate, and check staleness. Read these to understand how scripts are wired into skill workflows.

### Step 6 — Agent Definitions
**Read:** `agents/general-purpose.md`, `agents/codebase-pattern-finder.md`, `agents/mermaid-diagram-specialist.md`, `agents/nist-800-61r3-ir-reviewer.md`

The `agents/` directory holds specialized sub-agent definitions for focused tasks. Each is a markdown file with system prompt instructions. These differ from skills in that they are invoked autonomously by the AI, not by the user.

### Step 7 — Slash Commands
**Read:** `commands/sync-branch.md`, `commands/codex-plan.md`, `commands/compose-email.md`, `commands/explain-changes-mental-model.md`

The `commands/` directory provides workflow automation as slash commands. Browse a few to understand how they differ from skills: commands are shorter, more focused, and invoked directly with `/command-name` syntax.

### Step 8 — Build and Distribution Tooling
**Read:** `scripts/build_plugins.py`, `scripts/bump_version.py`

The `scripts/` directory contains the Python tools that package and distribute this toolkit. `build_plugins.py` creates the `.tgz` bundles for the marketplace; `bump_version.py` handles semantic versioning. These are the CI/CD backbone.

### Step 9 — CI/CD Automation
**Read:** `.github/workflows/main.yaml`, `.github/workflows/auto-bump.yaml`, `.github/workflows/sync-gepetto.yaml`, `.github/workflows/sync-datadog-cli.yaml`

GitHub Actions workflows automate maintenance: CI validation on PRs, automatic version bumping on release, and synchronization of the two upstream-sourced skills.

### Step 10 — Contributing and Extending
**Read:** `CONTRIBUTING.md`, `skills/skill-creator/SKILL.md`, `skills/plugin-forge/SKILL.md`, `.claude/commands/add-skill.md`

`CONTRIBUTING.md` explains how to add new skills. The `skill-creator` and `plugin-forge` skills provide AI-assisted scaffolding. The `add-skill` Claude command automates the setup of a new skill directory within this repo.

---

## File Map

### Build Tooling

| File | Summary |
|---|---|
| `scripts/build_plugins.py` | Packages all skills, agents, and commands into distributable plugin bundles for the marketplace |
| `scripts/bump_version.py` | Updates semantic version numbers across plugin configuration files |

### Plugin Configuration

| File | Summary |
|---|---|
| `.claude-plugin/marketplace.json` | Central plugin registry — all 56 plugins listed with metadata for installation |
| `.claude/commands/add-skill.md` | Internal Claude command to scaffold a new skill into the repo |
| `.claude/commands/sync-skills-readme.md` | Regenerates the skills table in README.md |

### CI/CD Pipelines

| File | Summary |
|---|---|
| `.github/workflows/main.yaml` | Main CI/CD workflow — tests, validation, build checks on PRs |
| `.github/workflows/auto-bump.yaml` | Automatic semantic version bump on release |
| `.github/workflows/sync-gepetto.yaml` | Synchronizes `gepetto` skill from upstream |
| `.github/workflows/sync-datadog-cli.yaml` | Synchronizes `datadog-cli` skill from upstream |

### Skills with Executable Scripts

| File | Summary |
|---|---|
| `skills/session-handoff/scripts/create_handoff.py` | Creates session handoff documents with git context and project state |
| `skills/session-handoff/scripts/validate_handoff.py` | Validates handoff document quality and completeness |
| `skills/session-handoff/scripts/list_handoffs.py` | Lists all handoff documents with metadata and completion status |
| `skills/session-handoff/scripts/check_staleness.py` | Checks whether handoff documents are stale based on git history |
| `skills/plugin-forge/scripts/create_plugin.py` | Scaffolds new plugin directories from templates |
| `skills/plugin-forge/scripts/bump_version.py` | Bumps version numbers in plugin configuration files |
| `skills/daily-meeting-update/scripts/claude_digest.py` | Generates daily meeting digests from Claude Code session activity |
| `skills/meme-factory/scripts/meme_generator.py` | Generates meme images by combining templates with text overlays |
| `skills/draw-io/scripts/convert-drawio-to-png.sh` | Converts draw.io diagrams to PNG via the draw.io CLI |
| `skills/draw-io/scripts/find_aws_icon.py` | Searches and retrieves AWS service icons for architecture diagrams |
| `skills/dependency-updater/scripts/check-tool.sh` | Checks if required dependency management tool is installed |
| `skills/dependency-updater/scripts/run-taze.sh` | Runs `taze` to update JavaScript/TypeScript dependencies |
| `skills/qa-test-planner/scripts/create_bug_report.sh` | Generates formatted bug report files |
| `skills/qa-test-planner/scripts/generate_test_cases.sh` | Generates test case files from a template |

### Skills with Templates / Assets

| File | Summary |
|---|---|
| `skills/design-system-starter/templates/component-template.tsx` | React TypeScript component template for new UI components |
| `skills/design-system-starter/templates/design-tokens-template.json` | Design token configuration template |
| `skills/database-schema-designer/assets/templates/migration-template.sql` | SQL migration template for database schema changes |
| `skills/marp-slide/assets/theme-*.css` | 7 CSS themes for Marp slide presentations |

---

## Complexity Hotspots

These files have high complexity and deserve careful review before editing:

### High-Complexity Skill Definitions

| File | Why it's complex |
|---|---|
| `skills/api-design/SKILL.md` | Comprehensive API design workflow with multi-phase analysis |
| `skills/c4-architecture/references/c4-syntax.md` | Full C4 model syntax reference with many diagram types |
| `skills/c4-architecture/references/advanced-patterns.md` | Advanced C4 patterns requiring architectural knowledge |
| `skills/command-creator/references/best-practices.md` | Extensive command design guidelines |
| `skills/crafting-effective-readmes/references/art-of-readme.md` | Long-form essay on README philosophy |
| `skills/mermaid-diagrams/SKILL.md` | Multi-diagram-type generation with complex decision trees |
| `skills/react-dev/SKILL.md` | React 19 patterns, hooks, server components — broad scope |
| `skills/gepetto/SKILL.md` | Multi-phase research protocol with external review processes |
| `skills/session-handoff/scripts/check_staleness.py` | Complex git-history-based staleness calculation (385 lines) |
| `skills/session-handoff/scripts/create_handoff.py` | Full handoff document generation with git introspection (385 lines) |
| `skills/session-handoff/scripts/validate_handoff.py` | Multi-factor quality scoring with secret scanning (316 lines) |

### High-Complexity Agent Definitions

| File | Why it's complex |
|---|---|
| `agents/mermaid-diagram-specialist.md` | Covers all Mermaid diagram types with detailed syntax guidance |
| `agents/ui-ux-designer.md` | Broad UX scope: research, wireframing, design critique |

### High-Complexity Configuration

| File | Why it's complex |
|---|---|
| `.claude-plugin/marketplace.json` | 926 lines — the full plugin catalog with metadata for 56 plugins |

---

## Getting Started

### Install the full toolkit

```bash
npx skills add softaworks/agent-toolkit
```

### Install as a Claude Code plugin marketplace

```bash
/plugin marketplace add softaworks/agent-toolkit
/plugin
```

Then browse the Marketplaces tab and install individual plugins.

### Install a specific skill

```bash
/plugin install session-handoff@agent-toolkit
/plugin install codex@agent-toolkit
/plugin install react-dev@agent-toolkit
```

### Contributing a new skill

1. Read `CONTRIBUTING.md` for naming conventions and structure requirements
2. Run the `skill-creator` skill (`/skill-creator`) to scaffold the new skill
3. Or use the internal `.claude/commands/add-skill.md` command
4. Follow the layout in `skills/session-handoff/` as the reference implementation
5. Add an entry to `.claude-plugin/marketplace.json`
6. Open a PR — CI will validate the structure

### Development workflow

```bash
# Build all plugin bundles
python3 scripts/build_plugins.py

# Bump version
python3 scripts/bump_version.py

# Regenerate the README skills table
/sync-skills-readme
```
