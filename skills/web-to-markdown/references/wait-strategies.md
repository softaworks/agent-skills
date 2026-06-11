# web2md Wait Strategy Reference

## Choosing the Right Wait Strategy

| Page Type | Recommended Strategy | Reasoning |
|-----------|---------------------|-----------|
| Static HTML / news articles | `--wait-until load` | Fast; content is in initial HTML |
| React/Vue/Angular SPA | `--wait-until networkidle2` | Waits for JS hydration |
| Infinite scroll / lazy images | `--wait-until networkidle2 --wait-ms 2000` | Extra settle time |
| Dashboard with async data | `--wait-until domcontentloaded --wait-for '[data-loaded]'` | Wait for data-ready attribute |
| Login-walled | `--interactive --user-data-dir ./tmp/web2md-profile` | Human completes login |
| Cloudflare / bot detection | `--interactive` first run, then `--user-data-dir` to reuse session | |
| Heavy analytics (GA, Segment) | `--wait-until networkidle0` | Waits for ALL network quiet (slower) |

## networkidle0 vs networkidle2

- `networkidle0`: zero open connections for 500ms — catches analytics beacons but often hangs on websocket pages
- `networkidle2`: fewer than 3 connections for 500ms — practical default; rarely hangs

## Selector Wait Pattern

Use `--wait-for` with the most stable, content-specific selector — not a container that renders before data arrives.

Bad: `--wait-for '.app-container'`  (renders empty)
Good: `--wait-for '.article-body p'` (renders with content)

## Batch Conversion

For multiple URLs, run one `web2md` command per URL into a shared output directory. web2md auto-names files from the page `<title>` tag, slugified. Collision-safe for distinct pages; identical titles will overwrite — add a counter prefix if needed.

```bash
mkdir -p ./out
for url in "${urls[@]}"; do
  web2md "$url" --wait-until networkidle2 --out ./out/
done
```

## Chrome Path Auto-Detection Order

web2md tries (in order):
1. `CHROME_PATH` env var
2. Standard install locations per OS (Linux: `/usr/bin/google-chrome`, `/usr/bin/chromium-browser`)
3. `which google-chrome`, `which chromium`

Override with `--chrome-path` when running in non-standard environments (Snap, Flatpak, NixOS).

## Container / CI Notes

In headless CI (Docker, GitHub Actions):
- Add `--no-sandbox` — kernel sandbox is unavailable without `SYS_ADMIN` capability
- Or run the container with `--cap-add SYS_ADMIN`
- `networkidle0` often hangs in CI due to keepalive connections; prefer `networkidle2` + `--wait-ms`

## Persistent Sessions

`--user-data-dir` stores cookies, localStorage, and service workers. Use a **dedicated directory** (not your real Chrome profile) to avoid corrupting browser state. Safe pattern:

```bash
web2md 'https://example.com' --interactive --user-data-dir ./tmp/web2md-profile --out ./out/
# After first interactive login, subsequent runs reuse the session:
web2md 'https://example.com/protected' --user-data-dir ./tmp/web2md-profile --out ./out/
```
