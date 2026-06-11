# Excalidraw Delegation Templates

Use these templates verbatim when creating subagent tasks. Do NOT modify the Return constraints — they prevent subagents from returning raw JSON into the main context.

## Element Schema (What Subagents Work With)

Excalidraw JSON has two top-level keys:
- `type: "excalidraw"` — file marker
- `elements: []` — array of element objects
- `appState: {}` — viewport/UI state (ignore for content extraction)
- `files: {}` — embedded images by hash (ignore unless user asks about images)

### Element Types and Useful Fields

| type | Content Fields | Ignore Fields |
|------|---------------|---------------|
| `rectangle` / `ellipse` / `diamond` | `id`, `text` (if labeled), `groupIds` | `x`, `y`, `width`, `height`, `seed`, `version`, `roughness`, `strokeColor`, `fillStyle`, `opacity` |
| `text` | `id`, `text`, `fontSize`, `groupIds` | All positioning, all styling |
| `arrow` / `line` | `id`, `startBinding.elementId`, `endBinding.elementId`, `label.text` | All geometric points |
| `frame` | `id`, `name` | All positioning |

**Extraction strategy for subagents:** `jq '[.elements[] | select(.type == "text" or .type == "arrow") | {type, id, text, startBinding, endBinding}]'` — reduces 22k token file to ~200 tokens before processing.

---

## Template: Read / Understand

```
Task: Extract and explain the architecture in [FILE.excalidraw.json]

Steps:
1. Use jq to extract text and arrow elements only: jq '[.elements[] | select(.type == "text" or .type == "arrow") | {type, id, text, startBinding, endBinding, label}]' [FILE]
2. Build a component list from text elements
3. Build a relationship map from arrows (startBinding.elementId → endBinding.elementId, resolved to text labels)
4. Identify any frames (logical groupings)

Return (text only — no raw JSON):
- Component list with descriptions
- Directed relationships (A → B format)
- Frame/group boundaries if present
- One-paragraph architecture summary
```

---

## Template: Modify / Add Element

```
Task: Add [COMPONENT] to [FILE.excalidraw.json], connected to [EXISTING-COMPONENT]

Steps:
1. Read file; use jq to find [EXISTING-COMPONENT] element id and bounding box
2. Choose a position that does not overlap existing elements (place right/below with 100px gap)
3. Generate a new element object:
   - type: "rectangle"
   - id: crypto.randomUUID() or nanoid(20)
   - x/y: computed from step 2
   - width: 160, height: 60 (standard box)
   - strokeColor: "#1e1e1e", backgroundColor: "transparent", fillStyle: "solid"
   - text: "[COMPONENT]"
4. Generate an arrow element from [EXISTING-COMPONENT].id to new element.id
5. Append both to elements array; write file

Return:
- New element id
- Chosen position (x, y)
- Arrow id
- Confirmation "File updated: [N] total elements"
```

---

## Template: Create New Diagram

```
Task: Create a new Excalidraw diagram showing [DESCRIPTION], write to [FILE.excalidraw.json]

Steps:
1. List all components/nodes and their relationships from [DESCRIPTION]
2. Plan a grid or flow layout (top-to-bottom for flows, left-to-right for pipelines)
3. Assign positions: start at x=100, y=100; spacing: 200px horizontal, 150px vertical
4. Create element objects for each node (rectangle + text pair or rectangle with label)
5. Create arrow objects for each relationship
6. Wrap in Excalidraw file structure:
   {"type":"excalidraw","version":2,"source":"","elements":[...],"appState":{"gridSize":null},"files":{}}
7. Write to [FILE]

Return:
- File path written
- Component count
- Relationship count
- Bulleted list of components included
```

---

## Template: Compare Two Diagrams

```
Task: Compare [FILE1.excalidraw.json] vs [FILE2.excalidraw.json]

Steps:
1. Extract text labels from FILE1 (jq as above)
2. Extract text labels from FILE2 (jq as above)
3. Compute set differences: only-in-A, only-in-B, shared
4. Compare arrow relationships: list connections unique to each file

Return (no raw JSON):
- Components only in [FILE1]: ...
- Components only in [FILE2]: ...
- Shared components: ...
- Key relationship differences
- One-sentence summary of architectural difference
```

---

## Subagent Failure Recovery

If a subagent returns raw JSON or element dumps, do NOT pass it to main context. Re-delegate with this override prepended to the task:

```
IMPORTANT: Your previous attempt returned raw JSON. Return ONLY:
- Plain text bullet lists
- No JSON objects
- No element IDs unless specifically requested
- Summarize, do not quote
```

If the file exceeds the Read tool limit (>2000 lines), instruct the subagent to use Bash with `jq` to extract content rather than the Read tool.
