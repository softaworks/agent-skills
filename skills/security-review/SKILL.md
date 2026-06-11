---
name: security-review
version: 1.0.0
description: "Security-aware review layer for engineering artifacts — React/frontend XSS vectors, database schema access control and encryption decisions, OpenAPI securitySchemes and scope design, TypeScript runtime type guard failures, and dependency supply-chain hygiene. Use when asked to security-review code, audit for vulnerabilities, check for XSS, review auth patterns, check JWT validation, audit npm dependencies, or add security hardening. Pairs with react-dev, database-schema-designer, and openapi-to-typescript."
---

# Security Review

Security findings have no middle ground: either the attack path exists or it does not. The job is to determine which.

## Mindset

1. **Exploitability, not CVE score.** A critical-severity CVE in a library you call with no user-controlled input is a zero-risk finding in your codebase. A medium-severity finding in an input path exposed to the public internet is your highest-priority work. Always trace the data path from user input to the vulnerable sink before assigning severity.
2. **React escapes JSX — but not href, src, or dangerouslySetInnerHTML.** React's JSX interpolation escapes HTML entities in text content. It does NOT sanitize `href` (javascript: injection), `src` (data: injection), or anything passed to `dangerouslySetInnerHTML`. These three vectors are the most commonly missed XSS surface in React codebases because developers trust "React handles escaping."
3. **ORM parameterization has intentional escape hatches — and they are the injection vectors.** Prisma `$queryRaw`, Sequelize `literal()`, and TypeORM `createQueryBuilder().where(rawString)` all bypass parameterization by design. Every ORM raw escape hatch in a codebase is a mandatory review target.
4. **JWT signature verification is not JWT validation.** A verified signature proves the token was signed with the correct key. It does not validate that the token has not expired (`exp`), was issued at a sane time (`iat`), is intended for this audience (`aud`), or came from the expected issuer (`iss`). Most JWT libraries default to silent-pass on missing claims — absence of `exp` does not trigger an error, it produces an immortal token.
5. **TypeScript types are compile-time assertions, not runtime enforcement.** A `User` type with no `isAdmin` property does not prevent `req.body.isAdmin = true` from reaching a database write. Mass assignment attacks bypass the type system entirely because types are erased at runtime. Explicit allowlist validation at the controller layer is required regardless of TypeScript strictness.
6. **Non-exploitable findings still require grading.** A non-exploitable XSS today can become exploitable with one future code change, one new dependency, or one route added to the application. Mark the finding with its current exploitability status and the condition that would activate it — do not discard it.

## Navigation

**Use this skill when:**
- Auditing React components or frontend code for XSS, CSRF, or injection vectors
- Reviewing database schemas for access control, encryption at rest, and audit logging gaps
- Reviewing OpenAPI specs or API contracts for auth scope design and sensitive data exposure
- Auditing TypeScript code for runtime type assertion failures masking security assumptions
- Reviewing npm dependencies for supply chain risk, provenance, and audit findings
- Adding security hardening to any engineering artifact produced by another skill

**Do NOT use this skill when:**
- Designing new features without an existing artifact to review (use the appropriate engineering skill first)
- Network-layer or infrastructure security (firewall rules, VPC design, TLS configuration) — these require infrastructure-specific context outside this skill's scope

**Cross-skill routing:**
- Working on a database schema with RLS, encryption, or audit log requirements? Use **database-schema-designer** for schema modeling first, then return here for security validation of the resulting schema.
- Reviewing or writing React components? Use **react-dev** for type-safe component patterns, then apply this skill to audit the resulting components for XSS vectors and CSP alignment.
- Designing or consuming an OpenAPI spec? Use **openapi-to-typescript** for type generation and client scaffolding, then apply this skill to audit securitySchemes, scope granularity, and error response exposure.

## Coverage Areas

### React / Frontend

**XSS Vectors to inspect in every React review:**

| Vector | Pattern | Risk |
|--------|---------|------|
| `dangerouslySetInnerHTML` | `<div dangerouslySetInnerHTML={{ __html: userInput }} />` | Direct DOM injection; sanitize with DOMPurify before assignment |
| `href` injection | `<a href={userInput}>` | `javascript:alert(1)` executes on click; validate `href` starts with `https://` or `/` |
| `src` injection | `<img src={userInput} />` | `data:` URIs can exfiltrate via CSP-bypass in some browsers; validate against an allowlist |
| `innerHTML` via `ref` | `ref.current.innerHTML = userInput` | Bypasses React's escaping entirely; use `textContent` or sanitize |
| `eval` / `new Function` | Template rendering, i18n interpolation | Remote code execution if user input reaches these; audit i18n library interpolation syntax |

**CSP header design checklist:**
- `default-src 'self'` as baseline — no wildcard origins
- `script-src` must not include `'unsafe-inline'` or `'unsafe-eval'` in production; use nonces or hashes
- `connect-src` allowlist must match actual API domains — overly broad `*` negates exfiltration protection
- `frame-ancestors 'none'` or specific allowlist to prevent clickjacking

