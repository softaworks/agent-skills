# OpenAPI-to-TypeScript: Edge Cases & Advanced Patterns

## anyOf vs oneOf vs allOf — The Real Distinction

OpenAPI authors often misuse these. Claude must interpret **intent** not just semantics:

| Combiner | OpenAPI intent | TypeScript output |
|----------|---------------|-------------------|
| `oneOf`  | Exactly one matches (discriminated or plain union) | `A \| B` |
| `anyOf`  | One or more match (validation rule, not a type) | `A \| B` (same as oneOf — TypeScript has no "one-or-more" type) |
| `allOf`  | All schemas must apply (composition/inheritance) | `extends Base` or intersection `A & B` |

**anyOf warning**: Specs that use `anyOf` to mean "nullable" are very common. `anyOf: [SchemaA, {type: "null"}]` → `SchemaA | null`. Do NOT generate `A | B | null` when the null variant is the only non-schema member.

## Discriminated Unions (oneOf + discriminator)

When a `discriminator.propertyName` is present, generate a proper tagged union:

```yaml
# OpenAPI
oneOf:
  - $ref: '#/components/schemas/Cat'
  - $ref: '#/components/schemas/Dog'
discriminator:
  propertyName: petType
  mapping:
    cat: '#/components/schemas/Cat'
    dog: '#/components/schemas/Dog'
```

```typescript
// Correct output — NOT a plain union
export type Pet = Cat | Dog;

// Type guard uses the discriminant — NOT structural checks
export function isPet(value: unknown): value is Pet {
  if (typeof value !== 'object' || value === null) return false;
  const petType = (value as any).petType;
  return petType === 'cat' || petType === 'dog';
}

// Narrowing helper (generate alongside type guard)
export function narrowPet(value: Pet): value is Cat {
  return value.petType === 'cat';
}
```

Never generate a structural type guard for a discriminated union — it becomes O(n×fields) and breaks when subschemas share field names.

## Circular References

Detection: a schema is circular when resolving it encounters its own `$ref` before completion. Common patterns:

```yaml
# Self-referential tree node
TreeNode:
  type: object
  properties:
    children:
      type: array
      items:
        $ref: '#/components/schemas/TreeNode'

# Mutually recursive (Category → Product → Category)
Category:
  properties:
    featuredProduct:
      $ref: '#/components/schemas/Product'
Product:
  properties:
    category:
      $ref: '#/components/schemas/Category'
```

**Resolution strategy** (in order):
1. Direct self-reference in array → `children?: TreeNode[]` (TypeScript handles recursive interfaces natively — no alias needed)
2. Direct self-reference in object property → use `interface` (not `type` alias) — interfaces support recursive property types
3. Mutually recursive across 2+ schemas → generate all interfaces first, then add properties — TypeScript resolves forward references in interfaces

**Never** break circularity by inlining expanded types — this causes infinite expansion.

## additionalProperties

| OpenAPI | TypeScript |
|---------|-----------|
| `additionalProperties: true` | `[key: string]: unknown` index signature |
| `additionalProperties: false` | Exact interface, no index signature |
| `additionalProperties: {type: string}` | `[key: string]: string` |
| `additionalProperties: {$ref: X}` | `[key: string]: X` |
| absent | Omit index signature (TypeScript default is open) |

Warning: an index signature `[key: string]: T` makes ALL named properties also satisfy `T`. If a named property has an incompatible type, TypeScript will error. Use `[key: string]: T | NamedPropType` to reconcile.

## nullable (OpenAPI 3.0 vs 3.1)

OpenAPI 3.0.x uses `nullable: true` (not a type system feature):
```yaml
# OAS 3.0
name:
  type: string
  nullable: true
```
→ `name?: string | null`

OpenAPI 3.1 uses JSON Schema `type: [string, null]` or `oneOf: [{type: string}, {type: null}]`.
Detect version from `openapi:` field before processing nullable.

## Path Parameter Collision in Request Types

When a path has both path params and query params, generate separate interfaces or a merged one:

```typescript
// GET /users/{id}/posts?page=1
// Option A: merged (simpler for consumers)
export interface GetUserPostsRequest {
  id: string;      // path param
  page?: number;   // query param
}

// Option B: split (more faithful to OpenAPI structure)
export interface GetUserPostsPathParams { id: string; }
export interface GetUserPostsQueryParams { page?: number; }
```

Default to merged (Option A) unless the spec has >5 path params + >3 query params (then split improves readability).

## readOnly / writeOnly Properties

| Marker | Request interface | Response interface |
|--------|------------------|--------------------|
| `readOnly: true` | Omit the field | Include the field |
| `writeOnly: true` | Include the field | Omit the field |

Most generators ignore this. Implementing it correctly requires generating separate request/response schemas even when they share a `$ref`.

## Schema with no type field

OpenAPI allows schemas with no `type` (accepts any JSON value):
```yaml
metadata:
  description: Arbitrary metadata
```
→ `metadata?: unknown` (not `any` — preserves strict mode compatibility)

## Large Enum Lists

When an enum has >20 values, generate a `const` object + derived type instead of a union:

```typescript
// For large enums
export const CountryCode = {
  US: 'US', GB: 'GB', DE: 'DE', // ... 200+ values
} as const;
export type CountryCode = typeof CountryCode[keyof typeof CountryCode];
```

This enables exhaustiveness checking via `Object.values(CountryCode)` and avoids IDE slowdowns from giant union types.
