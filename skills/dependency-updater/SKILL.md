---
name: dependency-updater
description: Smart dependency management for any language. Auto-detects project type, applies safe updates automatically, prompts for major versions, diagnoses and fixes dependency issues. Trigger phrases: "update dependencies", "update deps", "outdated packages", "dependency audit", "fix dependency conflicts", "security audit packages", "why won't my packages install".
license: MIT
metadata:
  version: 2.0.0
---

# Dependency Updater

## Mindset

- **Pinned versions are load-bearing** — a fixed version without `^` or `~` is a *decision*, not an oversight. Someone got burned and locked it. Never "fix" it to a range without checking git blame.
- **Lock files are the ground truth** — `package.json` is a *request*, `package-lock.json` is *what actually runs*. When they diverge (e.g., after a `git pull` that updated package.json but not the lock), `npm install` silently installs different code than production.
- **`npm audit --force` is a footgun** — it resolves vulnerabilities by *downgrading or breaking semver constraints*, leaving the project in an inconsistent state that CI can't reproduce. Practitioners use targeted upgrades, not force.
- **Major version bumps require changelog archaeology** — tools can detect the version delta but not whether your usage of the old API was in the breaking-change surface. Always check the migration guide before approving a major.
- **Monorepos compound the risk** — updating a shared package at the root can silently change behavior in workspaces that weren't tested. Run workspace-scoped installs after root changes.

## Navigation

**Use this skill when**:
- User asks to update, upgrade, or refresh dependencies/packages/deps
- User reports install failures, peer-dependency warnings, or version conflicts
- User asks for a security audit or vulnerability scan of packages
- User asks what packages are outdated or stale

**Do NOT use this skill when**:
- User wants to *add a new* package (that's a feature task, not an update)
- User is working inside a container/locked environment with no write access to package files
- The project uses Nix, Bazel, or vendored deps — standard update tools break these

**Quick decision tree**:
```
User request type?
├── "update" / "outdated" → full update workflow (detect → scan → apply → audit)
├── "security" / "vuln" / "audit" → audit-only workflow
├── "broken" / "can't install" / "conflict" → diagnosis mode
└── "specific package X" → targeted update, not bulk
```

## Philosophy

Safety over convenience: auto-apply only what semver guarantees is backward-compatible, gate everything else behind explicit user approval, and never mutate pinned versions or lock files in ways the ecosystem's install command wouldn't.

## NEVER

- **NEVER run `npm audit --force`** — it breaks semver constraints, can *downgrade* packages to older vulnerable versions, and produces a lock file that diverges from package.json in ways that break reproducible installs. Use `npm audit fix` (no `--force`) or upgrade the specific package manually.
- **NEVER run `pip-review --auto` without a virtualenv active** — it upgrades system Python packages, which breaks OS-level tools that depend on specific versions (particularly on Debian/Ubuntu). Always confirm a venv is active first.
- **NEVER auto-apply MAJOR updates in bulk** — even if the user says "update everything", batch-approving majors makes it impossible to bisect which package broke the build. Present each major individually with current → new and a link to the changelog.
- **NEVER delete and regenerate a lock file as the first fix** — `rm package-lock.json && npm install` wipes all transitive version pins, meaning dependencies-of-dependencies can jump to breaking versions. Use this only as a last resort after targeted fixes fail.
- **NEVER run `go get -u ./...` in a module with replace directives** — `-u` ignores `replace` directives for indirect dependencies, silently upgrading past the pinned fork/patch. Use `go get pkg@version` for each module individually.
- **NEVER skip `go mod tidy` after `go get` updates** — Go's toolchain won't error, but `go.sum` will contain stale hashes that fail verification in hermetic CI environments.
- **NEVER treat `cargo update` as safe for workspace crates** — `cargo update` respects semver *ranges* in Cargo.toml but doesn't check that workspace member crates compile together. Always run `cargo check --workspace` after.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| `npm install` succeeds locally but CI fails | Lock file not committed, or committed with wrong line endings | `git add package-lock.json` with `.gitattributes` setting `text=auto eol=lf` |
| `npm audit fix` creates new vulnerabilities | Downgraded a transitive dep to an older vulnerable version | `git checkout package-lock.json`, upgrade the *direct* dep that pulls in the vulnerable transitive |
| Peer dependency warnings flood output but nothing breaks | npm v7+ installs peers automatically; warnings are noise if app works | Check with `npm ls <peer>` — if only one version installed, safe to ignore |
| `pip install -r requirements.txt` works but `pip check` fails | requirements.txt has incompatible upper bounds from different authors | Use `pip-compile` (pip-tools) to resolve a coherent set; add `pip check` to CI |
| `bundle update` downgrades an unrelated gem | Bundler re-solves the whole graph; a newer gem narrowed a shared constraint | Use `bundle update --conservative gem-name` to update only the target gem's graph |
| `go get -u` introduces a module that fails `go mod verify` | Checksum mismatch — module contents changed after publish (supply chain risk) | Do NOT ignore; report to the module maintainer; pin to last known-good SHA |

---

## Workflow

**Step 1 — Detect**: Scan for package files (`package.json`, `go.mod`, `Cargo.toml`, `requirements.txt`, `Gemfile`, `pom.xml`, `*.csproj`). Check for workspace/monorepo patterns. Identify the package manager (npm vs yarn vs pnpm matters for lock file format).

**Step 2 — Prerequisites**: Verify tooling. For Node.js, prefer `taze` over `ncu` (taze respects workspace protocols). For Python, confirm virtualenv is active before any `pip` mutation.

**Step 3 — Scan**: Run the ecosystem's outdated command. Categorize results:
- Fixed (no range specifier) → **skip, note in report**
- PATCH/MINOR within current range → **auto-apply**
- MAJOR or outside current range → **queue for user approval**

**Step 4 — Apply safe updates**: Apply PATCH + MINOR. For Node.js: `taze minor --write` then `npm install`. Run tests if available.

**Step 5 — Gate majors**: For each MAJOR update, present: package name, current version, target version, and changelog URL. Ask individually. Apply only approved ones.

**Step 6 — Audit**: Run the ecosystem's security scanner. Report findings by severity. Do NOT auto-fix — present the vulnerable package, the fix version, and whether it's a breaking change.

**Step 7 — Report**: Summary of what changed, what was skipped (pinned), what needs manual attention (majors declined, unfixed vulns).

---

## Commands Reference

See [`references/commands-by-language.md`](references/commands-by-language.md) for the full command reference per ecosystem.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/check-tool.sh` | Verify a tool is installed, print install hint if missing |
| `scripts/run-taze.sh` | Run taze with safe flags (minor mode, workspace-aware) |
