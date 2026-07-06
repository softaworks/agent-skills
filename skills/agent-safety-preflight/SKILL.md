---
name: agent-safety-preflight
description: Run a local repo safety preflight before Claude Code, Codex, Cursor, MCP tools, hooks, or other AI coding agents get shell, package-script, or secret-adjacent scope.
trigger: explicit
---

# Agent Safety Preflight

Use this skill before handing a repository to an autonomous coding agent, Claude Code hook, Codex/Cursor workflow, MCP-backed toolchain, plugin marketplace package, or long-running TDD/agent loop.

It gives the user a quick Green / Yellow / Red receipt so they can decide what the agent may read or run before tool access starts.

## Quick Start

Run the free local scanner against the current repository:

```bash
bash /mnt/skills/user/agent-safety-preflight/scripts/run-preflight-lite.sh .
```

Or run the scanner source directly:

```bash
git clone https://github.com/el-zachariah/ai-agent-safety-starter-pack.git /tmp/agent-preflight
python3 /tmp/agent-preflight/agent_preflight_lite.py . --json
python3 /tmp/agent-preflight/agent_preflight_lite.py .
```

## What It Checks

- Agent instruction files such as `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, and `.cursor/rules/*`.
- Claude, Cursor, MCP, Copilot, Dev Container, and plugin/skill marketplace config.
- GitHub Actions workflows and package scripts an agent might execute.
- Secret-adjacent files such as `.env`, `.npmrc`, `.pypirc`, SSH keys, and token-looking config.
- Risky shell patterns such as `rm -rf`, `curl | sh`, `chmod 777`, `docker.sock`, and force-push commands.

## Workflow

1. Ask what agent or workflow is about to run: Claude Code, Codex, Cursor, MCP server, hook loop, PR bot, or another coding agent.
2. Run the local scanner against the target repo.
3. Read the decision level and risk buckets.
4. Produce a short receipt with allowed commands, must-ask commands, excluded files, and follow-up checks.
5. If the result is Yellow or Red, tighten the run rules before giving the agent shell/package-script/MCP/API scope.

## Receipt Template

```markdown
Agent preflight receipt
- Repo checked: <repo/path>
- Agent/tool about to run: <Claude Code / Codex / Cursor / MCP / hook loop>
- Decision: Green / Yellow / Red
- Risk buckets found: <agent instructions, MCP/Cursor/Claude config, package scripts, workflows, secret-adjacent files, risky shell>
- Commands allowed without asking: <install/test/read-only commands>
- Commands that must ask first: <deploy, destructive, credential, production, network, long-running background>
- Files/tools excluded before agent access: <paths or none>
```

## Output Guidance

Present the result as a practical go/no-go note, not as a security audit.

- **Green**: low signal. Normal code review discipline is likely enough.
- **Yellow**: agent can proceed only with written run rules and must-ask boundaries.
- **Red**: stop before broad tool access; remove secrets, review workflows/scripts, and define command restrictions first.

## Limits

This is a lightweight preflight, not a sandbox, malware scanner, secret scanner, vulnerability audit, or guarantee that an agent run is safe.
