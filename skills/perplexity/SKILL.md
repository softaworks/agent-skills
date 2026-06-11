---
name: perplexity
description: Web search and real-time research using Perplexity AI. Use when user says "search", "find", "look up", "ask perplexity", "research", or "what's the latest" for generic queries. NOT for library/framework docs (use Context7), workspace questions (use Nx MCP), or gt CLI (use Graphite MCP).
---

# Perplexity Skill

## Mindset

- **Perplexity is a precision instrument, not a firehose** — every extra result and token costs context budget that every subsequent tool call competes for. Constraint by default, expand only on explicit need.
- **Query phrasing determines result quality more than any parameter** — Perplexity's LLM reranks results against the query intent, not raw keywords. A tightly framed question ("postgres advisory lock timeout behavior 2024") beats a vague one ("postgres locks") every time.
- **Search returns sources you evaluate; Ask synthesizes a position** — treat them as distinct tools, not interchangeable alternatives. Choosing wrong wastes a round-trip.
- **The tool-selection chain is a hard prerequisite** — Perplexity is reached only after specialized MCPs (Context7, Graphite, Nx) are ruled out. Jumping straight to Perplexity for docs questions returns inferior, outdated answers.
- **perplexity_research is a trap, not a feature** — it looks like "more thorough" but it consumes 30–50k tokens with no structural advantage over the researcher agent, which provides citations, planning, and synthesis control.

## Navigation

**Use this skill when**:
- User says "search", "find", "look up", "research", "what's the latest", "ask perplexity"
- Topic is general web knowledge, current events, or best-practice surveys
- Need to discover resources (tutorials, articles, benchmarks) not pinned to a codebase

**Do NOT use this skill when**:
- Library/framework API docs → **Context7 MCP** (canonical, versioned, structured)
- Any `gt` command or Graphite workflow → **Graphite MCP**
- Questions about THIS workspace's build/project config → **Nx MCP**
- A specific URL needs scraping → **URL Crawler**
- Deep multi-source synthesis with citations → **Researcher agent** (`/research`)

**Quick decision tree**:
```
Does query mention "gt " or "graphite"?  → Graphite MCP
Does query ask for framework/lib API?    → Context7 MCP
Is query about THIS repo/build config?  → Nx MCP
Does user want a formal research report? → /research agent
Need URLs/source links?                  → perplexity_search
Need a synthesized explanation?          → perplexity_ask
```

## Philosophy

Perplexity tools are the general-purpose fallback after specialized tools are exhausted. Use them conservatively — tight queries, minimal result counts — and escalate to the researcher agent rather than the raw research tool when depth is needed.

## NEVER

- **NEVER call `perplexity_research` directly** — because it burns 30–50k tokens with no user-visible advantage over `/research <topic>`, which adds citations, multi-step planning, and result control. Even one accidental call can exhaust the session context budget.
- **NEVER use default `max_results` (10) or `max_tokens_per_page` without setting limits** — because the Perplexity MCP defaults are calibrated for thoroughness, not cost; 10 results × 1024 tokens floods context before the answer is even processed. Start at `max_results: 3, max_tokens_per_page: 512`.
- **NEVER run Perplexity Search for library/framework API questions** — because Perplexity indexes blog posts and Stack Overflow, not versioned API references. Results will be outdated or wrong for the version in use; Context7 has canonical structured docs.
- **NEVER send a vague keyword query when a specific question would work** — because Perplexity's model optimizes against the full query string. "best practices" returns noise; "postgres connection pool sizing for high-concurrency OLTP 2024" returns actionable signal.
- **NEVER issue multiple Perplexity calls for sub-questions you could batch into one** — because each call occupies a serial tool slot and adds latency. Compose a single Ask message that covers related sub-questions together.
- **NEVER use perplexity_ask for tasks that need source URLs** — because Ask synthesizes without guaranteed citation links; if the user will need to verify or share sources, use Search so you get linkable results.

## Query Formulation Strategies

**For Search** — optimize for source discovery:
- Include year or recency signal: `"postgres replication lag monitoring 2024"`
- Name the ecosystem explicitly: `"Next.js 14 App Router data fetching patterns"` not `"react data fetching"`
- Add format hint when relevant: `"docker compose health check examples github"`

**For Ask** — optimize for synthesis:
- Frame as a direct question: `"What are the production trade-offs between Kafka and RabbitMQ for event sourcing?"`
- Scope to avoid shallow coverage: include constraints (`"for a team of 5"`, `"in a Kubernetes environment"`)
- Ask one composite question rather than chaining multiple Ask calls

**Parameter ladder**:
| Situation | max_results | max_tokens_per_page |
|-----------|-------------|---------------------|
| Default (first attempt) | 3 | 512 |
| Nothing useful found | 5 | 768 |
| User needs comprehensive list | 7 | 1024 |
| Never go above | 10 | 2048 |

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|--------------|----------|
| Results are outdated or wrong version | Query didn't specify version/year; Perplexity indexed old content | Add version number and year to query; try Context7 for API-specific questions |
| Results are off-topic or too broad | Query was vague keywords, not a question | Rewrite as a specific question with ecosystem context |
| Context window pressure after search | Used default (10) results with high token limit | Re-run with `max_results: 3, max_tokens_per_page: 512`; summarize rather than pass raw output |
| Ask returns no citations | Normal behavior for Ask tool | Switch to Search if user needs linkable sources |
| perplexity_research call timed out or blew context | The tool is inherently expensive | Abort; use `/research <topic>` researcher agent instead |

## Tool API Reference

```typescript
// Search — returns URLs + snippets
mcp__perplexity__perplexity_search({
  query: "specific question with context and year",
  max_results: 3,           // ALWAYS set; default 10 is too high
  max_tokens_per_page: 512  // ALWAYS set; reduce context cost
})

// Ask — returns synthesized answer (no guaranteed URLs)
mcp__perplexity__perplexity_ask({
  messages: [{ role: "user", content: "Direct question scoped with constraints" }]
})

// Research — PROHIBITED: use /research agent instead
// mcp__perplexity__perplexity_research(...)  ← NEVER CALL
```

## Tool Priority Chain

1. Context7 MCP — library/framework docs
2. Graphite MCP — any `gt` CLI mention
3. Nx MCP — THIS workspace questions
4. **Perplexity Search** — generic searches needing sources
5. **Perplexity Ask** — conversational synthesis
6. Researcher agent (`/research`) — deep multi-source reports
7. WebSearch — absolute last resort
