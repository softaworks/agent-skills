# Dockerfile Patterns — Production Reference

## Multi-Stage: Node.js Application

```dockerfile
# ---- Stage 1: build dependencies ----
FROM node:20-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# ---- Stage 2: build (only if transpilation is needed) ----
FROM node:20-slim AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci                          # includes devDependencies for build
COPY . .
RUN npm run build

# ---- Stage 3: production image ----
FROM node:20-slim AS production
# Create non-root user before dropping privileges
RUN useradd --uid 1001 --no-create-home --shell /bin/false appuser
WORKDIR /app
# Copy only what runtime needs
COPY --from=deps --chown=appuser:appuser /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appuser /app/dist ./dist
COPY --chown=appuser:appuser package.json ./
USER appuser
EXPOSE 3000
# Exec form — PID 1 receives SIGTERM
ENTRYPOINT ["node", "dist/server.js"]
```

**Why three stages instead of two:**
- `deps` installs only production deps (no devDependencies contamination in the final image)
- `builder` installs all deps for compilation, its heavy `node_modules` is discarded
- `production` receives only the compiled output and production deps
- If there is no build step (pure JS, no transpilation), collapse `deps` and `builder` into one stage

## Multi-Stage: Go Binary

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download                 # cached separately from source changes
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app ./cmd/server

# Distroless: no shell, no package manager, minimal attack surface
FROM gcr.io/distroless/static-debian12:nonroot AS production
COPY --from=builder /app /app
EXPOSE 8080
ENTRYPOINT ["/app"]
```

**When NOT to use distroless:** if your service requires `exec` for debugging (`kubectl exec -it`), use `gcr.io/distroless/base` with the `:debug` tag in non-production environments, or maintain a separate debug image. Never ship the debug image to production.

## Single-Stage: Python Script (correct, simpler than multi-stage)

```dockerfile
FROM python:3.12-slim
# Install OS deps and clean in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN useradd --uid 1001 --no-create-home appuser
WORKDIR /app
# Dependencies before source — cache pip install separately from code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Drop privileges before copying app code
USER appuser
COPY --chown=appuser:appuser . .
CMD ["python", "-m", "app.main"]
```

**Why single-stage here:** Python runs interpreted; the source IS the artifact. Multi-stage would copy the same files and achieve nothing except complexity.

## Health Check Design

```dockerfile
# USELESS — checks that a port is bound, not that the app is ready
HEALTHCHECK CMD curl -f http://localhost:8080/ || exit 1

# BETTER — checks an endpoint that verifies actual application readiness
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/healthz || exit 1
```

The `/healthz` endpoint in application code should:
1. Attempt a lightweight read from each critical dependency (DB ping, cache ping)
2. Return 200 only when all dependencies respond within a tight timeout (100-500ms)
3. Return 503 with a JSON body identifying which dependency failed
4. NOT perform writes, migrations, or expensive queries — health checks fire every N seconds

```javascript
// Node.js example
app.get('/healthz', async (req, res) => {
  try {
    await db.raw('SELECT 1');  // DB connectivity check
    res.json({ status: 'ok', db: 'ok' });
  } catch (err) {
    res.status(503).json({ status: 'degraded', db: err.message });
  }
});
```

## Security Hardening Checklist

```dockerfile
# Read-only root filesystem: app cannot write to its own image layer
# Requires writable volumes for any directory the app writes to (logs, tmp, uploads)
# Set in docker run: --read-only, or in compose:
#   read_only: true
#   tmpfs:
#     - /tmp
#     - /var/run

# Drop all capabilities, add back only what is needed
# Set in compose:
#   cap_drop:
#     - ALL
#   cap_add:
#     - NET_BIND_SERVICE   # only if binding to port < 1024 as non-root (prefer port > 1024)

# No new privileges escalation
# Set in compose:
#   security_opt:
#     - no-new-privileges:true
```

## Image Tag Strategy

```dockerfile
# WRONG: non-deterministic across builds
FROM node:latest
FROM node:20

# CORRECT (digest pinning — immutable):
FROM node:20-slim@sha256:a1b2c3d4...

# ACCEPTABLE in practice (version + variant, no mutable latest):
FROM node:20.12.2-slim
```

For internal base images, use a registry mirror with immutable tag policies rather than digest pinning — digest changes on every security patch and requires automation to update. Mutable-but-versioned (`node:20.12.2`) balances determinism with maintainability for application images.
