---
name: command-creator
description: "Design and scaffold Claude Code slash commands (reusable workflow shortcuts invocable as /command-name). Covers prompt engineering for commands, parameter design, example cases, and command anti-patterns. Use when asked to automate a workflow as a slash command, create a /command, or turn a recurring prompt into a persistent tool. Triggers: slash command, create a command, /command-name pattern."
---

# Command Creator

This skill guides the creation of Claude Code slash commands — reusable workflows invoked with `/command-name` in Claude Code conversations.

## Mindset

Expert heuristics for command authorship:

1. **Write for autonomy, not for humans.** Every instruction must be executable without clarifying questions. Vague steps ("check for errors") are failures — the agent will stall or hallucinate.
2. **The description IS the interface.** The frontmatter `description` is what appears in `/help`. A weak description means no one invokes the command correctly. Write it as an imperative action statement.
3. **Anti-patterns before steps.** Identify what NOT to do first. The costliest failures (batching todos, tool confusion, retry loops) come from omission, not malformed steps.
4. **Pattern before content.** Choose a workflow pattern (Analyze→Act→Report, Run→Fix→Repeat, etc.) before writing a single instruction line. Mismatched pattern = structurally broken command.
5. **Success criteria are mandatory, not optional.** A command without a defined stop condition will run forever or stop arbitrarily. Both are failures.

## Navigation

**Use this skill when:**
- User asks to "create a command", "make a slash command", "add a command", "automate a workflow"
- User says "I keep doing X, can we make a command for it?"
- User wants to package a multi-step process for reuse
- User wants project-specific or global automation

**Do NOT use this skill when:**
- User wants to run an existing command (just run it)
- User wants to modify Claude's behavior via settings.json (use update-config skill)
- User wants a script, not a slash command — scripts live in `scripts/`, not `.claude/commands/`

**Decision tree — which pattern to recommend:**

```
Does the command fix/retry until passing?
  YES → Iterative Fixing (Run→Parse→Fix→Repeat)
  NO  → Does it coordinate multiple agents?
          YES → Agent Delegation (Context→Delegate→Iterate)
          NO  → Does it run one tool and return output?
                  YES → Simple Execution (Parse→Execute→Report)
                  NO  → Workflow Automation (Analyze→Act→Report)
```

**Location decision:**
```
Is user inside a git repo?
  YES → .claude/commands/ (project-level)
  NO  → ~/.claude/commands/ (global)
User says "global"? → Always ~/.claude/commands/
User says "project"? → Always .claude/commands/
```

## Philosophy

Commands are not documentation — they are agent programs. Every line must be an unambiguous, executable instruction. Optimize for the agent that will run it cold, without prior context, at 3am on a CI failure.

## NEVER

Anti-patterns that silently break commands — each has a non-obvious failure mode:

1. **NEVER use second-person ("you should", "you need to").** Agents parse imperative instructions; second-person triggers a reasoning mode that introduces hesitation and paraphrasing, causing drift from the intended steps.
2. **NEVER omit a stop condition on iterative commands.** Without `max iterations: N` or stuck-detection logic, the agent enters an infinite loop on unfixable errors, burning context and never surfacing the root cause.
3. **NEVER put anti-patterns only in reference files.** If the NEVER list isn't visible when the command is invoked, the agent never reads it. Critical constraints must be inline.
4. **NEVER use underscores in command names** (`submit_stack` → broken). Claude Code uses the filename as the invocation key; underscores silently prevent the command from appearing in `/help`.
5. **NEVER batch todo completions.** Marking all todos done at the end defeats progress tracking and means a mid-execution failure looks like success. Mark each todo complete immediately after its task finishes.
6. **NEVER write vague description fields** (`description: A command for CI stuff`). The description is the only thing visible in `/help` — vague descriptions mean the command is never invoked for its intended purpose.
7. **NEVER use the Task tool when Bash tool is correct** (and vice versa). Task tool spins up a subagent (expensive, for delegation). Bash tool runs commands directly. Using Task for `make lint` wastes context; using Bash for multi-agent orchestration silently drops agent specialization.

