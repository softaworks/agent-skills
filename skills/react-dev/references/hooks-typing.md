# Hooks Typing

Load this file when typing React hooks: `useState`, `useRef`, `useReducer`, `useContext`, or custom hooks.

## useState — explicit for unions and null

```typescript
const [user, setUser] = useState<User | null>(null);
const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');
const [count, setCount] = useState(0); // inferred as number — no annotation needed
```

## useRef — null for DOM, initial value for mutable

```typescript
// DOM ref — initialize with null, always use ?. when accessing
const inputRef = useRef<HTMLInputElement>(null);
inputRef.current?.focus();

// Mutable value ref — direct access is safe
const countRef = useRef<number>(0);
countRef.current += 1;

// Interval / timeout ref
const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
```

Never use `!` on DOM refs — use `?.` or guard with `if (ref.current)`.

## useReducer — discriminated union actions

```typescript
type State = { count: number; status: 'idle' | 'loading' };

type Action =
  | { type: 'increment' }
  | { type: 'reset' }
  | { type: 'set'; payload: number }
  | { type: 'setStatus'; payload: State['status'] };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + 1 };
    case 'reset':     return { ...state, count: 0 };
    case 'set':       return { ...state, count: action.payload };
    case 'setStatus': return { ...state, status: action.payload };
    default:          return action satisfies never; // exhaustive check
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0, status: 'idle' });
  return <button onClick={() => dispatch({ type: 'increment' })}>{state.count}</button>;
}
```

## Custom hooks — tuple returns with as const

Without `as const`, TypeScript widens the tuple to `(boolean | (() => void))[]`, losing positional types.

```typescript
function useToggle(initial = false): readonly [boolean, () => void] {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue(v => !v), []);
  return [value, toggle] as const;
}

// Usage — types are [boolean, () => void]
const [isOpen, toggleOpen] = useToggle();
```

## useContext — null guard pattern

```typescript
const UserContext = createContext<User | null>(null);

function useUser(): User {
  const user = useContext(UserContext);
  if (!user) throw new Error('useUser must be used inside UserProvider');
  return user;
}

function UserProvider({ children }: { children: React.ReactNode }) {
  const [user] = useState<User | null>(null);
  return <UserContext.Provider value={user}>{children}</UserContext.Provider>;
}
```

## useCallback — stable references for memoized children

```typescript
function Parent({ userId }: { userId: string }) {
  const handleDelete = useCallback(async () => {
    await deleteUser(userId);
  }, [userId]); // recreates only when userId changes

  return <ChildButton onDelete={handleDelete} />;
}
```

## useMemo — expensive computations

```typescript
function FilteredList({ items, filter }: { items: Item[]; filter: string }) {
  const filtered = useMemo(
    () => items.filter(item => item.name.includes(filter)),
    [items, filter]
  );
  return <ul>{filtered.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}
```

## useImperativeHandle — expose minimal imperative API

```typescript
type InputHandle = { focus: () => void; clear: () => void };

function FancyInput({ ref }: { ref?: React.Ref<InputHandle> }) {
  const innerRef = useRef<HTMLInputElement>(null);

  useImperativeHandle(ref, () => ({
    focus: () => innerRef.current?.focus(),
    clear: () => { if (innerRef.current) innerRef.current.value = ''; },
  }));

  return <input ref={innerRef} />;
}
```

## useSyncExternalStore — subscribing to external stores

```typescript
function useWindowWidth() {
  return useSyncExternalStore(
    (callback) => {
      window.addEventListener('resize', callback);
      return () => window.removeEventListener('resize', callback);
    },
    () => window.innerWidth,
    () => 1024 // server snapshot
  );
}
```

See also [hooks.md](hooks.md) for additional patterns already in references/.
