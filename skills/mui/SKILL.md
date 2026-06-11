---
name: mui
description: Material-UI v7 component library — sx prop styling, theme tokens, slots/slotProps pattern, Grid v2 size prop, Tailwind CSS layer integration, styled() vs sx vs GlobalStyles decisions. Use when working with MUI components, theming, responsive breakpoints, or migrating from MUI v5/v6.
---

# MUI v7 Patterns

## Mindset

- **sx is a performance cost, not free CSS**: every sx object is processed by the emotion cache on render. Static objects hoisted outside the component avoid re-creation. If a component re-renders >10×/sec with a complex sx, reach for `styled()` instead.
- **Theme tokens are contracts, not strings**: `'primary.main'` is resolved at render time against the active theme. Hardcoded hex breaks dark mode and white-labeling silently — the build won't catch it.
- **slots/slotProps is the v7 customization surface**: `componentsProps` and `components` overrides from v5/v6 still exist as aliases but are deprecated. New MUI components only accept `slots`/`slotProps`. Mixing both on the same component produces unexpected behavior.
- **Grid v2 is not backward-compatible**: the `item` prop is gone, `xs`/`sm`/`md` top-level props are gone. Only `size={{ xs: 12, md: 6 }}` works. A silent fallback renders all columns full-width if you use old props.
- **CSS layers (`enableCssLayer`) changes specificity globally**: enabling it means all MUI styles sit inside `@layer mui`, which loses to any unlayered CSS. Tailwind v4 uses layers by default — this is desirable for coexistence, but enabling it mid-project will break existing style overrides.

## Navigation

**Use this skill when**: writing or reviewing MUI component code, choosing between sx/styled()/GlobalStyles, customizing MUI theme, using Grid/Stack/Box layout, debugging specificity issues with MUI + Tailwind, migrating v5→v7 APIs.

**Do NOT use this skill when**: the project uses a different component library (Chakra, Ant Design, Radix); pure CSS/Tailwind-only styling with no MUI components present; creating charts (use recharts/Victory directly).

**Styling approach decision tree**:
```
Is the style applied globally (body, scrollbar, :root)?
  YES → GlobalStyles (not sx, not styled())
  NO → Is the component a native HTML element with no MUI props?
         YES → styled('div')(...) for static, sx for one-off
         NO → Does the style change every render (based on JS state)?
                YES → sx callback: sx={(theme) => ({ color: active ? theme.palette.primary.main : 'inherit' })}
                NO → Is it applied in >2 places?
                       YES → styled(Component)(...) or extract to *.styles.ts as SxProps const
                       NO → inline sx object hoisted outside component
```

## Philosophy

MUI's constraint-based API (spacing scale, palette tokens, breakpoint objects) exists to make design system changes propagate automatically. Every time you escape the constraint system (hardcoded px, hardcoded hex, inline `style={}`) you create a future migration debt. Work inside the system; only escape it deliberately.

## NEVER

- **NEVER use `style={}` on MUI components for anything other than CSS custom properties** — it bypasses the theme, breaks dark mode support, and is not overridable via `sx` (inline style wins specificity). The one valid use: setting `--css-var` values.
- **NEVER write `theme.palette.primary.main` inside `sx` string values** — use the shorthand `'primary.main'` token. Calling `useTheme()` just to pass values into sx is redundant; the sx callback `(theme) => ({...})` already receives the theme.
- **NEVER use `componentsProps`/`components` on v7 MUI components** — these are deprecated aliases that will be removed. Use `slots` and `slotProps`. Mixing them on one component causes the deprecated props to be silently ignored in some code paths.
- **NEVER put a new `{}` literal directly inside `sx` on a component that renders in a list or high-frequency loop** — `sx={{ p: 2 }}` creates a new object reference every render, defeating emotion's cache. Hoist to a `const styles` outside the component or module.
- **NEVER use Grid `xs`/`sm`/`md` as direct props on Grid items in v7** — they are silently ignored (no warning in production builds). Always use `size={{ xs: 12, md: 6 }}`.
- **NEVER override MUI component internals with global CSS class selectors** (`.MuiButton-root`) in production code — internal class names are considered unstable and can change across patch releases. Use `slotProps`, `sx`, or `styled()` with the component's `ownerState`.
- **NEVER call `useTheme()` solely to read a breakpoint value for conditional rendering** — use `useMediaQuery(theme.breakpoints.up('md'))` or the `sx` responsive object syntax instead. `useTheme()` in render paths increases bundle coupling.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Grid items all render full-width | Using old `xs`/`sm` props instead of `size={{ xs: 12 }}` | Replace top-level breakpoint props with `size` object |
| sx styles silently ignored | `componentsProps` and `slotProps` both set; old prop wins in some components | Remove `componentsProps`, use only `slotProps` |
| MUI styles lose to Tailwind | `enableCssLayer` active; unlayered Tailwind wins vs `@layer mui` | Ensure Tailwind config uses `@layer` or add `@layer utilities` wrapper |
| Dark mode: color not switching | Hardcoded hex in sx instead of theme token | Replace with `'primary.main'` or `(theme) => theme.palette.primary.main` |
| onBackdropClick has no effect | Removed in v7 Modal; handler silently dropped | Move logic to `onClose` with reason check: `onClose={(_, reason) => reason !== 'backdropClick' && close()}` |
| TypeScript: SxProps type error on array sx | Passing `[styles.a, styles.b]` — correct but needs `SxProps<Theme>[]` | Type the array explicitly or spread: `sx={{ ...styles.a, ...styles.b }}` |

## v7 Migration Quick Reference

```typescript
// v5/v6 → v7 breaking changes
onBackdropClick={fn}           // REMOVED → use onClose with reason
<Grid item xs={6}>             // REMOVED → <Grid size={6}>
import X from '@mui/material/X' // REMOVED → import { X } from '@mui/material'
componentsProps={{ root: {} }}  // DEPRECATED → slotProps={{ root: {} }}
```

## Styling Recipes

**Static styles (preferred — hoisted, typed):**
```typescript
import type { SxProps, Theme } from '@mui/material';
const styles = {
  card: { p: 2, borderRadius: 2, bgcolor: 'background.paper' } satisfies SxProps<Theme>,
};
```

**Theme-dependent dynamic styles:**
```typescript
sx={(theme) => ({
  border: `1px solid ${theme.palette.divider}`,
  [theme.breakpoints.up('md')]: { flexDirection: 'row' },
})}
```

**GlobalStyles (reset/global only):**
```typescript
import { GlobalStyles } from '@mui/material';
<GlobalStyles styles={{ '*': { boxSizing: 'border-box' }, body: { margin: 0 } }} />
```

**styled() — reusable semantic component:**
```typescript
const StatusChip = styled(Chip, {
  shouldForwardProp: (prop) => prop !== 'isActive',
})<{ isActive: boolean }>(({ theme, isActive }) => ({
  backgroundColor: isActive ? theme.palette.success.light : theme.palette.grey[300],
}));
```

## Snackbar Pattern

MUI has no built-in `useSnackbar` hook. Use notistack (`enqueueSnackbar`) or a local state pattern. See [resources/styling-guide.md](resources/styling-guide.md) for the full implementation.

## References

- [resources/styling-guide.md](resources/styling-guide.md) — sx vs styled() deep dive, emotion caching, GlobalStyles
- [resources/component-library.md](resources/component-library.md) — Card, Dialog, Form, Loading patterns with full code
- [resources/theme-customization.md](resources/theme-customization.md) — createTheme, palette, typography, component overrides
