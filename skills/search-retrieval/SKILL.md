---
name: search-retrieval
description: |
  Use this skill for any search, URL fetch, or external data retrieval task.
  Determines the correct tool (Google Grounding, SearXNG, Gemini fetch, Firecrawl)
  based on a decision tree, with anti-hallucination rules for links.
triggers:
  - search
  - find
  - look up
  - open the link
  - read the article
  - latest news
  - YouTube videos on
---

# Search & Data Retrieval

## HTTP Requests Rule (CRITICAL)

- **ALWAYS** use Python `requests` with `json=` parameter for ALL HTTP calls
- **NEVER** use `curl` for requests with text bodies — breaks Unicode/Cyrillic encoding

```python
import requests, os
response = requests.post(url, headers={...}, json={...}, timeout=30)
```

---

## Decision Tree — Choose the Right Tool

### 1. Google Grounding (built-in) — first choice for facts

- Fast facts, definitions, general questions
- Current news (synthesizes answer with sources)
- Verifying information, prices, release dates
- ⚠️ Does NOT return YouTube links
- ⚠️ No filters by time or domain

### 2. SearXNG — structured search with links

- Endpoint: `POST $SEARXNG_WEBHOOK_URL`
- Headers: `{"X-API-Key": "$SEARXNG_API_KEY", "Content-Type": "application/json"}`
- Returns list of URLs + snippets, NOT a synthesized answer

```python
import requests, os
response = requests.post(
    os.getenv("SEARXNG_WEBHOOK_URL"),
    headers={
        "X-API-Key": os.getenv("SEARXNG_API_KEY"),
        "Content-Type": "application/json"
    },
    json={
        "query": "YOUR QUERY here",
        "category": "general",
        "time_range": "",
        "engines": ""
    },
    timeout=30
)
results = response.json()
```

| Task | category | engines | time_range |
|------|----------|---------|------------|
| YouTube trends/videos | videos | youtube | month |
| Broad video search | videos | (empty) | month |
| News for a period | news | google news,bing news | week |
| Scientific papers | science | google scholar,semantic scholar,pubmed | (empty) |
| IT documentation | it | (empty) | (empty) |
| Images | images | google images,bing images | (empty) |
| General search (default) | general | (empty) | (empty) |

### 3. Gemini fetch (built-in) — read a specific URL

- Use when you have a concrete URL and need to read its content
- Suitable for articles, blogs, docs, regular websites
- Free, unlimited — always try BEFORE Firecrawl
- Triggers: "read the article", "open the link", "what's written on [URL]"

### 4. Firecrawl — only for complex scraping of a specific URL

- Endpoint: `POST https://api.firecrawl.dev/v1/scrape`
- Headers: `{"Authorization": "Bearer $FIRECRAWL_API_KEY"}`
- Body: `{"url": "TARGET_URL", "formats": ["markdown"]}`
- ⚠️ Limit: 500 requests — use sparingly
- Use ONLY when:
  - Gemini fetch returned empty or incomplete result
  - JavaScript/SPA site (dynamic content)
  - Need tables and structured data

```python
import requests, os

response = requests.post(
    "https://api.firecrawl.dev/v1/scrape",
    headers={"Authorization": f"Bearer {os.getenv('FIRECRAWL_API_KEY')}"},
    json={"url": url, "formats": ["markdown"]},
    timeout=30
)
content = response.json().get("data", {}).get("markdown", "")
```

---

## Tool Selection Matrix

| Task | Tool |
|------|------|
| Facts, news, definitions | Google Grounding |
| YouTube links & trends | SearXNG (videos) |
| Topic search with links | SearXNG (general) |
| Scientific papers | SearXNG (science) |
| Read a specific URL | Gemini fetch |
| JS/SPA site or tables | Firecrawl |

---

## Trend Monitoring Combo

1. SearXNG (category: videos, engines: youtube, time_range: month) → URL list
2. Gemini fetch → read descriptions/transcripts
3. Firecrawl → only if fetch failed
4. Google Grounding → verify facts and context

---

## Forbidden

- `curl` for requests with text (breaks encoding)
- Firecrawl for general topic search (wastes quota)
- Firecrawl instead of Gemini fetch for regular articles
- Google Grounding to find YouTube links (doesn't return them)
- Parallel duplicate requests without a reason

---

## Anti-Hallucination & Link Rules

- **Direct Links Only**: Never provide long encoded redirect URLs
- **YouTube Format**: Always use `watch?v=XXXXXXXXXXX` (exactly 11-char ID)
- **No Fabrication**: If no direct link in results — say "Link not found"
- **Source Verification**: Prioritize URLs from live search results over internal knowledge
- **Data Freshness**: For recent events (2024–2026), rely exclusively on search results
