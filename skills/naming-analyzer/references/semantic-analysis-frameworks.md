# Semantic Analysis Frameworks for Naming

## The Command-Query Separation (CQS) Name Test

Every function name should pass CQS: it either reads state (query) or changes state (command) — never both.

| Name | Passes CQS? | Fix |
|------|------------|-----|
| `getUser()` — but also updates lastLogin | FAIL | `fetchUserAndRecordLogin()` |
| `isValid()` — but logs to analytics | FAIL | `validate()` + separate `logValidationAttempt()` |
| `saveAndReturn()` | FAIL by design | split or rename to `persist()` |
| `calculateTotal()` — pure computation | PASS | keep |
| `setActive()` — sets flag | PASS | keep |

## Leaky Abstraction Detection

Names that reveal implementation details that the caller shouldn't know:

```
getFromRedis()        → fetchFromCache()     (caller shouldn't know storage layer)
saveToMongo()         → persist()            (same)
parseXMLResponse()    → parseResponse()      (if format may change)
callStripeAPI()       → chargeCard()         (caller shouldn't know vendor)
```

Exception: when the implementation IS the interface (e.g., a Redis adapter class named `RedisCache`).

## Temporal Coupling in Names

Names that imply ordering are often a code smell:

```
initThenProcess()     → smell: two steps coupled in one name
step1(), step2()      → smell: positional, brittle
beforeSave()          → smell: lifecycle hook mixed with logic
```

Better: Extract each step, name for what it does, let the caller sequence them.

## Abstraction Level Mismatch

Names should operate at a single abstraction level. Mixed-level names signal design problems:

```python
# Mixed: business concept + implementation detail
def create_user_and_send_welcome_email_via_sendgrid(user_data): ...

# Better: two functions at their own level
def create_user(user_data): ...
def send_welcome_email(user): ...  # internally uses sendgrid
```

## The Newspaper Test for Names

Read just the function/class names in a file — they should tell a coherent story to someone unfamiliar with the codebase. If a reader must open function bodies to understand what the module does, the names have failed.

## Scope-Length Heuristic (Practitioner Rule)

Scope length determines acceptable name brevity:

| Scope | Max acceptable abbreviation |
|-------|----------------------------|
| 1-line lambda | `x`, `e`, `_` OK |
| 5-line loop body | `i`, `k`, `err` OK |
| 20-line function | `usr`, `cfg` borderline |
| Module/class level | Full words required |
| Public API / exported | Full words + domain context required |

## The "Diff Readability" Test

Before suggesting a rename, ask: will this name make git diffs easier or harder to read?

- `data` → `apiResponse`: diff is clearer (context visible in hunks)
- `userConfigurationSettings` → `userCfgSettings`: diff is harder (the length was adding nothing)
- `e` → `error` in a module-level handler: diff is much clearer

Optimal name length = maximum clarity at the scope where it's read, not where it's defined.

## Anti-Pattern Catalog: Names That Seem Fine But Aren't

| Name | Hidden Problem |
|------|---------------|
| `Manager` suffix | Signals the class does too much; "manages" is not a behavior |
| `Helper` / `Utils` | Dumping ground; hides that no real abstraction exists |
| `process()` | Infinitely vague; every function "processes" something |
| `handle()` | Same — event handlers that grow into 200-line methods all started as `handle()` |
| `do_thing()` | `do_` prefix adds no information |
| `flag`, `status`, `mode` | Enums/booleans that should be named by what they represent |
| `current` prefix | `currentUser` vs `user` — "current" is always implicit in method scope |
| `new_` prefix | `new_value` — signals a refactor halfway done; merge or rename |
| `_v2` suffix | `UserService_v2` — versioning belongs in modules, not class names |
| `temp`, `tmp` | If it's still called `temp` in the final commit, it's not temp |
