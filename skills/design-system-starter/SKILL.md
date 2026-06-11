---
name: design-system-starter
description: Create and evolve design systems — design tokens (W3C/Style Dictionary format), atomic component architecture, theming, dark mode, WCAG 2.1 accessibility, and documentation scaffolding. Trigger phrases: "design system", "design tokens", "component library", "atomic design", "token architecture", "WCAG compliance", "dark mode theming".
license: MIT
metadata:
  version: 2.0.0
  tags: [design-system, ui, components, design-tokens, accessibility, frontend]
---

# Design System Starter

---

## Mindset

1. **Tokens are contracts, not values.** Primitive tokens own the raw hex/rem; semantic tokens reference primitives by alias. Changing a primitive propagates everywhere — but only if consumers use semantic tokens, never primitives directly in components.

2. **The atomic hierarchy is a dependency graph, not a naming convention.** Atoms have zero component dependencies. Molecules depend only on atoms. Breaking this means any atom refactor cascades unpredictably into molecules and organisms. Enforce it structurally, not just by folder name.

3. **Accessibility debt compounds faster than tech debt.** Retrofitting focus traps, ARIA live regions, and color contrast into an established library costs 3-5x building them in. Build accessible primitives first; accessibility is cheaper at atom level than organism level.

4. **Dark mode is a theming problem, not a CSS problem.** If dark mode is solved with `dark:` class overrides scattered across components rather than semantic token swaps, you've made every future theme (high-contrast, branded) require the same scattered changes. Semantic tokens that swap at theme boundary is the only scalable approach.

5. **The system's API surface is harder to change than its internals.** Prop names, slot patterns, and export shapes become load-bearing the moment a second team adopts the library. Treat the component API as a public contract from day one.

---

## Navigation

**Use this skill when**:
- Starting a design token architecture from scratch or auditing an existing one
- Scaffolding component libraries with React/Vue/Svelte + TypeScript
- Implementing multi-theme support (dark mode, branded variants, high-contrast)
- Establishing WCAG 2.1 AA compliance patterns for an existing or new library
- Producing Style Dictionary / W3C DTCG token JSON structures
- Advising on atomic design component decomposition

**Do NOT use this skill when**:
- The user wants a single one-off component (use a generic React/CSS skill instead)
- The project already has a mature design system (Material UI, Chakra, Radix) and just needs customization — advise extending the existing system rather than creating a parallel one
- The task is purely visual design (Figma layout, brand identity) with no implementation component

If the component library is built on Material UI, also load mui for MUI-specific token consumption via sx shorthand and slotProps customization.

**Quick decision tree**:
- Has an existing component library? → Extend via tokens/theming, don't rebuild atoms
- Greenfield project? → Start with token tiers, then atoms, then documentation tooling
- Existing codebase with inconsistent styles? → Audit first (`checklists/design-system-checklist.md`), then extract tokens from existing values

---

## Philosophy

A design system is a living contract between design and engineering — not a component dump. Every decision at the token and API layer is a long-term commitment. Optimize for the maintenance burden of the second year, not the delivery speed of the first sprint.

---

## NEVER

- **NEVER let components consume primitive tokens directly** — because when `blue-600` becomes `brand-600` in a rebrand, every component needs a manual update instead of one token swap. Components must only reference semantic tokens (`color.text.primary`, `color.brand.interactive`).

- **NEVER use `rgba()` hardcodes in component styles** — because they don't participate in the token system, break dark mode, and are invisible to Style Dictionary transforms. All color values must trace back to a token reference.

- **NEVER create circular token references** (`A → B → A`) — Style Dictionary resolves references in topological order; cycles produce silent build failures or `undefined` output values that only surface at runtime. Always audit with `style-dictionary build --verbose` before shipping token changes.

- **NEVER solve dark mode with duplicated class overrides** (e.g., Tailwind `dark:bg-gray-900` on every element) — it couples theme logic to every component, making a third theme (high-contrast, branded) require a full codebase scan. Use semantic token swap at the `:root`/`[data-theme]` boundary instead.

- **NEVER ship components with CSS-in-JS runtime cost in a performance-critical library** — libraries like `emotion`/`styled-components` with dynamic interpolations re-compute styles per render. For shared libraries, prefer CSS variables (zero runtime) or build-time CSS Modules. Runtime CSS-in-JS is acceptable in application code, not in a design system consumed by many teams.

- **NEVER namespace tokens with the framework name** (e.g., `react-button-primary`) — tokens must be framework-agnostic because the same token set may be consumed by React, native mobile, and email templates simultaneously. Token names describe *intent*, not implementation.

