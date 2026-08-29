# Hermes Tweet

Add catalog-guided X research and approval-gated X actions to Hermes Agent
through Xquik.

## Use Cases

- Search X posts, replies, profiles, timelines, and trends
- Monitor brands, launches, accounts, keywords, and communities
- Research creators, audiences, and public conversations
- Export followers or following accounts
- Run approved posts, replies, likes, retweets, follows, DMs, media actions,
  monitors, webhooks, extraction jobs, and giveaway draws

## Install

Install and enable the plugin:

```bash
hermes plugins install Xquik-dev/hermes-tweet --enable
```

Hermes scans plugins during installation and updates. Review each warning. A
dangerous verdict blocks installation or disables the update.

Or install the published package in the Hermes environment:

```bash
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python hermes-tweet
hermes plugins enable hermes-tweet
```

Set `XQUIK_API_KEY` on the Hermes runtime host for authenticated reads. Keep
`HERMES_TWEET_ENABLE_ACTIONS` unset or false unless the workflow needs an
approved private or mutating operation.

After environment changes, run `/reload` in an active CLI session. Restart
gateway and cron sessions. Remote Hermes Desktop profiles need the plugin and
environment variables on the remote host.

## Tools

| Tool | Purpose |
| --- | --- |
| `tweet_explore` | Search the endpoint catalog without an API call. |
| `tweet_read` | Call catalog-listed public read endpoints. |
| `tweet_action` | Call approved private or mutating endpoints. |

Start with `tweet_explore`. Use only the method and path it returns. Keep
`tweet_action` disabled for unattended workflows without an approval step.

## Verify

```bash
hermes plugins list
hermes tools list
hermes -z "Use tweet_explore to show Xquik capabilities." --toolsets hermes-tweet
```

Confirm `tweet_explore` works without an API key. Confirm `tweet_read` appears
after the key is configured. Confirm `tweet_action` stays hidden until actions
are enabled.

## Resources

- [Hermes Tweet repository](https://github.com/Xquik-dev/hermes-tweet)
- [Xquik setup guide](https://docs.xquik.com/guides/hermes-tweet)
- [Hermes Agent plugin guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [PyPI package](https://pypi.org/project/hermes-tweet/)

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.
