# State File Schema Reference

## File location

`.agent_os_state.json` in the repository root (relative paths only for all file entries).

## Schema

```json
{
  "last_updated": "ISO-8601 timestamp",
  "agents": {
    "Agent-01": {
      "specialization": "auth",
      "ticket": "TICKET-42",
      "active_files": ["src/auth/login.ts"],
      "skills": ["git", "web-scrap"],
      "git_status": "2 commits ahead",
      "health": "RUNNING",
      "blocker": null,
      "previous_holder": null
    }
  },
  "locks": {
    "src/auth/login.ts": "Agent-01"
  }
}
```

## Field notes

| Field | Type | Notes |
|-------|------|-------|
| `last_updated` | ISO-8601 string | Updated on every write; use to detect stale state |
| `health` | enum | RUNNING, IDLE, BLOCKED, DONE, ERROR, UNKNOWN |
| `blocker` | string or null | Agent ID that holds the blocking lock; null if unblocked |
| `previous_holder` | string or null | Set when a force-release occurs; audit trail |
| `active_files` | array of strings | Relative paths from repo root only |
| `locks` | object | Map of `relative_path → agent_id`; single source of truth for lock ownership |

## Backup convention

Before any write, copy `.agent_os_state.json` to `.agent_os_state.json.bak` to enable single-step recovery from mid-write corruption.

## Validation

Always run `jq . .agent_os_state.json` before reading state into memory. If it fails, the file is corrupt — do not proceed with stale in-memory assumptions.
