# Jira Cloud vs Server/Data Center Behavioral Differences

Understanding which deployment type you are targeting is critical — they have different APIs, authentication schemes, and field formats.

---

## Detection

| Signal | Likely Deployment |
|--------|-------------------|
| URL ends in `.atlassian.net` | Cloud |
| Self-hosted domain (e.g., `jira.company.com`) | Server or Data Center |
| `JIRA_BASE_URL` contains `atlassian.net` | Cloud |
| MCP Atlassian Rovo tools available | Cloud (Rovo is Cloud-only) |

---

## API Differences

| Concern | Jira Cloud (REST API v3) | Jira Server/DC (REST API v2) |
|---------|--------------------------|-------------------------------|
| API base path | `/rest/api/3/` | `/rest/api/2/` |
| Description format | **ADF required** (JSON) | Wiki markup text (string) |
| Comment format | **ADF required** (JSON) | Wiki markup text (string) |
| User identifier | `accountId` (opaque ID) | `name` (username string) |
| User lookup | `/user/search?query=...` | `/user/search?username=...` |
| Sprint field | `customfield_10020` (common) | Custom field ID varies by install |
| Epic link | `customfield_10014` (common) | Custom field ID varies by install |
| MCP Rovo support | Yes | No (API-only) |

---

## ADF Requirement (Jira Cloud Only)

Jira Cloud API v3 requires the Atlassian Document Format (ADF) for `description` and `body` fields — plain strings are silently ignored or cause 400 errors.

### Minimal ADF for plain text

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [
        {"type": "text", "text": "Your description text here"}
      ]
    }
  ]
}
```

### ADF with heading + bullets

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": {"level": 2},
      "content": [{"type": "text", "text": "Problem"}]
    },
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Users cannot log in on Safari."}]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Affects Safari 16+"}]
            }
          ]
        },
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [{"type": "text", "text": "Chrome unaffected"}]
            }
          ]
        }
      ]
    }
  ]
}
```

### ADF with code block

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "codeBlock",
      "attrs": {"language": "python"},
      "content": [{"type": "text", "text": "def example():\n    pass"}]
    }
  ]
}
```

---

## Authentication Differences

| Method | Jira Cloud | Jira Server/DC |
|--------|-----------|----------------|
| API Token | Yes (`user:api_token` Basic auth) | Sometimes (plugin-dependent) |
| Password | Deprecated/disabled | Yes (Basic auth) |
| OAuth 2.0 | Yes (3LO recommended) | OAuth 1.0a (legacy) |
| Personal Access Token (PAT) | Yes (header: `Authorization: Bearer PAT`) | Yes (DC 8.14+) |

**Cloud API token format:**
```bash
curl -u "user@example.com:$API_TOKEN" \
  "https://yourco.atlassian.net/rest/api/3/issue/PROJ-123"
```

**Server PAT format:**
```bash
curl -H "Authorization: Bearer $PAT" \
  "https://jira.company.com/rest/api/2/issue/PROJ-123"
```

---

## User Reference Differences

Cloud uses opaque `accountId`; Server uses username strings.

```bash
# Cloud: find accountId
curl -u "$USER:$TOKEN" \
  "https://yourco.atlassian.net/rest/api/3/user/search?query=john@example.com" \
  | jq '.[0].accountId'

# Server: use username directly
curl -u "$ADMIN:$PASS" \
  "https://jira.company.com/rest/api/2/user?username=jdoe"
```

---

## CLI (jira-cli) Behavior

The `jira` CLI (ankitpokhrel/jira-cli) detects the deployment type from `~/.config/.jira/.config.yml`. It handles both Cloud and Server automatically. However:

- **Transition names on Server** may differ from Cloud workflows — always run `jira issue move --help` or list transitions before moving.
- **Custom fields** use different IDs per install — on Server, check your instance's field configuration.
- **Sprint management** requires the board ID on both, but board IDs differ between deployments.

---

## Traps Specific to Each Deployment

### Cloud-only traps
- Sending plain string as `description` → silently fails or 400; must use ADF
- Using display name for `assignee` → must use `accountId` (Cloud strictly enforces this)
- Using `"Epic Link"` JQL field → replaced by `parentEpic` or `"Epic Link"` depending on company migrated date; test with `getJiraProjectIssueTypesMetadata` first

### Server-only traps
- Using API v3 path (`/rest/api/3/`) → returns 404; Server is always v2
- Sending ADF JSON as description → Server treats it as literal JSON text
- PATs not available on Server < 8.14 (Data Center); use Basic auth with password

