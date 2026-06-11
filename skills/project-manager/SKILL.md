---
name: project-manager
description: >
  Central OS Agent for multi-agent development workflows. Tracks live agent states,
  maintains .agent_os_state.json, enforces file-level dependency locking, detects
  state corruption, and renders a CLI dashboard. Trigger keywords: "system status",
  "agent dashboard", "project status", "check blockers", "register agent", "agent
  is working on", "who owns", "lock conflict", "unblock agent".
---

## Mindset

Multi-agent state is **eventually inconsistent by default**. Every read of `.agent_os_state.json` can be stale. Treat it as an advisory ledger, not ground truth — confirm with the actual agent before acting on lock data.

File-level locks are a proxy for intent, not enforcement. Two agents can both write to the same file without triggering a lock error if they registered their ownership naively. The lock only prevents corruption when agents *ask before acting*.

A BLOCKED agent that has been blocked for more than one polling cycle is a system smell, not a normal operating state. Silent blocks cascade: Agent-03 blocks Agent-07, and Agent-07's downstream dependency is never surfaced unless you check transitively.

Dashboard freshness degrades immediately. Timestamps older than 2 minutes in a hot session mean the reporting agent is either hung, disconnected, or running in a shell that lost its context window.

Health status and blocker fields are self-reported — an agent can lie or go silent without updating its own record.

## Navigation

**Use this skill when**:
- Coordinating 2+ agents that share files, branches, or output artifacts
- Diagnosing why an agent is stuck, silent, or producing stale output
- Running "system status", "agent dashboard", or "check blockers"
- Registering, updating, or releasing agents and their file locks
- Investigating a lock conflict or state corruption scenario

**Do NOT use this skill when**:
- Only one agent is active — single-agent workflows have no coordination overhead to manage
- The project has no shared files between agents — lock management adds friction with no benefit
- You are debugging code logic rather than agent coordination; use the `code-review` or `systematic-debugging` skill instead

**Quick triage**: If an agent reports BLOCKED → check lock owner → verify owner is still alive → if stale, force-release. If multiple agents report BLOCKED on the same file → lock owner crashed without cleanup; see recovery table below.

## Philosophy

State without freshness guarantees is noise. Every coordination decision must account for the age of the state data, the trustworthiness of the reporting agent, and the transitive dependency graph — not just the direct lock entry.

## NEVER

- NEVER release a lock based solely on a requesting agent's claim that it needs the file — always verify with the lock-holder's current status first, because phantom release creates a race condition where both agents write simultaneously.
- NEVER treat a missing `.agent_os_state.json` as a clean slate without checking if an agent crashed mid-write — a partial write leaves a corrupt JSON file that silently fails future reads; always validate with `jq . .agent_os_state.json` before assuming the file is absent.
- NEVER mark an agent DONE and release all its locks in a single step — release locks file-by-file and confirm downstream agents are notified before transitioning status, because batch-release can trigger a thundering herd where 3+ blocked agents all start writing the same dependency simultaneously.
- NEVER propagate a lock from a crashed agent to the requester without recording the original lock owner in a `previous_holder` field — without audit history, you cannot determine whether a file was modified in a partially-applied state when the original agent died.
- NEVER use agent self-reported `health` as the primary signal for scheduling new work — an agent in state RUNNING can be CPU-starved, token-limited, or stuck in a retry loop; cross-check with `last_updated` timestamp delta before assigning dependent tasks.
- NEVER store absolute paths in `active_files` or the `locks` map — path portability breaks when the state file is shared across machines or worktrees; use paths relative to the repo root.
- NEVER allow two agents to hold a lock on the same file simultaneously, even if one claims it is "read-only" — read locks that turn into write locks mid-execution are the most common source of state corruption in concurrent Claude Code sessions.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Agent reports BLOCKED but lock-holder shows DONE | Lock was not released on completion (crash or missed cleanup step) | Manually call "agent [ID] finished [file]" for each file the dead agent held; verify `locks` map is empty for those paths |
| `.agent_os_state.json` fails JSON parse | Agent crashed mid-write, leaving partial JSON | Run `jq . .agent_os_state.json`; if corrupt, restore from `.agent_os_state.json.bak` if present, or reconstruct from each agent's last self-report |
| Multiple agents claim to own the same lock entry | Race condition on simultaneous registration | Last-write-wins policy applied; re-interview each agent for its actual file set; rebuild the `locks` map from scratch |
| Dashboard timestamp is stale (>2 min in active session) | Agent is hung, token-exhausted, or context was reset | Treat agent as UNKNOWN health; do not assign new work; attempt a ping ("update [Agent-ID] status to PING") and wait one cycle |
| Transitive block chain (A blocks B, B blocks C) | No deadlock detection in baseline schema | Walk the `blocker` fields recursively; if any chain loops back to itself, you have a deadlock — break it by promoting the oldest lock-holder's work to completion or reassigning |
| Agent registers with no `active_files` and immediately claims RUNNING | Agent is faking status to appear active | Cross-check against actual git diff for that agent's branch; no file changes = agent is idle or misconfigured |

## Commands

- **"system status"** / **"dashboard"**: Render the full dashboard. See [references/dashboard-format.md](references/dashboard-format.md).
- **"register agent [ID] as [specialization]"**: Add a new agent entry to state.
- **"update [Agent-ID] status to [status]"**: Update an agent's health field.
- **"agent [ID] is working on [file]"**: Acquire a lock; check for conflicts first.
- **"agent [ID] finished [file]"**: Release the file lock; notify dependents.
- **"check blockers"**: List all blocked agents with transitive chain analysis.
- **"recommend skills for [Agent-ID]"**: Suggest skills based on current error/git state.
- **"force-release [file]"**: Override a stale lock; record `previous_holder` before release.

## State File

Schema and validation details: [references/state-schema.md](references/state-schema.md)

Key rule: always read → validate → mutate → write. Never write without a preceding read in the same operation sequence.
