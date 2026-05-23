# Search & Data Retrieval Skill

Intelligent decision tree for selecting the right search or data retrieval tool. Prevents common mistakes like using Firecrawl for general search (wastes quota) or Google Grounding to find YouTube links (it can't return them).

## Purpose

This skill teaches the agent a **4-tool decision tree** for any external data task:

- **Google Grounding** — fast facts, news synthesis, date/price checks
- **SearXNG** — structured search with URLs and snippets (YouTube, news, science, images)
- **Gemini fetch** — read a known URL (articles, docs, blogs)
- **Firecrawl** — scrape JS/SPA sites or extract structured tables (use sparingly)

## When to Use This Skill

Activate when the agent needs to:

- Answer a factual question about current events
- Find YouTube videos on a topic
- Search for articles or papers with source links
- Read the content of a specific URL
- Scrape a dynamic site or extract table data

**Activation keywords**: "search", "find", "look up", "open the link", "read the article", "what's on [URL]", "latest news about", "YouTube videos on"

## Key Rules

### Tool Selection Matrix

| Task | Tool |
|------|------|
| Facts, news, definitions | Google Grounding |
| YouTube links & trends | SearXNG (category: videos) |
| Topic search with URLs | SearXNG (category: general) |
| Scientific papers | SearXNG (category: science) |
| Read a specific URL | Gemini fetch |
| JS/SPA site or tables | Firecrawl |

### Critical HTTP Rule

Always use Python `requests` with `json=` parameter for HTTP calls — never `curl` for requests with text bodies. This prevents Cyrillic and Unicode encoding issues.

### Firecrawl Conservation

Firecrawl has a 500-request limit. Use it **only** when Gemini fetch returns empty results or the target is a JavaScript-rendered page.

## Trend Monitoring Combo

For multi-step trend research:
1. SearXNG `videos` + `youtube` engine → get URL list
2. Gemini fetch → read descriptions/transcripts
3. Firecrawl → only if fetch fails
4. Google Grounding → fact-check and add context

## Anti-Hallucination Rules

- **Direct links only** — never provide encoded redirect URLs
- **YouTube format** — always `watch?v=XXXXXXXXXXX` (11-char ID)
- **No fabrication** — if no direct link found, say "Link not found"
- **Data freshness** — for 2024–2026 trends, rely on live search results, not internal knowledge
