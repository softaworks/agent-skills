---
name: plugin-forge
description: Create and manage Claude Code plugins — plugin.json manifests, marketplace.json registration, skills/commands/agents/hooks wiring, version bumping, and directory-source plugin troubleshooting. Use when building a new plugin, adding components to an existing plugin, diagnosing silent plugin load failures, or publishing to a marketplace.
---

# Plugin Forge

## Mindset

1. **The loader is picky about git.** Directory-source plugins must have a `.git` dir with at least one commit. A missing or empty repo causes a silent "source type not supported" failure — not an error you can see in the manifest or logs. Git first, always.
2. **Two manifests, one truth.** Version drift between `plugin.json` and `marketplace.json` causes install mismatches that are hard to diagnose. Treat them as a single atomic update.
3. **Agents don't hot-reload from marketplace.** Marketplace plugins load skills and commands on install; agent definitions only take effect after a session restart AND a `sudo cp` to `.claude/agents/`. The install command alone is not enough.
4. **Skills load lazily; size the SKILL.md for that.** Only the `description` field is read at startup. The full SKILL.md loads only when the skill triggers. Bloated SKILL.md files waste context on every activation, not just startup.
5. **Component paths resolve from plugin root, not from `.claude-plugin/`.** A common off-by-one: putting `commands/` inside `.claude-plugin/` instead of at the plugin root. The manifest only lives in `.claude-plugin/`; everything else is at root.

## Navigation

**Use this skill when**:
- Scaffolding a new plugin (directory structure, manifest, marketplace registration)
- Adding a component to an existing plugin (command, skill, agent, hook, MCP server)
- Diagnosing a plugin that installs without error but shows no commands/skills in session
- Bumping plugin versions across both manifests
- Setting up a directory-source marketplace in `settings.json`

**Do NOT use this skill when**:
- Writing the *content* of a skill (SKILL.md authoring) — use skill-judge to evaluate SKILL.md quality after authoring, and agent-md-refactor when plugin instruction files become bloated
- Configuring hooks behavior or MCP server logic — plugin-forge handles the wiring, not the implementation
- Publishing to the upstream claude.ai plugin registry — that uses a different submission flow

**Quick decision tree for ambiguous input**:
- "My plugin isn't loading" → go to [When Things Go Wrong](#when-things-go-wrong) first
- "I need to add a command" → component wiring path (see `references/plugin-structure.md`)
- "I need a new plugin from scratch" → use `scripts/create_plugin.py` then register in marketplace

## Philosophy

Plugin-forge exists because the gap between "plugin installed" and "plugin works" is filled with silent failures. Every decision here prioritizes diagnosability: correct git state, valid manifests, proper path placement, and restart discipline — because the loader gives you nothing when it fails.

## NEVER

- **NEVER create a directory-source plugin without initializing git** — the loader treats non-git directories as unsupported source type and fails silently with no error in the install output. Run `git init && git add -A && git commit -m "init"` before registering.
- **NEVER update version in only one manifest** — `plugin.json` and `marketplace.json` must stay in sync. A mismatch causes the marketplace to serve stale metadata while the plugin runs the new code, making version tracking unreliable and rollbacks dangerous.
- **NEVER put component directories inside `.claude-plugin/`** — `.claude-plugin/` is manifest-only. Commands, skills, agents, hooks, and `.mcp.json` must live at the plugin root. Nesting them inside `.claude-plugin/` results in silent load failure with no directory-not-found warning.
- **NEVER rely on `/plugin install` alone to activate agents** — marketplace install does not copy agent definitions to `.claude/agents/`. Agents require a manual `cp` to the agents directory plus a full session restart. Skipping either step means the agent is invisible to Claude.
- **NEVER name a skill directory with spaces or uppercase** — the skill loader uses the directory name as the skill identifier. Non-kebab-case names cause lookup mismatches where the skill exists on disk but cannot be resolved by the trigger system.
- **NEVER ship a SKILL.md over 500 lines** — the full file loads into context on every skill activation. Oversized skills consume token budget silently and degrade performance across the whole session. Move heavy reference content to `references/` subdirectory files.
- **NEVER hardcode absolute paths in manifests or hooks** — use `${CLAUDE_PLUGIN_ROOT}` for dynamic resolution in hooks/MCP configs. Absolute paths break portability across machines and for other users of a shared marketplace.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Plugin installs without error but `/command` is not available | Component dirs inside `.claude-plugin/` instead of plugin root, OR session not restarted after install | Move dirs to plugin root; `/plugin uninstall` then reinstall; restart session |
| Directory-source install fails with "source type not supported" | Plugin directory has no `.git` or zero commits | `git init && git add -A && git commit -m "init"` in plugin root, then reinstall |
| Plugin installs but shows wrong version | `plugin.json` and `marketplace.json` versions are out of sync | Use `scripts/bump_version.py` to update both atomically; uninstall and reinstall |
| Agent defined in plugin is not visible to Claude | Agents don't auto-load from marketplace; manual copy required | `sudo cp agents/<name>.md ~/.claude/agents/` and restart session completely |
| Skill triggers but reads wrong SKILL.md | Skill directory name doesn't match the `name:` field in frontmatter | Align directory name and frontmatter `name:` field; they must be identical |
| Hook fires but `${CLAUDE_PLUGIN_ROOT}` resolves incorrectly | Plugin was installed to a non-standard path | Verify install path with `/plugin list`; check hooks.json uses variable not literal path |
| MCP server from plugin doesn't appear in session | `.mcp.json` is missing or inside `.claude-plugin/` instead of plugin root | Move `.mcp.json` to plugin root; reinstall plugin |

## Reference Docs

| Reference | Content |
|-----------|---------|
| `references/plugin-structure.md` | Full directory schema, manifest fields, component placement rules |
| `references/marketplace-schema.md` | Marketplace JSON format, source types (local/GitHub/git URL), team distribution via settings.json |
| `references/workflows.md` | Step-by-step create/test/publish workflows, conventional commit conventions |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/create_plugin.py` | Scaffold new plugin with correct structure, manifests, and marketplace registration |
| `scripts/bump_version.py` | Update version atomically in both `plugin.json` and `marketplace.json` |
