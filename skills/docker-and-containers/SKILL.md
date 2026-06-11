---
name: docker-and-containers
version: 1.0.0
description: "Expert Docker and container patterns — multi-stage build design, layer cache ordering, image size optimization, signal handling (SIGTERM/PID 1 gap), compose health dependencies, and container security hardening. Use when writing Dockerfiles, diagnosing build cache misses, sizing images, securing containers, debugging startup race conditions, or designing compose service dependencies."
---

# Docker and Containers

## Mindset

1. **Layer cache is a directed acyclic graph, not a stack.** Every instruction after a cache miss re-executes. The ordering rule is: most stable content first. `COPY package.json` before `COPY .` because your application code changes every commit but dependencies change once a week. A single mis-ordered COPY invalidates all downstream layers on every build.
2. **Shell form ENTRYPOINT is always wrong.** `ENTRYPOINT ["node", "server.js"]` (exec form) makes Node.js PID 1 — it receives SIGTERM directly. `ENTRYPOINT node server.js` (shell form) makes `/bin/sh -c` PID 1 — it does not forward signals. Your app never receives SIGTERM and Kubernetes/Docker kills it with SIGKILL after the grace period, causing ungraceful shutdown every time.
3. **Image layers are append-only — deletion is not deletion.** `COPY . .` then `RUN rm -rf secrets/` leaves `secrets/` in the lower layer permanently, visible via `docker history`. Same for `RUN apt-get install X && RUN apt-get clean` — the package cache was written in layer N, the clean ran in layer N+1, the cache is still in layer N. Commands that write and delete must be in the same `RUN`.
4. **A health check that checks a port is not a health check.** `curl -f http://localhost:8080/` returns 200 whether the app has a working database connection or not. Check an endpoint that exercises an actual dependency: `/healthz` that queries the DB and returns 200 only when ready. Compose `depends_on: condition: service_healthy` is meaningless without a health check that represents real readiness.
5. **Secrets baked into images are permanent.** `ENV API_KEY=secret` is visible in `docker inspect` on any host with pull access. `ARG SECRET` is visible in `docker history`. Neither is erased by a subsequent layer. Runtime secret injection (mounted files, environment from a secrets manager at startup) is the only safe path.

## Navigation

**Use this skill when:**
- Writing or reviewing a Dockerfile (new service, base image upgrade, size reduction)
- Diagnosing slow or broken build cache (layer invalidation debugging)
- Designing compose service startup order with health dependency requirements
- Hardening a container for production (non-root, capabilities, read-only filesystem)
- Debugging graceful shutdown failures (SIGTERM not received, zombie processes)
- Choosing between single-stage vs. multi-stage build

**Do NOT use this skill when:**
- Kubernetes deployment YAML design (pod specs, resource limits, liveness vs. readiness probes at the k8s layer) — those have different semantics than Docker health checks
- Container runtime selection (containerd, CRI-O, gVisor) — this skill covers Docker/Compose-layer decisions
- CI/CD pipeline orchestration beyond the image build step

**Decision tree — multi-stage vs. single-stage:**

```
Is the build producing a compiled artifact (Go binary, Java jar, webpack bundle)?
├── YES → Multi-stage: builder stage compiles, production stage copies artifact only
└── NO → Is the runtime the same as the build environment?
         ├── YES → Single-stage is correct; multi-stage adds complexity with no benefit
         └── NO (e.g., Python venv to slim image) → Multi-stage to avoid build tools in production
```

**Decision tree — alpine vs. slim vs. distroless:**

```
Does the app need a shell at runtime (startup scripts, exec into container)?
├── YES → use slim (debian-based, has bash/sh, ~80MB base)
└── NO → Does the app dynamically link glibc?
          ├── YES, statically linked → distroless/static (~2MB, no shell, no package manager)
          ├── YES, dynamically linked → distroless/base (~20MB, glibc only)
          └── UNKNOWN / uses musl → alpine (~5MB, musl libc — verify all dependencies compile against musl)
```

## Philosophy

Container images are artifacts, not environments. The image defines what runs, not where it runs. Every byte in the image is a liability: a larger attack surface, a slower pull, a staler dependency. Build the smallest image that runs the application correctly, signal-handles cleanly, and contains zero credentials.

## NEVER

