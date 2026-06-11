---
name: database-schema-designer
description: Design production-ready SQL and NoSQL database schemas. Use when asked to design schema, create tables, model data, database design, schema for, or architect a data model. Covers normalization, indexing strategy, migration patterns, constraint design, and platform-specific traps for PostgreSQL, MySQL, and MongoDB.
license: MIT
---

# Database Schema Designer

## Mindset

1. **Access pattern is the schema.** No access pattern = no schema. Extract the 3 most frequent read queries first; the schema exists to serve them. Normalization is a starting point, not a destination.
2. **The database enforces what the application forgets.** Every constraint you skip becomes a data integrity incident at 2am. Defensive schema design is not premature optimization.
3. **UUID v4 as a clustered PK is a silent perf killer.** Random UUIDs fragment B-tree indexes on every insert. Use `BIGSERIAL`/`BIGINT AUTO_INCREMENT` for high-write tables; use UUIDv7 (time-ordered) or `gen_random_uuid()` only when distributed ID generation is required.
4. **TOAST in PostgreSQL means your "small" table isn't small.** Columns exceeding 2KB are silently moved to a TOAST table; a query that SELECTs a wide TEXT column on 100k rows does 100k TOAST lookups. Know your column widths before indexing.
5. **Migrations run on live data.** Every DDL change is a production operation. Design for zero-downtime: add before remove, nullable before constrained, never rename in one step.

## Navigation

**Use this skill when**: designing a new schema from scratch, reviewing an existing schema for problems, planning a migration, choosing between SQL/NoSQL, or optimizing a slow query via schema changes.

**Do NOT use this skill when**: writing ORM model code without schema intent (use the ORM docs), tuning query plans without schema changes (use EXPLAIN), or designing application-layer caching (Redis patterns are separate).

**Quick decision tree:**
```
Need schema help?
  ├─ New design → start with access patterns, then entities
  ├─ Existing schema review → load references/schema-design-checklist.md
  ├─ Performance problem → check indexes first, denormalize second
  └─ Migration plan → expand "When Things Go Wrong" section below
```

## Philosophy

Schema design is a contract between your data and your future self. Make the database enforce correctness at rest so application bugs produce errors, not silent corruption. Every deviation from normalized form must earn its keep with a measured performance justification.

## NEVER

- **NEVER use UUID v4 as a clustered primary key on high-write tables** — random insertion order causes B-tree page splits on every insert; at 1M+ rows/day this degrades write throughput 3-10x versus sequential keys. Use `BIGSERIAL` or UUIDv7 instead.
- **NEVER store monetary values in FLOAT or DOUBLE** — IEEE 754 rounding means `0.1 + 0.2 = 0.30000000000000004`; a single rounding error in financial data can cascade into reconciliation failures across millions of transactions. Always `DECIMAL(19,4)`.
- **NEVER add a NOT NULL column to a large table in a single migration** — PostgreSQL and MySQL rewrite the entire table; on a 500GB table this locks writes for minutes. Pattern: add nullable → backfill in batches → add constraint.
- **NEVER create a polymorphic `entity_type` + `entity_id` column pair without a partial index** — these columns can never have a foreign key; without a partial index per type, every query requires a full scan. Create `CREATE INDEX ... WHERE entity_type = 'post'` for each type.
- **NEVER rely on application-side cascades instead of database-level ON DELETE** — application code can be bypassed (direct SQL, migrations, admin tools); orphaned rows accumulate silently. Define ON DELETE strategy on every FK.
- **NEVER index every column "just in case"** — each index doubles write amplification and consumes buffer pool; on a write-heavy table, 10 unused indexes can halve insert throughput. Index exactly the queries you have, not the queries you imagine.
- **NEVER use `TEXT` for enum-like fields without a CHECK constraint or lookup table** — `status VARCHAR(20)` without `CHECK (status IN ('active','inactive'))` will contain 'Active', 'ACTIVE', 'activ', and NULL within a year.

## When to Break the Rules

