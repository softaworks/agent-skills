---
name: api-design
description: Design API contracts before implementation — protocol selection, pagination, versioning, error standardization, OpenAPI spec authoring, and breaking-change classification. Use when asked to "design an API", "spec out endpoints", "pick REST vs GraphQL", "define error responses", "plan API versioning", or "write an OpenAPI spec". Sits between requirements-clarity (what to build) and openapi-to-typescript (typed interfaces from spec).
---

## Mindset

- **The spec is a contract, not documentation.** An API spec written after the fact documents what was shipped. A spec written before implementation constrains what gets shipped. Spec-first is a design discipline, not a paperwork exercise.
- **The HTTP status code IS the error signal.** A 200 with `{"success": false}` in the body is a protocol violation that breaks every intermediary — proxies, caches, circuit breakers, monitoring dashboards — because they all treat 2xx as success. The body elaborates; the status decides.
- **Consumers don't read your source code.** Every invariant you enforce in the backend (write-once fields, enum transitions, per-org rate limits) must appear explicitly in the contract. If it isn't in the spec, frontend will rediscover it at 4 PM on release day.
- **Pagination is a data consistency guarantee, not a performance knob.** The correct pagination strategy depends on whether the underlying data changes during iteration. Offset breaks silently on concurrent writes. Cursor is required for correctness on any live data set — not just for performance.
- **Versioning debt compounds.** Every URL path version (`/v1/`, `/v2/`) is a permanent branch in production. Non-breaking evolution (additive fields, new optional params) should not create a new version. Reserve versioning for genuine breaking changes.
- **Error codes are machine interfaces.** `"Email is invalid"` is a display string. `INVALID_EMAIL` is a contract. Consumers branch on codes, not sentences. Sentences are localized, truncated, and changed mid-iteration. Codes are not.

## Navigation

**Use this skill when**:
- Designing a new API surface (REST, GraphQL, gRPC) before any implementation
- Choosing between protocol options and need decision criteria beyond "REST is standard"
- Defining error response structure, pagination strategy, or versioning policy
- Writing or reviewing an OpenAPI spec (spec-first or code-first)
- Classifying whether a proposed change is breaking or non-breaking
- Documenting rate limiting, auth schemes, or retry conventions in a spec

**Do NOT use this skill when**:
- Backend implementation is already complete and you need consumer-facing docs — use backend-to-frontend-handoff-docs
- You have an OpenAPI spec and need TypeScript interfaces — use openapi-to-typescript
- Requirements are still vague ("build me a user API") — use requirements-clarity first
- You need database schema design — use database-schema-designer

**Quick decision tree**:
```
Is the API surface new (no prior contract exists)?
  YES → Start at Protocol Selection, then Pagination, then Versioning
  NO  → Skip to Breaking-Change Classification; existing contract governs

Does the user have a written OpenAPI spec?
  YES → Jump to Spec Review; check for common omissions
  NO  → Ask: spec-first or code-first? (see section below)

Is the user asking about errors/status codes?
  YES → Error Standardization section; apply RFC 7807
```

## Philosophy

API design is constraint selection. Every decision — protocol, pagination style, version scheme, error shape — closes future options in exchange for present clarity. Bad API design is not missing features; it is missing constraints. Underconstrained APIs allow callers to build assumptions that are never honored, and allow implementers to ship behaviors that are never documented.

## NEVER

