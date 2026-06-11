# Compose Patterns — Production Reference

## Health-Gated Startup (service_healthy vs. service_started)

```yaml
# compose.yml — base configuration
services:
  postgres:
    image: postgres:16.2
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: app
      POSTGRES_PASSWORD_FILE: /run/secrets/db_password
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d appdb"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s    # grace period before first check counts as failure
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    depends_on:
      postgres:
        condition: service_healthy    # waits for postgres healthcheck to pass
        restart: true                 # restart api if postgres restarts (compose v2.20+)
    environment:
      DATABASE_URL: postgres://app@postgres/appdb
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt   # dev only — use external: true in prod

volumes:
  postgres_data:
```

**`service_started` vs. `service_healthy`:**
- `service_started` (default): compose waits until the container's process starts. For a database, this means the container is running but the DB may still be initializing, accepting connections, and refusing queries. Race condition at startup.
- `service_healthy`: compose polls the healthcheck until it passes before starting dependent services. Eliminates the startup race condition. Requires a `healthcheck` defined on the dependency — if no healthcheck is defined, compose silently falls back to `service_started` behavior without error.

## Override Files for Dev vs. Prod

```
compose.yml          # base: what runs everywhere
compose.override.yml # dev overrides: auto-loaded by `docker compose up`
compose.prod.yml     # prod overrides: explicit `docker compose -f compose.yml -f compose.prod.yml up`
```

```yaml
# compose.yml — base
services:
  api:
    image: myapp/api:${IMAGE_TAG:-local}
    environment:
      NODE_ENV: production
    restart: unless-stopped
```

```yaml
# compose.override.yml — dev (auto-loaded)
services:
  api:
    build: .                          # build locally instead of pulling
    image: myapp/api:local
    environment:
      NODE_ENV: development
    volumes:
      - .:/app                        # bind mount for live reload
      - /app/node_modules             # anonymous volume to shadow host node_modules
    ports:
      - "9229:9229"                   # debugger port not exposed in prod
    command: ["node", "--inspect=0.0.0.0:9229", "dist/server.js"]
```

```yaml
# compose.prod.yml — production
services:
  api:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
    read_only: true
    tmpfs:
      - /tmp
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
```

**Why not a single compose.yml with environment conditionals?** Compose does not support conditional blocks. Environment variables can override individual values but cannot toggle entire blocks (volumes, ports, deploy). Override files are the idiomatic and readable solution.

## Volume vs. Bind Mount Decision

```
Is this production?
├── YES → Use named volumes only.
│         Bind mounts couple the container to a specific host path.
│         Permission drift (UID mismatch) causes silent write failures.
│         Host path may not exist on a new node in a cluster.
└── NO (local development)
         ├── Source code → bind mount (you want edits to reflect live)
         ├── Dependencies (node_modules, .venv) → anonymous volume or named volume
         │   Reason: switching git branches changes package.json; if node_modules
         │   is bind-mounted, the host directory reflects the old branch's installs
         │   until you re-run npm install. Use a volume to keep container deps isolated.
         └── Persistent data (DB data dir) → named volume
             Reason: named volumes survive container recreation; anonymous volumes do not.
```

```yaml
# Correct dev pattern: source mounted, deps isolated
services:
  app:
    volumes:
      - .:/app                        # bind: source code (live reload)
      - app_node_modules:/app/node_modules   # volume: isolated deps
      - app_dist:/app/dist            # volume: build output

volumes:
  app_node_modules:
  app_dist:
```

## Secrets in Compose (never ENV for production secrets)

```yaml
# WRONG: secret visible in `docker inspect`, process environment, /proc/PID/environ
services:
  api:
    environment:
      DATABASE_PASSWORD: s3cr3t

# CORRECT: secret mounted as a file, read by application at startup
services:
  api:
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password   # app reads file, not env var

secrets:
  db_password:
    external: true   # managed by Docker Swarm secrets or an external secrets manager
```

Application-side pattern (Node.js):
```javascript
const password = process.env.DB_PASSWORD_FILE
  ? fs.readFileSync(process.env.DB_PASSWORD_FILE, 'utf8').trim()
  : process.env.DATABASE_PASSWORD;  // fallback for local dev without secrets
```

## Compose for Local Development: Full Example

```yaml
# compose.override.yml — development
services:
  postgres:
    ports:
      - "5432:5432"    # expose to host for local DB tools (TablePlus, psql)

  redis:
    image: redis:7.2-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 2s
      retries: 3

  api:
    build:
      context: .
      target: deps      # build only to the deps stage — skip production optimizations
    volumes:
      - .:/app
      - api_node_modules:/app/node_modules
    environment:
      NODE_ENV: development
      LOG_LEVEL: debug
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  api_node_modules:
```
