---
name: jira
description: Use when the user mentions Jira issues (e.g., "PROJ-123"), asks about tickets, wants to create/view/update issues, check sprint status, or manage their Jira workflow. Triggers on keywords like "jira", "issue", "ticket", "sprint", "backlog", "transition", "epic", or issue key patterns like ABC-123.
---

# Jira

Natural language interaction with Jira. Supports CLI and MCP backends. Covers Jira Cloud and Server/Data Center.

---

## Mindset

1. **Fetch before you touch.** Never assume current state — an issue could have been updated 30 seconds ago. Always retrieve before editing or transitioning.

2. **IDs, not names.** Jira Cloud rejects display names for users, transition names, and link types. Resolve every identifier to its machine ID before acting. "Done" is not a transition ID; "5f3a..." is.

3. **Cloud and Server are different APIs.** Cloud requires ADF for descriptions; Server takes plain markup. Cloud uses `accountId`; Server uses `username`. Cloud is `/rest/api/3/`; Server is `/rest/api/2/`. Detect first, act second.

4. **Notifications are not free.** Every field update notifies all watchers. Bulk-editing 20 tickets sends 20 notification storms. Get explicit approval before any batch operation.

5. **Transitions have gates.** Workflow enforces order. "To Do" → "Done" may be blocked if the project requires "In Progress" as an intermediate step. Get available transitions, pick from that list.

---

## Navigation

**Use this skill when:**
- User mentions a Jira issue key (pattern `[A-Z]+-[0-9]+`)
- User asks to create, view, update, comment on, or transition a ticket
- User asks about sprint status, backlog, or epics
- User wants to search or filter Jira issues (JQL)

**Do NOT use this skill when:**
- User is asking about GitHub Issues, Linear, Azure DevOps, or other trackers — route to the appropriate skill
- User wants to configure Jira itself (workflow schemes, field configurations) — those require Jira admin UI
- User wants Confluence pages — use Confluence-specific MCP tools

**Backend decision tree:**

```
1. Is `jira` CLI available?
   → Run: which jira
   → YES: USE CLI BACKEND (references/commands.md)

2. Are Atlassian MCP tools available?
   → Look for mcp__claude_ai_Atlassian_Rovo__* in tool list
   → YES: USE MCP BACKEND (references/mcp.md)

3. Neither available?
   → GUIDE USER TO SETUP (see "No Backend Available" below)
```

**Deployment detection (critical for Cloud vs Server behavior):**

```
URL contains .atlassian.net  → Jira Cloud  → ADF required, accountId for users
URL is self-hosted domain    → Server/DC   → Wiki markup OK, username for users
MCP Rovo tools present       → Jira Cloud  → ADF required
```

See `references/cloud-vs-server.md` for full differences.

| Backend | When to Use | Reference |
|---------|-------------|-----------|
| **CLI** | `jira` command available | `references/commands.md` |
| **MCP** | Atlassian MCP tools available | `references/mcp.md` |
| **Neither** | Neither available | Guide to install CLI |

---

## Philosophy

Jira is a shared workspace. Every action you take ripples outward — to watchers, to linked tickets, to sprint boards. Treat each operation as a deliberate edit to a team's shared record, not a personal note. Confirm before you change; verify after you do.

---

## Quick Reference (CLI)

> Skip this section if using MCP backend.

| Intent | Command |
|--------|---------|
| View issue | `jira issue view ISSUE-KEY` |
| List my issues | `jira issue list -a$(jira me)` |
| My in-progress | `jira issue list -a$(jira me) -s"In Progress"` |
| Create issue | `jira issue create -tType -s"Summary" -b"Description"` |
| Move/transition | `jira issue move ISSUE-KEY "State"` |
| Assign to me | `jira issue assign ISSUE-KEY $(jira me)` |
| Unassign | `jira issue assign ISSUE-KEY x` |
| Add comment | `jira issue comment add ISSUE-KEY -b"Comment text"` |
| Open in browser | `jira open ISSUE-KEY` |
| Current sprint | `jira sprint list --state active` |
| Who am I | `jira me` |

---

## Quick Reference (MCP)

> Skip this section if using CLI backend.

| Intent | MCP Tool |
|--------|----------|
| Search issues | `mcp__claude_ai_Atlassian_Rovo__searchJiraIssuesUsingJql` |
| View issue | `mcp__claude_ai_Atlassian_Rovo__getJiraIssue` |
| Create issue | `mcp__claude_ai_Atlassian_Rovo__createJiraIssue` |
| Update issue | `mcp__claude_ai_Atlassian_Rovo__editJiraIssue` |
| Get transitions | `mcp__claude_ai_Atlassian_Rovo__getTransitionsForJiraIssue` |
| Transition | `mcp__claude_ai_Atlassian_Rovo__transitionJiraIssue` |
| Add comment | `mcp__claude_ai_Atlassian_Rovo__addCommentToJiraIssue` |
| User lookup | `mcp__claude_ai_Atlassian_Rovo__lookupJiraAccountId` |
| List projects | `mcp__claude_ai_Atlassian_Rovo__getVisibleJiraProjects` |

See `references/mcp.md` for full MCP patterns.

---

## ADF Requirement (Jira Cloud)

Jira Cloud API v3 requires Atlassian Document Format (ADF) for `description` and `body` fields. Sending a plain string is silently ignored or causes a 400 error.

**Minimal ADF for any description:**
```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Your description here"}
      ]
    }
  ]
}
```