- **NEVER skip the `composite` token tier for complex multi-property values** — shadows, typography styles, and border shorthand are composite tokens. Treating them as loose scalar groups makes it impossible for Style Dictionary to output platform-correct formats (Android uses separate shadow properties; iOS uses NSShadow).

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Style Dictionary build produces `undefined` values | Circular token reference or misspelled alias path | Run `style-dictionary build --verbose`; check reference chain with `{token.path.here}` syntax audit |
| Dark mode flashes white on load (FOUC) | Theme class applied after hydration (SSR/SSG mismatch) | Set theme attribute server-side; use `<script>` before `<body>` to read `localStorage` and set `data-theme` synchronously |
| Semantic tokens not resolving in consuming app | Consumer imports primitive token file directly, not the semantic layer | Enforce barrel exports that only expose semantic tokens; add lint rule `no-restricted-imports` for primitive token paths |
| Component a11y audit fails WCAG AA | Color chosen from primitive scale without contrast check | Run contrast ratio check between semantic `text` and `background` pairs at every theme boundary; automate with `jest-axe` in CI |
| Token JSON grows unwieldy (500+ tokens) | Skipped the tier separation (primitives / semantics / component-level) | Refactor into three files: `tokens/primitive.json`, `tokens/semantic.json`, `tokens/component.json`; Style Dictionary supports multi-source |
| Two teams define conflicting component APIs | No API review process before merge | Establish a Design System RFC template; any new prop or slot addition requires a signed-off proposal before implementation |

---

## Token Architecture

Three tiers — always three, never collapse them:

1. **Primitive** — raw values, no aliases (`color.blue.600 = #2563eb`)
2. **Semantic** — intent aliases referencing primitives (`color.brand.interactive = {color.blue.600}`)
3. **Component** — component-scoped overrides referencing semantic (`component.button.background = {color.brand.interactive}`)

Style Dictionary config pattern:
```js
// style-dictionary.config.js
module.exports = {
  source: ['tokens/primitive.json', 'tokens/semantic.json', 'tokens/component.json'],
  platforms: {
    css: { transformGroup: 'css', buildPath: 'dist/', files: [{ destination: 'tokens.css', format: 'css/variables' }] },
    js:  { transformGroup: 'js',  buildPath: 'dist/', files: [{ destination: 'tokens.js',  format: 'javascript/es6' }] }
  }
};
```

Full token JSON templates: `templates/design-tokens-template.json`

---

## Component API Checklist

Before shipping any new component:

- [ ] Props use consistent naming (`variant`, `size`, `isDisabled` — not mixed conventions)
- [ ] All interactive states covered: default, hover, focus-visible, active, disabled, loading
- [ ] Polymorphic render supported via `as` prop or `asChild` (Radix pattern) where applicable
- [ ] Compound component pattern used for complex compositions (`Card.Header`, `Card.Body`)
- [ ] Every interactive element reachable by keyboard; focus ring visible at 3:1+ contrast
- [ ] ARIA attributes documented; screen reader behavior tested with VoiceOver + NVDA
- [ ] No inline `rgba()` or hardcoded hex — all colors via CSS variables/tokens

Full component template: `templates/component-template.tsx`
Full accessibility and composition examples: `references/component-examples.md`
Full audit checklist: `checklists/design-system-checklist.md`

---

## Theming Pattern (Dark Mode Done Right)

```css
/* tokens.css — generated by Style Dictionary */
:root {
  --color-bg-primary: #ffffff;
  --color-text-primary: #111827;
  --color-brand-interactive: #2563eb;
}

[data-theme="dark"] {
  --color-bg-primary: #111827;
  --color-text-primary: #f9fafb;
  --color-brand-interactive: #60a5fa;
}
```

Components reference only `var(--color-*)` — never a raw hex. Theme switches by toggling `data-theme` on `<html>`. No component file changes required for any theme addition.

---

## Workflow Sequence

1. **Audit** — run `checklists/design-system-checklist.md` against existing codebase
2. **Token extraction** — identify all unique values in use; map to primitive → semantic tiers
3. **Atom build** — Button, Input, Label, Icon, Badge with full state coverage and a11y
4. **Style Dictionary integration** — multi-platform output (CSS vars, JS ES6, optionally iOS/Android)
5. **Documentation** — Storybook stories per component; accessibility section mandatory
6. **API freeze + RFC process** — lock prop contracts before second team adoption
7. **Versioning** — semver; breaking prop changes = major; new variants = minor

---

## Bundled Resources

| File | Purpose |
|------|---------|
| `templates/design-tokens-template.json` | W3C DTCG-format token file with all tiers |
| `templates/component-template.tsx` | TypeScript React component scaffold |
| `references/component-examples.md` | Button, FormField, Card, Modal, polymorphic patterns |
| `checklists/design-system-checklist.md` | Pre-launch audit checklist |
