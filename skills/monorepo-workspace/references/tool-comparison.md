# Tool Comparison: Nx vs Turborepo vs pnpm Workspaces vs Lerna

Reference for the monorepo-workspace skill.

---

## Decision Matrix

| Criterion | Nx | Turborepo | pnpm Workspaces | Lerna |
|-----------|-----|-----------|-----------------|-------|
| Polyglot support | Yes (custom executors) | No (JS/TS only) | No | No |
| Code generators | Yes (schematics) | No | No | No |
| Affected computation | Yes (project graph) | Yes (file hash) | No (manual) | No |
| Remote cache | Nx Cloud (paid/free tier) | Vercel Remote Cache (free) | No | No |
| Config overhead | High (project.json per pkg) | Low (turbo.json root only) | Minimal | Medium |
| Publishing support | Plugin-based | No | `pnpm publish -r` | First-class |
| Learning curve | High | Low | Low | Medium |
| Active maintenance | Yes | Yes | Yes | Maintenance mode |

---

## Nx

**Best for**: Polyglot repos, teams that want scaffolding/generators, large orgs with many packages that need enforced module boundaries.

**Non-obvious criteria**:
- Nx's "module boundary" lint rules (`@nx/enforce-module-boundaries`) are the only tool in this space that can enforce which packages may import from which — critical for platform teams that need to prevent app-level code from importing internal platform code.
- Nx generators create consistent new packages from templates, eliminating the "copy-paste tsconfig and forget to rename" failure.
- The Nx project graph reads both `package.json` dependencies AND Nx-specific `implicitDependencies` — if you forget to declare an implicit dep (e.g., a shared build script), affected computation will miss it.

**Minimum config**:
```json
// nx.json
{
  "targetDefaults": {
    "build": { "dependsOn": ["^build"], "cache": true },
    "test":  { "cache": true },
    "lint":  { "cache": true }
  }
}
```

```json
// packages/my-lib/project.json
{
  "name": "my-lib",
  "targets": {
    "build": { "executor": "@nx/js:tsc", "options": { "main": "src/index.ts" } }
  }
}
```

---

## Turborepo

**Best for**: Pure JS/TS repos, teams that want minimal configuration overhead, projects already using Vercel infrastructure.

**Non-obvious criteria**:
- Turbo's cache key is computed from input file hashes + task config hash. If a task reads from environment variables, those vars MUST be declared in `env` or `globalEnv` — otherwise the cache key ignores them and cache hits return stale output when the env changes.
- `turbo run build --filter=@acme/app` runs build for `@acme/app` AND all its dependencies (because `dependsOn: ["^build"]` is the default). This is correct behavior — not a bug — but surprises engineers who expect filter to mean "only this package."
- The `outputs` field must exactly match what the task writes. Over-specifying outputs (e.g., `["dist/**", ".next/**"]` when only `dist/` is written) causes cache misses because Turbo verifies output existence on restore.

**Minimum config**:
```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**"],
      "cache": true
    },
    "test": {
      "dependsOn": ["^build"],
      "cache": true
    },
    "lint": {
      "cache": true
    }
  }
}
```

---

## pnpm Workspaces (No Orchestrator)

**Best for**: Small monorepos (2–5 packages), teams that want workspace linking without task runner complexity, library-only repos where publish order matters more than incremental builds.

**Non-obvious criteria**:
- Without a task runner, "affected" computation doesn't exist — you run all tasks always. This is acceptable for small repos but does not scale.
- `pnpm -r run build` runs build in all packages respecting topological order (dependencies build before consumers) — this is built in, no config needed.
- `pnpm deploy` copies a specific workspace package + its resolved dependencies to a target directory, suitable for deploying a single service from a monorepo without shipping the whole workspace.

**Workspace config**:
```yaml
# pnpm-workspace.yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - '!**/__tests__/**'
```

**Internal reference**:
```json
// packages/app/package.json
{
  "dependencies": {
    "@acme/utils": "workspace:*"
  }
}
```

---

## Lerna

**Current status**: Maintained by Nx team. Feature development is minimal. The publishing and versioning features remain solid; the task orchestration is deprecated in favor of Nx or Turbo as the task runner.

**When to keep Lerna**: Existing repos that use `lerna publish` and `lerna version` with a well-established changelog workflow. Do not migrate unless the publishing workflow is also broken.

**When to migrate off Lerna**: Greenfield repos, repos where you're adopting Lerna for task running (use Turbo or Nx instead), repos where the changelog noise from fixed versioning is causing real pain.

**Hybrid pattern** (common in legacy repos):
```json
// lerna.json — publishing only, no task running
{
  "version": "independent",
  "npmClient": "pnpm",
  "useWorkspaces": true,
  "command": {
    "publish": { "conventionalCommits": true }
  }
}
```
Then add Turborepo for task running alongside. Lerna touches `package.json` versions + git tags; Turbo runs build/test/lint. They don't conflict.

---

## Migration Notes

### pnpm workspaces → Turborepo
1. Add `turbo.json` to root (see minimum config above)
2. Add `turbo` to root `devDependencies`
3. Replace `pnpm -r run build` with `turbo run build` in CI
4. Verify `outputs` globs match your actual build artifacts

### Nx → Turborepo (JS/TS only repos wanting simpler config)
1. Export Nx project graph to understand current dependency structure
2. Replace `project.json` targets with `turbo.json` pipeline entries
3. Remove `nx.json`, `project.json` files
4. Note: you lose module boundary enforcement and generators

### Lerna → Independent versioning with Changesets
1. Install `@changesets/cli`
2. Run `changeset init`
3. Replace `lerna version` with `changeset version`
4. Replace `lerna publish` with `changeset publish`
5. Remove `lerna.json` last — verify CI is green first
