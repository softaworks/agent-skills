# React 19 Breaking Changes

React 19 introduces breaking changes that require migration. Load this file when working with React 19 features, `ref` as prop, `useActionState`, or `use()`.

## ref as prop — forwardRef deprecated

```typescript
// React 19 - ref as regular prop (forwardRef removed)
type ButtonProps = {
  ref?: React.Ref<HTMLButtonElement>;
} & React.ComponentPropsWithoutRef<'button'>;

function Button({ ref, children, ...props }: ButtonProps) {
  return <button ref={ref} {...props}>{children}</button>;
}
```

## useActionState — replaces useFormState

`useFormState` is removed in React 19 and throws at runtime. `useActionState` also returns `isPending` as a third value.

```typescript
import { useActionState } from 'react';

type FormState = { errors?: string[]; success?: boolean };

function Form() {
  const [state, formAction, isPending] = useActionState(submitAction, {});
  return (
    <form action={formAction}>
      {isPending && <span>Submitting...</span>}
      {state.errors?.map(e => <p key={e}>{e}</p>)}
    </form>
  );
}
```

## use() — unwraps promises and context

Do NOT `await` the promise before passing to `use()` — that defeats streaming.

```typescript
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspends until resolved
  return <div>{user.name}</div>;
}
```

Context via `use()`:

```typescript
function Component() {
  const theme = use(ThemeContext); // can be called conditionally
  return <div className={theme}>...</div>;
}
```

## useOptimistic — optimistic UI updates

```typescript
function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimistic] = useOptimistic(
    todos,
    (state, newTodo: Todo) => [...state, newTodo]
  );

  async function handleAdd(formData: FormData) {
    const title = formData.get('title') as string;
    addOptimistic({ id: 'temp', title, done: false });
    await addTodo(title); // server action
  }

  return (
    <form action={handleAdd}>
      {optimisticTodos.map(todo => <li key={todo.id}>{todo.title}</li>)}
    </form>
  );
}
```

## useTransition — non-blocking state updates

```typescript
function SearchPage() {
  const [isPending, startTransition] = useTransition();
  const [query, setQuery] = useState('');

  function handleSearch(value: string) {
    startTransition(() => setQuery(value));
  }

  return (
    <>
      <input onChange={e => handleSearch(e.target.value)} />
      {isPending && <Spinner />}
      <Results query={query} />
    </>
  );
}
```

## Migration Checklist

- [ ] Replace all `forwardRef` wrappers — pass `ref` as a regular prop
- [ ] Replace `useFormState` with `useActionState` (update import)
- [ ] Remove `ReactDOM.render` — use `createRoot`
- [ ] Replace `defaultProps` on function components with default parameter values
- [ ] Audit `use(promise)` call sites — ensure promise is NOT awaited before passing
- [ ] Replace `ReactDOM.hydrate` with `hydrateRoot`
- [ ] Update `act` import from `react` not `react-dom/test-utils`
