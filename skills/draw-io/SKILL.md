---
name: draw-io
description: Create, edit, review, and convert draw.io diagrams (.drawio XML). Use for AWS architecture diagrams, flowcharts, layout adjustment, PNG export, icon selection, and Quarto/reveal.js slide integration. Triggers on: "draw a diagram", "create architecture diagram", "edit drawio", "add AWS icon", "convert to PNG", "fix layout", "drawio XML".
---

# draw.io Diagram Skill

## Mindset

1. **XML-first thinking**: draw.io files are plain XML — read and write them as structured data, not as visual canvas operations. Every position, style, and connection is deterministic from the XML.
2. **Layer ordering is load order**: Elements render in document order — put arrows before boxes, not after, or arrows will overdraw icons. This is non-obvious because draw.io GUI handles z-order separately.
3. **Verify with PNG, not XML**: Layout bugs (overflow, label collision, arrow penetration) are invisible in XML. Always run conversion and inspect the raster output before declaring done.
4. **Icon type is a decision, not a guess**: resourceIcon vs productIcon vs generic shape have different geometry contracts. Choosing wrong produces misaligned or invisible icons. Use the selector table below.
5. **Margins are asymmetric**: 30px is the minimum inner margin for straight edges, but rounded corners (`rounded=1`) consume extra space — add strokeWidth × 2 to your margin calculations.

## Navigation

### Use this skill when
- Creating or editing `.drawio` XML files
- Selecting the right AWS icon style (resource vs product vs group)
- Converting diagrams to PNG for slides or documentation
- Debugging element overflow, arrow overlap, or label collision
- Setting up consistent fonts for Quarto / reveal.js presentations

### Do NOT use this skill when
- The target format is Mermaid, PlantUML, or Excalidraw — use the matching skill
- You need a diagram embedded directly in Markdown without a separate file
- The goal is purely a sequence diagram — Mermaid sequence syntax is faster

### Icon-Type Decision Tree

| Scenario | Use | Style Fragment |
|---|---|---|
| Single AWS service (EC2, Lambda, S3, RDS…) | resourceIcon | `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{name}` |
| AWS service product tile (larger, with label strip) | productIcon | `shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.{name}` |
| VPC / subnet / availability zone boundary box | Group shape | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_{name}` |
| Non-AWS box (database, user, external system) | Generic shape | `rounded=1;whiteSpace=wrap;html=1` |
| AWS Cloud outer boundary | AWS Cloud group | `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt` |

Standard resourceIcon size: 60×60px. productIcon: 80×80px. Group boxes: size to contents.

## Philosophy

draw.io diagrams are source code: they must be deterministic, diff-able, and reproducible. Treat every XML edit with the same discipline as code — no magic numbers, no visual tweaks without understanding the coordinate system, and always verify the rendered output.

## NEVER

- **NEVER edit `.drawio.png` files directly** — they are auto-generated artifacts; edits are silently overwritten on next conversion and the source XML diverges from the rendered image.
- **NEVER use `mxgraph.aws3.*` icons** — the aws3 set is deprecated and renders placeholder boxes in current draw.io versions; always use `mxgraph.aws4.*`.
- **NEVER rely on `exitX`/`exitY` connection points on text elements** — text cells have no port geometry; the connector snaps to the bounding box corner unpredictably. Use explicit `mxPoint sourcePoint`/`targetPoint` coordinates instead.
- **NEVER set `background="#ffffff"` on the mxGraphModel** — white backgrounds break dark-theme slides and PDFs; omit the attribute or set `page="0"` to get transparent output.
- **NEVER place arrows after icon/box elements in XML** — draw.io renders in document order; arrows declared after shapes render on top of icons, obscuring them. Arrows must appear immediately after the title cell.
- **NEVER assume 30px margin is enough inside a rounded container** — `rounded=1` with `strokeWidth=3` eats ~9px of visual space on each side; use `frameMargin = 30 + (strokeWidth × 2)` as your actual inner boundary.
- **NEVER abbreviate AWS service names in labels** — use "Amazon ECS", not "ECS"; "AWS Lambda", not "Lambda". Official names are required for compliance diagrams and searchability.

## Conversion Commands

```sh
# Convert all .drawio files via pre-commit hook
mise exec -- pre-commit run --all-files

# Convert specific file
mise exec -- pre-commit run convert-drawio-to-png --files assets/my-diagram.drawio