- **NEVER use offset pagination for any resource that can be modified during iteration** — offset is computed against the current state of the dataset. Between page 1 and page 2, concurrent inserts shift every subsequent row. Items are skipped or duplicated invisibly, with no error to surface. Cursor pagination anchors to a stable position regardless of concurrent writes.
- **NEVER define error responses as a single string `message` field** — a bare string message is consumed by displaying it to users. Machine-readable error bodies (`code` + `detail` + optional `field`) allow consumers to branch programmatically: retry on `RATE_LIMIT_EXCEEDED`, show a field hint on `INVALID_EMAIL`, escalate on `PERMISSION_DENIED`. Strings cannot support this without string parsing.
- **NEVER return HTTP 200 with a `success: false` body** — the HTTP status is the error signal for every layer that touches the response (proxy, cache, CDN, circuit breaker, monitoring alert, client SDK). A 200 disables all of that. The body is elaboration only; it cannot override the status.
- **NEVER version your API in the URL by default** — `/v1/users` creates a permanent production branch. When `/v2/users` ships, `/v1/users` must remain operational indefinitely (or you break clients). Header versioning (`API-Version: 2024-01`) makes version negotiation explicit and allows sunset without a parallel URL tree. Override this ONLY when developer experience for public APIs demands URL discoverability.
- **NEVER design a PATCH endpoint that treats absent fields as nulls** — in a partial update, an absent field means "do not change this field." A null field means "set this field to null." These are distinct intents. A PATCH that collapses them forces callers to always send every optional field to protect values they don't want cleared — defeating the purpose of PATCH.
- **NEVER use boolean query parameters for state that could acquire a third value** — `?active=true/false` will eventually need `?active=pending` or `?active=null`. Boolean URL params cannot express this; the API must be redesigned. Use `?status=active|inactive|pending` from the start.
- **NEVER define rate limit behavior without spec-level documentation** — rate limits that are not in the spec are discovered by consumers via production 429 errors. Document the limit scope (per user, per IP, per org), the algorithm (token bucket, sliding window), and the response headers (`Retry-After`, `X-RateLimit-Remaining`) before the API ships.

## Protocol Selection

### REST vs GraphQL vs gRPC Decision Criteria

| Criterion | REST | GraphQL | gRPC |
|-----------|------|---------|------|
| Consumer profile | Multiple external clients, public APIs | Frontend teams with highly variable query shapes | Internal service-to-service, performance-critical |
| Schema evolution | Additive (non-breaking); versioning for removals | Schema-first; deprecations via `@deprecated` directive | Proto files; strongly typed; forward/backward compat via field numbers |
| Payload control | Fixed shapes; over/under-fetch common | Consumer-specified; fetch only needed fields | Fixed shapes; binary encoding |
| Tooling maturity | Broadest ecosystem | Good; Apollo, graphql-codegen | Strong in polyglot; requires protoc toolchain |
| Error handling | HTTP status codes + RFC 7807 body | Always 200; errors in `errors[]` array | gRPC status codes (not HTTP) |
| Caching | Native HTTP caching (ETags, Cache-Control) | Query hashing required; no standard cache key | Application-level only |

**Non-obvious selection criteria practitioners miss**:

- **GraphQL's 200-for-everything is a deliberate trade-off, not a design flaw.** But it means your HTTP-layer monitoring (Datadog, Sentry, uptime checks) will report 100% success even during partial outages. You must instrument on the `errors` array, not on HTTP status.
- **REST over-fetching is a performance problem only after you have the traffic.** Premature GraphQL adoption for "performance" typically means paying the schema-design and tooling tax before you have evidence over-fetching is actually a bottleneck.
- **gRPC requires HTTP/2.** Browser clients cannot use gRPC directly (gRPC-Web is a separate protocol with a proxy layer). If you have browser consumers, gRPC is an internal transport, not a public API.
- **REST and GraphQL are not exclusive.** Large platforms often serve a REST API for external partners (stable, versioned contracts) and GraphQL for internal frontend (flexible, schema-driven iteration).

## Pagination Patterns

### Cursor vs. Offset Trade-offs

**Offset pagination** (`?page=2&limit=20`, `?offset=40`):
- Simple to implement, intuitive for humans, supports random access ("go to page 10")
- **Breaks silently on concurrent writes**: if 5 rows are inserted after page 1 is fetched, page 2 starts 5 rows later in the result set — rows are skipped, not duplicated, with no error
- **Breaks on large offsets**: `OFFSET 100000` in SQL requires the database to scan and discard 100,000 rows; performance degrades with depth
- Acceptable for: static datasets (product catalogs, historical archives), user-facing paginated reports where the user pages through manually