**CSRF token patterns:**
- SameSite=Strict cookies eliminate CSRF for browser-initiated requests but break cross-origin OAuth flows
- SameSite=Lax cookies protect state-changing GET requests; POST requires a separate CSRF token
- Double-submit cookie pattern: send token in both cookie and header; server validates they match

**Supply chain (frontend):**
- `npm audit` identifies known CVEs; it does NOT identify exploitable paths — grade each finding by whether user-controlled input reaches the vulnerable function in that library
- Subresource Integrity (SRI) hashes on CDN-loaded scripts prevent compromise via CDN hijacking
- Pin exact versions in `package-lock.json`; `^` and `~` ranges allow automatic minor/patch upgrades that can introduce regressions silently

### Database Schemas

**Row-Level Security (PostgreSQL RLS):**
- `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` alone does nothing — you must also create `POLICY` definitions
- Default-deny: with RLS enabled and no policies, the table owner bypasses RLS; all other roles see zero rows
- Multi-tenant SaaS pattern: `CREATE POLICY tenant_isolation ON orders USING (tenant_id = current_setting('app.tenant_id')::uuid)` — set `app.tenant_id` at connection time via `SET LOCAL`
- Never use `SECURITY DEFINER` functions to bypass RLS without explicit audit — they run as the function owner, not the calling user

**Encryption at rest decisions:**
- Column-level encryption (pgcrypto, application-layer) for PII fields (SSN, payment card, health data) — full-disk encryption does not protect against compromised application credentials
- Key rotation: encrypted columns require a migration strategy for re-encryption; design the key reference (key version ID stored alongside ciphertext) before first write
- Never store encryption keys in the same database as encrypted data

**Audit logging hooks:**
- Trigger-based audit log: `CREATE TRIGGER audit_users AFTER INSERT OR UPDATE OR DELETE ON users FOR EACH ROW EXECUTE FUNCTION log_change()` — captures who changed what and when at the database layer, immune to application bypass
- Include `session_user`, `current_timestamp`, old and new row snapshots
- Write audit logs to a separate schema with restricted DELETE privileges — the application role that writes data must not be able to delete its own audit trail

**SQL injection via ORMs:**
- Prisma: `$queryRaw` is safe with tagged template literals (`$queryRaw\`SELECT * FROM users WHERE id = ${id}\``); `$queryRawUnsafe(string)` is not — it concatenates the string directly
- Sequelize: `Model.findAll({ where: sequelize.literal(userInput) })` — `literal()` is an injection vector; use `Op` operators instead
- TypeORM: `createQueryBuilder().where(rawString, params)` is safe if params are bound; `.where(\`status = '${userInput}'\`)` is a direct injection vector
- Knex: `.whereRaw(string)` with no bindings is an injection vector; use `.whereRaw('status = ?', [userInput])`

### API Contracts (OpenAPI)

**securitySchemes completeness:**
- Every operation must reference a security scheme or explicitly declare `security: []` (public endpoint) — undeclared security means the spec is incomplete, not that the endpoint is secure
- OAuth2 scopes must map to actual permission boundaries — broad scopes (`write:all`) indicate mass-assignment risk at the server; scope granularity should match resource-level operations
- API key schemes: document whether keys are per-user, per-app, or per-environment — ambiguity leads to over-privileged keys shared across environments

**OWASP API Security Top 10 2023 — the API-specific list:**
1. Broken Object Level Authorization (BOLA) — verify caller owns the resource, not just that they are authenticated
2. Broken Authentication — JWT validation completeness (see JWT section), token rotation, refresh token storage
3. Broken Object Property Level Authorization — mass assignment; ensure write operations accept only explicitly allowlisted fields
4. Unrestricted Resource Consumption — rate limiting, pagination limits, max request body size
5. Broken Function Level Authorization — admin endpoints accessible to regular users
6. Unrestricted Access to Sensitive Business Flows — bot-driven abuse of legitimate flows (account creation, checkout)
7. Server-Side Request Forgery (SSRF) — any URL parameter passed to a server-side fetch
8. Security Misconfiguration — default credentials, CORS `*`, missing security headers
9. Improper Inventory Management — shadow APIs, deprecated versions still reachable
10. Unsafe Consumption of APIs — insufficient validation of data received from third-party APIs

**Sensitive field exposure in error responses:**
- Stack traces in 500 responses expose file paths, library versions, and internal architecture — disable in production
- Validation error messages that mirror field names exactly help attackers enumerate valid fields
- `WWW-Authenticate` response headers on 401s should not reveal the auth scheme implementation details beyond what is required by RFC 7235

### TypeScript Runtime Safety

**Runtime type guard failures masking security assumptions:**
```typescript
// UNSAFE — TypeScript trusts the assertion; at runtime, body is whatever the client sends
function handleUpdate(body: UpdateUserRequest) {
  db.update(body); // mass assignment: body.isAdmin reaches the DB
}

// SAFE — explicit allowlist at controller layer
function handleUpdate(rawBody: unknown) {
  const body = UpdateUserSchema.parse(rawBody); // Zod/Valibot validates shape and types
  db.update({ name: body.name, email: body.email }); // explicit field selection
}
```

