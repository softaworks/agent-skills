# Remote Cache Setup

Reference for the monorepo-workspace skill — what gets cached, invalidation models, and setup for Nx Cloud, Turborepo Remote Cache, and self-hosted options.

---

## What Remote Caching Actually Caches

Remote caches store **task output artifacts**, not source code. When a cache hit occurs:
- The task (build, test, lint) is skipped entirely
- Cached output files are restored to the expected `outputs` directory
- Cached stdout/stderr is replayed so CI logs look identical

**What is NOT cached**:
- The node_modules installation step (use lockfile caching for that)
- Any side effects a task performs outside its declared `outputs` (e.g., writing to a database, uploading to S3)
- Tasks that explicitly set `"cache": false`

**The invalidation model**: Cache keys are computed from a hash of:
1. Input file contents (source files + config files affecting the task)
2. Task configuration (the task definition itself)
3. Declared environment variables
4. Dependency task cache keys (recursive — if a dep rebuilds, the consumer also rebuilds)

A cache miss on an upstream package propagates to all downstream consumers. This is correct behavior. A change to `@acme/utils` should invalidate the cache for every app that depends on it.

---

## Nx Cloud

**Free tier**: 500 CI pipeline executions/month for open source; paid plans for private repos beyond the free tier.

**What it adds over local cache**: Shared cache across all CI runners and developer machines. Developer A builds `@acme/utils`; developer B gets a cache hit when they run the same task with the same inputs, even on a different machine.

**Setup**:
```bash
npx nx connect
# Nx adds NX_CLOUD_ACCESS_TOKEN to your CI secrets and updates nx.json
```

```json
// nx.json (auto-updated by nx connect)
{
  "nxCloudAccessToken": "...",
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx-cloud",
      "options": {
        "cacheableOperations": ["build", "test", "lint", "e2e"]
      }
    }
  }
}
```

**Non-obvious**: Nx Cloud also provides distributed task execution (DTE) — CI tasks are distributed across agents automatically. This is a separate feature from remote caching and requires additional CI config. Do not conflate them.

**Cache miss debugging**:
```bash
nx run my-lib:build --verbose
# Shows the cache key computation and which inputs caused a miss
```

---

## Turborepo Remote Cache

**Default provider**: Vercel (free for Vercel users, $0 storage cost).

**Setup with Vercel**:
```bash
npx turbo login       # authenticate with Vercel account
npx turbo link        # link repo to Vercel team for shared cache
```

**CI environment variables** (set in CI secrets, not committed):
```
TURBO_TOKEN=<vercel-token>
TURBO_TEAM=<vercel-team-slug>
```

**Verifying cache hits in CI**:
```bash
turbo run build --dry=json | jq '.tasks[] | {task: .taskId, cache: .cache}'
# "cache": {"status": "HIT"} or "MISS"
```

**Non-obvious — the `env` field is mandatory for correct invalidation**:
```json
// turbo.json
{
  "tasks": {
    "build": {
      "env": ["NODE_ENV", "API_URL"],
      "outputs": ["dist/**"]
    }
  }
}
```
If `build` reads `API_URL` but it's not in `env`, cache hits will restore output built against a different API URL. This is a silent correctness bug, not a performance bug — the output is wrong, not just stale.

---

## Self-Hosted Remote Cache

### Turborepo: Ducktape (open source, self-hosted)

`ducktape` is the most widely used self-hosted Turbo cache server:

```bash
docker run -p 3000:3000 \
  -e TURBO_TOKEN=your-secret-token \
  ducktape/ducktape:latest
```

CI config:
```bash
export TURBO_API=https://your-cache-server.internal
export TURBO_TOKEN=your-secret-token
export TURBO_TEAM=your-team
turbo run build
```

### Nx: Custom Remote Cache

Nx supports custom remote cache via a cache plugin. The simplest self-hosted option uses S3-compatible storage:

```bash
npm install @nx-remotecache/s3 -D
```

```json
// nx.json
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "@nx-remotecache/s3",
      "options": {
        "region": "us-east-1",
        "bucket": "your-nx-cache-bucket",
        "cacheableOperations": ["build", "test", "lint"]
      }
    }
  }
}
```

**IAM policy** (minimum required):
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject", "s3:HeadObject"],
  "Resource": "arn:aws:s3:::your-nx-cache-bucket/*"
}
```

---

## Cache Debugging Checklist

| Symptom | Check |
|---------|-------|
| Cache never hits despite identical code | Env vars not declared in `env`/`globalEnv`; dynamic file reads (e.g., timestamps) in source; non-deterministic build output |
| Cache hits but output is wrong | Side effect outside declared `outputs`; env var affecting output not in cache key |
| Cache hits locally but misses in CI | `inputs` includes files that differ between local/CI (e.g., `.env.local`); add to `.gitignore` AND `turbo.json` `inputs` exclusions |
| Stale cache persisting after config change | Task config hash includes `turbo.json` content — a config change should bust the cache; if not, verify the cache server is using the correct hash algorithm version |
