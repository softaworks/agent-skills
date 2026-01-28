---
description: Create a detailed implementation plan using Codex 5.2 with high reasoning
argument-hint: "<what you want to plan>"
allowed-tools: Read, Write, Bash, AskUser
---

# Codex Plan Command

You are being asked to create a detailed implementation plan using a Codex subagent. Your job is to:
1. Understand the user's planning request
2. Ask clarifying questions using AskUser to improve plan quality
3. Craft an excellent, detailed prompt for Codex
4. Execute Codex to generate and save the plan

**Always uses:** `gpt-5.2-codex` with `high` reasoning

## User Request

```
$ARGUMENTS
```

## Step 1: Analyze the Request

Look at what the user wants to plan. Identify:
- What is the core goal?
- What technology/domain is involved?
- What aspects are ambiguous or underspecified?
- What decisions would significantly impact the plan?

## Step 2: Ask Clarifying Questions

**Use AskUser to ask 3-6 targeted clarifying questions** before generating the plan.

Good clarifying questions:
- Narrow down scope and requirements
- Clarify technology choices
- Understand constraints (time, budget, team size)
- Identify must-haves vs nice-to-haves
- Uncover integration requirements
- Determine security/compliance needs

### Example Question Patterns

**For "implement auth":**
- What authentication methods do you need? (email/password, OAuth providers like Google/GitHub, SSO, magic links)
- Do you need role-based access control (RBAC) or just authenticated/unauthenticated?
- What's your backend stack? (Node/Express, Python/Django, etc.)
- Where will you store user credentials/sessions? (Database, Redis, JWT stateless)
- Do you need features like: password reset, email verification, 2FA?
- Any compliance requirements? (SOC2, GDPR, HIPAA)

**For "build an API":**
- What resources/entities does this API need to manage?
- REST or GraphQL?
- What authentication will the API use?
- Expected scale/traffic?
- Do you need rate limiting, caching, versioning?

**For "migrate to microservices":**
- Which parts of the monolith are you migrating first?
- What's your deployment target? (K8s, ECS, etc.)
- How will services communicate? (REST, gRPC, message queues)
- What's your timeline and team capacity?

**For "add testing":**
- What testing levels do you need? (unit, integration, e2e)
- What's your current test coverage?
- What frameworks do you prefer or already use?
- What's the most critical functionality to test first?

## Step 3: Gather Context

After getting answers, also gather relevant context:
- Read key files in the codebase if applicable
- Check existing architecture/patterns
- Note any existing plans or documentation

## Step 4: Craft the Codex Prompt

Create a detailed prompt that includes:
1. **Clear objective** - What plan needs to be created
2. **All requirements** - Everything learned from clarifying questions
3. **Constraints** - Technology choices, timeline, team size
4. **Context** - Relevant codebase info, existing patterns
5. **File references** - List of important files/docs the Codex should read for context
6. **Plan structure** - What sections the plan should include
7. **Output instructions** - Write to `codex-plan.md` in current directory

### Including File References (IMPORTANT)

Always include a section in the prompt telling Codex which files to read first for context:

```
## Files to Read for Context

Before creating the plan, read these files to understand the current codebase:

**Architecture & Config:**
- `README.md` - Project overview
- `package.json` / `pyproject.toml` - Dependencies and scripts
- `.env.example` - Environment variables needed

**Existing Code Patterns:**
- `src/lib/db.ts` - How database connections are handled
- `src/middleware/auth.ts` - Existing auth patterns (if any)
- `src/types/index.ts` - Type definitions

**Documentation:**
- `docs/architecture.md` - System architecture
- `docs/api.md` - API documentation

Read these files FIRST to understand existing patterns before creating the plan.
```

Adapt this list based on what you discovered in Step 3 (Gather Context). Include:
- Config files relevant to the task
- Existing code that will be modified or extended
- Documentation about architecture/patterns
- Type definitions or schemas
- Test files showing testing patterns used

**Critical instruction to include:** Tell Codex to NOT ask any further clarifying questions - it has all the information it needs and should just write the plan and save the file.

## Step 5: Save Prompt for Manual Execution

Save the crafted prompt to `prompt_to_codex.md` for manual execution.

The user will execute Codex manually using:

```bash
# --full-auto: Executa automaticamente sem interação humana
# --skip-git-repo-check: Pula verificação se está em um repositório git
# -c model=gpt-5.2-codex: Usa o modelo GPT-5.2 Codex (mais avançado)
# -c model_reasoning_effort=high: Ativa raciocínio de alto nível (deep thinking)
# --output-last-message: Salva a última mensagem do Codex em arquivo
codex exec --full-auto --skip-git-repo-check \
  -c model=gpt-5.2-codex \
  -c model_reasoning_effort=high \
  --output-last-message /tmp/codex-plan-result.txt \
  "$(cat prompt_to_codex.md)"
```

Or read the prompt and execute it:
```bash
cat prompt_to_codex.md  # Review the prompt first
```

## Example Full Flow

**User:** `/codex-plan help me implement auth into my webapp`

