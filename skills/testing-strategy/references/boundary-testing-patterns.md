# Boundary-Value Testing Patterns by Data Type

Bugs live at boundaries. This is not a heuristic — it is a documented empirical finding across software testing research going back to Myers (1979). For every conditional in business logic, test n-1, n, and n+1 around every threshold.

## Numeric Boundaries

| Scenario | Test Values |
|----------|------------|
| `age >= 18` | 17, 18, 19 |
| `quantity > 0` | -1, 0, 1 |
| `amount <= 1000` | 999, 1000, 1001 |
| `0 <= score <= 100` | -1, 0, 1, 99, 100, 101 |
| Integer overflow | MAX_INT - 1, MAX_INT, MAX_INT + 1 |
| Float precision | 0.1 + 0.2 (not 0.3), values near epsilon |

## String Boundaries

| Scenario | Test Values |
|----------|------------|
| Required field | empty string `""`, whitespace-only `"   "`, one char `"a"` |
| Max length (e.g., 255) | 254 chars, 255 chars, 256 chars |
| Email format | `a@b.c` (minimal valid), no `@`, double `@`, trailing dot |
| URL | `http://`, `https://`, missing protocol, localhost |
| Encoding | ASCII-safe string, Unicode (emoji, CJK), null byte `\0`, SQL injection payload |

## Collection/Array Boundaries

| Scenario | Test Values |
|----------|------------|
| Non-empty check | `[]`, `[item]`, `[item, item]` |
| Pagination | page 0, page 1, last page, page beyond last |
| First/last element access | index 0, index -1, index length-1, index length |
| Deduplication logic | all unique, all same, one duplicate |

## Date and Time Boundaries

These are the most commonly missed boundaries in practice:

| Scenario | Test Values |
|----------|------------|
| End of month | Feb 28 (non-leap), Feb 28 (leap), Feb 29, Mar 1 |
| End of year | Dec 31, Jan 1 of next year |
| Timezone at midnight | 23:59:59 UTC is next day in UTC+1 |
| Daylight saving time | 1:59 AM → 3:00 AM (spring forward), 2:00 AM twice (fall back) |
| Epoch | Unix timestamp 0 (Jan 1 1970), negative timestamps |
| Leap second | Not usually testable but worth noting for financial systems |

## Null / Undefined / Missing

JavaScript/TypeScript specific — the most common source of runtime errors:

| Value | Distinct from |
|-------|--------------|
| `null` | `undefined` (explicitly set to no-value vs. never set) |
| `undefined` | missing key entirely (`obj.key === undefined` vs. `'key' in obj === false`) |
| `""` | `null` (empty string is a value; null is absence of value) |
| `0` | `false`, `null`, `undefined` (all falsy; only some are "no value") |
| `NaN` | invalid numeric operation; `NaN !== NaN` by IEEE spec |

**Pattern**: any function that accepts an optional parameter must be tested with the parameter absent, null, undefined, and an empty-equivalent value. Do not assume they're the same.

## Boolean Boundary Anti-Patterns

Tests that only cover `true` and `false` miss:
- Default value when not set
- What happens when the flag is toggled mid-operation
- What happens when two boolean flags interact (4 combinations, not 2)

For two independent flags A and B, test all four: `(F,F), (T,F), (F,T), (T,T)`.

## State Machine Boundaries

For any enum or status field:
- Every valid transition (A → B when allowed)
- Every invalid transition (A → C when not allowed — what is the error behavior?)
- Boundary states: initial state, terminal state, error state
- Duplicate transition (A → A — idempotent or error?)
- Missing state (what if the value is an unexpected enum variant from a future API version?)

## Practical Workflow

1. For each function with a conditional, list every threshold value.
2. Write tests for n-1, n, n+1 around each threshold.
3. For string inputs: always include empty, whitespace-only, and max-length.
4. For collections: always include empty, single-element, and two-element.
5. For dates: always include end-of-month, end-of-year, DST transition if timezone-aware.
6. For nullable values: always include null, undefined, and empty-equivalent separately.

The test count grows linearly with boundaries. The bug-catch rate grows much faster.
