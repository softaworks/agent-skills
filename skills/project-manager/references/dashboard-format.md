# Dashboard Format Reference

## Output structure

When asked for "system status" or "dashboard", render this exact markdown:

```
## AGENT OS DIGITAL TWIN DASHBOARD
-----------------------------------------------------------------------
[Agent ID]    [Active Skill]    [Git Status]      [Current Task]   [Status]
-----------------------------------------------------------------------
Agent-01      git, web-scrap    2 Commits Ahead   Fix Login Bug    RUNNING
Agent-02      db-schema, sql    Clean             Migrate Users    IDLE
Agent-03      jest, coverage    Uncommitted       Write UI Tests   BLOCKED (by 01)

### Active Interactivity Matrix:
- Agent-01 is modifying `src/auth/login.ts`.
- Agent-03 execution paused: `src/auth/login.ts` locked by Agent-01.

### Required Actions:
- [ ] Merge Agent-01 branch to release Agent-03.
- [ ] Load `performance-profiler` skill to Agent-02 for upcoming DB migration.

### State Freshness:
- Last updated: [timestamp]
- Agents with stale timestamps (>2 min): [list or "none"]
```

## Status labels

| Label | Meaning |
|-------|---------|
| RUNNING | Agent is actively executing work |
| IDLE | Agent has no current task |
| BLOCKED | Agent is waiting on a lock held by another agent |
| DONE | Agent completed its work item; locks should be released |
| ERROR | Agent encountered an unrecoverable error |
| UNKNOWN | No heartbeat for >2 minutes; treat as potentially dead |

## Interactivity Matrix rules

- Only list file interactions where a lock is active.
- Show all transitive block chains (A→B→C), not just direct blocks.
- If the `locks` map is empty, output "No active file locks."

## Required Actions generation

- One action item per blocked agent.
- One action item per agent with skills mismatch (agent needs a tool it doesn't have loaded).
- One action item per UNKNOWN-health agent.
