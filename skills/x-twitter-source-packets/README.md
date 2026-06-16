# X/Twitter Source Packets

Turn user-approved public X/Twitter material into compact evidence packets for research, launch, support, and content workflows.

## Purpose

This skill helps agents gather and preserve enough context to support a downstream task without mixing source collection with drafting, scoring, posting, or account actions.

## When To Use

Use this skill when you need:

- Tweet or reply evidence before writing
- Public X/Twitter examples for product, support, or launch work
- Follower, profile, or media context for a source-grounded brief
- TweetClaw/OpenClaw results converted into a reusable packet

## Optional TweetClaw Path

TweetClaw requires OpenClaw 2026.7.1 or newer. Install it only after the user
approves this collection path:

```bash
openclaw plugins install clawhub:@xquik/tweetclaw
openclaw config set plugins.entries.tweetclaw.config.apiKey "$XQUIK_API_KEY"
```

Inspect the current `tools.alsoAllow` value:

```bash
openclaw config get tools.alsoAllow
```

Merge `explore` and `tweetclaw` with existing entries. If the setting is empty,
set both tools:

```bash
openclaw config set tools.alsoAllow '["explore", "tweetclaw"]'
```

Use `explore` for local route discovery. Use `tweetclaw` only for approved
source collection. Supported tasks include tweet and reply search, tweet and
user lookup, follower export, media context, and existing monitor or webhook
results.

## What It Produces

The skill produces a Markdown packet with:

- Goal, scope, collection authority, and capture time
- Source table with URLs, tweet IDs, authors, timestamps, metrics, and relevance
- Context notes for threads, replies, media, repeated themes, and uncertainty
- Limits and handoff instructions for the next skill

## Safety Boundaries

This skill does not post, reply, send DMs, upload media, create monitors, create webhooks, schedule content, or change accounts. Those actions require a separate explicit approval flow.

See the [TweetClaw setup](https://github.com/Xquik-dev/tweetclaw#install) for the
current install and runtime contract.

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
