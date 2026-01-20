# Agent Skills

A curated collection of skills for AI coding agents. Skills are packaged instructions and scripts that extend agent capabilities across development, documentation, planning, and professional workflows.

Skills follow the [Agent Skills](https://agentskills.io/) format.

---

## 🧭 Quick Navigation

**[📚 Available Skills](#-available-skills)** • **[🤖 Agents & Commands](#-agents--commands)** • **[🚀 Installation](#-installation)** • **[📖 Skill Structure](#-skill-structure)** • **[🤝 Contributing](#-contributing)** • **[📄 License](#-license)** • **[🔗 Links](#-links)**

---

## 📚 Available Skills

| Category | Skill | Description |
|----------|-------|-------------|
| 🤖 AI Tools | [codex](skills/codex/README.md) | Advanced code analysis with GPT-5.2 |
| 🤖 AI Tools | [gemini](skills/gemini/README.md) | Large-scale review (200k+ context) |
| 🤖 AI Tools | [perplexity](skills/perplexity/README.md) | Web search & research |
| 🔮 Meta | [agent-md-refactor](skills/agent-md-refactor/README.md) | Refactor bloated agent instruction files |
| 🔮 Meta | [command-creator](skills/command-creator/README.md) | Create Claude Code slash commands |
| 🔮 Meta | [plugin-forge](skills/plugin-forge/README.md) | Build Claude Code plugins & manifests |
| 🔮 Meta | [skill-judge](skills/skill-judge/README.md) | Evaluate skill design quality |
| 📝 Documentation | [backend-to-frontend-handoff-docs](skills/backend-to-frontend-handoff-docs/README.md) | API handoff docs for frontend |
| 📝 Documentation | [c4-architecture](skills/c4-architecture/README.md) | C4 architecture diagrams with Mermaid |
| 📝 Documentation | [crafting-effective-readmes](skills/crafting-effective-readmes/README.md) | Write effective README files |
| 📝 Documentation | [draw-io](skills/draw-io/README.md) | Create & edit draw.io diagrams |
| 📝 Documentation | [excalidraw](skills/excalidraw/README.md) | Work with Excalidraw diagrams |
| 📝 Documentation | [frontend-to-backend-requirements](skills/frontend-to-backend-requirements/README.md) | Document API requirements |
| 📝 Documentation | [marp-slide](skills/marp-slide/README.md) | Professional presentation slides |
| 📝 Documentation | [mermaid-diagrams](skills/mermaid-diagrams/README.md) | Software diagrams with Mermaid |
| 📝 Documentation | [writing-clearly-and-concisely](skills/writing-clearly-and-concisely/README.md) | Clear, professional writing |
| 🎨 Design & Frontend | [design-system-starter](skills/design-system-starter/README.md) | Create design systems |
| 🎨 Design & Frontend | [mui](skills/mui/README.md) | Material-UI v7 patterns |
| 🎨 Design & Frontend | [openapi-to-typescript](skills/openapi-to-typescript/README.md) | Convert OpenAPI to TypeScript |
| 🎨 Design & Frontend | [react-dev](skills/react-dev/README.md) | Type-safe React 18-19 with TypeScript |
| 🛠️ Development | [database-schema-designer](skills/database-schema-designer/README.md) | Design robust database schemas |
| 🛠️ Development | [dependency-updater](skills/dependency-updater/README.md) | Smart dependency management |
| 🛠️ Development | [naming-analyzer](skills/naming-analyzer/README.md) | Suggest better variable/function names |
| 🛠️ Development | [reducing-entropy](skills/reducing-entropy/README.md) | Minimize codebase size |
| 🛠️ Development | [session-handoff](skills/session-handoff/README.md) | Seamless AI session transfers |
| 🎯 Planning | [game-changing-features](skills/game-changing-features/README.md) | Find 10x product opportunities |
| 🎯 Planning | [gepetto](skills/gepetto/README.md) | Detailed implementation planning |
| 🎯 Planning | [requirements-clarity](skills/requirements-clarity/README.md) | Clarify requirements before coding |
| 🎯 Planning | [ship-learn-next](skills/ship-learn-next/README.md) | Turn learning into actionable reps |
| 👔 Professional | [difficult-workplace-conversations](skills/difficult-workplace-conversations/README.md) | Navigate difficult conversations |
| 👔 Professional | [feedback-mastery](skills/feedback-mastery/README.md) | Deliver constructive feedback |
| 👔 Professional | [professional-communication](skills/professional-communication/README.md) | Technical communication guide |
| 🧪 Testing | [qa-test-planner](skills/qa-test-planner/README.md) | Comprehensive QA test planning |
| 📦 Git | [commit-work](skills/commit-work/README.md) | High-quality git commits |
| 🔧 Utilities | [datadog-cli](skills/datadog-cli/README.md) | Debug with Datadog logs & metrics |
| 🔧 Utilities | [domain-name-brainstormer](skills/domain-name-brainstormer/README.md) | Generate & check domain names |
| 🔧 Utilities | [humanizer](skills/humanizer/README.md) | Remove AI writing patterns |
| 🔧 Utilities | [meme-factory](skills/meme-factory/README.md) | Generate memes with API |
| 🔧 Utilities | [web-to-markdown](skills/web-to-markdown/README.md) | Convert webpages to Markdown |

---

## 🤖 Agents & Commands

> **Requires [Claude Code CLI](https://docs.anthropic.com/claude-code)** — These agents and commands are exclusive to Claude Code users.
>
> For full access, add the marketplace and install plugins:
> ```bash
> /plugin marketplace add softaworks/agent-skills
> /plugin install codex@agent-skills
> ```

### Agents

Specialized sub-agents that Claude Code can delegate tasks to:

| Agent | Description |
|-------|-------------|
| ascii-ui-mockup-generator | Visualize UI concepts through ASCII mockups |
| codebase-pattern-finder | Find similar implementations and patterns |
| communication-excellence-coach | Email refinement, tone calibration, roleplay |
| general-purpose | Default agent for complex multi-step tasks |
| mermaid-diagram-specialist | Create flowcharts, sequence diagrams, ERDs |
| ui-ux-designer | Research-backed UI/UX design feedback |

### Slash Commands

Reusable workflows invoked with `/command-name`:

| Command | Description |
|---------|-------------|
| `/codex-plan` | Create implementation plans using Codex 5.2 |
| `/compose-email` | Draft professional emails |
| `/explain-changes-mental-model` | Build mental model of code changes |
| `/explain-pr-changes` | Generate PR summaries |
| `/sync-branch` | Sync feature branch with main |
| `/sync-skills-readme` | Update README skills table |

---

## 🚀 Installation

### Quick Install (Recommended)

```bash
npx add-skill softaworks/agent-skills
```

This method works with multiple AI coding agents (Claude Code, Codex, Cursor, etc.)

### Register as Plugin Marketplace

Run the following command in Claude Code:

```bash
/plugin marketplace add softaworks/agent-skills
```

### Install Plugins

**Option 1: Via Browse UI**

1. Select **Browse and install plugins**
2. Select **agent-skills**
3. Select the plugin(s) you want to install
4. Select **Install now**

**Option 2: Direct Install**

```bash
# Install specific skill
/plugin install codex@agent-skills
/plugin install humanizer@agent-skills

# Install specific agent
/plugin install agent-codebase-pattern-finder@agent-skills

# Install specific command
/plugin install command-codex-plan@agent-skills
```

**Option 3: Ask the Agent**

Simply tell Claude Code:

> Please install Skills from github.com/softaworks/agent-skills

### Available Plugins

Each skill, agent, and command is an individual plugin that can be installed separately:

- **Skills** → See [Available Skills](#-available-skills) for the full list
- **Agents** → See [Agents](#agents) (install as `agent-<name>@agent-skills`)
- **Commands** → See [Slash Commands](#slash-commands) (install as `command-<name>@agent-skills`)

### Update Plugins

To update plugins to the latest version:

1. Run `/plugin` in Claude Code
2. Switch to **Marketplaces** tab
3. Select **agent-skills**
4. Choose **Update marketplace**

You can also **Enable auto-update** to get the latest versions automatically.

### Manual Installation

**For Claude Code (Manual)** — Skills only
```bash
cp -r skills/<skill-name> ~/.claude/skills/
```

**For claude.ai** — Skills only

Add skills to project knowledge or paste SKILL.md contents into the conversation.

---

## 📖 Skill Structure

Each skill contains:
- `SKILL.md` - Detailed instructions for the agent (with YAML frontmatter)
- `README.md` - User-friendly documentation with examples
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)

---

## 🤝 Contributing

Contributions are welcome! When adding new skills:

1. Follow the [Agent Skills](https://agentskills.io/) format
2. Include both `SKILL.md` (for agents) and `README.md` (for users)
3. Add YAML frontmatter to `SKILL.md` with `name:` and `description:` fields
4. Update this README.md with a link to your skill

---

## 📄 License

MIT

---

## 🔗 Links

- [Agent Skills Format](https://agentskills.io/)
- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [GitHub Repository](https://github.com/softaworks/agent-skills)
