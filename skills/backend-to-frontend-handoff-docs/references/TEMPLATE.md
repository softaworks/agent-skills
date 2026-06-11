# API Handoff Template

Use this scaffold for full handoffs (complex business logic, state machines, non-trivial validation).
For simple CRUD, use the shortcut: endpoint + example JSON + error codes only.

---

```markdown
# API Handoff: [Feature Name]
**Version**: v1 | **Date**: YYYY-MM-DD | **Backend author**: [name/handle]

## Business Context
[2–4 sentences: What problem does this solve? Who is the user? What domain terms does frontend need? What invariants does the backend enforce that frontend must understand?]

---

## Endpoints

### [METHOD] /path/to/endpoint

- **Purpose**: [One line: what this endpoint does from the consumer's perspective]
- **Auth**: [Exact header: `Authorization: Bearer <jwt>` with scope `expenses:approve`] OR [`public`]
  - 401 → not authenticated (redirect to login)
  - 403 → authenticated but lacks role `manager` (show permission error, do not retry)
- **Request**:
  ```json
  {
    "field": "value — type, constraints (e.g., required, max 500 chars, must match /^[A-Z]{2}$/)"
  }
  ```
- **Response** (200/201):
  ```json
  {
    "field": "value — type, nullability (e.g., string | null), meaning"
  }
  ```
- **Response** (error):
  | Status | Condition | Body shape |
  |--------|-----------|------------|
  | 400 | Malformed JSON | `{"error": "bad_request"}` |
  | 422 | Validation failure | `{"errors": [{"field": "amount", "code": "too_large", "message": "..."}]}` |
  | 409 | Duplicate submission within window | `{"code": "duplicate_submission", "retryAfter": 86400}` |
  | 404 | Resource not found or soft-deleted | `{"error": "not_found"}` |
- **Notes**: [Rate limits, pagination cursor vs. offset, idempotency key, ordering guarantees, anything non-obvious]

[Repeat block for each endpoint]

---

## Data Models / DTOs

```typescript
// Exact TypeScript shape frontend should use for typing
interface ExampleDto {
  id: number;                          // always present
  status: 'pending' | 'approved' | 'rejected'; // exhaustive — no other values
  comment: string | null;              // present-but-null when no comment (not absent)
  createdAt: string;                   // ISO 8601 UTC, e.g. "2026-01-18T10:30:00Z"
  approvedBy?: {                       // absent (not null) when status !== 'approved'
    id: number;
    displayName: string;
  };
}
```

**Nullability conventions used in this API**:
- `field?: T` — key absent from response (use `?.` access)
- `field: T | null` — key present, value null (use `=== null` check)

---

## Enums & Constants

| Value | Meaning | Display Label | Terminal? |
|-------|---------|---------------|-----------|
| `pending` | Submitted, awaiting review | Pending | No |
| `approved` | Approved by manager | Approved | Yes |
| `rejected` | Rejected by manager | Rejected | Yes |

**Is this enum exhaustive?** YES — backend will not add values without a major version bump.
(If NO: frontend must handle unknown values gracefully, e.g., display as "Unknown status".)

---

## Validation Rules

Frontend should mirror these for UX (backend enforces them authoritatively):

| Field | Rule | UX implication |
|-------|------|----------------|
| `amount` | Required, positive number, max 2 decimal places, ≤ 10000 | Show currency input; cap at 10,000; disable submit if 0 |
| `comment` | Optional, max 500 chars, trimmed | Show character counter at 400+ chars |
| `category` | Required, must match enum values | Dropdown, not free text |

---

## Business Logic & State Machine

[Use when the feature has meaningful state transitions. Skip for stateless CRUD.]

```
pending ──[approve]──► approved (terminal)
pending ──[reject]───► rejected (terminal)
```

- **Transition rules enforced by backend** (frontend must handle the error, not prevent the action client-side):
  - Only users with role `manager` can approve/reject
  - Cannot approve own submissions
  - Terminal states cannot transition (422 with `code: already_finalized`)
  - Approval window: must occur within 30 days of submission (422 with `code: window_expired`)

---

## Integration Notes

- **Recommended flow**: [e.g., "Fetch list (GET /expenses) → select item → open modal → POST /expenses/:id/approve → refresh list item via GET /expenses/:id"]
- **Optimistic UI**: [SAFE / NOT SAFE — reason. "Not safe: permission checks on approve depend on server-side role resolution."]
- **Caching**: [e.g., "List response includes `Cache-Control: max-age=30`. Invalidate on POST/PATCH to this resource."]
- **Real-time**: [e.g., "No websocket. Poll GET /expenses/:id every 5s while status=pending if you need live updates."]
- **Pagination**: [cursor-based: `?cursor=<opaque_string>&limit=25` | offset-based: `?page=1&pageSize=25` | none]

---

## Test Scenarios

Cover these in frontend integration tests or manual QA:

1. **Happy path**: [e.g., "Manager approves pending expense → 200 → UI shows 'Approved' badge"]
2. **Validation error**: [e.g., "Submit with amount=0 → 422 → show inline field error"]
3. **Auth failure**: [e.g., "Non-manager clicks approve → 403 → show 'Permission denied' toast, do not navigate away"]
4. **Conflict**: [e.g., "Approve already-approved expense → 422 `already_finalized` → show 'Already processed' message"]
5. **Not found**: [e.g., "Fetch deleted expense → 404 → redirect to list with 'Item no longer available' message"]

---

## Open Questions / TODOs

| Question | Owner | Deadline |
|----------|-------|----------|
| [e.g., "Should partial approvals be supported in Q2?"] | [PM name] | [date] |

[Omit section entirely if none.]
```

---

## Shortcut Template (Simple CRUD)

For endpoints with no business logic, obvious field names, standard CRUD semantics:

```markdown
# API Handoff: [Feature Name] (Minimal)

### GET /api/users/:id
- **Auth**: Bearer token required (any authenticated user)
- **Response** (200):
  ```json
  { "id": 1, "email": "user@example.com", "displayName": "Jane Smith", "avatarUrl": "https://..." }
  ```
- 404 if user not found or soft-deleted.
```
