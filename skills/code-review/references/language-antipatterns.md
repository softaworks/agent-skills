# Language-Specific Anti-Patterns

Patterns that pass visual inspection and linting but introduce correctness failures or performance problems.

---

## JavaScript / TypeScript

### Promise.all vs. Sequential Await

**Pattern reviewers miss:**
```ts
// Looks clean. Runs sequentially. Latency = A + B + C.
const user = await fetchUser(id);
const perms = await fetchPermissions(id);
const prefs = await fetchPreferences(id);

// Correct for independent fetches. Latency = max(A, B, C).
const [user, perms, prefs] = await Promise.all([
  fetchUser(id),
  fetchPermissions(id),
  fetchPreferences(id),
]);
```

**Why missed**: Sequential await reads like clean, linear logic. The performance cost is invisible in a diff unless you know both functions are async and independent. In hot paths (API handlers, server-side rendering), this is the single most common 3x latency regression hiding behind readable code.

**Review trigger**: any block with 2+ awaits on independent data — check whether they can be parallelized.

---

### Type Assertion Hiding Runtime Errors

**Pattern reviewers miss:**
```ts
// Compiles clean. Runtime crash if API changes response shape.
const data = response.json() as ApiResponse;
console.log(data.user.id); // TypeError if data.user is undefined

// Correct: validate at the boundary.
const raw = await response.json();
const data = ApiResponseSchema.parse(raw); // Zod/Valibot/io-ts
```

**Why missed**: `as SomeType` reads as a type annotation, not a lie. TypeScript types are erased at runtime — the assertion tells the compiler to trust you, not to enforce anything. Every `as` on untrusted external data (API responses, localStorage, URL params, form inputs) is a potential runtime crash disguised as type safety.

**Review trigger**: any `as` cast applied to `JSON.parse()`, `response.json()`, `localStorage.getItem()`, or URL/form data.

---

### Non-Null Assertion on Values That Can Be Null

**Pattern reviewers miss:**
```ts
const el = document.getElementById('root')!;
el.appendChild(child); // crash if 'root' doesn't exist in test env or SSR

// Correct: explicit guard
const el = document.getElementById('root');
if (!el) throw new Error("Missing #root element");
el.appendChild(child);
```

**Why missed**: `!` is visually subtle. Reviewers read past it because it looks like punctuation. In test environments or SSR contexts, the element won't exist and the crash will only appear outside the happy path.

---

### Mutating State in Array Methods

**Pattern reviewers miss:**
```ts
// Looks like a transform. Mutates original.
const updated = items.map(item => {
  item.processed = true; // mutation
  return item;
});

// Correct: return new object
const updated = items.map(item => ({ ...item, processed: true }));
```

**Why missed**: `.map()` signals "transform without mutation" by convention. A reviewer skimming the shape of the code assumes immutability. The mutation causes hard-to-trace bugs in React state, Redux stores, and any caller that holds a reference to the original array.

---

## Python

### Mutable Default Arguments

**Pattern reviewers miss:**
```python
# The default list is created ONCE at function definition time.
def add_item(item, collection=[]):
    collection.append(item)
    return collection

add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] — not ['b']

# Correct: use None sentinel
def add_item(item, collection=None):
    if collection is None:
        collection = []
    collection.append(item)
    return collection
```

**Why missed**: The mutable default arg issue is in Python FAQs, but it still ships regularly because reviewers spot-check function signatures without running the mental model of "this default is evaluated once." The bug only appears on the second call, not in unit tests that call the function once per test.

**Review trigger**: any default argument that is a list, dict, or set literal.

---

### Late Binding in Closures

**Pattern reviewers miss:**
```python
# All lambdas capture the variable `i`, not its value.
funcs = [lambda: i for i in range(3)]
funcs[0]()  # returns 2, not 0
funcs[1]()  # returns 2, not 1

# Correct: bind at definition time via default argument
funcs = [lambda i=i: i for i in range(3)]
```

**Why missed**: The loop looks like it creates three independent functions. The fact that Python closures capture variables (not values) is non-obvious. This exact pattern appears in callback registration, event handler setup, and test parametrization. The bug manifests at call time, not definition time, so it's invisible in code that only sets up the closures.

**Review trigger**: any lambda or nested function defined inside a loop that references the loop variable.

---

### Exception-Swallowing Bare Except

**Pattern reviewers miss:**
```python
try:
    result = fetch_data()
except:
    result = None  # catches KeyboardInterrupt, SystemExit, MemoryError

# Correct: catch specific exceptions
try:
    result = fetch_data()
except (ConnectionError, TimeoutError) as e:
    log.warning("fetch failed: %s", e)
    result = None
```

**Why missed**: `except:` looks equivalent to `except Exception:` but is not — it catches `BaseException`, including `KeyboardInterrupt` and `SystemExit`. Code that swallows these becomes unresponsive to Ctrl-C and SIGTERM, which causes deployment and container shutdown problems.

---

## SQL / ORM

### N+1 in ORMs That Look Clean

**Pattern reviewers miss:**
```python
# Django / SQLAlchemy — looks like one query, executes N+1
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # one SELECT per post

# Correct: eager load
posts = Post.objects.select_related('author').all()
```

**Why missed**: The ORM abstracts the queries. In the diff, it looks like two lines accessing an object. The N+1 only appears when you understand that `post.author` triggers a lazy load. In development with small datasets it's invisible; in production with thousands of rows it's a page timeout.

**Review trigger**: any loop that accesses a relationship attribute on an ORM object without a visible `select_related`, `prefetch_related`, `joinedload`, or `eager_load` call.

---

### Missing Index on Foreign Key Columns

**Pattern reviewers miss:**
```sql
-- Foreign key created, but no index on the referencing column.
ALTER TABLE orders ADD COLUMN user_id INT REFERENCES users(id);

-- Every JOIN or WHERE on user_id is a full table scan.
-- Correct:
ALTER TABLE orders ADD COLUMN user_id INT REFERENCES users(id);
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

**Why missed**: Most ORM migration generators create the FK constraint but not the index. The schema looks correct. The performance failure only appears under load when the table has meaningful rows. This is a diff-review blind spot because the constraint and the missing index are on the same column — it reads as complete.

---

### SELECT * in Application Queries

**Pattern reviewers miss:**
```python
# Fetches all columns including large BLOBs, deprecated fields, secrets
cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])

# Correct: explicit column list
cursor.execute("SELECT id, email, display_name FROM users WHERE id = %s", [user_id])
```

**Why missed**: `SELECT *` is acceptable for exploratory queries and is common in tutorial code. In application code, it causes three problems: it over-fetches data (performance), it breaks when columns are added or removed (fragility), and it may return columns containing sensitive data that the application code then accidentally logs or serializes.

---

## Cross-Language: Error Path Review

For any function that can fail, check the diff for:

1. **Does the error path return a meaningful error?** Or does it return `nil`, `None`, `null` with no signal about why?
2. **Is the error logged at the right level?** Swallowed errors at DEBUG that should be ERROR; conversely, expected errors (rate limits, cache misses) logged at ERROR that generate alert noise.
3. **Does the error path clean up resources?** Files, connections, locks, and goroutines acquired before the failure — are they released in the error path?

These are correctness findings, not style. Label them `correctness (blocker):` if the missing cleanup causes a resource leak or data corruption.
