---
name: crafting-effective-readmes
description: Use when writing, improving, or reviewing README files. Triggers: "write a README", "improve my README", "update README", "my README is outdated", "create documentation for my project". Covers OSS, internal, personal, and config project types.
---

# Crafting Effective READMEs

## Mindset

1. **The README is a cognitive funnel, not a table of contents.** Readers scan broad-to-specific: they decide in 10 seconds whether to read further. Every section either advances or stalls that funnel. Front-load the decision-enabling content (what + why + does it work for me).

2. **The documentation defines what the module does — the code does not.** A README without enough detail forces readers into source code. That's a failure. The goal is to keep users *out* of the source by providing everything needed to evaluate and use the project without reading implementation.

3. **Brevity is a feature, but incompleteness is a bug.** The ideal README is as short as it can be without being any shorter. When in doubt between too long and too short, choose too long — but put the excess in separate files, not in the README.

4. **Write for the stranger, not the author.** After 6 months, even the author is a stranger to their own project. The README is a contract with your future confused self as much as with new users.

5. **Match complexity to audience, not to effort.** A config folder README needs "what's here + why + gotchas" in 20 lines. An OSS library README needs install, quickstart, and API shape. Adding OSS sections to a config README is noise, not thoroughness.

## Navigation

**Use this skill when:**
- Writing a README from scratch for any project type
- Improving or restructuring an existing README
- Updating a README after project changes
- Reviewing a README for completeness or accuracy

**Do NOT use this skill when:**
- Writing other documentation (wikis, API docs, changelogs) — those have separate concerns
- Improving prose quality only — use `writing-clearly-and-concisely` instead
- The "README" is actually a CONTRIBUTING.md, CHANGELOG.md, or LICENSE — different audiences and formats

**Complexity decision tree:**

```
What is this project?
├── Config folder / dotfiles      → Simple (20-40 lines): what's here, why, gotchas, how-to-extend
├── Personal/portfolio project    → Medium (40-100 lines): what + stack + quick demo + learnings
├── Internal/team tool            → Medium (60-120 lines): setup + architecture + runbooks + gotchas
└── OSS library/CLI               → Full (100-300 lines): install + quickstart + API + contributing + license
    └── Is it a published package? → Also add: badges, examples, support channels
```

## Philosophy

A README is the one-stop shop that defines your project's contract with the world. It exists to keep users out of the source code. Everything else follows from that.

## NEVER

- NEVER open with implementation details before establishing what the project does — readers abandon before reaching the useful part. The description must appear in the first 5 lines.
- NEVER add badges to internal tools or config READMEs — badges signal "public OSS" and create noise for teammates who don't care about CI status on a dotfiles folder.
- NEVER write "Usage: See code for examples" or leave the usage section without at least one runnable example — this is the single most common reason a developer gives up and looks elsewhere.
- NEVER use a wall of prose for setup steps — numbered lists are not optional for installation; sequential prose causes missed steps and support requests.
- NEVER omit environment/OS prerequisites from install instructions — assuming "they know they need Node 18" is the most common cause of "it doesn't work" issues. State every non-obvious requirement.
- NEVER copy-paste a generic OSS template into an internal project — internal READMEs need runbooks and architecture, not badges and license text; wrong template creates confusion about intended audience.
- NEVER leave a README with a "Last Reviewed" date more than 6 months old without flagging it as potentially stale — a wrong README is worse than no README because it actively misleads.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| User can't figure out what the project does after reading | Description is buried below badges/ToC/motivation paragraphs | Move description to line 1-2; cut everything above it |
| Setup steps fail for new users but work for author | Prerequisites (OS version, env vars, global deps) assumed not stated | Add explicit Requirements subsection listing every non-obvious dependency |
| README feels too long but cutting feels wrong | Right content, wrong location — detail belongs in separate docs | Move API reference / deep examples to `docs/` or a wiki; link from README |
| Reviewer says README is "stale" | Project evolved but README wasn't updated as part of PRs | Add a "Last Reviewed" line; establish README-in-PR checklist habit |

## Reference Loading Guide

Load references only when needed — don't pull all into context:

| Situation | Load |
|-----------|------|
| Writing for a public OSS project | `references/art-of-readme.md` — cognitive funneling, brevity principles |
| Need section-by-section guidance | `references/make-a-readme.md` — concrete suggestions per section |
| OSS project needs a standardized format | `references/standard-readme-spec.md` + examples |
| Need a starting template | `templates/oss.md`, `templates/internal.md`, `templates/personal.md`, `templates/xdg-config.md` |
| Checking section completeness | `section-checklist.md` |

## Process

**Step 1 — Identify project type:** OSS / Personal / Internal / Config (ask if unclear; never assume OSS)

**Step 2 — Identify task:**
- Creating: use the matching template, ask "what problem in one sentence + quickest path to working"
- Updating: read current README, identify stale sections against actual project state
- Reviewing: check package.json/main files vs README claims; flag mismatches

**Step 3 — Apply the three-section minimum:** Every README needs Name + Description (1-2 sentences, what + why) + Usage (with at least one example).

**Step 4 — After drafting:** Ask "Anything else to highlight or include that I might have missed?"
