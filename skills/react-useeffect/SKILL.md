---
name: react-useeffect
description: Expert guidance on React useEffect — when to use it, when NOT to use it, and what to use instead. Triggers on: useEffect review, derived state, data fetching, race conditions, stale closure, cleanup, re-render loops, Strict Mode double-mount, synchronizing with external systems.
---

## Mindset

React's render cycle IS the reactive system. useEffect is an **opt-out**, not a feature. Every Effect you write is a gap where React can't optimize, lint, or trace for you.

**Heuristic 1 — The External System Test**: If you can describe the thing being synchronized without naming a non-React API (DOM, WebSocket, `localStorage`, third-party lib, `setInterval`), you don't have an external system. You have a data transformation problem. Solve it in render, not in an Effect.

**Heuristic 2 — The Timing Tells You**: If you care that code ran *because a user clicked*, use an event handler. If you care that code ran *because a component is visible on screen*, use an Effect. These are semantically different — Effects fire after paint, event handlers fire synchronously in the event loop.

**Heuristic 3 — The Double-Run Smell Test**: If running your Effect twice (React 18 Strict Mode) causes a visible bug, you have missing cleanup — not a Strict Mode problem. Fix the cleanup.

**Heuristic 4 — Object/function dependency trap**: If your dependency array contains an object or function created inline in render, your Effect runs every render even with a "stable" dep array. React compares by reference. Extract the value out, memoize the function, or restructure so a primitive is the dependency.

**Heuristic 5 — useEffect for data fetching is a last resort**: An Effect-based fetch has no loading deduplication, no cache, no server rendering, and introduces race conditions. Reach for React Query / SWR / server components before writing `useEffect(() => { fetch(...) })`.

---

## Navigation

**Use this skill when**:
- Reviewing or writing useEffect code
- A component has bugs like: stale values, double API calls, state update loops, notification fires on page load
- Deriving state from props/state with useState + useEffect
- Implementing subscriptions, timers, or DOM listeners
- Race conditions in async Effects

**Do NOT use this skill when**:
- The question is purely about state management (Redux, Zustand, Context) without an Effect
- The question is about React Server Components (they don't support Effects)
- The question is about React Query / SWR internals (those libraries handle Effect lifecycle internally)

**Quick routing decision**:
```
Does the code touch anything outside React's component tree?
  NO  → You don't need useEffect. Use render-time derivation, event handlers, or key prop.
  YES → Which external system?
         DOM / browser API     → useEffect with cleanup
         External store/event  → useSyncExternalStore (preferred) or useEffect
         Network fetch         → Framework/library preferred; useEffect with ignore flag if needed
         One-time app init     → Module-level guard (not Effect)
```

---

## Philosophy

useEffect exists to bridge React's declarative model and the imperative world outside it. The goal is to make that bridge as narrow as possible — every line inside a useEffect is code React cannot reason about. Shrink the bridge; expand render.

---

## NEVER

- **NEVER store derived values in state and sync them with useEffect** — because this creates a guaranteed stale render: the component renders once with the old derived value, then the Effect fires, setState triggers a second render. Use render-time computation or useMemo. The stale render is invisible in small apps but causes flickering and logic bugs in complex ones.

- **NEVER fire Effects in response to user events by watching state they set** — because Effects don't know *why* state changed. An Effect watching `isInCart` will fire on page load (when isInCart is already true from saved state), on prop change, and on any render that causes remounting — not just the user's click. The event handler knows exactly why and when.

- **NEVER chain Effects** (Effect A sets state → Effect B watches that state → Effect B sets more state) — because this creates N re-renders for N-effect chains, makes the data flow impossible to follow in React DevTools, and breaks features like time-travel debugging and state replay. Collapse the chain into a single event handler that computes the final state.

- **NEVER use useEffect to initialize one-time app-level logic** — because React 18 Strict Mode intentionally mounts twice in development, and your auth token check / localStorage init will run twice. Use a module-level `let didInit = false` guard or run the code at module scope with `if (typeof window !== 'undefined')`. The Effect lifecycle is component lifecycle, not application lifecycle.

- **NEVER include object/array/function literals in the dependency array without stabilizing them first** — because `{}` !== `{}` in JavaScript. An inline object in the dep array makes the Effect re-run every render, silently, with no lint warning. Wrap objects in useMemo, functions in useCallback, or restructure so only primitives are dependencies.

- **NEVER omit the AbortController or `ignore` flag pattern in async Effects** — because without it, a fast-typing user will see results from a slower earlier request overwrite results from a faster later one (classic race condition). The `ignore` flag is the minimum fix; AbortController also cancels the in-flight request.

- **NEVER call `setState` on unmounted components without cleanup** — because React 18 silenced the warning but the underlying logic error remains: the Effect has a reference to a component that's gone. The cleanup return function is mandatory for subscriptions, timers, and async operations.

---

## When Things Go Wrong

| Symptom | Likely Cause | Recovery |
|---------|-------------|----------|
| Component renders 2-3x on every update | Derived state in useState + useEffect sync | Replace useState+useEffect pair with render-time const or useMemo |
| API called twice on mount in dev | React 18 Strict Mode double-mount (by design) | Add cleanup: `return () => { ignore = true; }` — if it breaks with cleanup, the Effect has a bug |
| Notification / toast shows on page load unexpectedly | Effect watching state that's truthy on init | Move side-effect into the event handler that mutates the state |
| Effect re-runs every render despite "stable" deps | Object, array, or function in dep array created inline | Extract to useMemo/useCallback or decompose to primitive deps |
| Fetch shows stale results when input changes fast | Missing ignore flag / AbortController | Add `let ignore = false; return () => { ignore = true; }` inside Effect |
| Effect runs, but cleanup runs immediately after | StrictMode remount OR dependency object identity changes | Verify cleanup is correct (StrictMode) or stabilize deps (identity issue) |
| `setState` loop — component renders infinitely | Effect sets state that's in its own dep array | Remove the circular dep or restructure: derive instead of sync |

---

## Reference Files — Load on Demand

- **[anti-patterns.md](./references/anti-patterns.md)** — 9 coded examples with bad/good/why. Load when reviewing specific useEffect code or explaining a concrete mistake.
- **[alternatives.md](./references/alternatives.md)** — 8 replacement patterns (useMemo, key prop, useSyncExternalStore, custom fetch hook, etc.). Load when the answer is "don't use Effect — use X instead."
