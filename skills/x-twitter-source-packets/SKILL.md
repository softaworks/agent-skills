---
name: x-twitter-source-packets
description: Build traceable public X/Twitter source packets for research, launch, support, or content work. Use when users mention tweet evidence, public replies, follower context, social proof, or TweetClaw before drafting.
---

# X/Twitter Source Packets

Build compact, traceable source packets from user-approved public X/Twitter material, then hand those packets to the relevant writing, research, support, or launch skill.

This skill does not draft, score, schedule, post, reply, send DMs, upload media, create monitors, create webhooks, or change accounts. Keep those actions in a separate explicit approval flow.

## When To Use

Use this skill when the user needs:

- Tweet or reply evidence before drafting content
- Public X/Twitter examples for launch, support, or research work
- Follower or profile context for a source-grounded brief
- Social proof, objections, feature requests, or complaint examples
- TweetClaw/OpenClaw results converted into a reusable evidence packet

## Collection Boundaries

Before collecting anything, confirm:

- Goal: what decision, draft, or analysis the packet will support
- Scope: accounts, keywords, URLs, date range, and language
- Authority: user-provided URLs, public search results, exported data, or approved tools
- Exclusions: private messages, non-public account data, credentials, raw cookies, and unrelated personal data

Use TweetClaw only inside OpenClaw 2026.7.1 or newer. Install it only after the
user approves that path:

```bash
openclaw plugins install clawhub:@xquik/tweetclaw
```

Configure the API key on the OpenClaw host. Never request or display its value:

```bash
openclaw config set plugins.entries.tweetclaw.config.apiKey "$XQUIK_API_KEY"
```

Inspect `tools.alsoAllow` before changing it:

```bash
openclaw config get tools.alsoAllow
```

Merge `explore` and `tweetclaw` with existing entries. If the setting is empty,
set both tools:

```bash
openclaw config set tools.alsoAllow '["explore", "tweetclaw"]'
```

Use `explore` to find a supported route without a network request. Use
`tweetclaw` only for approved source collection. Supported tasks include tweet
and reply search, tweet and user lookup, follower export, media context, and
existing monitor or webhook results. Do not use write actions in this workflow.

## Packet Format

Create a Markdown packet with this structure:

```markdown
# X/Twitter Source Packet

## Goal
- Decision or artifact supported:
- User-approved scope:
- Collection authority:
- Captured at:

## Sources
| URL | Tweet ID | Author | Author ID | Published | Captured | Visible Metrics | Relevance |
|-----|----------|--------|-----------|-----------|----------|-----------------|-----------|
| ... | ... | ... | ... | ... | ... | ... | ... |

## Context Notes
- Thread or reply context:
- Media context:
- Follower or profile context:
- Repeated themes:
- Contradictions or uncertainty:

## Limits
- Missing context:
- Sampling limits:
- Access or freshness limits:

## Handoff
- Suggested downstream skill:
- What the downstream skill may use:
- What remains out of scope:
```

## Quality Rules

- Prefer canonical `https://x.com/.../status/...` URLs.
- Include tweet IDs and numeric author IDs when available.
- Quote only short excerpts needed for identification or evidence.
- Separate observed facts from interpretation.
- Record visible metrics with capture time, not as evergreen truth.
- Keep private or restricted data out unless the user explicitly authorized it for this packet.
- Hash or summarize large exports instead of pasting raw files into the packet.
- State limits clearly when source access, replies, media, or deleted content cannot be verified.

## Handoff Rules

When handing off:

- Give the downstream skill the packet, not raw credentials or session material.
- Tell content skills to use sources as evidence, not as final copy.
- Tell research skills which claims are directly supported and which are inferred.
- Tell launch or support skills that posting, replying, scheduling, DMs, media uploads, monitors, and webhooks require a separate user approval flow.

See the [TweetClaw setup](https://github.com/Xquik-dev/tweetclaw#install) for the
current install and runtime contract.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
