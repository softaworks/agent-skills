---
name: datadog-cli
description: Datadog CLI for searching logs, querying metrics, tracing distributed requests, and managing dashboards. Use when debugging production incidents, investigating error spikes, correlating traces, or analyzing service health in Datadog.
---

# Datadog CLI

## Mindset

- **Start with `errors` + `compare`, not raw search** — `errors` aggregates by service/type instantly; `compare` tells you if the spike is new or chronic. Raw search before these wastes API quota and context.
- **Trace ID is your thread through chaos** — when a user reports a broken transaction, get the trace ID first (`logs search` with `@http.url` or `@user.id`), then `logs trace` to reconstruct the full call chain across services. Don't search per-service manually.
- **`patterns` before reading individual logs** — Datadog indexes thousands of variants of the same error. `logs patterns` normalizes UUIDs/IPs/numbers into templates; reading raw logs before this is signal-diluting.
- **Dashboard updates are destructive** — the API replaces the entire dashboard JSON. A partial PUT deletes widgets you didn't include. Always `get` → modify → `update`.
- **Rate limits are silent trip wires** — the Logs Search API is capped at 300 requests/minute per org. `logs multi` with many parallel queries can exhaust quota for the whole team. Use `--limit` conservatively.

## Navigation

**Use this skill when**: searching Datadog logs, querying metrics timeseries, tracing distributed requests by trace ID, detecting log patterns, comparing error rates between time windows, managing dashboards, or investigating a production incident end-to-end.

**Do NOT use this skill when**:
- The user wants to configure Datadog monitors/alerts (requires Datadog API directly, not this CLI)
- The user wants to query Synthetics, RUM, or Security signals (not supported by this CLI)
- No `DD_API_KEY` + `DD_APP_KEY` are set — prompt for them first

**Ambiguous input decision tree**:
- "Check errors" → `errors --from 1h` then `logs compare`
- "Debug request X" → get trace ID → `logs trace`
- "Is the spike new?" → `logs compare --period 1h`
- "What's failing?" → `logs patterns --query "status:error"`

## Philosophy

Observability triage is a narrowing funnel: start wide (service-level aggregations), identify the signal (patterns), then zoom in (individual logs + traces). Never start at the bottom of the funnel.

## NEVER

- NEVER run `logs search` with `--query "*"` and no `--limit` — the default 100-result limit still pages through the full index scan; always scope by `service:` or `status:` to avoid hitting rate limits and returning noise.
- NEVER run `dashboards update` without first running `dashboards get` — the update endpoint replaces the full dashboard JSON; any widget you omit is permanently deleted from the dashboard.
- NEVER use `logs tail` in an automated/non-interactive context — it polls indefinitely and will block the agent; use `logs search` with a short `--from` window instead.
- NEVER send `logs multi` with more than 5 parallel queries without checking org rate limits — each parallel query counts as a separate API call; 10+ queries can exhaust the 300 req/min org limit mid-investigation.
- NEVER query metrics with `{*}` scope and a long window (e.g., `--from 7d`) — this returns all host timeseries; scope with `{service:X,env:prod}` or you'll get truncated/sampled data silently.
- NEVER interpret a 0-count result as "no errors" — it may mean the query matched no indexed facets (typo in service name, wrong env tag). Verify with `services --from 1h` to confirm the service is emitting logs at all.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| `401 Unauthorized` | `DD_API_KEY` or `DD_APP_KEY` not set / wrong org | `echo $DD_API_KEY` — if empty, export both keys; confirm keys are for the correct Datadog site |
| `429 Too Many Requests` | Org rate limit hit (300 req/min for Logs) | Wait 60 seconds; reduce `logs multi` parallelism; add `--limit 50` to searches |
| Empty results but no error | Wrong site (`datadoghq.com` vs `datadoghq.eu`) or service name typo | Run `services --from 24h` to confirm service exists; add `--site datadoghq.eu` if EU org |
| `logs trace` returns nothing | Trace ID format mismatch — some services emit `@trace_id`, others `@dd.trace_id` | The CLI searches both, but extend `--from` window; trace may have aged out of index (default 15-day retention) |
| Dashboard `update` wiped widgets | Sent partial JSON without fetching first | Restore from Datadog UI version history (Settings → Restore); next time always `get` → edit → `update` |
| `logs patterns` shows only 1 pattern | Query too narrow or low log volume | Widen `--from` window or remove service filter temporarily |

## Setup

```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
```

Keys: https://app.datadoghq.com/organization-settings/api-keys

For EU orgs, add `--site datadoghq.eu` to every command.

```bash
npx @leoflores/datadog-cli <command>
```

## Incident Triage — Standard Sequence

```bash
# 1. Aggregate: what services are erroring and how many?
npx @leoflores/datadog-cli errors --from 1h --pretty

# 2. Baseline: is this spike new or ongoing?
npx @leoflores/datadog-cli logs compare --query "status:error" --period 1h --pretty

# 3. Pattern: what are the error templates? (normalize before reading raw)
npx @leoflores/datadog-cli logs patterns --query "status:error service:api" --from 1h --pretty

# 4. Scope: narrow to the failing service
npx @leoflores/datadog-cli logs search --query "status:error service:api" --from 1h --limit 50 --pretty

# 5. Context: get logs around the failure timestamp
npx @leoflores/datadog-cli logs context --timestamp "2024-01-15T10:30:00Z" --service api --before 5m --after 2m --pretty

# 6. Trace: reconstruct full distributed call chain
npx @leoflores/datadog-cli logs trace --id "TRACE_ID" --pretty
```

## Commands Quick Reference

| Command | When to use |
|---------|-------------|
| `errors` | First look — error counts by service/type |
| `logs compare` | Determine if spike is new vs. baseline |
| `logs patterns` | Normalize error variants before reading raw |
| `logs search` | Targeted log retrieval (after narrowing) |
| `logs trace` | Reconstruct distributed request from trace ID |
| `logs context` | Get what happened just before/after a timestamp |
| `logs agg` | Break down logs by facet (status, host, error.kind) |
| `logs multi` | Parallel cross-service comparison (use sparingly) |
| `logs tail` | Interactive only — stream live logs |
| `metrics query` | Correlate log errors with CPU/latency/throughput |
| `services` | Verify a service is emitting logs (sanity check) |
| `dashboards` | CRUD — always `get` before `update` |

## Reference Docs

Load these only when needed for the specific task:

- **[logs-commands.md](references/logs-commands.md)** — full flag reference for all `logs *` subcommands
- **[query-syntax.md](references/query-syntax.md)** — operators, facet names, numeric comparisons, wildcard patterns
- **[metrics.md](references/metrics.md)** — metrics query format, APM metrics, aggregation functions
- **[workflows.md](references/workflows.md)** — multi-step workflows (real-time debug, service health, export)
- **[dashboards.md](references/dashboards.md)** — full dashboard CRUD reference + safe update workflow
