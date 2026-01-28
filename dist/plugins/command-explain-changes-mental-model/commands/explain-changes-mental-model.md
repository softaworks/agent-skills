---
description: Build a mental model of changes by splitting them into smaller logical chunks
argument-hint: [commit|branch|range|custom]
---

# Mental Model Builder

Analyze code changes and present them as a coherent mental model - breaking large diffs into logical chunks ordered by dependency so they can be understood incrementally.

## What This Command Does

1. **Gather changes** from the specified source (commit, branch, range, or custom input)
2. **Analyze and categorize** changes into logical groups by theme/purpose
3. **Identify dependencies** between change groups
4. **Present ordered explanation** so changes can be reviewed in a sensible sequence

## Usage

```bash
# Current working changes (staged + unstaged)
/mental-model

# Specific commit
/mental-model abc1234
/mental-model HEAD~3

# Branch comparison (vs main)
/mental-model feature/my-branch

# Explicit range
/mental-model main..HEAD
/mental-model origin/main...HEAD

# Custom - user will provide diff/changes in next message
/mental-model custom
```

## Implementation Steps

When this command is invoked:

### 1. Determine Change Source

Parse the argument to determine what changes to analyze:

**No argument provided:**
- Run `git diff HEAD` to get all uncommitted changes (staged + unstaged)
- If no changes found, report "No uncommitted changes to analyze"

**Argument looks like a commit hash** (7-40 hex chars):
- Run `git show <hash> --stat` first to verify it exists
- Run `git show <hash>` to get the full diff

**Argument looks like a branch name** (contains letters, no `..`):
- Detect main branch: check if `main` or `master` exists
- Run `git diff <main-branch>...<argument>` to compare

**Argument contains `..`** (explicit range):
- Use as-is: `git diff <argument>`

**Argument is "custom":**
- Tell the user: "Please paste or describe the changes you want me to analyze in your next message."
- Wait for user input before proceeding

### 2. Extract the Diff

Run the appropriate git command and capture the output:

```bash
# Example for commit
git show <hash> --no-color

# Example for range
git diff <range> --no-color
```

If the diff is very large (>5000 lines), use `--stat` first to get an overview, then selectively read the most important files.

### 3. Analyze and Categorize Changes

Group changes into logical categories based on:

- **Purpose**: What problem does this change solve?
- **Layer**: API, UI, business logic, data, infrastructure, tests, config
- **Feature area**: Authentication, payments, search, etc.
- **Type**: New feature, refactor, bug fix, cleanup

For each file changed, determine:
- What logical group it belongs to
- What other changes it depends on
- What changes depend on it

### 4. Build Dependency Graph

Identify how changes relate to each other:

- **Foundation changes**: Types, interfaces, schemas that other code depends on
- **Implementation changes**: Code that uses the foundation
- **Integration changes**: Code that ties implementations together
- **Test/config changes**: Usually depend on everything else

Order groups so that:
1. Dependencies come before dependents
2. Lower-level abstractions come before higher-level ones
3. Core changes come before peripheral changes

### 5. Present the Mental Model

Output the analysis in this format:

```markdown
## Mental Model: [Brief title of what these changes accomplish]

### High-Level Summary
[2-3 sentences explaining the overall goal and approach of these changes]

### Key Concepts to Understand
Before diving into the code, understand these concepts:
- **[Concept 1]**: [Brief explanation]
- **[Concept 2]**: [Brief explanation]
- **[Concept 3]**: [Brief explanation]

### Change Groups (in review order)

#### 1. [Group Name] - [Purpose]
**Files:** `file1.ts`, `file2.ts`
**Why this matters:** [Explain the purpose and context]
**Key changes:**
- [Change 1 and why]
- [Change 2 and why]
**Depends on:** Nothing (foundation)
**Enables:** [What other groups need this]

#### 2. [Group Name] - [Purpose]
**Files:** `file3.ts`, `file4.ts`
**Why this matters:** [Explain the purpose and context]
**Key changes:**
- [Change 1 and why]
- [Change 2 and why]
**Depends on:** Group 1
**Enables:** [What other groups need this]

[Continue for all groups...]

### Review Sequence
For the best understanding, review in this order:
1. **[Group 1]** - Start here because [reason]
2. **[Group 2]** - Then this because [reason]
3. **[Group 3]** - Finally this because [reason]

### Gotchas and Non-Obvious Details
- [Any tricky parts or things that might be confusing]
- [Implicit assumptions in the code]
- [Things that look wrong but are intentional]
```

## Important Notes

- **Focus on understanding, not just describing**: Explain WHY changes were made, not just WHAT changed
- **Use the user's domain language**: If the codebase has specific terminology, use it
- **Be honest about complexity**: If something is genuinely complex, say so and break it down further
- **Highlight the "aha moments"**: What insight makes everything click into place?
- **Skip trivial changes**: Don't waste mental bandwidth on import reordering, formatting, etc.

## Error Handling

If git command fails:
- Report the specific error
- Suggest alternatives (e.g., "Did you mean branch X?")

If diff is empty:
- Report "No changes found for the specified source"

If changes are too large to analyze meaningfully:
- Provide a high-level overview first
- Offer to deep-dive into specific areas: "This is a large changeset. Want me to focus on a specific area? (e.g., 'the API changes' or 'the database migrations')"

## Example Output

For a commit that adds user authentication:

```markdown
## Mental Model: Adding JWT-based User Authentication

### High-Level Summary
These changes add user authentication using JWT tokens. The flow is: user submits credentials → server validates → server returns JWT → client stores and sends JWT with requests → server validates JWT on protected routes.

### Key Concepts to Understand
- **JWT (JSON Web Token)**: A signed token containing user identity, passed in Authorization header
- **Middleware pattern**: Express middleware that runs before route handlers to check auth
- **Token refresh**: Mechanism to get new tokens without re-entering credentials

### Change Groups (in review order)

#### 1. Auth Types & Interfaces - Foundation
**Files:** `src/types/auth.ts`
**Why this matters:** Defines the shape of auth data used everywhere else
**Key changes:**
- Added `User`, `TokenPayload`, `AuthResponse` types
- These types ensure consistency across the auth system
**Depends on:** Nothing
**Enables:** All other auth code

#### 2. JWT Utilities - Token Operations
**Files:** `src/utils/jwt.ts`
**Why this matters:** Core logic for creating and validating tokens
**Key changes:**
- `signToken()` - creates JWT with user data and expiration
- `verifyToken()` - validates JWT and extracts payload
**Depends on:** Auth types
**Enables:** Auth middleware, login endpoint

[etc...]
```