**Cursor pagination** (`?cursor=<opaque_token>&limit=20`):
- Cursor anchors to a stable position (row ID, timestamp, composite key)
- Concurrent inserts/deletes do not affect positions relative to the cursor
- Cannot support random access ("jump to page 10") — only forward (and optionally backward) navigation
- Required for: feeds, activity streams, audit logs, any resource writable by concurrent processes during iteration
- **Cursor must be opaque to callers** — do not expose raw SQL offsets or timestamps as cursors; expose an opaque base64 token. This allows cursor implementation to change without breaking callers.

**Keyset pagination** is a variant of cursor where the position is based on indexed column values (e.g., `WHERE created_at < ? AND id < ?`). Use when sort order matters and you control the index.

### What Practitioners Get Wrong

- Choosing offset "for now" on a resource that accepts writes. The breakage is invisible in tests (tests don't write concurrently) and shows up as user-reported missing items in production feeds.
- Exposing cursor internals. A cursor like `?cursor=2024-05-01T12:00:00Z` couples callers to your sort implementation and breaks if you ever change the timestamp column type.
- Forgetting backward cursors. Most cursor implementations only go forward. If the product requires "go back," build `prev_cursor` from the start — retrofitting it changes the response schema.

## API Versioning Strategy

### URL vs. Header vs. Content Negotiation

**URL versioning** (`/v1/users`, `/v2/users`):
- Immediately visible; no special headers needed; easy to share URLs
- Creates permanent production branches — `/v1` must run indefinitely once published
- Encourages breaking changes by making them "cheap" (just bump `/v2`)
- Appropriate for: public APIs with diverse consumers who cannot control request headers (webhooks, third-party integrations, browser fetch without CORS pre-flight complexity)

**Header versioning** (`API-Version: 2024-01`, `X-API-Version: 2`):
- No URL pollution; single URL tree; version sunset without URL proliferation
- Not visible in browser address bar; harder to test manually; requires documentation
- Appropriate for: internal APIs, developer platforms where consumers control all request headers, APIs where sunset timelines are enforced

**Content negotiation** (`Accept: application/vnd.api+v2+json`):
- Standards-based; caches correctly (Vary header)
- Complex for consumers; rarely implemented correctly in practice
- Appropriate for: media APIs, hypermedia/HATEOAS APIs; almost never the right choice for standard JSON REST APIs

**Date-based header versioning** (used by Stripe, Anthropic) is the most sustainable pattern for high-churn APIs:
- Version string is a date: `API-Version: 2024-11-01`
- Each version is a snapshot of the API on that date
- Consumers pin to a version; new features ship as new version dates
- Breaking changes require a new date version; old dates run until sunset

### What Practitioners Get Wrong

- Versioning every release, not every breaking change. Versions are not release numbers. Non-breaking changes (additive fields, new optional params, new enum values) must not increment the version — this trains consumers to update version pins constantly and increases migration fatigue.
- Forgetting that "removing a field" is a breaking change even when the field was optional. Consumers who read the field get `undefined` after removal. Optional fields cannot be removed without a version bump.
- Adding URL versioning to a private internal API. Internal services can coordinate upgrades; they do not need permanent URL branches. Use header versioning or no versioning (coordinate rollout directly).

## Error Response Standardization

### RFC 7807 Problem Details

Use RFC 7807 (`application/problem+json`) as the standard error shape:

```json
{
  "type": "https://errors.example.com/invalid-input",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The request body contains invalid fields.",
  "instance": "/requests/abc123",
  "errors": [
    {
      "code": "INVALID_EMAIL",
      "field": "email",
      "detail": "The provided email address is not a valid format."
    }
  ]
}
```

**Required fields**: `type` (URI, dereferenceable or not), `title` (human, stable), `status` (mirrors HTTP status), `detail` (specific to this occurrence).

**The `errors` array extension** is not part of RFC 7807 base but is universally expected for validation errors. Always extend Problem Details with a machine-readable `errors` array for 422 responses.

### Status Code Taxonomy

| Situation | Correct Code | Common Wrong Code |
|-----------|-------------|-------------------|
| Validation error (bad input shape, invalid values) | **422 Unprocessable Entity** (RFC 4918) | 400 Bad Request |
| Malformed JSON / unparseable request body | 400 Bad Request | 422 |
| Not authenticated (no token, expired token) | 401 Unauthorized | 403 |
| Authenticated but lacks permission | 403 Forbidden | 401 |
| Resource not found | 404 Not Found | 200 with `null` body |
| Optimistic lock conflict / concurrent edit | 409 Conflict | 400 |
| Rate limit exceeded | 429 Too Many Requests | 400 or 503 |
| Downstream dependency unavailable | 503 Service Unavailable | 500 |
| Intentional temporary maintenance window | 503 with `Retry-After` | 500 |

**HTTP 422 for validation errors** is explicitly correct per RFC 4918. The common objection ("400 is simpler") is wrong: 400 means the server could not parse the request. 422 means the request was parsed, understood, and rejected due to semantic errors. These are different conditions. Monitoring dashboards, clients, and retry logic all benefit from the distinction.

### Error Code Taxonomy

Error codes must be:
- **Machine-parseable strings**: `INVALID_EMAIL`, not `"Email address is not valid"`
- **SCREAMING_SNAKE_CASE** (conventional, widely recognized)
- **Domain-scoped for large APIs**: `AUTH_TOKEN_EXPIRED`, `PAYMENT_CARD_DECLINED`, `USER_EMAIL_DUPLICATE`
- **Not sentences, not display strings** — the `detail` field carries the human message; `code` is for programmatic branching

Organize codes in tiers:
1. **Generic codes** (used by all endpoints): `VALIDATION_FAILED`, `NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `RATE_LIMIT_EXCEEDED`, `INTERNAL_ERROR`
2. **Domain codes** (resource-specific): `USER_EMAIL_DUPLICATE`, `ORDER_ALREADY_SUBMITTED`, `PAYMENT_INSUFFICIENT_FUNDS`
3. **Field-level codes** (in `errors[]` array): `INVALID_EMAIL`, `REQUIRED_FIELD_MISSING`, `VALUE_TOO_LONG`

### Retry Signal Conventions

| Code | Retryable? | Convention |
|------|-----------|------------|
| 429 | Yes, after backoff | Always include `Retry-After` header (seconds) |
| 503 | Yes, after backoff | Include `Retry-After` if duration is known |
| 502, 504 | Yes, immediate | Network/gateway errors; exponential backoff |
| 409 | Conditional | Re-fetch resource, re-apply change, retry |
| 422 | No | Validation error; retry without fixing input is pointless |
| 400, 401, 403, 404 | No | Client error; retry is identical to original failure |
| 500 | No (by default) | Internal server error; do not retry by default; operator should investigate |

## OpenAPI Spec Authoring

### Spec-First vs. Code-First

**Spec-first**: Write the OpenAPI spec before any implementation. Treat the spec as the source of truth. Implementation must match it.
- Use when: multiple consumers, cross-team coordination needed, public API, contract needs review/approval before dev starts
- Tooling: Swagger Editor, Stoplight Studio, Redocly
- Risk: spec drift if implementation deviates and spec is not updated

**Code-first**: Annotate code (decorators, docstrings); tooling generates the spec.
- Use when: solo developer, internal service, spec accuracy matters more than spec timing
- Tooling: FastAPI (Python), tsoa (TypeScript), Springdoc (Java)
- Risk: generated spec omits information code cannot express (intent, deprecation warnings, narrative descriptions)

**When spec-first is required** even if code-first is preferred:
- Any API with a partner or public consumer — they cannot wait for code to be written to see the contract
- Any API used by a frontend team that is developing in parallel — frontend needs types from the spec before backend is done

### Required Fields Practitioners Miss

In `paths`:
- `operationId` on every operation — without it, code generators use method+path as the function name, which is often unreadable
- `tags` on every operation — controls grouping in generated docs and SDK namespacing
- `summary` AND `description` — summary is one line for the table of contents; description carries nuance (state machine, error triggers, business rules)

In `components/schemas`:
- `description` on every property — a property named `status` with no description forces consumers to guess from example values
- `readOnly: true` on server-generated fields (IDs, timestamps) — without this, code generators include them in request bodies, allowing callers to attempt to set immutable fields
- `nullable: false` explicitly when a field is never null — prevents consumers from over-writing null handling

In `responses`:
- A response definition for **every** error status code the endpoint can return — not just 200 and a generic 4xx
- `default` response referencing a Problem Details schema — catches undocumented errors
- `headers` for `429` responses — document `Retry-After` and `X-RateLimit-*` headers here, not only in prose

In `security`:
- Specify security schemes at the operation level, not just globally, when endpoints have mixed auth (some public, some protected)

### Common OpenAPI Mistakes

- Defining all errors as `{ message: string }` in the spec, then returning RFC 7807 in implementation. The spec is wrong the day it ships.
- Using `additionalProperties: true` everywhere to avoid schema maintenance. This makes the spec useless as a contract — it permits any payload.
- Using `anyOf` where `oneOf` was intended. If only one variant is valid per request, use `oneOf` and add a `discriminator`.
- Omitting `format` on string fields that have known formats (`email`, `uri`, `date-time`, `uuid`) — validators and code generators use `format` to apply semantic validation.

## Breaking vs. Non-Breaking Change Classification

### What Practitioners Get Wrong

The common definition is: "breaking = removed field." The correct definition is: **a breaking change is any change that requires an existing well-behaved consumer to change their code.**

**Non-breaking (safe to ship without version bump)**:
- Adding a new optional field to a response (consumers ignore unknown fields if coded defensively)
- Adding a new optional query parameter
- Adding a new endpoint
- Adding a new enum value to a response field *if consumers are coded to handle unknown values* — this is the disputed case (see below)
- Relaxing a constraint (accepting a previously-invalid value)

**Breaking (requires version bump or migration path)**:
- Removing any field from a response, even an optional one
- Renaming a field
- Changing a field's type (string → number, string → string[])
- Changing a field's nullability (non-null → nullable, nullable → non-null)
- Adding a new **required** field to a request
- Removing or renaming a query parameter
- Changing the HTTP status code for a success response
- Tightening a constraint (rejecting a previously-valid value)
- Changing authentication scheme

**The disputed case: new enum values in responses**. Technically non-breaking (you added a value). In practice, breaking for consumers who use exhaustive switch statements or who validate response data against a known-values list. Treat new response enum values as breaking for any statically-typed consumer, or document explicitly that all enums are open-ended (consumers must handle unknown values).

**PATCH field removals are always breaking** — even if the field is optional. A consumer sending PATCH payloads with that field now sends an unknown field; behavior depends on server implementation (ignore vs. error).

## Rate Limiting Documentation

### Documenting Rate Limits in the OpenAPI Spec

Rate limits must appear in the spec — not only in prose documentation. Use response headers on every endpoint subject to rate limiting:

```yaml
responses:
  "200":
    headers:
      X-RateLimit-Limit:
        schema:
          type: integer
        description: Maximum requests allowed in the current window.
      X-RateLimit-Remaining:
        schema:
          type: integer
        description: Requests remaining in the current window.
      X-RateLimit-Reset:
        schema:
          type: integer
          format: int64
        description: Unix timestamp (seconds) when the window resets.
  "429":
    headers:
      Retry-After:
        schema:
          type: integer
        description: Seconds to wait before retrying.
    content:
      application/problem+json:
        schema:
          $ref: "#/components/schemas/ProblemDetails"
```

Document rate limit scope explicitly in endpoint descriptions:
- Per user? Per API key? Per organization? Per IP?
- Token bucket (burst allowed) or fixed window (no burst)?
- Separate limits per endpoint or global account limit?

### What Practitioners Get Wrong

- Documenting rate limits only in a separate "limits" guide page, not in the spec. Consumers encounter 429 before they find the guide.
- Omitting `Retry-After` on 429 responses. Without it, consumers implement arbitrary backoffs (usually too short or too long).
- Using the same rate limit scope for bulk and single-item endpoints. A `POST /bulk-import` (100 records/request) and `POST /records` (1 record/request) should not share the same per-request limit.

## Auth Scheme Selection in OpenAPI

### Bearer (JWT / opaque tokens)

```yaml
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT  # Informational only; not validated by tooling
```

Use for: user-facing APIs, APIs with short-lived session tokens, anywhere you need to embed claims without a database lookup.

Document explicitly:
- Token location (always `Authorization: Bearer <token>` for `http` scheme — but confirm no cookie fallback)
- Token lifetime and refresh flow
- What 401 means (token absent or expired) vs. 403 (token valid, permission denied)

### API Key

```yaml
components:
  securitySchemes:
    ApiKeyHeader:
      type: apiKey
      in: header
      name: X-API-Key
```

Use for: server-to-server, webhook consumers, partner integrations where user identity is not relevant.

`in` can be `header`, `query`, or `cookie`. **Prefer `header`** — API keys in query strings appear in server logs, browser history, and referrer headers.

### OAuth2

```yaml
components:
  securitySchemes:
    OAuth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          scopes:
            read:users: Read user profiles
            write:users: Create and update users
```

**Flow selection**:
| Consumer | Correct Flow |
|----------|-------------|
| Browser SPA or mobile app | `authorizationCode` with PKCE (no client secret) |
| Server-side web app | `authorizationCode` (can store client secret) |
| Machine-to-machine / service account | `clientCredentials` |
| Legacy / resource owner password flow | Avoid; `password` flow is deprecated in OAuth 2.1 |

**What practitioners get wrong**:
- Using `clientCredentials` for user-delegated access. Client credentials authenticate the application, not a user. No user identity or user-scoped permissions are in the token.
- Omitting `scopes` from the spec. Undocumented scopes force consumers to reverse-engineer required permissions from 403 errors.
- Using the `implicit` flow. It is deprecated in OAuth 2.1 and has known security weaknesses. Use `authorizationCode` + PKCE for SPAs.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Frontend reports missing items in paginated feed | Offset pagination on a writable resource | Migrate to cursor; add `next_cursor`/`prev_cursor` to response; deprecate `page`/`offset` params with a version sunset |
| Consumer cannot distinguish "field absent" from "field null" in PATCH | PATCH implementation does not differentiate | Define explicit null semantics in spec: document that absent = no-op, null = clear; enforce in validation layer |
| Multiple clients broken after adding a new enum value to response | Clients use exhaustive switch/match without default branch | Document all response enums as "open-ended"; add a breaking-change note to changelog; publish migration guide |
| Monitoring shows 100% success rate during outage | Errors returned as 200 with error body | Find all endpoints returning `success: false`; change to correct 4xx/5xx; this is always a breaking change — version accordingly |
| Rate limit scope is wrong (org-level limit but should be per-user) | Limit designed without multi-tenant analysis | Change scope; this is a behavioral breaking change; notify consumers before rollout |
| OpenAPI spec and implementation diverge over time | Code-first tooling not run as part of CI | Add spec regeneration to CI pipeline; fail CI on spec diff |

## Workflow

1. **Confirm protocol** — use the decision criteria table; document the rationale in the spec's `info.description`
2. **Define pagination strategy** — is any resource mutable during iteration? Yes → cursor required
3. **Define versioning policy** — document it in `info.description` before the first endpoint is designed
4. **Define error schema** — add a `ProblemDetails` component schema; reference it in every error response
5. **Author spec** — spec-first if consumers are parallel; code-first if solo/internal
6. **Classify each design decision** — for each field/endpoint, note whether future changes would be breaking
7. **Document rate limits** — every rate-limited endpoint gets response headers documented in spec
8. **Review auth scheme** — confirm flow type for each OAuth2 usage; confirm key location for API key auth

**Natural next steps after this skill**:
- `openapi-to-typescript` — generate TypeScript interfaces from the completed spec for frontend consumers
- `backend-to-frontend-handoff-docs` — after implementation, generate consumer-facing behavioral documentation
- `requirements-clarity` — if design reveals unresolved requirement gaps, return upstream
