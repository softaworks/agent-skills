# Server Components

Load this file when working with React Server Components, Server Actions, async data fetching, or the Server/Client boundary.

## Async data fetching in Server Components

Server Components can be `async` — fetch data directly without `useEffect`.

```typescript
export default async function UserPage({ params }: { params: { id: string } }) {
  const user = await fetchUser(params.id);
  return <div>{user.name}</div>;
}
```

## Parallel data fetching

Do NOT await sequentially — fetch in parallel with `Promise.all`:

```typescript
export default async function DashboardPage() {
  const [user, posts, comments] = await Promise.all([
    fetchUser('123'),
    fetchPosts('123'),
    fetchComments('123'),
  ]);
  return <Dashboard user={user} posts={posts} comments={comments} />;
}
```

## Server Actions — 'use server' for mutations

```typescript
'use server';

import { revalidatePath } from 'next/cache';

export async function updateUser(userId: string, formData: FormData) {
  const name = formData.get('name') as string;
  await db.user.update({ where: { id: userId }, data: { name } });
  revalidatePath(`/users/${userId}`);
}
```

## Client component consuming a Server Action

```typescript
'use client';

import { useActionState } from 'react';
import { updateUser } from '@/actions/user';

type State = { errors?: string[]; success?: boolean };

function UserForm({ userId }: { userId: string }) {
  const [state, formAction, isPending] = useActionState(
    (prev: State, formData: FormData) => updateUser(userId, formData),
    {}
  );
  return (
    <form action={formAction}>
      <input name="name" />
      <button type="submit" disabled={isPending}>Save</button>
      {state.errors?.map(e => <p key={e}>{e}</p>)}
    </form>
  );
}
```

## use() for promise handoff (streaming)

Pass the promise from Server to Client WITHOUT awaiting — this enables streaming via Suspense.

```typescript
// Server Component — do NOT await
async function Page() {
  const userPromise = fetchUser('123'); // no await
  return (
    <Suspense fallback={<Skeleton />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}

// Client Component — unwrap with use()
'use client';
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // suspends until resolved
  return <div>{user.name}</div>;
}
```

## Streaming with error boundaries

```typescript
export default function Page() {
  return (
    <ErrorBoundary fallback={<ErrorView />}>
      <Suspense fallback={<Skeleton />}>
        <SlowComponent />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Server/Client boundary rules

- A file with both `'use server'` and `'use client'` at module scope is invalid — bundler treats the entire file as one boundary.
- Server-only imports (`db`, `fs`, secret env vars) must never appear in Client Components.
- Only serializable data crosses the boundary: strings, numbers, plain objects, arrays, Dates. No functions, no class instances, no Symbols.
- To pass a server function to a client, use `'use server'` inline or import from a `*.server.ts` module.

## Patterns to avoid

```typescript
// BAD — awaiting before use() defeats streaming
async function Page() {
  const user = await fetchUser('123'); // blocks entire page
  return <UserProfile user={user} />;
}

// BAD — server-only import in client file
'use client';
import { db } from '@/lib/db'; // leaks db credentials to client bundle

// BAD — passing closure across boundary
<ClientComponent onAction={() => db.insert()} />
```