**Unsafe type assertions hiding injection vectors:**
- `as unknown as SafeQuery` double assertions are a code smell — they usually mean the developer knows the type is wrong but wants to suppress the error; audit the data provenance before each one
- `!` non-null assertions on user-provided data (`req.params.id!`) are a runtime crash waiting to happen and potentially an injection vector if the value flows to a database query
- Type predicates (`function isUser(x: unknown): x is User`) without runtime checks are as dangerous as `as User` — the predicate function must actually validate the shape

**Dependency hygiene (TypeScript projects):**
- SBOM generation: `npm sbom --sbom-format=spdx` (npm ≥ 9.7) or `syft . -o spdx-json` to produce a Software Bill of Materials for auditing and compliance
- npm provenance verification: packages published with provenance attestation (`--provenance` flag, npm ≥ 9.5) link the package to the source commit — prefer provenance-attested packages for critical dependencies
- Package name typosquatting detection: inspect `npm install` output for packages you did not intend to install; use `npm query ":root > .prod` to list only production dependencies and audit each name against the intended package list
- Lock file integrity: `package-lock.json` should be committed and its integrity hashes should be verified in CI (`npm ci` enforces this; `npm install` does not)

## NEVER

- **NEVER mark a security finding as informational without verifying the actual attack path** — a non-exploitable XSS today becomes exploitable with one future code change, one new dependency, or one route addition. Document the finding with its current exploitability status and the activation condition.
- **NEVER approve a JWT validation implementation that checks only the signature** — `exp`, `iat`, `aud`, and `iss` validation are equally required. A signed token with no `exp` is an immortal credential. Most JWT libraries do not throw on missing claims by default; these checks must be explicit.
- **NEVER allow raw SQL strings built from user input even inside a transaction** — a transaction provides atomicity, not injection protection. Parameterize at the query-builder level regardless of transaction context.
- **NEVER treat `npm audit --fix` as a security review** — `--fix` resolves dependency versions without verifying whether the vulnerability is reachable in your codebase or whether the version bump introduces breaking changes. It is a maintenance tool, not a security assessment.
- **NEVER expose stack traces or internal error details in production API error responses** — stack traces are reconnaissance data. They reveal file paths, library versions, internal class names, and architecture. Return opaque error IDs to clients; log full details server-side only.
- **NEVER skip `aud` validation on JWTs because "we only have one service"** — audience validation prevents token reuse across services when the architecture grows. Retrofitting `aud` validation after multiple services exist requires coordinated token migration. Enforce it from day one.
- **NEVER assume TypeScript strictness prevents mass assignment** — TypeScript types are erased at runtime. `req.body` is `any` at the HTTP boundary regardless of what the handler's parameter type says. Validate and allowlist at the boundary.

## Severity Grading

| Finding | Exploitability Assessment | Grade |
|---------|--------------------------|-------|
| `dangerouslySetInnerHTML` with user input, no sanitization | Direct: user input → DOM | Critical |
| `href={userInput}` without validation | Direct: `javascript:` URI | High |
| JWT missing `exp` validation | Direct: immortal tokens if issued without exp | High |
| ORM raw query with user string concatenation | Direct: SQL injection | Critical |
| `npm audit` high-severity CVE | Requires tracing actual call path — do not grade as High without confirming user input reaches the vulnerability | Needs triage |
| RLS enabled with no policies | Direct: all non-owner rows exposed | Critical |
| Stack trace in 500 response | Indirect: reconnaissance enables targeted attacks | Medium |
| Missing `aud` claim validation | Conditional: exploitable only when multiple services share signing key | Medium (document activation condition) |

## When Things Go Wrong

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| XSS fires despite React | `dangerouslySetInnerHTML`, `href`, or `src` bypassed React escaping | Sanitize with DOMPurify; validate URL schemes; never use `dangerouslySetInnerHTML` with unsanitized input |
| JWT accepted after expiry | `exp` not validated or library defaults to ignore missing `exp` | Explicitly set `ignoreExpiration: false`; verify library docs for default claim validation behavior |
| ORM query returns wrong tenant's data | Missing RLS policy or parameterization bypassed via raw query | Enable and test RLS policies; replace `literal()`/`$queryRawUnsafe` with parameterized equivalents |
| Mass assignment overwrites protected field | TypeScript type used as runtime validation | Add Zod/Valibot schema at controller boundary; explicit field allowlist before DB write |
| npm audit clean but supply chain incident | Typosquatted package or compromised transitive dep | Enable npm provenance verification; pin transitive deps in lock file; generate SBOM and audit against known-good list |
| API returns stack trace in production | Error middleware not stripping internals | Implement production error handler that returns `{ error: errorId }` only; log full trace server-side |

<!-- INJECT:B5:credential-rotation -->
<!-- Source: awesome-claude-code-subagents (MIT) — security-engineer.md (pattern-extracted, not verbatim) -->
## Track B / B5 — SOAR connector credential rotation & threat model
Per-connector rotation checklist, API-scope (least-privilege) audit, and a STRIDE-lite SOAR-platform threat model. Full reference: `~/soar/splunk-soar-base/knowledgebase/connector-credential-rotation.md`. Highest-value control: dual-approval gate on every destructive Tier 0/1 action.
