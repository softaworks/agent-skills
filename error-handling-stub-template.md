# Error Handling Stub Template for SKILL.md

A reference for skill authors on why error handling matters, what the minimum requirements are, and how to write error sections that actually help agents recover rather than stall.

---

## Why Error Handling Matters in Skills

Agents are stateless within a step. When a skill's workflow hits an unexpected state — a missing API key, an ambiguous command argument, a tool that returns no output — the agent has no built-in mechanism to recover. It will either:

1. Loop: re-attempt the same failing action with the same parameters, indefinitely.
2. Stall: stop and ask the user for clarification, producing an unhelpful open-ended question.
3. Hallucinate a recovery: invent a plausible-looking next step that makes the situation worse.

A skill without documented error paths is a skill that breaks silently in production. The skill author is the only person who knows what "success" looks like and therefore the only person who can define what "failure" looks like and what to do about it.

**Error handling in a SKILL.md is not optional documentation. It is the contract between the skill and every agent that runs it.**

---

## Minimum Requirement

Every skill that defines a workflow (a numbered sequence of steps) MUST document at least one error path. The error path must specify:

- What the failure condition looks like (observable signal, not a feeling)
- Why it typically occurs (root cause, not symptom)
- What the agent should do next (a concrete action, not "try again")

A skill with zero error paths will be rejected in review.

---

## Stub Template

Copy this block into any `SKILL.md` that has a workflow section. Replace bracketed placeholders with real content before submitting.

```markdown
## When Things Go Wrong

| Situation | Likely Cause | Recovery Action |
|-----------|-------------|-----------------|
| [most common tool/command failure] | [why it happens — missing dep, wrong env, bad arg] | [exact next step — which flag to change, which env var to set, which fallback to use] |
| [ambiguous input state] | [why the input is ambiguous — two valid interpretations, missing required field] | [decision rule — how to pick between options without asking the user] |
| [partial completion — some steps succeeded, then it stopped] | [why partial completion happens — rate limit, auth expiry mid-run, missing downstream dep] | [how to resume — idempotency check, which step to restart from, what state to verify first] |
```

Minimum: one row per failure mode you have personally observed or can reason about from the workflow. Three rows is a reasonable floor for any non-trivial skill.

---

## Three Failure Categories

Treat these as distinct. Conflating them produces recovery actions that do not match the actual problem.

### (a) Tool / Command Failures

A tool returned a non-zero exit code, an HTTP error, or no output when output was expected.

Examples: `npx` fails because the package is not installed; a CLI returns `401 Unauthorized`; a script exits with `command not found`.

Recovery pattern: check the prerequisite (is the tool installed, is the auth valid, is the argument correctly formed), fix that specific thing, re-run the exact same step. Do not skip to the next step in the workflow.

### (b) Ambiguous Input States

The agent received input that matches two or more valid interpretations and cannot proceed without choosing one.

Examples: the user said "deploy" without specifying environment; the config file has two entries with the same name; a search returns 40 results with no clear best match.

Recovery pattern: apply a decision rule documented in the skill (prefer staging over production; use the most recently modified entry; pick the result with the highest relevance score). Only escalate to the user if the decision rule cannot resolve the ambiguity. When escalating, present the two options explicitly — do not ask an open-ended question.

### (c) Partial Completions

Some steps in the workflow completed successfully before the failure. The system is now in a mixed state: some resources exist, some do not.

Examples: three of five files were uploaded before a rate limit hit; a database migration ran the first two steps before auth expired; a commit was staged but not pushed when the network dropped.

Recovery pattern: before re-running, verify what already completed (check file existence, query state, read a log). Resume from the first incomplete step, not from the beginning. Document which steps are idempotent (safe to re-run) and which are not (create operations that would duplicate records).

---

## Worked Examples

### Example 1: Tool Skill (Datadog CLI)

A tool skill wraps a CLI or API. Failures are usually environment or network failures.

```markdown
## When Things Go Wrong

| Situation | Likely Cause | Recovery Action |
|-----------|-------------|-----------------|
| `Error: Missing DD_API_KEY environment variable` | API key not exported in the current shell session | Run `export DD_API_KEY="..."` and `export DD_APP_KEY="..."` before retrying. Keys are at https://app.datadoghq.com/organization-settings/api-keys |
| Query returns zero results when errors are expected | Time window is too narrow or query syntax uses wrong field name | Widen `--from` to `4h`, then to `24h`. If still empty, verify field names with `npx @leoflores/datadog-cli logs search --query "*" --from 15m` and compare field names in the output |
| `npx` hangs or times out on first run | Large package download on slow connection | Kill the process, run `npx @leoflores/datadog-cli --version` once to cache the package, then retry the original command |
| Non-US site returns 403 | Default site is `datadoghq.com`; account is on EU or another region | Add `--site datadoghq.eu` (or the correct regional site) to every command |
```

