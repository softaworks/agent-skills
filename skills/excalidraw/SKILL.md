---
name: excalidraw
description: "Use when working with *.excalidraw or *.excalidraw.json files, user requests diagram creation/editing/explanation, mentions 'flowchart', 'architecture diagram', or 'Excalidraw' — delegates all file operations to subagents to prevent context exhaustion (single files: 4k–22k tokens)"
---

## Mindset

- Excalidraw files are **verbosity traps**: 79 elements × ~280 tokens/element = 22k tokens, but only `text` and `arrow` elements carry semantic content (~10% of file). The other 90% is visual noise.
- **Subagent isolation is free.** A subagent reading a 22k-token file costs nothing to the main context — only its summary (~500 tokens) crosses the boundary. This is always the right trade.
- The rationalization "I'll just quickly check the file" is the most common failure mode. "Quick checks" load the full JSON regardless of intent.
- Token cost comes from volume, not complexity. A "simple, straightforward" Excalidraw file is still 4k–22k tokens.
- Frame elements are grouping hints — subagents should use them to chunk their summaries into logical sections rather than flat component lists.

## Navigation

**Use this skill when:**
- File path ends in `.excalidraw` or `.excalidraw.json`
- User says: explain/update/create/compare diagram, show architecture, visualize flow, draw a flowchart
- Any operation touching Excalidraw files, including "just checking what's in" one

**Do NOT use this skill when:**
- User is asking about Mermaid, draw.io, Lucidchart, or other diagram formats
- User wants to generate a diagram concept only (no file I/O) — then just produce the design description

**Decision tree:**
```
Does the task touch a *.excalidraw file?
  YES → delegate to subagent (no exceptions)
  NO  → does it involve creating a new diagram?
          YES → delegate creation to subagent, get back file path + summary
          NO  → this skill is not needed
```

## Philosophy

Main agents are orchestrators, not file parsers. Every token spent parsing Excalidraw JSON is a token stolen from reasoning. Subagents are disposable context workers — use them for all file I/O and receive only the extracted meaning.

## NEVER

- NEVER use the Read tool on a `.excalidraw` or `.excalidraw.json` file — because the read succeeds silently and consumes 4k–22k tokens before you realize it; there is no size warning.
- NEVER rationalize reading a file as "one-time" or "just this once" — because every session starts fresh, so every read is "just this once"; the exception becomes the pattern.
- NEVER pass raw Excalidraw JSON (or element arrays) back through subagent return values — because a 79-element return dumps the full 22k tokens right back into main context, defeating isolation entirely.
- NEVER skip delegation for "small" files — because even the smallest real Excalidraw file is 4k tokens, and you cannot know the size without reading it (which is exactly what you're trying to avoid).
- NEVER tell a subagent to "read the file and describe everything you see" — because without explicit constraints, subagents default to quoting element details verbatim; always specify the Return format with "plain text only, no JSON".
- NEVER attempt to write Excalidraw JSON from memory without the element schema — because generated files with wrong `version`, missing `appState`, or invalid `id` formats silently fail to open in Excalidraw; use the schema in references/delegation-templates.md.
- NEVER use grep/strings to extract text from Excalidraw files in main context — because the surrounding JSON lines still load into the Read tool output; use `jq` inside the subagent instead.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Subagent returns a wall of JSON instead of a summary | Task prompt missing explicit Return format constraint | Re-delegate with "IMPORTANT: Return ONLY plain text bullet lists — no JSON, no element IDs" prepended |
| File exceeds Read tool limit in subagent (>2000 lines) | 79+ element diagrams hit the line cap | Instruct subagent to use Bash + `jq` to extract text/arrow elements before reading |
| Created diagram won't open in Excalidraw | Invalid file structure or missing required fields | Verify subagent used the canonical wrapper: `{"type":"excalidraw","version":2,"source":"","elements":[...],"appState":{"gridSize":null},"files":{}}` |
| Subagent positions new elements overlapping existing ones | No collision avoidance in modification prompt | Provide explicit position: tell subagent to find the bounding box of existing elements and offset by 200px |
| Arrows missing from created diagram | Subagent created nodes but forgot connection elements | Check that the task template included explicit arrow creation steps; re-delegate with the Modify template from references/ |

## Delegation Pattern

**Main agent responsibilities:**
1. Detect Excalidraw file involvement
2. Choose the correct template (Read / Modify / Create / Compare)
3. Dispatch Task tool with the template
4. Receive text-only summary
5. Respond to user — main context never touches the file

**Load the full templates:** `references/delegation-templates.md` — read this file before constructing subagent tasks. It contains:
- Exact `jq` commands for content extraction
- Element schema (which fields carry meaning vs. noise)
- Standard element dimensions and positioning conventions
- Subagent failure recovery prompts

## Quick Reference

| Operation | Template to Use | Subagent Returns |
|-----------|----------------|------------------|
| Understand diagram | Read/Understand | Component list + directed relationships + summary |
| Add element | Modify/Add Element | New element id + position + confirmation |
| Create new diagram | Create New Diagram | File path + component count + bulleted list |
| Compare two diagrams | Compare Two Diagrams | Set differences + relationship deltas |

## Token Reality Check

| Scenario | Without Delegation | With Delegation |
|----------|--------------------|-----------------|
| Single large file (79 elements) | 22k tokens (45% of 50k budget) | ~500 tokens |
| 7-diagram project survey | 67k tokens (33% of 200k budget) | ~2k tokens |
| Two-file comparison | 18k tokens | ~800 tokens |

**The Iron Law: Main agents NEVER read Excalidraw files. Delegation is not optional.**