| Rule | When to Break | Guard Rails |
|------|--------------|-------------|
| Normalize to 3NF | OLAP / reporting tables where JOIN cost dominates | Document the denorm + add comment in schema |
| FK constraints on every relationship | Ultra-high write throughput (>50k inserts/sec); some sharded DBs can't enforce cross-shard FKs | Enforce referential integrity at application layer with tests |
| Sequential INT primary key | Distributed/multi-writer systems where coordination is impossible | Use UUIDv7 (time-ordered) not v4 |
| UTC timestamps everywhere | Systems requiring local time audit trails (legal, compliance) | Store both: `event_at TIMESTAMPTZ`, `event_at_local TEXT` |
| Single schema per domain | Multi-tenant SaaS with strong isolation requirements | Schema-per-tenant or row-level security (PostgreSQL RLS) |

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Writes slowing down as table grows | Too many indexes; UUID v4 PK fragmentation | `pg_stat_user_indexes` to find unused indexes; switch to UUIDv7 or BIGSERIAL on next rebuild |
| Migration hangs on large table | Adding NOT NULL or adding index without CONCURRENTLY | Kill migration; use `CREATE INDEX CONCURRENTLY`; add column nullable first |
| Orphaned rows accumulating | Missing ON DELETE CASCADE or RESTRICT | Audit with `LEFT JOIN ... WHERE fk IS NULL`; add FK constraints in a quiet window |
| Query ignores index | Leading column not in WHERE clause; implicit cast mismatch; low cardinality | `EXPLAIN ANALYZE` to confirm; fix column order or cast; use partial index |
| TOAST bloat causing slow SELECTs | Wide TEXT/JSONB columns selected unnecessarily | `SELECT only_needed_cols`; move large blobs to object storage, store URL |
| Schema drift between environments | Migrations applied out of order | Use a migration framework (Flyway, Alembic, golang-migrate) with checksums; never hand-edit prod |

## Core Decision Framework

### SQL vs NoSQL

| Signal | Choose SQL | Choose NoSQL |
|--------|-----------|-------------|
| Data shape | Relational, structured | Hierarchical, variable schema |
| Query needs | Ad-hoc joins, aggregates | Known access patterns only |
| Consistency | ACID required | Eventual OK |
| Scale pattern | Vertical + read replicas | Horizontal sharding |

**Default: SQL.** NoSQL requires knowing your access patterns with certainty before design; SQL tolerates query pattern changes.

### Primary Key Selection

| Scenario | Choice | Reason |
|----------|--------|--------|
| Single-server OLTP | `BIGSERIAL` / `BIGINT AUTO_INCREMENT` | Sequential, fast inserts, small storage |
| Distributed / multi-writer | UUIDv7 (`pg_uuidv7` extension) | Time-ordered, avoids fragmentation |
| Junction table | Composite `(a_id, b_id)` | Natural PK, no surrogate needed |
| External system sync | Natural key + surrogate | Natural key as UNIQUE, surrogate as PK |

### Index Decision Tree

```
Need an index?
  ├─ FK column? → YES, always
  ├─ In WHERE or JOIN ON? → YES, if cardinality > 10%
  ├─ In ORDER BY only? → partial index if filtering first
  ├─ Full-text search? → GIN (Postgres) / FULLTEXT (MySQL)
  └─ JSONB field query? → GIN on the column
```

**Composite index column order:** equality filters first, then range filters, then ORDER BY columns. The leftmost column must appear in your WHERE clause for the index to activate.

## Platform-Specific Traps

### PostgreSQL
- `SERIAL` is deprecated — use `GENERATED ALWAYS AS IDENTITY`
- `TIMESTAMP` has no timezone; use `TIMESTAMPTZ` everywhere
- `CREATE INDEX` locks table; `CREATE INDEX CONCURRENTLY` does not (but can't run in a transaction)
- JSONB GIN index covers containment (`@>`), not equality on extracted fields — use a functional index: `CREATE INDEX ON orders ((data->>'status'))`
- `VACUUM` does not reclaim disk space; `VACUUM FULL` does but locks. Use `pg_repack` for live bloat reclaim.

### MySQL / MariaDB
- InnoDB clusters the table on the PK — UUID v4 causes the fragmentation problem hardest here
- `DATETIME` vs `TIMESTAMP`: TIMESTAMP stores in UTC, auto-converts; DATETIME stores literal value. Use TIMESTAMP unless you need dates beyond 2038.
- `utf8` in MySQL is actually `utf8mb3` (3-byte max); emoji breaks silently. Always `utf8mb4`.
- Altering a column type on a large InnoDB table copies the full table in-place — use `pt-online-schema-change` or `gh-ost`.

### MongoDB
- Document size hard limit: 16MB. Embedding unbounded arrays (e.g., all comments in a post) hits this. Reference when the child collection grows without bound.
- Indexes are per-collection, not enforced across collections — referential integrity is entirely application responsibility.
- `$lookup` (join) is expensive; if you need it on hot paths, you embedded wrong.

## References

Load these when needed — do not include in every response:

- **Full checklist**: `references/schema-design-checklist.md` — use during schema review or audit tasks
- **Normalization deep dive**: explain 1NF/2NF/3NF with examples only when user asks to normalize an existing schema
- **Migration patterns**: expand zero-downtime steps only when user asks for migration scripts

Once your schema is designed, use openapi-to-typescript to generate TypeScript interfaces from an OpenAPI spec that mirrors your data model — especially useful for readOnly/writeOnly field splitting between read/write DTOs.