### Example 2: Creative Skill (Domain Name Brainstormer)

A creative skill has no external tool failures but does have ambiguous input and quality failures.

```markdown
## When Things Go Wrong

| Situation | Likely Cause | Recovery Action |
|-----------|-------------|-----------------|
| All suggested domains are taken | Common keywords are heavily registered | Pivot strategy: use compound words, portmanteaus, or invented words. Ask the user for 2-3 adjectives that describe the brand feeling (not the product) and generate a second pass |
| User says "I don't like any of these" without elaboration | Suggestions missed an unstated constraint (length, tone, language) | Ask exactly two clarifying questions: maximum character count, and one word that captures the brand's personality. Do not regenerate until both are answered |
| Availability check is inconclusive (WHOIS timeout) | WHOIS rate limiting or DNS propagation delay | Mark those domains as "unverified" and recommend the user check registrar.com manually. Do not present them as available |
| User provides a name in a language other than English | Transliteration or cultural meaning may be undesirable | Flag potential issues (homonyms, negative connotations in target markets) before presenting the name as a recommendation |
```

### Example 3: Process Skill (Commit Work)

A process skill orchestrates multi-step Git operations. Partial completions are the dominant failure mode.

```markdown
## When Things Go Wrong

| Situation | Likely Cause | Recovery Action |
|-----------|-------------|-----------------|
| `git add -p` exits with no hunks selected | File has no unstaged changes or was already fully staged | Run `git status` and `git diff --cached` to confirm current state. If the file is already staged, proceed to the review step |
| Pre-commit hook fails after staging | Hook detected lint errors, secrets, or test failures | Do NOT use `--no-verify`. Read the hook output, fix the specific violation, re-stage only the affected files, and retry the commit. Amending is not an option if the previous commit is on a remote branch |
| Commit message is rejected by hook (subject too long, wrong type) | Project enforces Conventional Commits format with a subject length limit | Rewrite the subject line to `type(scope): short summary` under 72 characters. Common types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test` |
| `git diff --cached` shows unexpected files | Earlier patch staging accidentally included an unrelated hunk | Run `git restore --staged <path>` for the unexpected file, then re-run `git add -p` for that file only |
```

---

## NEVER Patterns

These patterns consistently cause agent loops or security failures. Do not use them in any skill.

### NEVER: "Try again" without specifying what to change

Bad:
```
If the command fails, try again with different parameters.
```

Why it fails: "different" is undefined. The agent will retry with identical parameters, or guess a change that makes the situation worse.

Good:
```
If the command returns exit code 1, add the `--verbose` flag to see the full error, then fix the specific error shown before retrying.
```

### NEVER: Authentication failures without a documented fallback path

Bad:
```
If authentication fails, check your credentials.
```

Why it fails: the agent will attempt to "check credentials" by reading environment variables, config files, and potentially trying alternative credential sources — exposing secrets in the process. It will not know when to stop.

Good:
```
If authentication returns 401:
1. Confirm the env var is set: `echo $MY_API_KEY` (shows length only — do not print the value).
2. If the variable is empty, stop and ask the user to set it. Do not attempt to retrieve or infer the key.
3. If the variable is set but auth still fails, the key may be expired or revoked. Direct the user to the credential management page (URL here). Do not try alternative keys.
```

### NEVER: Open-ended escalation questions

Bad:
```
If unsure how to proceed, ask the user.
```

Why it fails: the agent produces a vague question ("How should I proceed?") that the user cannot usefully answer without already knowing the state of the workflow.

Good:
```
If the ambiguity cannot be resolved by the decision rules above, stop and present the user with exactly two options in this format:
"I found two matches: [option A] and [option B]. Which should I use?"
Do not proceed until the user answers.
```

---

## Checklist for Skill Authors

Before submitting a skill with a workflow section, confirm:

- [ ] At least one row in the "When Things Go Wrong" table
- [ ] Every row names a concrete observable failure signal (not "something goes wrong")
- [ ] Every recovery action specifies what to do, not just what the problem is
- [ ] Authentication failures have a documented stop condition (agent will not try to discover credentials)
- [ ] Partial completion steps identify which operations are idempotent
- [ ] No row uses "try again" without a specific parameter or condition change
- [ ] Ambiguous input states have a decision rule, not an open-ended user question
