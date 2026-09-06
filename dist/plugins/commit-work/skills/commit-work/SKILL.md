---
name: commit-work
description: "Create high-quality git commits: review/stage intended changes, split into logical commits, and write clear commit messages (including Conventional Commits). Use when the user asks to commit, craft a commit message, stage changes, or split work into multiple commits."
---

# Commit work

## Goal
Make commits that are easy to review and safe to ship:
- only intended changes are included
- commits are logically scoped (split when needed)
- commit messages describe what changed and why

If the repository states its own commit rules (AGENTS.md or CLAUDE.md, often under "Commit Discipline"), those take precedence over this skill.

## Inputs to ask for (if missing)
- Single commit or multiple commits? (If unsure: default to multiple small commits when there are unrelated changes.)
- Commit style: Conventional Commits are required.
- Any rules: max subject length, required scopes.

## Workflow (checklist)
1) Inspect the working tree before staging
   - `git status`
   - `git diff` (unstaged)
   - If many changes: `git diff --stat`
2) Decide commit boundaries (split if needed)
   - Split by: feature vs refactor, backend vs frontend, formatting vs logic, tests vs prod code, dependency bumps vs behavior changes.
   - If unrelated changes are mixed in one file, commit one concern first and the next afterwards; a file cannot be split non-interactively.
3) Stage only what belongs in the next commit
   - Stage explicit paths: `git add <path> ...`. Avoid `git add .` and `git add -A`, which sweep in unrelated work.
   - To unstage: `git restore --staged <path>`
   - `git add -p` and `git restore --staged -p` are interactive; an agent cannot drive them. If a file genuinely needs hunk-level splitting, hand that step to the human.
4) Review what will actually be committed
   - `git diff --cached`
   - Sanity checks:
     - no secrets or tokens
     - no accidental debug logging
     - no unrelated formatting churn
5) Describe the staged change in 1-2 sentences (before writing the message)
   - "What changed?" + "Why?"
   - If you cannot describe it cleanly, the commit is probably too big or mixed; go back to step 2.
6) Write the commit message
   - Use Conventional Commits (required):
     - `type(scope): short summary`
     - blank line
     - body (what/why, not implementation diary)
     - footer (BREAKING CHANGE) if needed
   - For multi-line messages, supply the body directly — `git commit -F -` with a heredoc, or repeated `-m` flags. `git commit -v` opens an editor an agent cannot use.
   - Use `references/commit-message-template.md` if helpful.
7) Run the smallest relevant verification
   - Run the repo's fastest meaningful check (unit tests, lint, or build) before moving on.
8) Repeat for the next commit until the working tree is clean

## Deliverable
Provide:
- the final commit message(s)
- a short summary per commit (what/why)
- the commands used to stage/review (at minimum: `git diff --cached`, plus any tests run)
