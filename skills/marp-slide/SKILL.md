---
name: marp-slide
description: Create professional Marp presentation slides with 7 built-in themes (default, minimal, colorful, dark, gradient, tech, business). Use when users request slides, presentations, Marp documents, or say "make it look good", "かっこよく", "良い感じに". Supports custom themes, image layouts, and vague aesthetic improvement requests.
---

# Marp Slide Creator

## Mindset

1. **Marp is a renderer, not an editor** — every directive, class name, and image keyword you write is parsed by a CSS engine. Typos render silently wrong, not with errors. Validate by mental-rendering each slide before outputting.
2. **One slide = one claim** — if you need more than 5 bullets to cover a slide's topic, it's two slides. Density kills presentation slides; practitioners split aggressively.
3. **CSS in templates is load-bearing** — the embedded `<style>` block in each template is what makes the theme work. Stripping or moving it breaks every slide. Copy the whole template block, then replace content only.
4. **`bg` images live on a separate layer** — `![bg right:40%](img.png)` is not an inline image; it's a CSS background panel. Placing it after bullets instead of before them doesn't change the layout — position in the markdown file is irrelevant for `bg` images; only the keyword matters.
5. **Frontmatter drives the output format** — `size: 16:9` vs `4:3` changes every margin calculation downstream. Choose before writing content, not after.

## Navigation

**Use this skill when**: user asks to create slides, a presentation, or a Marp `.md` file; user says "make it look good", "かっこよく", "良い感じに"; user provides raw content and wants it formatted as slides.

**Do NOT use this skill when**: user wants a static document or report (use standard markdown); user explicitly wants PowerPoint `.pptx` without Marp pipeline; user wants interactive web animations.

**Quick theme decision**:
- Technical / code / developer → `tech` or `dark`
- Business / corporate / proposal → `business`
- Academic / content-first → `minimal`
- Creative / event / youth → `colorful` or `gradient`
- General / unsure → `default`

## Philosophy

Every slide is a contract with the audience: one idea, clearly stated, visually uncluttered. The theme provides the visual contract; your job is to enforce the content contract — no slide should require the speaker to explain what the slide is about before explaining what it means.

## NEVER

- NEVER use `---` as a slide separator *inside* a fenced code block — because Marp's parser is line-level and will split the slide mid-code-block, destroying the fence and producing broken HTML output.
- NEVER embed raw `<style>` overrides that redefine `section` padding below `40px` — because Marp's built-in themes size all content assuming the default section padding; reducing it causes text to collide with page-number badges and header/footer elements at export time.
- NEVER use standard Markdown image syntax `![](img.png)` when you mean a background split — because without the `bg` keyword the image renders inline as a content-layer element, not as the CSS background panel, producing a broken layout that looks correct in VS Code preview but wrong in PDF/PPTX export.
- NEVER put `<!-- _class: lead -->` on non-title slides to center content — because `lead` is a semantic class that also suppresses the slide's h2 border/decoration in most themes; using it on content slides silently removes structural styling mid-deck.
- NEVER use `paginate: true` at the global level without also suppressing it on the title slide with `<!-- _paginate: false -->` — because page "1" printed on the title slide confuses audiences and is a practitioner tell that the author didn't check the output.
- NEVER mix `*` (asterisk) unordered list bullets and `-` (dash) bullets on the same slide — because `*` activates Marp's **fragmented list** feature (progressive reveal in HTML mode), while `-` does not; mixing them produces one list that partially animates and one that doesn't, with no visual warning.
- NEVER use `backgroundImage: url(...)` in frontmatter when your theme template already sets a background via CSS — because the frontmatter directive takes precedence over theme CSS, wiping the theme's gradient/texture and making the slide look unstyled even though it parsed correctly.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Slide splits mid-code-block | `---` separator inside fenced block | Move `---` outside the fence; use `<!-- -->` comment as visual break inside the block instead |
| Background image covers all text | Missing `left`/`right` keyword on `![bg]` | Add `![bg right:40%]` to reserve text space; without directional keyword, `bg` is full-bleed |
| Theme styling gone after edit | `<style>` block accidentally deleted | Re-copy the style block from the template in `assets/template-{theme}.md` |
| Page numbers on title slide | `paginate: true` global, no per-slide override | Add `<!-- _paginate: false -->` immediately after the title slide's opening `---` |
| Bullets animate unexpectedly in HTML | Mixed `*` and `-` list markers | Standardize all lists to `-`; reserve `*` only when progressive reveal is intentional |
| Math formula renders as raw text | `marp: true` missing from frontmatter | Ensure frontmatter is present and `marp: true` is set; math requires Marp Core to activate KaTeX |

## Workflow

**1. Select theme** using the decision tree in Navigation above. If the user gave vague aesthetic instructions, infer from content domain.

**2. Copy the full template** from `assets/template-{theme}.md` — do not reconstruct from scratch. The embedded CSS is non-trivial.

**3. Set frontmatter**:
```markdown
---
marp: true
theme: default   # or the chosen theme name
size: 16:9
paginate: true
---
```

**4. Title slide** (always first):
```markdown
<!-- _class: lead -->
<!-- _paginate: false -->

# Presentation Title

Presenter · Date
```

**5. Content slides** — enforce 1 message per slide, 3–5 bullets, concise h2 titles:
```markdown
---

## Short Title

- Point one (parallel structure)
- Point two
- Point three
```

**6. Image slides** — read `references/image-patterns.md` before using any `bg` syntax:
```markdown
---

## Feature Overview

![bg right:40%](diagram.png)

- Explanation 1
- Explanation 2
```

**7. Save** to `/mnt/user-data/outputs/` with `.md` extension.

## Reference Loading Triggers

Load these files only when needed — they are large:

| Trigger | File to read |
|---------|-------------|
| Custom theme request, CSS questions | `references/theme-css-guide.md` |
| Any `bg`, filter, or split-screen image | `references/image-patterns.md` |
| Math formulas, emoji, fragmented lists | `references/advanced-features.md` |
| Official theme names (`gaia`, `uncover`) | `references/official-themes.md` |
| Theme selection uncertainty | `references/theme-selection.md` |
| Quality review / "make it better" | `references/best-practices.md` |

## Quality Gate

Before delivering, verify:
- [ ] `marp: true` in frontmatter
- [ ] Title slide has `<!-- _class: lead -->` and `<!-- _paginate: false -->`
- [ ] No `---` separators inside code fences
- [ ] All `bg` images use directional keyword if text coexists on slide
- [ ] List markers consistent (`-` only unless progressive reveal intended)
- [ ] CSS `<style>` block intact from template
- [ ] File saved to `/mnt/user-data/outputs/`
