---
name: monorepo-workspace
description: Expert workspace orchestration for monorepos. Covers tool selection (Nx vs Turborepo vs pnpm workspaces vs Lerna), build graph and affected computation, shared config inheritance, dependency graph discipline, publishing strategy (independent vs fixed versioning), remote caching, TypeScript internal package references, and package granularity sizing. Trigger phrases: "set up a monorepo", "nx vs turborepo", "affected packages", "workspace config", "monorepo build", "remote cache", "internal packages", "circular dependency in monorepo", "workspace versioning".
license: MIT
metadata:
  version: 1.0.0
---

# Monorepo Workspace

## Mindset

- **The build graph is the product** — the workspace tool is irrelevant; what matters is whether the dependency graph accurately reflects your actual code graph. A mismatched graph produces false-positive "affected" runs or, worse, silently skips rebuilds. Keep them in sync by treating package.json `dependencies` as a code contract, not metadata.
- **Coarse packages beat fine-grained every time** — splitting one domain into ten packages to achieve "isolation" means ten versions of `tsconfig.json`, ten places to add a lint rule, and ten entries in changelogs for every cross-cutting change. One package per domain is almost always the right boundary. Split only when release cadences truly diverge or when a package needs to be published independently.
- **Shared utilities are a dependency magnet** — every file you add to a `shared/` or `utils/` package marks every consumer as "affected" on every change. Keep shared packages small and stable; a file that changes weekly belongs in the package that owns the domain, not in a shared utility.
- **`workspace:` protocol is a build-time contract, not a publishing one** — package managers resolve `workspace:*` at install time, but bundlers and `tsc` don't understand it at publish time. Published packages must be built to concrete versions; internal-only packages can stay on `workspace:`.
- **Incremental CI is the only reason to have a monorepo** — if you're running all tests on every commit, you've adopted 100% of the monorepo complexity with 0% of the benefit. Affected computation is non-optional.

## Navigation

**Use this skill when**:
- Choosing or migrating between Nx, Turborepo, pnpm workspaces, or Lerna
- Debugging why "affected" computation marks too many or too few packages
- Setting up shared tsconfig / ESLint config across packages
- Detecting or resolving circular dependencies between workspace packages
- Deciding between independent and fixed versioning strategies
- Configuring remote caching (Nx Cloud, Turborepo Remote Cache, self-hosted)
- Troubleshooting TypeScript path aliases vs `workspace:` protocol issues
- Sizing package granularity (too many vs too few packages)

**Do NOT use this skill when**:
- Updating individual package versions within an existing monorepo — use **dependency-updater** for that
- Setting up a single-package repository with no workspace tooling
- Questions about container orchestration or service meshes (different kind of "mono")

**Tool selection decision tree**:
```
What is your primary constraint?
├── Polyglot (Go, Rust, Python alongside JS/TS)?
│   └── → Nx  (generator ecosystem + polyglot executor support)
├── Pure JS/TS, want minimal config, fastest cold-cache?
│   └── → Turborepo  (zero-config cache, simpler mental model)
├── No build orchestrator wanted, just package linking?
│   └── → pnpm workspaces alone  (workspace: protocol, no task runner overhead)
└── Existing Lerna repo?
    ├── Publishing-only use case → keep Lerna for versioning, add Turbo for tasks
    └── Greenfield → migrate off Lerna; it's in maintenance mode
```

**Versioning strategy decision tree**:
```
Do all packages in the repo share a single release?
├── Yes (e.g., a design system with a single version promise)
│   └── Fixed versioning — acceptable; changelogs will be noisy for small repos
└── No (packages have independent release cadences)
    └── Independent versioning — required; fixed versioning forces semver lies
```

## Philosophy

A monorepo is a discipline problem, not a tooling problem. The tools enforce what the team already agreed on. Pick the simplest tool that accurately computes the affected set and caches task outputs; spend the saved time on keeping the dependency graph honest.

## NEVER

