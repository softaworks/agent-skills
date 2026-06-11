---
name: frontend-to-backend-requirements
description: Translate frontend UI needs into backend requirements documents without specifying implementation. Use when frontend needs to communicate API requirements to backend, or user says 'backend requirements', 'what data do I need', 'API requirements', 'what should the backend provide', or is describing data needs for a UI component or screen.
---

## Mindset

- **You are a journalist, not an architect.** Your job is to describe what the user sees and does — not design the system that makes it happen. The moment you specify a field name or endpoint structure, you've crossed the line.
- **Ambiguity is information.** If you're unsure whether two UI elements share data, say so explicitly. Backend uses those uncertainty signals to design for real usage, not imagined usage.
- **Requirements age.** A doc that gets one round of feedback and is never touched again is a liability. The Discussion Log section is the most important part — it captures the negotiation, not just the outcome.
- **"Simple" is not simple.** "Just give me all the user's data" causes N+1 query disasters, over-fetching, and security leaks. Frontend developers who think in terms of rendering often underestimate the cost of data aggregation. Surface that tension in questions.
- **Boundary enforcement is your constraint, not backend's.** If you catch yourself writing "the response should contain...", stop. That's backend territory. Reframe as "I need to display..." or "the user needs to be able to...".

## Navigation

**Use this skill when**:
- A frontend developer needs to communicate data needs to a backend team
- Planning a new feature that requires new or modified API support
- Documenting what an existing UI actually needs (often before refactoring an API)
- Any user says: "backend requirements", "what data do I need", "API requirements", "what should the backend provide"

**Do NOT use this skill when**:
- The user wants to design the API itself (use an API design skill instead)
- The user wants to document existing endpoints (use API docs tooling)
- The backend is a BFF (Backend for Frontend) they own — the boundary dynamic changes
- There is no backend team; they're working solo with a self-owned API

**Quick decision**: If the user is describing what they want to *build*, they need API design. If they're describing what they want to *display*, this skill applies.

## Philosophy

Frontend requirements are a contract negotiation, not a specification. The document's job is to communicate intent and surface uncertainty — not to constrain the backend into a corner before they've had a chance to think.

## NEVER

- NEVER specify field names, endpoint paths, HTTP methods, or JSON structure — because doing so anchors the backend to your mental model of the data, which is almost always wrong about something. Backend has constraints (normalization, existing schemas, caching layers) you can't see from the UI.
- NEVER omit the "why" behind a data need — because without context, backend will make assumptions that optimize for their convenience, not your use case. "Show me the user's name" leads to a different schema decision than "Show the user's name on a public-facing receipt where it must match their legal ID."
- NEVER write requirements for only the happy path — because backend will build exactly what you describe. If you don't document the empty state, the error state, and the "partially loaded" state, you'll get an API that only handles success.
- NEVER finalize requirements without explicit open questions — because silence implies agreement. An unchallenged requirement is treated as a signed contract. Forcing the backend to respond to questions surfaces design mismatches before they're coded.
- NEVER treat the document as one-way — because requirements docs that get no backend response die in a drawer. The Discussion Log is the mechanism that makes this a living document. If backend hasn't responded, the doc isn't done.
- NEVER describe requirements in terms of component implementation ("the Card component needs...") — because this ties requirements to a UI decision that may change. Describe user goals, not component structure.

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|--------------|----------|
| Backend says the requirements are contradictory | Frontend described two different screens as if they used the same data, but the data is scoped differently | Split the requirements by screen and clarify which user/context scoping applies to each |
| Requirements doc is ignored entirely | It reads like a spec, not a request — backend feels dictated to | Reframe every bullet as a question or observation; add explicit "let me know if this assumption is wrong" phrases throughout |
| Backend returns a different shape than expected | The requirements didn't explain the relationship between data entities | Revise the doc to describe how pieces relate ("for each X, I also need to show its Y") rather than listing fields in isolation |
| Backend says the data doesn't exist | You described display logic as if it were a stored property (e.g., "I need the user's 'completion percentage'") | Distinguish between computed/derived data needs and stored data needs — ask backend if the computation should happen server-side or client-side |

---

## Output

All output goes to `.claude/docs/ai/<feature-name>/backend-requirements.md` — no chat output.

Use the template at [references/output-template.md](references/output-template.md).

See [references/elicitation-questions.md](references/elicitation-questions.md) for elicitation questions to ask the user before writing the doc.

See [references/worked-example.md](references/worked-example.md) for a complete realistic example.

## Ownership Boundary (quick reference)

| Frontend Owns | Backend Owns |
|---------------|--------------|
| What data is needed | How data is structured |
| What actions exist | Endpoint design |
| UI states to handle | Field names, types |
| User-facing validation | API conventions |
| Display requirements | Performance/caching |