- **NEVER use the `latest` tag in production Dockerfiles** — `latest` is a mutable pointer; a registry push by any team member silently changes what your `docker pull` fetches. Pin to a digest (`image@sha256:...`) or an immutable version tag. Your build is otherwise non-deterministic across environments.
- **NEVER store secrets in `ENV`, `ARG`, or `COPY`** — they appear in `docker inspect`, `docker history`, and are baked into the layer graph permanently. A subsequent layer that deletes the secret does not remove it from earlier layers. Use runtime secret injection: mounted secret files, environment variables set by the orchestrator at start time, or a secrets manager SDK.
- **NEVER run `RUN apt-get update` in a separate layer from `apt-get install`** — the update layer is cached. On a subsequent build days later, Docker uses the stale cached update layer, `apt-get install` runs against an outdated package index, and packages are silently "not found" or install wrong versions. Always `RUN apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*` in a single instruction.
- **NEVER use shell form for `ENTRYPOINT`** — `ENTRYPOINT node server.js` wraps the process in `/bin/sh -c`, which becomes PID 1. The shell does not forward SIGTERM to child processes. Your application never receives the graceful-shutdown signal and gets SIGKILL'd after the stop grace period expires. Use exec form: `ENTRYPOINT ["node", "server.js"]`.
- **NEVER use `ADD` instead of `COPY` for local files** — `ADD` has two implicit behaviors that `COPY` does not: it auto-extracts tar archives and it fetches from URLs. If a file path happens to be tar-shaped or a future maintainer adds a URL argument, `ADD` silently does something different than expected. `COPY` copies files. Use `COPY` for files; use `RUN curl` with explicit flags if you need network fetch.
- **NEVER run the production container process as root when a non-root option exists** — a container escape (kernel vulnerability, misconfigured mount) with root inside the container is root on the host in many configurations. Add a non-root user and place `USER nonroot` after all `RUN` instructions that require root (package installs, chowns), but before the final `COPY` of application files.
- **NEVER write-then-delete in separate `RUN` instructions** — files written in one layer persist in the image even if deleted in the next. Package caches, build artifacts, and secrets must be created and removed in the same `RUN` command using `&&`.

## Core Patterns

See `references/dockerfile-patterns.md` for annotated production-ready Dockerfiles.
See `references/compose-examples.md` for compose health dependency and override file patterns.

### Signal-safe ENTRYPOINT

```dockerfile
# WRONG — shell form, PID 1 is /bin/sh, SIGTERM not forwarded
ENTRYPOINT node server.js

# CORRECT — exec form, PID 1 is node, receives SIGTERM directly
ENTRYPOINT ["node", "server.js"]
```

If the application does not handle SIGTERM itself, use `tini` as a minimal init:
```dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--", "node", "server.js"]
```

### Layer ordering for cache efficiency

```dockerfile
# WRONG — code change invalidates npm install on every build
COPY . .
RUN npm ci

# CORRECT — package.json changes rarely; code changes often
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY . .
```

### Non-root user placement

```dockerfile
# WRONG — USER before package install requires root but breaks permission
USER nonroot
RUN apt-get install -y curl    # fails: nonroot has no apt access

# CORRECT — root for installs, then drop privileges before app code
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 1001 --no-create-home nonroot
USER nonroot
COPY --chown=nonroot:nonroot . .
```

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Build cache always misses at `RUN npm install` | `COPY . .` appears before `COPY package.json` — code changes invalidate package copy | Reorder: copy lockfile first, install, then copy source |
| Container exits immediately on `docker stop` with exit code 137 | Shell-form ENTRYPOINT; app never receives SIGTERM; Docker sends SIGKILL after grace period | Switch to exec-form ENTRYPOINT; optionally add tini for signal forwarding |
| `apt-get install` fails with "unable to find package" in CI but not locally | `apt-get update` in a cached layer; local cache is warm, CI cache is stale | Merge update and install into a single `RUN` instruction |
| Image is unexpectedly large after `RUN rm -rf build-artifacts/` | Deletion in a separate layer — files still exist in the layer that wrote them | Combine write and delete in one `RUN`; use multi-stage to avoid the files entirely |
| Compose service starts before database is ready, crashes | `depends_on` with `condition: service_started` (default) — only waits for container start, not readiness | Add `healthcheck` to the database service; use `condition: service_healthy` in dependent service |
| Secret visible in `docker history` | `ARG SECRET` or `ENV SECRET` used during build | Remove from Dockerfile entirely; inject at runtime via orchestrator secrets or mounted file |
| Volume data stale after git branch switch | Bind mount persists host directory state across branches; node_modules or build cache reflects old branch | Use named volume for dependency caches in development; bind mount only source code |