**You ask (using AskUser):**
```
I'd like to create a detailed auth implementation plan for you. A few questions first:

1. What authentication methods do you need?
   - Email/password
   - OAuth (Google, GitHub, etc.)
   - Magic links
   - SSO/SAML

2. Do you need role-based access control (admin, user, etc.) or just authenticated vs not?

3. What's your backend stack? (e.g., Node/Express, Python/FastAPI, Next.js API routes)

4. Where will you store sessions? (Database, Redis, JWT stateless)

5. Do you need any of these features?
   - Password reset
   - Email verification
   - Two-factor authentication (2FA)
   - Remember me / persistent sessions

6. Any compliance requirements? (SOC2, GDPR, HIPAA)
```

**User answers:** "Email/password and Google OAuth. Using Next.js with Prisma and Postgres. Need basic roles (admin/user). Yes to password reset and email verification. No 2FA for now. No special compliance."

**You craft prompt for Codex:**
```
Create a detailed implementation plan for adding authentication to a Next.js web application.

## Requirements
- Authentication methods: Email/password + Google OAuth
- Framework: Next.js (App Router)
- Database: PostgreSQL with Prisma ORM
- Role-based access: Admin and User roles
- Features needed:
  - User registration and login
  - Password reset flow
  - Email verification
  - Google OAuth integration
  - Session management
- NOT needed: 2FA, SSO, special compliance

## Plan Structure

Use this template structure:

# Plan: [Task Name]

**Generated**: [Date]
**Estimated Complexity**: [Low/Medium/High]

## Overview
[Brief summary of what needs to be done and the general approach, including recommended libraries/tools]

## Prerequisites
- [Dependencies or requirements that must be met first]
- [Tools, libraries, or access needed]

## Phase 1: [Phase Name]
**Goal**: [What this phase accomplishes]

### Task 1.1: [Task Name]
- **Location**: [File paths or components involved]
- **Description**: [What needs to be done]
- **Dependencies**: [Task IDs this depends on, e.g., "None" or "1.2, 2.1"]
- **Complexity**: [1-10]
- **Test-First Approach**:
  - [Test to write before implementation]
  - [What the test should verify]
- **Acceptance Criteria**:
  - [Specific, testable criteria]

### Task 1.2: [Task Name]
[Same structure...]

## Phase 2: [Phase Name]
[...]

## Testing Strategy
- **Unit Tests**: [What to unit test, frameworks to use]
- **Integration Tests**: [API/service integration tests]
- **E2E Tests**: [Critical user flows to test end-to-end]
- **Test Coverage Goals**: [Target coverage percentage]

## Dependency Graph
[Show which tasks can run in parallel vs which must be sequential]
- Tasks with no dependencies: [list - these can start immediately]
- Task dependency chains: [show critical path]

## Potential Risks
- [Things that could go wrong]
- [Mitigation strategies]

## Rollback Plan
- [How to undo changes if needed]

### Task Guidelines
Each task must:
- Be specific and actionable (not vague)
- Have clear inputs and outputs
- Be independently testable
- Include file paths and specific code locations
- Include dependencies so parallel execution is possible
- Include complexity score (1-10)

Break large tasks into smaller ones:
- Bad: "Implement Google OAuth"
- Good:
  - "Add Google OAuth config to environment variables"
  - "Install and configure passport-google-oauth20 package"
  - "Create OAuth callback route handler in src/routes/auth.ts"
  - "Add Google sign-in button to login UI"
  - "Write integration tests for OAuth flow"

## Instructions
- Write the complete plan to a file called `codex-plan.md` in the current directory
- Do NOT ask any clarifying questions - you have all the information needed
- Be specific and actionable - include code snippets where helpful
- Follow test-driven development: specify what tests to write BEFORE implementation for each task
- Identify task dependencies so parallel work is possible
- Just write the plan and save the file

Begin immediately.
```

**Save the prompt to `prompt_to_codex.md` for manual execution.**

## Important Notes

- **Always ask clarifying questions first** - Don't skip this step
- **Use AskUser tool** - This is interactive planning
- **Save prompt to `prompt_to_codex.md`** - User will execute manually
- **Tell Codex not to ask questions** - It should just execute
- **Expected output file:** `codex-plan.md` in current working directory (created by Codex)
- **Model to use:** `gpt-5.2-codex` with `high` reasoning effort

## Your Task Flow

1. Analyze the user's planning request above
2. Ask clarifying questions using AskUser
3. Gather context from codebase if needed
4. Craft a detailed prompt for Codex
5. **Save the prompt to `prompt_to_codex.md`** (do NOT execute)
6. Show the user they can now execute it manually with:
   ```bash
   codex exec --full-auto --skip-git-repo-check \
     -c model=gpt-5.2-codex \
     -c model_reasoning_effort=high \
     --output-last-message /tmp/codex-plan-result.txt \
     "$(cat prompt_to_codex.md)"
   ```
7. **STOP and wait** - Ask the user to send you the final plan (`codex-plan.md`) when Codex finishes. Do NOT do anything else until the user sends the plan.

## Step 7: Wait for the Plan

After showing the execution command, you MUST:

1. **Ask the user to send the plan** - Say something like:
   > "Quando o Codex terminar, me envie o conteúdo do arquivo `codex-plan.md` para eu revisar."

2. **Do NOT proceed** - Do not take any other action
3. **Do NOT assume** - Do not guess what the plan contains
4. **Just wait** - The user will paste or send the plan when ready

**IMPORTANT:** Your job is DONE after step 6. Just wait for the user to send the generated plan.