## When Things Go Wrong

| Symptom | Root Cause | Fix |
|---|---|---|
| Command never appears in `/help` | Filename uses underscores instead of hyphens | Rename file to `kebab-case.md` |
| Agent asks clarifying questions mid-execution | Steps are vague or use second-person | Rewrite steps in imperative form with explicit expected outcomes |
| Agent loops forever on CI failure | No stuck-detection or max-iteration guard | Add `If same error appears 3 times: STOP and report` |
| Todos all marked done instantly | Instructions say "mark all complete at end" | Rewrite to mark each todo complete immediately after its step |
| Wrong location (project vs global) | Auto-detect not run, or user intent not checked | Run `git rev-parse --is-inside-work-tree` first; confirm with user |
| Command breaks on some machines | Hard-coded absolute paths in command body | Use relative paths or environment variables |

## About Slash Commands

Slash commands are markdown files stored in `.claude/commands/` (project-level) or `~/.claude/commands/` (global/user-level) that get expanded into prompts when invoked. They are ideal for:

- Repetitive workflows (code review, PR submission, CI fixing)
- Multi-step processes that need consistency
- Agent delegation patterns
- Project-specific automation

## Bundled Resources

Load these references when needed — do not load all upfront:

- **references/patterns.md** — Command patterns with decision guides (Workflow Automation, Iterative Fixing, Agent Delegation, Simple Execution)
- **references/examples.md** — Full source for real commands (submit-stack, ensure-ci, create-implementation-plan)
- **references/best-practices.md** — Quality checklist, writing guidelines, template structure, advanced patterns

## Command Creation Workflow

### Step 1: Determine Location

Auto-detect the appropriate location:

1. Check git repository status: `git rev-parse --is-inside-work-tree 2>/dev/null`
2. Default:
   - In git repo → Project-level: `.claude/commands/`
   - Not in git repo → Global: `~/.claude/commands/`
3. Override: if user says "global" → `~/.claude/commands/`; if user says "project" → `.claude/commands/`

Report chosen location before proceeding.

### Step 2: Select Pattern

Load **references/patterns.md** and use the decision tree above to recommend a pattern. Ask: "Which pattern is closest to what you want to create?" before writing a single instruction.

### Step 3: Gather Command Information

#### A. Name and Purpose

- Command name: kebab-case only (`submit-stack` ✅, `submit_stack` ❌)
- Description: imperative, action-oriented, for `/help` output

#### B. Arguments

- Does the command take arguments? Required or optional?
- `argument-hint: <required>` or `argument-hint: [optional]` in frontmatter

#### C. Workflow Steps

- Initial checks (file existence, git status)
- Main actions and tool choices
- Error handling approach
- Success criteria and stop conditions

#### D. Tool Restrictions

- Which tools to use (Bash vs Task vs Edit)
- Which tools to explicitly prohibit
- Any files to read for context

### Step 4: Generate Optimized Command

Load **references/best-practices.md** before writing. Apply:

- Imperative/infinitive form (verb-first, never "you should")
- Explicit tool names per step
- Expected outcomes after each action
- Realistic examples (not foo/bar)
- Error handling with specific recovery actions
- Clear stop conditions

### Step 5: Create the Command File

1. Determine full file path (project: `.claude/commands/[name].md`, global: `~/.claude/commands/[name].md`)
2. Ensure directory exists: `mkdir -p [directory-path]`
3. Write the command file using the Write tool
4. Confirm with user: file location, what it does, how to invoke it

### Step 6: Test and Iterate (Optional)

Suggest: `You can test this command by running: /command-name [arguments]`

Be ready to iterate on feedback and update the file.

## Summary

1. **Detect location** (project vs global, confirm with user)
2. **Select pattern** using decision tree before writing
3. **Gather information** (name, purpose, arguments, steps, tools)
4. **Generate optimized command** with agent-executable instructions
5. **Create file** at appropriate location
6. **Confirm and iterate** as needed

Focus on creating commands that agents can execute autonomously, with unambiguous steps, explicit tool usage, inline anti-patterns, and defined stop conditions.
