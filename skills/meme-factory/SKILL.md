---
name: meme-factory
description: Generate memes using the memegen.link API or textual formats (greentext, copypasta, ASCII, wojak, etc.). Use when users request memes, want to add humor to content, create social media visuals, or need comedic commentary. Trigger keywords: meme, funny, humor, drake, distracted boyfriend, this is fine, greentext.
---

# Meme Factory

---

## Mindset

**Template-emotion fit trumps caption cleverness.** A mediocre caption in the right template lands harder than a perfect joke in the wrong one. Drake works for comparisons; Two-Buttons works for dilemmas; "fine" works for denial. Get the structure right first.

**Irony has a half-life.** Overused templates (e.g., `distracted`, `changemind`) carry cultural baggage — the moment you pick one, the audience already predicts the punchline. Your text must subvert the expectation, not confirm it. A surprise in the bottom text is where the laugh lives.

**Text density is a trust fund you can't overdraw.** Each extra word is a withdrawal. The sweet spot is 3–5 words per caption line. Long-form humor belongs in textual formats (copypasta, chat logs); image memes are haiku, not essays.

**Memegen.link is stateless and idempotent.** Every parameter is in the URL. No upload, no session. If you can construct the URL correctly, it works. The failure modes are all encoding problems, not API problems.

**Textual memes (greentext, wojak, chat logs) are zero-dependency.** They render anywhere Markdown renders, they're accessible, and they give more pacing control than image memes. Reach for them when the joke requires timing or escalation.

---

## Navigation

**Use this skill when**: user asks for a meme, wants to add humor to a post or doc, needs a social media image, or wants to comment on something ironically.

**Do NOT use this skill when**: the request needs sensitive humor (political, personal tragedy, marginalized groups) — generate text commentary instead. Do not produce memes targeting real individuals by name.

**Quick decision tree:**
- Needs visual + shareable URL → memegen.link image meme
- Needs pacing, escalation, or long-form comedy → textual format (greentext, chat log, copypasta)
- Blog/doc embed → either; prefer textual for accessibility
- Social media card (1200×630) → image meme with `?width=1200&height=630`

---

## Philosophy

The meme's job is compression: take a shared cultural structure (the template), inject a specific surprise (your caption), and let the delta between expectation and reality do the comedic work. Your role is to find the right template, write the minimum text that creates maximum surprise, and get out.

---

## NEVER

- **NEVER use `~n` as a newline escape** — it is not a valid memegen.link tilde-escape. The valid set is `~q` `~p` `~s` `~h`. Using `~n` renders literal `~n` text on the image. Use `%0A` for line breaks inside a caption segment.

- **NEVER encode a literal hyphen as `-`** — memegen.link uses `--` (double hyphen) to represent a literal `-` in captions; a single `-` is treated as a space alternative. A caption like `ci-cd` becomes `ci--cd` in the URL, not `ci-cd`.

- **NEVER use `_` to represent a literal underscore** — it encodes as `__` (double underscore). A single `_` is a space. Using one underscore for a literal underscore produces a space on the image.

- **NEVER pick a template by name recognition alone** — `distracted`, `changemind`, and `two-buttons` are irony-collapsed: so many uses exist that audiences see the punchline before reading it. Use them only when you can genuinely subvert the expected direction. Otherwise pick a fresher template.

- **NEVER embed cultural-context-heavy templates without checking decay** — `ugandanknuckles`, `harold` (hide the pain), and `coffin-dance` had peak windows; outside that window they signal "out of touch." When in doubt, use structurally universal templates (`drake`, `gru-plan`, `surprised-pikachu`) that remain legible regardless of recency.

- **NEVER stack more than 2 image memes without a textual break** — readers experience visual fatigue; 3+ images in sequence reads as a slideshow, not comedy. Interleave text formats to control pacing.

- **NEVER leave alt text as `![meme]` or `![funny image]`** — screen readers announce it verbatim. The alt text should describe the joke, e.g., `![Drake rejecting "manual deploy", approving "CI/CD pipeline"]`. The description is the accessibility fallback for the punchline.

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Image shows literal `~n` on screen | Used `~n` as newline escape (not valid) | Replace with `%0A` |
| Hyphen disappeared or became a space | Single `-` used instead of `--` for a literal dash | Double the hyphens: `ci--cd` |
| Template returns 404 | Template ID wrong or misspelled | Fetch `https://api.memegen.link/templates/` and search by keyword |
| Caption text runs off image | Too many words per line (>6 words) | Split at `%0A` or shorten; image memes are haiku, not paragraphs |
| Meme lands flat / misses | Template-emotion mismatch or irony-collapsed template | Re-evaluate: does the template's inherent structure match the joke's logical shape? |

---

## Quick Reference

| Action | Format |
|--------|--------|
| Basic image meme | `https://api.memegen.link/images/{template}/{top}/{bottom}.png` |
| Blank one side | Use `_` (single underscore) as the placeholder |
| Social card sizing | Append `?width=1200&height=630` |
| Remove watermark | Append `?watermark=none` |
| Multiline caption | Use `%0A` between lines inside a caption segment |
| Browse templates | https://api.memegen.link/templates/ |
| API docs | https://api.memegen.link/docs/ |

### Encoding Cheatsheet

| Character | Encode as |
|-----------|-----------|
| Space | `_` |
| Literal hyphen `-` | `--` |
| Literal underscore `_` | `__` |
| `?` | `~q` |
| `%` | `~p` |
| `/` | `~s` |
| `#` | `~h` |
| `"` | `''` (two single quotes) |
| Newline | `%0A` |

---

## Template Selection

| Joke shape | Template |
|------------|----------|
| Reject A, approve B | `drake` |
| Agonizing choice between two bad options | `two-buttons` |
| Plan that collapses at the last step | `gru-plan` |
| Denial while chaos is visible | `fine` |
| Shocked by inevitable outcome | `surprised-pikachu` |
| X is everywhere | `buzz` |
| One does not simply... | `mordor` |
| Statement + "change my mind" (use sparingly) | `change-my-mind` |
| Distracted by new thing (use sparingly) | `distracted` |

---

## Textual Meme Formats

When pacing, escalation, or accessibility matters more than a shareable image, use textual formats. Full guide: [references/markdown-memes-guide.md](references/markdown-memes-guide.md)

| Format | Structure | Best for |
|--------|-----------|----------|
| Greentext | Code fence + `>` lines | Narrative self-deprecation, tech stories |
| Wojak dialogue | Bold archetype names + short lines | Character contrast, internal conflict |
| Chat log | Code fence + `[HH:MM] user:` | Incident retrospectives, system failures |
| Copypasta | Code fence, wall of dramatic text | Parody of overblown outrage |
| Corporate satire | Heading + checkboxes + legal footer | Workplace absurdity |
| Tumblr chain | Nested blockquotes `>` `>>` `>>>` | Escalating reactions |

**Load [references/markdown-memes-guide.md](references/markdown-memes-guide.md)** when: user wants a textual meme, asks for greentext/copypasta/ASCII, or the joke requires multi-step pacing.

**Load [references/examples.md](references/examples.md)** when: user needs ready-to-paste outputs or platform integration (Slack, Discord, GitHub PR comments).

---

## Validation Checklist

After generating any meme:

- [ ] Text 3–5 words per line (image); longer OK for textual formats
- [ ] Template shape matches the logical structure of the joke
- [ ] Special characters encoded correctly (hyphens doubled, no `~n`)
- [ ] Alt text describes the joke, not just "meme"
- [ ] For image memes: verify URL returns 200 before presenting
