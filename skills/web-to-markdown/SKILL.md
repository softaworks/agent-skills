---
name: web-to-markdown
description: "Converts web pages (including JavaScript-rendered SPAs) to clean Markdown using the local web2md CLI (Puppeteer + Readability). Use when the user asks to: fetch a URL as markdown, scrape/convert/archive a web page, extract article content, save a webpage to markdown, convert a site page to text, or handle login-walled content. Trigger keywords: fetch URL markdown, web page to markdown, scrape to markdown, convert webpage, extract article, save page as markdown."
metadata:
  version: 0.2.0
---

# web-to-markdown

## Mindset

- A page that "loaded" in a browser is not the same as a page ready for extraction — SPAs hydrate after the DOM fires `DOMContentLoaded`, so the right wait strategy determines success or garbage output.
- Readability scores content by density and structure; nav bars, cookie banners, and sidebars share markup patterns with articles — if output is noisy, the selector or wait strategy is wrong, not Readability.
- Browser sessions are stateful; `--user-data-dir` is the correct persistence primitive — never try to replay login flows with scripted clicks when interactive mode exists.
- `networkidle0` sounds safer than `networkidle2` but routinely hangs on websocket-connected pages and analytics beacons; `networkidle2` is the right default.
- web2md auto-names files from `<title>` slugified — identical titles on different pages silently overwrite; always check output file count when batch-converting.

## Navigation

**Use this skill when**:
- User asks to fetch a URL as Markdown, convert/scrape/archive a webpage, extract article content
- Page is JavaScript-rendered (React, Vue, Angular, Next.js) and raw HTTP fetch returns empty/incomplete content
- User needs to handle a login wall, CAPTCHA, or bot-detection gate before extracting
- Batch converting multiple URLs to markdown files

**Do NOT use this skill when**:
- A simple `WebFetch` built-in tool would suffice (static HTML, no JS rendering required)
- The user wants to interact with a live web app — this is read-only content extraction
- The URL is behind a corporate VPN with no local Chrome access

**Decision tree for ambiguous requests**:
- User says "get this page" → ask: does it need JS rendering? If no, suggest WebFetch; if yes, use this skill
- User says "scrape" → this skill (Puppeteer handles it)
- User says "convert to markdown" + URL → this skill

## Philosophy

Treat every page as JS-rendered until proven otherwise. A slow, correct extraction that waits for the real content is worth more than a fast extraction of boilerplate shell markup.

## NEVER

- NEVER use `--wait-until networkidle0` as a default — because pages with persistent WebSocket connections or analytics SDKs (Segment, Intercom, Heap) never reach zero open connections, causing indefinite hangs.
- NEVER write to the user's real Chrome profile directory — because web2md in Puppeteer can corrupt Chrome's profile lock files and extension state; always use a dedicated `--user-data-dir` path like `./tmp/web2md-profile`.
- NEVER skip output validation after writing files — because web2md exits 0 even on partial renders; an empty or 200-byte `.md` file signals extraction failure, not success.
- NEVER run multiple web2md batch processes concurrently against the same `--user-data-dir` — because Chrome's profile locking causes a crash-loop with no useful error message.
- NEVER use `--wait-for '.container'` or other layout wrappers — because layout elements render before data arrives in SPAs; wait for content-bearing selectors (e.g., `.article-body p`, `[data-content]`) that only appear when real data is present.
- NEVER omit `--no-sandbox` in Docker/CI environments without `SYS_ADMIN` capability — because Puppeteer's sandbox requires kernel-level privileges and fails silently with a cryptic "Target closed" error rather than a clear permission denial.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Output file is empty or < 500 bytes | Wait strategy too fast; Readability found no main content | Add `--wait-ms 2000` or `--wait-for '<content-selector>'`; try `--headful` to inspect visually |
| "Chrome not found" error | Auto-detection failed (Snap/Flatpak/NixOS install) | Set `CHROME_PATH` env var or pass `--chrome-path $(which chromium)` |
| Command hangs indefinitely | `networkidle0` on websocket page, or profile lock collision | Switch to `networkidle2`; kill Chrome processes and clear `--user-data-dir` lockfile |
| "Target closed" in CI | Missing sandbox privileges | Add `--no-sandbox`; or run container with `--cap-add SYS_ADMIN` |
| Login wall blocks content | Session not persisted | Run once with `--interactive --user-data-dir ./tmp/web2md-profile`; subsequent runs reuse the session |
| Duplicate filenames overwrite in batch | Multiple URLs share the same `<title>` | Rename outputs after each run or pipe through a counter prefix script |

## Workflow

1. Check `web2md` is installed: `command -v web2md`
   - If missing: `cd ~/workspace/softaworks/projects/web2md && npm install && npm run build && npm link`
2. Validate URL(s) start with `http://` or `https://`
3. Select wait strategy (default: `--wait-until networkidle2`; see references/wait-strategies.md for decision guide)
4. Run conversion:
   - Single URL to file: `web2md '<url>' --wait-until networkidle2 --out ./page.md`
   - Single URL, auto-named in dir: `mkdir -p ./out && web2md '<url>' --wait-until networkidle2 --out ./out/`
   - Print to stdout: `web2md '<url>' --print`
   - Login-walled: `web2md '<url>' --interactive --user-data-dir ./tmp/web2md-profile --out ./out/`
   - Batch: loop one `web2md` per URL into shared `--out ./out/`
5. Validate: `ls -la <output>` and `wc -c <file>` — flag anything under 500 bytes as likely failed
6. Return file path(s) or Markdown content

## Reference

- Wait strategy selection guide and CI notes: `references/wait-strategies.md`