# Run conversion script directly
bash ~/.claude/skills/draw-io/scripts/convert-drawio-to-png.sh assets/diagram.drawio
```

Internal drawio CLI flags used:

| Option | Effect |
|---|---|
| `-x` | Export mode |
| `-f png` | PNG output format |
| `-s 2` | 2× scale (high resolution) |
| `-t` | Transparent background |
| `-o` | Output path |

## Font Settings

For Quarto / reveal.js slides, set font at both model and element level:

```xml
<mxGraphModel defaultFontFamily="Noto Sans JP" ...>
  ...
  <mxCell style="text;html=1;fontSize=27;fontFamily=Noto Sans JP;" .../>
```

Font size: use 1.5× standard (≈18px minimum; 27px for slide titles). Japanese text: allow 30–40px per character width.

## Layout Rules

### Coordinate System
- `x`, `y` = top-left corner of element bounding box
- Element center = `y + height/2`
- To vertically align two elements: set their center values equal

### Container Margins
```text
Effective inner boundary = containerY + 30 + (strokeWidth × 2)
                          to
                          containerY + containerHeight - 30 - (strokeWidth × 2)
```

### Arrow Placement (XML Order)
```xml
<!-- 1. Title -->
<mxCell id="title" value="Diagram Title" .../>

<!-- 2. Arrows — MUST come before icons/boxes -->
<mxCell id="arrow1" style="edgeStyle=orthogonalEdgeStyle;" edge="1" ...>
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="200" y="150" as="sourcePoint"/>
    <mxPoint x="500" y="150" as="targetPoint"/>
  </mxGeometry>
</mxCell>

<!-- 3. Icons and boxes (rendered on top of arrows) -->
<mxCell id="ec2" style="shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.ec2" .../>
```

### Edge Label Offset
```xml
<!-- Label above arrow -->
<mxPoint x="0" y="-40" as="offset"/>

<!-- Label below arrow -->
<mxPoint x="0" y="40" as="offset"/>
```

## AWS Icon Reference

Search for icons:
```sh
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py ec2
python ~/.claude/skills/draw-io/scripts/find_aws_icon.py lambda
```

Full catalog: [references/aws-icons.md](references/aws-icons.md)
Layout rules in depth: [references/layout-guidelines.md](references/layout-guidelines.md)

## Diagram Type Selector

| When the user asks for… | Recommend this diagram type |
|---|---|
| "How does the system work?" | Context Diagram |
| "What are the main components?" | System Diagram |
| "How are services wired together?" | Component Diagram |
| "Where does it run / what regions?" | Deployment Diagram |
| "How does data move?" | Data Flow Diagram |
| "What happens step by step?" | Sequence Diagram |

## When Things Go Wrong

| Symptom | Likely Cause | Fix |
|---|---|---|
| Icon renders as empty box or placeholder | Using `mxgraph.aws3.*` (deprecated) | Replace with `mxgraph.aws4.*` equivalent |
| Arrow appears on top of icons, obscuring them | Arrow element declared after icon cells in XML | Move arrow `mxCell` entries above icon cells |
| Text overflows container boundary in PNG | Margin calculation ignored strokeWidth | Add `strokeWidth × 2` to 30px base margin |
| Connector endpoint snaps to wrong position | Using `exitX`/`exitY` on a text element | Switch to explicit `mxPoint sourcePoint`/`targetPoint` |
| PNG background is white instead of transparent | `background="#ffffff"` in mxGraphModel | Remove attribute or set `page="0"` |
| Image too small / blurry in reveal.js | `auto-stretch` not disabled | Add `auto-stretch: false` to slide YAML header |
| Font differs between elements | `fontFamily` not set per-cell, only on model | Set `fontFamily=Noto Sans JP` in each cell's style |

## Quality Checklist

- [ ] No `background="#ffffff"` (transparent, `page="0"`)
- [ ] Font size ≥ 18px; `fontFamily` set on model and each text cell
- [ ] All arrows declared before icon/box cells in XML
- [ ] Arrow endpoints 20px+ clear of label bounding boxes
- [ ] Internal elements: 30px + (strokeWidth × 2) margin from container edges
- [ ] AWS icons use `mxgraph.aws4.*` (not aws3)
- [ ] AWS service labels use official full names
- [ ] No redundant decorative icons
- [ ] PNG conversion run and visually inspected
- [ ] reveal.js: `auto-stretch: false` in YAML if used in slides
