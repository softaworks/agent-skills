---
name: minimax
description: Configure MiniMax text models, regional API endpoints, capabilities, thinking behavior, and token pricing. Use when users mention MiniMax-M3, MiniMax-M2.7, MiniMax API setup, or MiniMax regions.
---

# MiniMax Provider Guide

Use this skill when configuring a MiniMax text model or selecting a MiniMax API region.

## Configuration Workflow

1. Ask which region the user needs: `global_en` or `cn_zh`. Default to `global_en` only when no region is specified.
2. Ask whether the integration uses the chat completions API or the messages API.
3. Select the model from the capability table below.
4. Use the matching regional base URL. Do not combine endpoints from different regions.
5. Read the API key from `MINIMAX_API_KEY`. Never print, log, or commit it.
6. Present the chosen model, region, API style, base URL, and capability assumptions before making changes.

## Regional Endpoints

| Region | Chat completions base URL | Messages base URL | Documentation |
| --- | --- | --- | --- |
| `global_en` | `https://api.minimax.io/v1` | `https://api.minimax.io/anthropic` | `https://platform.minimax.io/docs` |
| `cn_zh` | `https://api.minimaxi.com/v1` | `https://api.minimaxi.com/anthropic` | `https://platform.minimaxi.com/docs` |

## Model Selection

| Model | Context window | Input modalities | Thinking behavior |
| --- | ---: | --- | --- |
| `MiniMax-M3` | 1,000,000 tokens | text, image, video | adaptive or disabled |
| `MiniMax-M2.7` | 204,800 tokens | text | always on |

Choose `MiniMax-M3` when the request needs image or video input, a context window above 204,800 tokens, or configurable thinking. Choose `MiniMax-M2.7` for text-only requests that require always-on thinking.

## Token Pricing

Prices are in USD per million tokens.

| Model | Input | Output | Cache read | Cache write |
| --- | ---: | ---: | ---: | ---: |
| `MiniMax-M3` | $0.60 | $2.40 | $0.12 | Not specified |
| `MiniMax-M2.7` | $0.30 | $1.20 | $0.06 | $0.375 |

Use these values for estimates only. State the assumptions and calculate each token category separately.

## Validation Checklist

- The model ID is exactly `MiniMax-M3` or `MiniMax-M2.7`.
- The endpoint belongs to the selected region.
- Image and video inputs are used only with `MiniMax-M3`.
- Thinking is always on for `MiniMax-M2.7`.
- The API key remains in `MINIMAX_API_KEY` and is never included in output.
