---
name: react-dev
version: 1.0.0
description: "Type-safe React component patterns for TypeScript — generic components, discriminated union props, React 19 ref/action patterns, TanStack Router and React Router v7 type safety. Use when writing or reviewing typed React components, hooks, Server Components, or router integration. Triggers: TypeScript React component, React 19, useActionState, forwardRef migration, TanStack Router, Server Action. NOT for MUI-specific or vanilla JS React."
---

# React TypeScript

Type-safe React = compile-time guarantees = confident refactoring.

## Mindset

1. **Props shape behavior, not just data.** Discriminated unions at the prop level eliminate impossible states before runtime — model your variants in the type, not in conditionals.
2. **Inference is a contract.** When TypeScript infers a generic, it locks in the relationship across all usages. Explicit annotations at call sites break that contract and cost you safety downstream.
3. **Server/Client boundary is a compile-time seam.** Treat `'use server'` and `'use client'` like interface boundaries — only serializable data crosses them. Promises passed from Server to Client via `use()` are the intended bridge.
4. **Avoid null coercion on DOM refs.** `inputRef.current!` trades a compile error for a runtime crash. Guard with `?.` or initialize with a default value.
5. **Routing type safety is architectural, not cosmetic.** Choosing TanStack Router vs React Router v7 determines whether search params, path params, and loader data are typed at definition time or inferred from generated artifacts — pick based on project constraints, not familiarity.

## Navigation

**Use this skill when:**
- Building typed React components, hooks, or event handlers
- Implementing generic components (Table, List, Select, Modal)
- Typing event handlers, forms, refs
- Using React 19 features (Actions, Server Components, `use()`, `useActionState`)
- Integrating TanStack Router or React Router v7
- Custom hooks with proper typing

**Do NOT use this skill when:**
- Working in non-React TypeScript (Node scripts, libraries, Zod schemas standalone)
- Vanilla JS React with no TypeScript

Building a shared component library rather than app components? Use design-system-starter for token architecture, atomic hierarchy, and WCAG 2.1 accessibility patterns.

If the user is working with Material UI components specifically, switch to the mui skill for MUI v7 sx caching, slotProps, and Grid v2 patterns.

### Router Decision Tree

```
Does the project use a meta-framework (Next.js, Remix)?
├─ Yes → Next.js: use App Router + Server Actions (no separate router library needed)
│         Remix/React Router v7: already baked in — use Framework Mode loaders/actions
└─ No → Is file-based routing required?
         ├─ Yes → React Router v7 (Framework Mode with Vite plugin)
         └─ No → Does the team need compile-time Zod search-param validation?
                  ├─ Yes → TanStack Router (validateSearch + generated route tree)
                  └─ No → Either works; prefer TanStack Router for greenfield SPA,
                           React Router v7 for teams already familiar with Remix patterns
```

**TanStack Router strengths:** Compile-time route tree, Zod `validateSearch`, full type inference from `useLoaderData`/`useSearch`/`useParams` without code generation at runtime.

**React Router v7 strengths:** Framework Mode generates `+types/` per route — loader return type is automatically inferred by component. Familiar for Remix users. Better SSR story.

MANDATORY — read [references/tanstack-router.md](references/tanstack-router.md) and [references/react-router.md](references/react-router.md) before implementing routing.

## Philosophy

Model the impossible as unrepresentable: every `any`, every optional field that should be required, and every missing discriminant is a bug deferred to production. Type-safe React is not about satisfying the compiler — it is about encoding product rules in a language the compiler enforces.

## NEVER

- **`any` for event handlers** — `any` widens the handler to accept events from unrelated elements, so `e.target.value` won't narrow correctly and you'll get silent `undefined` at runtime instead of a type error at compile time.
- **`JSX.Element` as children type** — `JSX.Element` excludes strings, numbers, arrays, fragments, and `null`, rejecting valid children at compile time while `React.ReactNode` accepts all renderable values correctly.
- **`forwardRef` in React 19+** — `forwardRef` wraps your component in an extra HOC layer and is deprecated; React 19 passes `ref` as a regular prop, so `forwardRef` adds indirection with no benefit and breaks the new ref cleanup return type.
- **`useFormState` (deprecated)** — replaced by `useActionState` which also returns `isPending` as a third value; `useFormState` is removed in React 19 and will throw at runtime.
- **Awaiting promises before passing to `use()`** — `use(await fetchUser())` defeats streaming: it blocks the Server Component until the promise settles, eliminating the concurrent rendering benefit that `use()` + Suspense is designed to provide.
- **Mixing Server and Client component logic in the same file** — a file with both `'use server'` and `'use client'` at module scope is invalid; the bundler treats the entire file as one boundary, so server-only imports (db, fs) will leak into the client bundle.
- **Non-null assertion (`!`) on DOM refs** — `inputRef.current!` crashes if the component unmounts or the ref hasn't attached yet; use optional chaining (`?.`) or guard the call site explicitly.
- **Inline object/function literals in JSX props without `useCallback`/`useMemo`** — every render creates a new reference, triggering child re-renders even when `React.memo` is applied, making memoization silently ineffective.

## When Things Go Wrong

| Symptom | Root Cause | Fix |
|---|---|---|
| `Type 'string' is not assignable to type 'never'` on discriminated union | Switch/if is missing a case arm, so TypeScript narrows to `never` | Add the missing branch or an exhaustive check `default: satisfies never` |
| `Property 'current' does not exist` on ref | Ref typed as `RefObject<T>` but used in a non-null context | Use optional chaining `ref.current?.focus()` or check `if (ref.current)` first |
| Server Action throws "Functions cannot be passed directly to Client Components" | Passing an un-serializable callback as a prop across the Server/Client boundary | Wrap with `'use server'` inline or import from a server module; never pass closures |
| `useLoaderData` returns `unknown` in TanStack Router | Route's `loader` return type is not inferred because `from` is missing or wrong | Pass `{ from: routeId }` explicitly: `useLoaderData({ from: '/users/$userId' })` |
| React Router v7 `+types/` import missing | Vite plugin not configured or route file not under the routes directory | Check `vite.config.ts` for `reactRouter()` plugin and verify file is under `app/routes/` |
| Child component re-renders despite `React.memo` | Prop is an inline object/function literal — new reference on every parent render | Hoist the value outside the component or wrap with `useMemo`/`useCallback` |

## Reference Loading Triggers

MANDATORY — read the indicated reference file before working on each task:

| Task | Reference |
|---|---|
| React 19 features (`ref` as prop, `useActionState`, `use()`, migration) | [references/react-19-changes.md](references/react-19-changes.md) |
| Component props, discriminated unions, children typing, polymorphic components | [references/component-patterns.md](references/component-patterns.md) |
| Server Components, Server Actions, streaming, Server/Client boundary | [references/server-components.md](references/server-components.md) |
| Typing hooks (`useState`, `useRef`, `useReducer`, `useContext`, custom hooks) | [references/hooks-typing.md](references/hooks-typing.md) |
| Generic components (Table, List, Select, Modal, FormField) | [references/generic-components.md](references/generic-components.md) |
| Event handler typing (mouse, form, keyboard, drag, clipboard) | [references/event-handlers.md](references/event-handlers.md) |
| TanStack Router routes, search params, loader data | [references/tanstack-router.md](references/tanstack-router.md) |
| React Router v7 loaders, actions, `+types/` generation | [references/react-router.md](references/react-router.md) |