**When using MCP `createJiraIssue` or `editJiraIssue` on Cloud:** pass the description as ADF JSON, not a plain string.

**When using the `jira` CLI:** the CLI handles format conversion internally — pass plain text or markdown normally.

See `references/cloud-vs-server.md` for more ADF examples (headings, bullets, code blocks).

---

## Workflow

**Creating tickets:**
1. Detect deployment (Cloud vs Server) — determines description format
2. Research context if user references code/tickets/PRs
3. Draft ticket content (use ADF if Cloud + MCP)
4. Review with user
5. Create using appropriate backend

**Updating tickets:**
1. Fetch issue details first
2. Check status (careful with in-progress tickets)
3. Show current vs proposed changes
4. Get approval before updating
5. Add comment explaining changes

---

## NEVER

- **NEVER send a plain text string as `description` on Jira Cloud (MCP)** — Cloud API v3 requires ADF JSON. A plain string is silently discarded, creating a ticket with a blank description and no error message.

- **NEVER transition without fetching current status first** — Workflows enforce intermediate states. "To Do" → "Done" silently fails if "In Progress" is required first. Always call `getTransitionsForJiraIssue` and pick from the returned list.

- **NEVER assign using a display name (MCP/Cloud)** — Only `accountId` works on Jira Cloud. Display names are silently accepted but the assignment is dropped. Call `lookupJiraAccountId` first.

- **NEVER edit a description without showing the original** — Jira has no undo for field edits. Fetch the current description, show it to the user, and confirm before replacing.

- **NEVER use `/rest/api/3/` endpoints against a Server/Data Center instance** — Server only exposes v2. The request returns 404 with no helpful error. Check the URL — `.atlassian.net` = Cloud (v3); everything else = Server (v2).

- **NEVER use `--no-input` (CLI) without first checking required fields** — Silently fails with cryptic output if project-required fields (e.g., story points, components) are missing. Run `jira issue create` interactively once on a new project to learn its required fields.

- **NEVER assume transition names are universal** — "Done", "Closed", "Complete", "Resolved" vary by project workflow. A transition named "Done" in one project may be "Closed" in another. Always get available transitions for the specific issue.

- **NEVER bulk-modify without explicit approval** — Each ticket update notifies all watchers independently. Editing 10 tickets sends 10 separate notification storms. Show the full list of affected tickets and get a single explicit go-ahead.

---

## When Things Go Wrong

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `description` is blank after create (MCP Cloud) | Sent plain string instead of ADF | Retry with ADF JSON; see `references/cloud-vs-server.md` |
| Transition fails silently | Missing intermediate state in workflow | Fetch transitions list; look for required intermediate step |
| Assignment dropped (MCP) | Used display name instead of accountId | Call `lookupJiraAccountId`, use the returned ID |
| `404` on REST call | Called v3 endpoint against Server instance | Switch to `/rest/api/2/`; Server does not expose v3 |
| `400 Bad Request` on create | Required project field missing | Call `getJiraProjectIssueTypesMetadata` to see required fields |
| `401 Unauthorized` (MCP) | MCP session expired | Run `/mcp` to reconnect Atlassian service |
| `403 Forbidden` | Missing project permission | User needs Browse/Edit Project permission in Jira admin |
| CLI `move` fails with unknown state | Transition name mismatch | Check exact names in that project's workflow; names are case-sensitive |

---

## Issue Key Detection

Issue keys follow the pattern: `[A-Z]+-[0-9]+` (e.g., PROJ-123, ABC-1).

When a user mentions an issue key in conversation:
- **CLI:** `jira issue view KEY` or `jira open KEY`
- **MCP:** `mcp__claude_ai_Atlassian_Rovo__getJiraIssue` with the key

---

## Safety

- Always show the command/tool call before running it
- Always get approval before modifying tickets
- Preserve original information when editing
- Verify updates after applying
- Always surface authentication issues clearly so the user can resolve them

---

## No Backend Available

If neither CLI nor MCP is available, guide the user:

```
To use Jira, you need one of:

1. jira CLI (recommended):
   https://github.com/ankitpokhrel/jira-cli

   Install: brew install ankitpokhrel/jira-cli/jira-cli
   Setup:   jira init

2. Atlassian MCP:
   Configure in your MCP settings with Atlassian credentials.
   Note: Atlassian MCP (Rovo) only supports Jira Cloud.
```

---

## Deep Dive

**LOAD reference when:**
- Creating issues with complex fields or multi-line content
- Building JQL queries beyond simple filters
- Troubleshooting errors or authentication issues
- Working with transitions, linking, or sprints
- Targeting a specific deployment type (Cloud vs Server)

**Do NOT load reference for:**
- Simple view/list operations (Quick Reference above is sufficient)
- Basic status checks (`jira issue view KEY`)
- Opening issues in browser

| Task | Load Reference? |
|------|-----------------|
| View single issue | No |
| List my tickets | No |
| Create with description (Cloud, MCP) | **Yes** — ADF format required (`cloud-vs-server.md`) |
| Create with description (CLI) | **Yes** — CLI needs `/tmp` pattern (`commands.md`) |
| Transition issue | **Yes** — need transition ID workflow (`mcp.md`) |
| JQL search | **Yes** — for complex queries (`mcp.md`) |
| Link issues | **Yes** — see `mcp.md` for link type details |
| Cloud vs Server behavior | **Yes** — `references/cloud-vs-server.md` |

References:
- CLI patterns: `references/commands.md`
- MCP patterns: `references/mcp.md`
- Cloud vs Server: `references/cloud-vs-server.md`
