# MiniMax Skill

Configure MiniMax text models with the correct regional API base, model capabilities, thinking behavior, and token pricing.

## When to Use

Use this skill when a request mentions:

- MiniMax API configuration
- `MiniMax-M3` or `MiniMax-M2.7`
- Global or China-region MiniMax endpoints
- MiniMax model capabilities, thinking behavior, or cost estimates

## What It Covers

- Region selection for `global_en` and `cn_zh`
- Chat completions and messages API base URLs
- Model selection for text, image, and video inputs
- Context windows and thinking behavior
- Input, output, and cache token pricing
- API key handling through `MINIMAX_API_KEY`

## Installation

Install the plugin from the Agent Toolkit marketplace:

```text
/plugin install minimax@agent-toolkit
```

Then ask the agent to configure MiniMax, select a region or model, or estimate token costs. See `SKILL.md` for the full workflow and current configuration tables.
