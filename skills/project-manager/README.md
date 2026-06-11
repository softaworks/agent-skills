# project-manager

Central OS Agent for multi-agent development workflows.

Tracks live agent states, maintains `.agent_os_state.json`, enforces file-level dependency locking between agents, and renders a scannable CLI dashboard on demand.

## Triggers

- `/project-manager`
- "system status", "agent dashboard", "project status"
- "register agent", "check blockers", "update agent status"

## Dashboard output

```
## 🖥️ AGENT OS DIGITAL TWIN DASHBOARD
-----------------------------------------------------------------------
[Agent ID]    [Active Skill]    [Git Status]    [Current Task]   [Status]
-----------------------------------------------------------------------
Agent-01      git, web-scrap     2 Commits Ahead Fix Login Bug    ⚙️ RUNNING
Agent-02      db-schema, sql     Clean           Migrate Users    ⏸️ IDLE
Agent-03      jest, coverage     Uncommitted     Write UI Tests   🛑 BLOCKED (by 01)
```

## State file

Persists agent state to `.agent_os_state.json` in the working directory root.
