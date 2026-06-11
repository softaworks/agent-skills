# Integration Details & Detection Reference

## Detection Commands (run silently, suppress all errors)

| Integration | Detection Command | Notes |
|-------------|-------------------|-------|
| Claude Code History | `ls ~/.claude/projects/*/*.jsonl 2>/dev/null \| head -1` | Presence of any .jsonl file |
| GitHub CLI | `gh auth status 2>/dev/null` | Exit code 0 = authenticated |
| Jira CLI | `which jira 2>/dev/null` | Existence only; may need `jira auth` |
| Atlassian MCP | Check if `mcp__atlassian__*` tools available | MCP context check |
| Git | `git rev-parse --is-inside-work-tree 2>/dev/null` | Current directory |

## GitHub/Git Pull Commands

```bash
# Commits by current user in last 24h
git log --author="$(git config user.name)" --since="24 hours ago" --oneline

# PRs opened by user (gh CLI)
gh pr list --author="@me" --state=all --limit=10 --json number,title,state,url

# PRs reviewed by user
gh search prs --reviewed-by="@me" --updated=">$(date -d '24 hours ago' +%Y-%m-%d)" --json number,title,url

# Merged PRs by user
gh pr list --author="@me" --state=merged --limit=5 --json number,title,url
```

## Claude Code Digest Script

```bash
# Get yesterday's sessions as JSON
python3 ~/.claude/skills/daily-meeting-update/scripts/claude_digest.py --format json

# Get today's sessions
python3 ~/.claude/skills/daily-meeting-update/scripts/claude_digest.py --date today --format json

# Filter to specific project
python3 ~/.claude/skills/daily-meeting-update/scripts/claude_digest.py --project ~/my-app --format json
```

**Fallback if script fails:** Skip Claude Code integration silently, proceed with interview. The script is supplemental — never block the standup flow.

## Jira Pull (CLI)

```bash
# Tickets assigned to me, updated in last 24h
jira issue list --assignee=me --updated=-24h --output=json
```

## Atlassian MCP (if available)

Use `mcp__atlassian__search_issues` with JQL:
```
assignee = currentUser() AND updated >= -24h ORDER BY updated DESC
```

## Output Template Reference

```markdown
# Daily Update - [DATE]

## Yesterday
- [Items from interview + tool data]

## Today
- [Items from interview + Jira suggestions]

## Blockers
- [Blockers or "No blockers"]

## PRs & Reviews (if GitHub pulled)
- **Opened:** PR #N - title
- **Merged:** PR #N - title
- **Reviews:** PR #N (approved/changes requested)

## Jira (if pulled)
- PROJ-N: Title (Status)

## Topics for Discussion
- [Topics or "None"]

---
*Links:*
- [PR/ticket URLs]
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `gh: command not found` | GitHub CLI not installed | Skip GitHub integration, continue |
| `gh auth status` fails | Not authenticated | Skip GitHub, note to user optionally |
| `jira: command not found` | Jira CLI not installed | Skip Jira, check for Atlassian MCP |
| `claude_digest.py` fails | Python not installed / no sessions | Skip silently, continue with interview |
| Git not a repo | Not in git directory | Skip git integration for current dir, ask about specific repos |
| MCP tools unavailable | Not in Claude Code context | Skip MCP integrations entirely |
