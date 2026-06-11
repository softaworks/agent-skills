# Shared Config Patterns

Reference for the monorepo-workspace skill — tsconfig inheritance, ESLint layout, and the config-package pattern.

---

## TypeScript: tsconfig Extends Chain

### The Three-Layer Pattern

```
tsconfig.base.json          ← root: compiler options only, no files/include/exclude
  └── packages/*/tsconfig.json    ← per-package: extends base, adds include/paths
        └── packages/*/tsconfig.build.json  ← build variant: excludes tests, emits .d.ts
```

**Root `tsconfig.base.json`** (compiler options only — never include `include`, `exclude`, or `references` here):
```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

**Per-package `tsconfig.json`** (development + IDE, includes tests):
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src",
    "paths": {
      "@acme/utils": ["../utils/src/index.ts"]
    }
  },
  "include": ["src/**/*", "tests/**/*"]
}
```

**Per-package `tsconfig.build.json`** (emit only, excludes tests):
```json
{
  "extends": "./tsconfig.json",
  "exclude": ["**/*.test.ts", "**/*.spec.ts", "tests/**/*"],
  "compilerOptions": {
    "paths": {}
  }
}
```

**Critical**: The `paths` override in `tsconfig.build.json` clears aliases because published consumers resolve imports through `node_modules`, not through TypeScript path mapping. If you leave `paths` active in the build config, the emitted `.d.ts` files contain unresolvable import paths for external consumers.

### Project References (Alternative to paths)

For large repos where IDE performance matters, TypeScript project references are more reliable than `paths`:

```json
// packages/app/tsconfig.json
{
  "extends": "../../tsconfig.base.json",
  "references": [
    { "path": "../utils" }
  ]
}
```

```bash
# Build with incremental compilation — only rebuilds changed packages
tsc --build packages/app/tsconfig.json
```

Project references require each referenced package to have a `tsconfig.json` with `"composite": true` and `"declaration": true`. The build order is computed by `tsc --build` automatically — you do not need a separate task runner for TypeScript-only dependency ordering.

---

## ESLint: Flat Config in Monorepos

**Flat config (`eslint.config.mjs`) is the correct choice for new monorepos.** The legacy `extends`-based config has resolution ambiguity in hoisted `node_modules` that causes plugin version conflicts.

### Root flat config with per-package overrides

```js
// eslint.config.mjs (root)
import js from '@eslint/js';
import ts from 'typescript-eslint';

export default ts.config(
  js.configs.recommended,
  ...ts.configs.strict,
  {
    // Global ignores
    ignores: ['**/dist/**', '**/node_modules/**', '**/*.gen.ts']
  },
  {
    // Per-package overrides via files glob
    files: ['packages/app/**/*.ts'],
    rules: {
      // app-specific rules
    }
  }
);
```

Each package can have its own `eslint.config.mjs` that imports and extends the root:
```js
// packages/utils/eslint.config.mjs
import rootConfig from '../../eslint.config.mjs';
export default [
  ...rootConfig,
  {
    rules: { 'no-console': 'error' }  // stricter for library packages
  }
];
```

**Non-obvious**: With flat config, ESLint stops traversing upward when it finds a config file. A package-level `eslint.config.mjs` completely replaces the root config unless you explicitly import and spread it. This is different from the legacy behavior where `extends` chains merged configs.

---

## The "Config Package" Pattern — When It's Right vs Over-Engineering

### When it's right

A dedicated `@acme/tsconfig` or `@acme/eslint-config` package makes sense when:
- Multiple **separate repos** need to share the same config (publish to npm)
- Config changes need their own semantic versioning and changelog
- More than ~8 packages consume the config and drift is a real problem

```
packages/
  tsconfig/           ← @acme/tsconfig
    tsconfig.base.json
    tsconfig.react.json
    tsconfig.node.json
    package.json
```

```json
// packages/app/package.json
{
  "devDependencies": { "@acme/tsconfig": "workspace:*" }
}
// packages/app/tsconfig.json
{ "extends": "@acme/tsconfig/tsconfig.react.json" }
```

### When it's over-engineering

A config package is overhead when:
- All consumers are in the same monorepo (just use `../../tsconfig.base.json`)
- The team is fewer than 5 engineers — the coordination cost exceeds the consistency benefit
- You're spending time versioning config changes — config should be boring

**Default rule**: start with a root-level `tsconfig.base.json` and a root `eslint.config.mjs`. Only extract to a config package when you have a second repo that needs to consume it.
