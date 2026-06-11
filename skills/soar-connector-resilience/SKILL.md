---
name: soar-connector-resilience
description: Per-platform connector failure behavior documentation for all 7 SOAR platforms (Splunk SOAR, Swimlane Turbine, XSOAR, n8n, Torq, TheHive, Sentinel). Use when designing playbooks that must handle connector timeout, rate-limit, auth failure, or network partition mid-execution without silent failure. Seeded from chaos-engineer fault injection patterns.
---

# SOAR Connector Resilience — Failure Behavior Reference

## Why This Matters
Connector failures mid-playbook are the most common source of silent IR failures. A playbook that "ran successfully" but skipped the VirusTotal enrichment step because of a 429 rate-limit — without logging or alerting — produces a false sense of coverage.

## Per-Platform Failure Behavior

### Splunk SOAR (Phantom)
| Failure Mode | Default Behavior | Safe Pattern |
|-------------|-----------------|--------------|
| App timeout | Action marked `failed`; playbook continues to next block | Check `action_result.get_status()` before consuming output |
| 429 Rate-limit | Action marked `failed` immediately; no built-in retry | Use `retry` decorator in app code; add wait block in playbook |
| Auth failure (401) | Action marked `failed`; asset marked unhealthy | Alert on `asset_health` webhook; rotate credential; re-run |
| Network partition | Action hangs until `action_timeout` (default 300s) then `failed` | Set `action_timeout` per-action; never rely on default |
| Partial output | Action marked `success` with incomplete data — **silent** | Validate `len(action_result.get_data()) > 0` before downstream use |

### Swimlane Turbine
| Failure Mode | Default Behavior | Safe Pattern |
|-------------|-----------------|--------------|
| Connector timeout | Task transitions to `error` state; canvas stops task graph | Wire `on_error` edge to analyst notification task |
| 429 Rate-limit | Connector raises exception; task errors | Add retry logic in Runner subclass `execute()` with exponential backoff |
| Auth failure | Task errors with connector exception | Health-check action in connector; alert on repeated auth failures |
| Canvas task error | Workflow halts at errored task; no auto-resume | Always wire `on_error` transitions; never leave tasks with terminal error state unhandled |
| Approval task timeout | `sla_breach_default` option auto-selected | Ensure `sla_breach_default` is explicitly set to safe default; never leave null |

### Cortex XSOAR
| Failure Mode | Default Behavior | Safe Pattern |
|-------------|-----------------|--------------|
| Integration timeout | Command returns error entry; playbook continues | Check `isError(result)` before consuming; use `return_error()` in integration |
| 429 Rate-limit | Integration raises exception; task marked error | Implement `@retry` decorator with backoff in integration Python |
| Auth failure | Integration returns error entry | Alert on repeated integration errors; auto-rotate via credential store |
| Playbook task error | Task marked error; playbook halts unless `continue_on_error=true` | Set `continue_on_error` deliberately; log all error paths |

### n8n
| Failure Mode | Default Behavior | Safe Pattern |
|-------------|-----------------|--------------|
| Node error | Workflow stops at errored node; error output not processed | Connect Error Workflow in workflow settings; handle via error trigger node |
| HTTP timeout | Node fails after `timeout` ms (default: no timeout) | Set explicit timeout on HTTP Request nodes; handle with Error branch |
| 429 Rate-limit | Node fails unless retry is configured | Enable "Retry on Fail" in node settings (max retries + wait between) |
| Auth failure | Node fails with 401/403 | Use credential test blocks; alert on repeated auth failures |
| Partial batch | Loop succeeds even if some items fail — **silent** | Use "Continue on Fail" + check `$json["error"]` in subsequent node |

### Torq HyperSOC
| Failure Mode | Default Behavior | Safe Pattern |
|-------------|-----------------|--------------|
| Step failure | Workflow pauses; operator can retry or skip | Wire explicit error-handling branches; use Send-for-Approval on destructive steps |
| Rate-limit | Step fails; no built-in retry | Add Python scripting step with retry loop before integration step |
| Auth failure | Step fails with connector error | Monitor via Torq activity log; webhook on repeated failures |
| Case update failure | Case update step fails silently if Case closed | Check Case status before writing; handle with conditional |

### TheHive
| Failure Mode | Default Behavior | Safe Pattern |
|-------------|-----------------|--------------|
| Cortex analyzer timeout | Analyzer job stays `InProgress` until global timeout | Poll job status; alert if `InProgress` > 10 min |
| Cortex responder failure | Responder job marked `Failure`; case task stays open | Check responder job status before closing task |
| API rate-limit | 429 returned; no built-in retry in thehive4py | Wrap API calls in retry decorator; use exponential backoff |
| Case closed during response | API returns 400; task update fails | Check case status before any write operations |

### Microsoft Sentinel (Logic Apps)
| Failure Mode | Default Behavior | Safe Pattern |
|-------------|-----------------|--------------|
| Action failure | Run fails at failed action; downstream actions skipped | Set `runAfter` with `Failed`/`TimedOut` conditions to handle errors |
| 429 Rate-limit | Action retried per Logic App retry policy (default: 4 retries, 20s interval) | Customize retry policy on connector actions; increase for high-volume playbooks |
| Auth failure (token expiry) | Action fails; Logic App does NOT auto-renew MSI token in all scenarios | Use Managed Identity where possible; set short token cache TTL |
| Parallel branch failure | Other branches continue; no cross-branch failure propagation | Use `Configure run after` on join actions to handle partial failures |
| Approval email timeout | Approval waits indefinitely unless timeout configured | Set `actionTimeout` on approval action (ISO 8601 duration, e.g. `PT4H`) |

## Universal Failure Patterns to Avoid

- **NEVER consume connector output without checking success status** — partial or error outputs silently downstream is the #1 root cause of phantom-clean IR runs
- **NEVER leave approval tasks without an SLA breach default** — indefinite waits orphan incidents
- **NEVER assume a "success" status means complete data** — validate output volume, not just status code
- **NEVER skip error-path wiring** — every task/node with a destructive downstream action needs an error branch that notifies an analyst
- **NEVER rate-limit without backoff** — immediate retry on 429 worsens the condition; minimum 30s wait, exponential preferred
