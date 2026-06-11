# Commands by Language

Reference for the dependency-updater skill. Each section covers scan, update, install, and audit commands.

---

## Node.js (npm / yarn / pnpm)

```bash
# Preferred: taze (respects workspace:* protocols, caret/tilde ranges)
taze                                      # scan all
taze minor --write                        # apply minor+patch
taze major --write --include pkg1,pkg2    # apply approved majors only
taze -r                                   # recursive (monorepo)

# Fallback: npm
npm outdated
npm update                                # minor/patch within ranges only
npm install pkg@latest                    # specific package to latest

# Install after changes
npm install          # npm
pnpm install         # pnpm
yarn                 # yarn

# Security
npm audit                                 # show vulnerabilities
npm audit fix                             # fix without breaking semver (safe)
# DO NOT: npm audit fix --force           # breaks constraints

# Conflict diagnosis
npm ls pkg-name           # show why a version was installed
npm explain pkg-name      # dependency path explanation
npm dedupe                # collapse duplicate transitive versions
```

**Lock file formats**: `package-lock.json` (npm), `yarn.lock` (yarn), `pnpm-lock.yaml` (pnpm). Never commit more than one.

---

## Python

```bash
# Scan
pip list --outdated
pip-review                           # interactive review

# Update
pip install --upgrade pkg-name       # single package
# WARNING: only inside active virtualenv:
pip-review --auto                    # all packages

# Verify consistency
pip check                            # detect incompatible installed packages

# Security
pip-audit                            # CVE scan via PyPI advisory db
safety check                         # alternative (requires API key for full data)

# Conflict resolution
pipdeptree -p pkg-name               # why a package is at its current version
pip-compile requirements.in          # regenerate requirements.txt with full resolution
```

**Virtualenv check before any mutation**: `python -c "import sys; assert sys.prefix != sys.base_prefix, 'Not in venv'"`.

---

## Go

```bash
# Scan
go list -m -u all                    # show available updates for all modules

# Update (targeted — safer than bulk -u)
go get pkg@latest                    # single module
go get pkg@v1.2.3                    # pin to specific version

# CAUTION with bulk update:
# go get -u ./...  — ignores replace directives for indirect deps

# Tidy (always run after any go get)
go mod tidy                          # remove unused, add missing, update go.sum

# Verify (supply chain check)
go mod verify                        # verify go.sum hashes match downloaded content

# Security
govulncheck ./...                    # Go vulnerability database scan
```

---

## Rust

```bash
# Scan
cargo outdated                       # requires cargo-outdated: cargo install cargo-outdated

# Update (within Cargo.toml semver ranges)
cargo update                         # all crates within ranges
cargo update -p crate-name           # single crate

# After update, always verify workspace compiles
cargo check --workspace

# Security
cargo audit                          # requires cargo-audit: cargo install cargo-audit
```

---

## Ruby

```bash
# Scan
bundle outdated

# Update (conservative = only updates the named gem's subgraph)
bundle update --conservative gem-name
bundle update                        # full re-solve (use carefully — see NEVER list)

# Install
bundle install

# Security
bundle audit                         # requires: gem install bundler-audit
bundle audit update                  # refresh the advisory database first
```

---

## Java (Maven)

```bash
# Scan
mvn versions:display-dependency-updates
mvn versions:display-plugin-updates

# Update
mvn versions:use-latest-releases     # updates to latest release (skips snapshots)
mvn versions:use-latest-versions     # includes snapshots

# Security
mvn dependency:tree                  # review full tree
mvn dependency-check:check           # OWASP dependency check plugin
```

---

## .NET

```bash
# Scan
dotnet list package --outdated
dotnet list package --vulnerable     # security scan

# Update (no bulk command — must update per package)
dotnet add package PackageName               # latest stable
dotnet add package PackageName --version X.Y.Z  # specific version

# Tool: dotnet-outdated (third-party, recommended)
dotnet tool install -g dotnet-outdated
dotnet outdated                              # then apply interactively
```

---

## Emergency Resets (last resort only)

### Node.js
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```
Risk: all transitive versions re-resolved; may introduce new breakage.

### Python
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip check
```

### Go
```bash
rm go.sum
go mod tidy      # regenerates go.sum from module cache or network
go mod verify    # confirm integrity
```
