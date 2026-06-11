---
name: openapi-to-typescript
description: Converts OpenAPI 3.0 JSON/YAML to TypeScript interfaces, discriminated unions, and type guards. Use when asked to generate types from OpenAPI, convert schema to TS, create API interfaces, generate TypeScript types from a spec, or turn swagger/openapi into TypeScript.
---

## Mindset

- **Specs lie about their own combiners.** `anyOf` is frequently used where `oneOf` was intended, and vice versa. Read the `discriminator` field and the actual schema structure — not just the combiner keyword — to determine the correct TypeScript output.
- **Circular references are not errors.** TypeScript interfaces support recursive property types natively. Never break a circular ref by inlining or by reaching for `unknown` — generate the interface first, add properties second.
- **`readOnly`/`writeOnly` creates two distinct shapes.** A single `$ref` schema with `readOnly` fields must yield different request and response interfaces. Generators that ignore this produce runtime bugs at the boundary.
- **The `required` array governs optionality, not `nullable`.** A field absent from `required[]` is optional (`?`). A field with `nullable: true` is `T | null`. These are orthogonal — apply both when both are present.
- **anyOf with a null variant is nullable, not a union.** `anyOf: [SchemaA, {type: "null"}]` means `SchemaA | null`, not an open-ended union type.

## Navigation

**Use this skill when**: user asks to generate TypeScript types from OpenAPI/Swagger, convert a spec to TS, create API interfaces from a JSON/YAML schema, or mentions "openapi to typescript", "swagger types", "generate interfaces from spec".

**Do NOT use this skill when**:
- The spec is OpenAPI 2.0 (Swagger) — flag the version gap; the `nullable` and component model differ significantly
- The user wants a full API client (fetch functions, axios wrappers) — this skill generates types only
- The user wants Zod/io-ts/valibot schemas — those are runtime validators with different trade-offs than type guards

**Quick decision tree for ambiguous input:**
```
Has discriminator.propertyName?
  YES → discriminated union + narrowing helper (not structural type guard)
  NO  → oneOf/anyOf → plain union | null check for null-only anyOf variants
Is it allOf with inline properties?
  YES → prefer `extends Base` over intersection `&` (cleaner IDE errors)
  NO  → intersection type is fine
Circular ref detected?
  YES → use interface (not type alias) — interfaces resolve forward refs
```

## Philosophy

Generate types that serve TypeScript consumers first, OpenAPI spec authors second. A type that compiles but misleads (wrong optionality, missing discriminants, bloated guards) is worse than a type that requires a one-line manual edit.

## NEVER

- **NEVER generate structural type guards for discriminated unions** — when a `discriminator.propertyName` exists, check only that field; structural checks across all properties break when subtypes share field names and produce false positives.
- **NEVER use `any` for unresolved or schema-less properties** — use `unknown`; `any` silently disables type checking for the entire call chain downstream, while `unknown` forces explicit narrowing at the consumer.
- **NEVER resolve `$ref` inline when it creates a circular expansion** — detect circularity via a visited-set during traversal; output the name reference and move on; inlining causes infinite recursion in the generator and a broken output file.
- **NEVER generate a single interface for schemas with mixed `readOnly`/`writeOnly` fields** — a `readOnly: true` field must be omitted from request types and present in response types; conflating them produces types that accept illegal write payloads silently.
- **NEVER produce an index signature `[key: string]: T` without reconciling named property types** — TypeScript requires all named properties to be assignable to the index signature value type; incompatible named fields cause a compile error that will be blamed on the generator.
- **NEVER treat `anyOf` with a single non-null variant as a union** — `anyOf: [Schema, {type: null}]` is the OAS 3.0 nullable pattern; output `Schema | null`, not `Schema | null | never`.
- **NEVER skip the `openapi` version check before processing** — OAS 3.0.x and 3.1 use incompatible nullable conventions (`nullable: true` vs `type: [string, null]`); processing with the wrong convention silently drops nullability.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| TypeScript error: index signature incompatible with named property | Generated `[key: string]: T` but a named field has type `U` where `U` is not assignable to `T` | Widen index type to `T \| U`, or remove index signature if `additionalProperties: false` |
| Type guard always returns false at runtime | Structural guard on a discriminated union — sibling schemas share the checked field names | Re-generate the guard using only `discriminator.propertyName` value check |
| Infinite loop in generator | Undetected circular `$ref` | Track visited schema names in a `Set`; on revisit, emit the name reference and return |
| Compiled output has no `null` variant but API returns null | `nullable: true` on OAS 3.0 field was ignored, or OAS 3.1 `type: [string, null]` not parsed | Check spec version; re-apply nullable logic per version |
| `extends` clause causes TS error: base has incompatible property | `allOf` base and inline object both declare the same field with different types | Merge the field definitions; use the more specific type and add a JSDoc note |
| Large union type causes IDE slowdown | Enum with 30+ values generated as `"A" \| "B" \| ...` | Switch to `const` object pattern: `export const Enum = {...} as const; export type Enum = typeof Enum[keyof typeof Enum]` |

## Core Workflow

1. Read the file; detect `openapi:` version — abort with clear message if not 3.0.x
2. Build a schema registry from `components/schemas` (name → schema object)
3. Detect circular refs: traverse each schema with a visited-set; record circular pairs
4. Process schemas in dependency order (leaf schemas first) — see [edge cases](references/edge-cases.md) for combiner and circular ref handling
5. Generate request/response interfaces from `paths`; split `readOnly`/`writeOnly` fields correctly
6. Write output with header comment; default path `types/api.ts`

## Key Type Mappings

| OpenAPI construct | TypeScript output |
|-------------------|-------------------|
| `type: string/number/boolean/null` | `string` / `number` / `boolean` / `null` |
| `type: integer` | `number` |
| `nullable: true` (OAS 3.0) | `T \| null` |
| `type: [T, null]` (OAS 3.1) | `T \| null` |
| `enum: [...]` (≤20 values) | `"a" \| "b" \| ...` |
| `enum: [...]` (>20 values) | `const` object + derived type |
| `oneOf` / `anyOf` | `A \| B` (check for discriminator first) |
| `allOf` with `$ref` + inline | `interface Foo extends Base { extraField: T }` |
| `additionalProperties: true` | `[key: string]: unknown` |
| `additionalProperties: {type: T}` | `[key: string]: T` |
| No `type` field | `unknown` |

See [references/edge-cases.md](references/edge-cases.md) for: anyOf/oneOf/allOf detailed rules, discriminated union output, circular reference resolution, readOnly/writeOnly splitting, path parameter merging, and large enum patterns.
