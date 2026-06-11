# Safe Rename Checklist

Use this before applying any rename suggestion to determine blast radius.

## Serialization Boundary Check

| Signal | Risk Level | Required Action |
|--------|-----------|-----------------|
| Field appears in JSON/YAML output consumed by external callers | CRITICAL | Deprecation period; alias old name |
| Field name matches a DB column (ORM mapping) | HIGH | Migration script + rollback plan |
| Name appears in an OpenAPI/Swagger spec | HIGH | Bump minor version; keep old field as deprecated |
| Name is a proto field (`snake_case` in .proto file) | CRITICAL | Never rename — proto field numbers + names are wire-stable |
| Name is a Redux action type string (`"USER_LOGIN_SUCCESS"`) | HIGH | Old name must remain as alias until all reducers updated |
| Name appears in a test fixture file (JSON/CSV) | MEDIUM | Update fixtures atomically with code |
| Name only appears in internal code, no serialization | LOW | Rename freely |

## Pre-Rename Commands

```bash
# Find all serialized uses (JSON keys, DB columns, env vars)
grep -rn '"old_name"' .          # JSON keys
grep -rn "'old_name'" .          # Python dict keys / YAML
grep -rn "old_name:" .           # YAML / struct tags
grep -rn "old_name" migrations/  # DB migrations

# Check if name is exported in a public package
grep -rn "^func OldName\|^var OldName\|^const OldName" .

# Find consumer repos (if in a monorepo)
grep -rn "old_name" ../other-services/
```

## Deprecation Pattern (when you cannot rename immediately)

```python
# Python: alias + deprecation warning
@property
def old_name(self):
    import warnings
    warnings.warn("old_name is deprecated; use new_name", DeprecationWarning, stacklevel=2)
    return self.new_name
```

```typescript
// TypeScript: keep old interface key as deprecated
interface User {
  /** @deprecated use displayName */
  name?: string;
  displayName: string;
}
```

## Cognitive Load Budget

Names live in working memory. Each name a reader must hold costs ~7 bits of cognitive load.
- Rename when: the existing name actively misleads or requires a comment to understand
- Do NOT rename when: the name is merely suboptimal and the file is stable/rarely read

## Framework-Specific Protected Names

| Framework | Protected Pattern | Why |
|-----------|------------------|-----|
| Django ORM | `Meta.db_table`, field `db_column` | Maps to physical schema |
| SQLAlchemy | `Column(name=...)` | Physical column name, not Python attr |
| Pydantic v1 | `Field(alias=...)` | JSON key in serialized output |
| React | `displayName` on components | Used by DevTools for debugging |
| Redux | action type strings | String-matched in reducers across files |
| gRPC/Protobuf | any field in `.proto` | Wire format, field numbers immutable |
| Terraform | `resource "type" "name"` | State file key — rename = destroy+recreate |
