---
name: backend-to-frontend-handoff-docs
description: Generate API handoff documentation for frontend developers after backend work is complete. Use when backend implementation is done and needs to be documented for frontend integration. Trigger phrases: 'create handoff', 'document API', 'frontend handoff', 'API documentation', 'document endpoints for frontend'.
---

## Mindset

**You are writing a contract, not a tutorial.** Frontend developers (and their AI) should be able to implement integration with zero questions after reading this document. Every omission creates a Slack message, a meeting, or a bug.

- **Asymmetry of pain**: The frontend developer discovers your omission at 4 PM on release day. Document what you know right now, even if it feels obvious.
- **Business logic leaks through the API**: If the backend enforces "a user can only submit once per 24-hour window per org," that rule must appear in the handoff — not just the HTTP 429 it produces. Frontend needs to disable the button, not just handle the error.
- **Error taxonomy beats status codes**: "Returns 422" tells frontend nothing. "Returns 422 with `{code: 'duplicate_submission', retryAfter: 86400}` when..." tells them how to build the error message.
- **Enums drift**: If the backend adds a new status mid-iteration and the handoff is stale, frontend silently mishandles it. Flag all enums as exhaustive or open-ended explicitly.
- **Auth is a contract, not an afterthought**: Document the token location (header vs cookie), the exact scope/role string, and what happens on expiry — not just "auth required."

## Navigation

**Use this skill when**:
- Backend API implementation is complete (endpoints, DTOs, validation, business logic done)
- A feature involves frontend integration that spans teams or AI agents
- API contracts changed and frontend needs a delta of what broke

**Do NOT use this skill when**:
- Backend work is still in progress — a premature handoff becomes a liability when contracts change
- The API is internal backend-to-backend (microservices, queue consumers)
- Frontend already has a Swagger/OpenAPI spec auto-generated from annotations — extend that instead of creating parallel docs

**Quick decision: full doc vs. shortcut**

| Signal | Action |
|--------|--------|
| CRUD endpoint, obvious field names, no business rules | Shortcut: endpoint + example JSON only |
| Any business logic, non-obvious validation, or state machine | Full template (see `references/TEMPLATE.md`) |
| Multiple related endpoints with shared DTOs | Full template; group by user flow, not by HTTP verb |

## Philosophy

The handoff document is the API's *behavioral specification from the consumer's perspective*. It is not a description of what the backend does internally — it is a precise description of what the frontend can rely on, what it cannot assume, and what it must handle.

## NEVER

- **NEVER document internal class names, service layer names, or file paths** — because frontend contracts break when backend refactors, and internal names create cargo-cult coupling where frontend assumes structure that will change.
- **NEVER write "see code for details"** — because the handoff's entire purpose is to eliminate the need to read backend code. Any reference to source is an admission of failure.
- **NEVER use `any` or vague types like `object` in DTO examples** — because frontend TypeScript inference collapses to `any`, nullability bugs appear at runtime, and discriminated union narrowing is impossible without exact types.
- **NEVER omit the error response shape** — because frontend error handling almost always branches on the error body (`code`, `message`, `field`), not just on the HTTP status. A 422 with no documented body forces frontend to `console.log` in production.
- **NEVER document validation rules as "see frontend" or "same as UI"** — because backend validation is authoritative; frontend mirrors it for UX only. If the handoff doesn't list backend constraints, frontend re-derives them from HTTP errors at the worst possible time.
- **NEVER describe auth as "token required"** — because "token" is ambiguous across Bearer, cookie, API key, and session schemes. Document the exact header name, token format, scope string, and the HTTP status returned on auth failure (401 vs 403 mean different things).
- **NEVER omit nullability** — because `field?: string` (absent) vs `field: string | null` (present-but-null) are different serialization contracts. Frontend optional chaining fails differently on each, and the bug is invisible until edge data hits.
- **NEVER ship a handoff without at least one concrete example payload per endpoint** — because abstract field descriptions ("string, the user's name") are interpreted differently by every reader. A real example is unambiguous.
- **NEVER use "TBD" as a placeholder in a shipped handoff** — because frontend will assume TBD means "not my problem" and ship without handling that case. If it's genuinely unresolved, make it a blocking `## Open Questions` item with an owner and deadline.
- **NEVER generate the handoff before verifying that the actual implementation matches the docs** — because copy-pasting from a spec that was written before implementation is the #1 source of handoff drift. Read the actual controller/route handler before writing the response shape.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Frontend says "we're getting a different response shape than documented" | Handoff written from spec, not from live code | Re-read the actual handler/serializer; update handoff; increment version suffix |
| Frontend asks "what does status X mean?" | Enum listed without business meaning or display label | Add `Meaning` and `Display Label` columns to enum table; see `references/TEMPLATE.md` |
| Frontend asks "when do we get a 401 vs 403?" | Auth section only said "auth required" | Document exact condition for each: 401 = not authenticated, 403 = authenticated but lacks role/scope |
| Handoff is already v4 and frontend still has questions | Business logic section is absent or too thin | Write a dedicated state machine table for multi-status workflows; move endpoint docs to secondary |
| Handoff is 2000 lines and nobody reads it | Full template applied to trivial CRUD | Use the shortcut path; inline the example JSON; drop sections that add no information |

## Workflow

1. **Read the actual implementation** — controller/route handler, DTO/schema, middleware. Do not rely on memory or spec.
2. **Classify complexity** — use the Navigation decision table to pick full vs. shortcut path.
3. **Fill the template** — see `references/TEMPLATE.md` for the full document scaffold.
4. **Write to file** — save to `.claude/docs/ai/<feature-name>/api-handoff.md`. Use `-v2`, `-v3` suffixes for iterations.
5. **Verify before saving** — every field name, type, and status code must match the live implementation.

**Output rule**: Write the markdown directly to the file. Do not echo it in chat. Reference the file path in your response only.

If the project has an OpenAPI spec, recommend openapi-to-typescript to the frontend team as an alternative to hand-reading the handoff doc — it generates typed interfaces directly from the spec.

## Reference Files

- `references/TEMPLATE.md` — Full handoff document scaffold with all sections