- **NEVER import across package boundaries using relative paths** (`../../other-package/src/index.ts`) — relative imports bypass the workspace dependency graph entirely, are invisible to `nx affected` / `turbo --filter`, and silently break when packages are moved or renamed. Always import by the package name declared in `package.json` (`import { x } from '@acme/utils'`).
- **NEVER add a shared utility to the root `package.json`** — root-level dependencies become implicit globals for every package in the workspace. When a package is published or extracted, the dependency disappears without warning. Declare all runtime dependencies in the consuming package's own `package.json`.
- **NEVER ignore circular dependency warnings** — circular deps cause Webpack/esbuild/tsc to non-deterministically choose which module to evaluate first. The failure mode is intermittent: it works in dev (warm module cache) and breaks in CI (cold build). By the time you see it fail, the graph is already tangled and untangling it requires refactoring across multiple packages simultaneously.
- **NEVER use fixed versioning when packages have independent release cadences** — fixed versioning bumps every package to the same version on every release. A one-line change in `@acme/button` forces `@acme/data-layer` to publish a new version with no actual changes. Consumers subscribe to changelogs and receive noise, eroding trust in semver signals.
- **NEVER run `npm install` (or `yarn install`) inside an individual workspace package directory** — running install at the package level creates a nested `node_modules` that shadows the hoisted root dependencies. You get two copies of React, two copies of TypeScript, peer-dependency mismatches, and builds that differ between developers depending on what order they ran commands. Always install from the workspace root.
- **NEVER skip affected computation by running all tasks on every CI commit** — in a 50-package monorepo, running the full test suite on a one-line doc change is the reason teams abandon monorepos. Affected computation is the value proposition; bypassing it to "be safe" is the same as not having a monorepo at all.
- **NEVER use TypeScript path aliases (`paths` in tsconfig) as a substitute for `workspace:` references in published packages** — path aliases are resolved by the TypeScript compiler during local development but are invisible to consumers who install the published package. At publish time, the import resolves to a path that doesn't exist in the npm tarball. Use path aliases only for internal app packages that are never published.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| `nx affected` marks every package on every PR | A shared utility package is touched frequently; all consumers are downstream | Audit the shared package's change frequency; move volatile files to the owning domain package; split stable helpers into a truly-stable `@acme/core` |
| Turborepo cache never hits in CI | `outputs` in `turbo.json` doesn't match what the task actually writes, or the task reads env vars not listed in `env` | Add the missing env vars to `globalEnv` or task-level `env`; verify `outputs` globs with `turbo run build --dry=json` |
| `tsc` succeeds locally but fails in CI with "cannot find module '@acme/utils'" | Path aliases work locally (tsconfig `paths`) but the package isn't installed in CI because it's not in `dependencies` | Add `"@acme/utils": "workspace:*"` to the consuming package's `dependencies`; never rely solely on path aliases for cross-package imports |
| Circular dependency causes intermittent build failure | Two packages import from each other, even indirectly | Run `nx graph` or `madge --circular --extensions ts src/` to visualize; extract the shared interface/type to a third package that neither depends on the other |
| Published package missing files at runtime | `package.json` `files` field doesn't include build output directory | Audit `files` array; add `dist/` or equivalent; verify with `npm pack --dry-run` before publishing |
| `workspace:*` in a published package causes install failure for consumers | `workspace:` protocol was not replaced with a concrete version before publishing | Ensure publish pipeline runs `pnpm publish` (which auto-replaces `workspace:*`) or add a `prepack` script to rewrite versions |

---

## Tool Deep-Dives

See [`references/tool-comparison.md`](references/tool-comparison.md) for decision criteria, configuration examples, and migration notes for Nx, Turborepo, pnpm workspaces, and Lerna.

See [`references/shared-config-patterns.md`](references/shared-config-patterns.md) for tsconfig extends chains, ESLint flat config layout, and the "config package" pattern.

See [`references/remote-cache-setup.md`](references/remote-cache-setup.md) for Nx Cloud, Turborepo Remote Cache, and self-hosted cache configuration.

---

## Package Granularity Sizing

**The right question is not "should this be its own package?" but "does this have a different release cadence or a different set of consumers than its sibling code?"**

Signs a package is too fine-grained:
- More than one package changes in every PR
- The package has only one consumer and that consumer is in the same repo
- The package contains fewer than ~5 source files
- Changelog entries always appear in pairs or triples across packages

Signs a package is too coarse:
- Different teams own different subdirectories and frequently conflict on semver
- A single package is consumed by both internal apps and external npm consumers
- Build times for a single package exceed 60 seconds (indicates too many responsibilities)

**Default rule**: one package per product domain (auth, payments, ui-components, api-client). Split only when you have evidence of divergent release cadence, not in anticipation of it.

---

## Dependency Graph Discipline

Detecting circular dependencies early is cheaper than debugging them later:

```bash
# Nx — visualize full graph, highlights cycles
nx graph

# TypeScript — list all files compiled (reveals unexpected cross-package imports)
tsc --listFiles --noEmit 2>&1 | grep other-package

# madge — dedicated circular dep detector for JS/TS
npx madge --circular --extensions ts ./packages/

# pnpm — workspace dependency graph
pnpm list --recursive --depth 1
```

**Extraction pattern for breaking a cycle**: If `package-a` imports from `package-b` and vice versa, the shared type or interface they both need belongs in `package-shared` that neither depends on. Do not move logic — only the shared contract (types, interfaces, constants).

---

## Navigation Callout

For per-project dependency updates within the monorepo (upgrading lodash, bumping React version, fixing a CVE in a specific package), use **dependency-updater** — this skill covers workspace structure and build orchestration, not individual package version management.
