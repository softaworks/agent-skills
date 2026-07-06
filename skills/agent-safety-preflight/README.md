# Agent Safety Preflight

A lightweight Agent Skills package for teams that let Claude Code, Codex, Cursor, MCP tools, PR bots, hooks, or other AI coding agents work inside real repositories.

Run it before the agent gets shell, package-script, workflow, MCP/API, or secret-adjacent scope. It produces a Green / Yellow / Red repo handoff receipt that can be pasted into a PR, issue, runbook, or agent session log.

## When to Use This Skill

Use `agent-safety-preflight` when you need to:

- Check a repo before an AI coding agent starts editing or running commands.
- Review `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/*`, MCP config, Claude plugin files, or Copilot instructions.
- Spot package scripts, GitHub Actions, Dev Container lifecycle commands, or plugin/skill manifests before an agent inherits them.
- Write a concise handoff receipt for allowed commands, must-ask commands, and excluded files.

## Quick Start

```bash
/agent-safety-preflight
```

Then ask the agent to run the bundled script:

```bash
bash /mnt/skills/user/agent-safety-preflight/scripts/run-preflight-lite.sh .
```

The script clones the public lite scanner from:

```text
https://github.com/el-zachariah/ai-agent-safety-starter-pack
```

and runs it locally against the repo path you provide.

## Example Receipt

```markdown
Agent preflight receipt
- Repo checked: ./my-app
- Agent/tool about to run: Claude Code with MCP tools
- Decision: Yellow
- Risk buckets found: agent instructions, package scripts, GitHub Actions, secret-adjacent files
- Commands allowed without asking: tests, lint, read-only inspection
- Commands that must ask first: deploy, database migration, credential access, destructive cleanup
- Files/tools excluded before agent access: .env, production deploy workflow, npm publish script
```

## Why It Helps

AI coding agents often inherit repo-local instructions, hooks, workflow files, package scripts, and MCP/tool config. This skill gives the user a visible pre-run checkpoint before an agent is trusted with broad tool access.

## Limits

This is not a sandbox, malware scanner, secret scanner, compliance audit, or security guarantee. It is a quick local preflight and receipt generator for safer agent handoffs.
