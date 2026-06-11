# Feedback Phrasing

The technical finding and the comment about the technical finding are separate skills. Good findings delivered badly get ignored, disputed, or worked around without being fixed. Bad phrasing also signals low reviewer calibration, reducing the weight of the next comment.

---

## Giving Feedback: The Comment Formula

```
[category] ([severity]): [observation or question]. [suggested fix if applicable].
```

Examples:
- `correctness (blocker): this will throw if items is empty — Array.prototype.reduce with no initial value on an empty array throws TypeError. Add an initial value: items.reduce((acc, x) => acc + x, 0).`
- `comprehensibility (minor): after the second read this function does three distinct things (validate, transform, persist). A future maintainer will have to read all 60 lines to understand any one of them. Consider extracting into three functions.`
- `nit: "data" could be "userData" to distinguish from the API response object above.`

---

## Asking vs. Asserting

Use questions when you're uncertain whether the code is wrong or you're missing context:

- "Does this handle the case where `user.role` is undefined?" (not "this crashes if role is undefined")
- "Is there a reason this is sequential rather than Promise.all?" (not "this is slow, use Promise.all")
- "What happens here if the DB write fails after the cache is updated?" (not "race condition")

Questions invite the author to confirm or provide context. If the author confirms the concern, the finding stands. If they provide context you didn't have, you update your understanding — and then the question is whether the code should make that context visible to the next reader without the PR thread.

**When to assert instead of ask**: when you're certain the code is wrong — a syntax error, a known language pitfall (mutable default arg, late binding closure), a provably incorrect algorithm. Asking "is this intentional?" for a mutable default arg wastes cycles. Label it correctness and show the fix.

---

## "I'd Do It Differently" vs. "This Is Wrong"

State this explicitly. Authors can't read your intent.

- "This is wrong because [reason] — correctness (blocker)."
- "I'd approach this differently — I'd use X because Y — but this implementation is correct. Nit if you want to reconsider."
- "Not sure which approach is better here. I'd lean toward X because it's more consistent with how we handle this in module Z. Minor."

The cost of false certainty: if you mark a preference as a correctness finding and the author complies, you've introduced unnecessary churn. If they push back and you're wrong, you've damaged your reviewer credibility for future real findings.

---

## Feedback Phrases to Avoid

| Phrase | Problem | Better |
|--------|---------|--------|
| "just rename this" | Minimizes effort; perceived as dismissive | "nit: `data` → `userData` would distinguish it from the API response variable above" |
| "this could be simplified" | Not actionable without the simplification | "comprehensibility (minor): [show the simplified version]" |
| "consider using X" | Too soft for a correctness finding, too strong for a nit | Label it explicitly: "nit: consider..." or "correctness (major): use X because..." |
| "this is wrong" | No reason, no fix | "correctness (blocker): this is wrong because [specific reason]. Fix: [specific fix]." |
| "not sure about this" | Author can't act on uncertainty without a specific concern | State the concern: "not sure this handles the null case — what happens when X is null?" |
| "..." | A review comment with no content | Delete it; or write the thought |

---

## Receiving Feedback: The Author Protocol

### The NEVER Rule

**NEVER explain the context that makes the feedback wrong — fix the code so it communicates that context itself.**

When a reviewer misunderstands your code, the correct response is not:
- "I explained this in the PR description"
- "This was discussed in the design doc"
- "If you look at the calling code, it's clear that..."

Those responses are telling the reviewer they're wrong and that the code is fine. But the code is not fine: it is unclear enough that a qualified person, reading it fresh, misunderstood it. That is the bug. Fix the code, not the reviewer.

### The Author Response Workflow

For each piece of feedback:

1. **Read the label.** Is it a blocker, major, minor, or nit? If it's unlabeled, ask: "Is this blocking or a suggestion?"
2. **Distinguish "wrong" from "different."** If the reviewer says the code is incorrect, verify. If they say they'd do it differently, you are allowed to disagree — but explain why your choice is better, not just that it's yours.
3. **Apply the NEVER rule.** If your first instinct is to write a comment explaining why the feedback is based on a misunderstanding, stop. Ask yourself: "How do I fix the code so that misunderstanding is impossible?"
4. **Respond to every comment.** Even if you're not making a change, respond with why. "Declining: this is consistent with the pattern in [module] — see [file:line]." Silence makes reviewers feel ignored and escalates nits into blocked PRs.
5. **Don't argue about nits.** If it's a nit, apply it or explain briefly why you're not. Spending three comments defending a variable name is a worse signal than a variable name you disagree with.

### When the Feedback Is Genuinely Wrong

It happens. Reviewers miss context. Handle it without winning:

- State the specific reason the feedback doesn't apply: "This branch is only reachable when X is already validated at [line]. The null case can't reach here."
- Then ask: "Does the code make that clear enough, or should I add a comment to the guard clause?" This turns a disagreement into a collaboration on clarity.
- If the reviewer still disagrees, escalate to a call rather than a thread. Comment threads are the wrong medium for resolving genuine technical disagreement.

---

## Review Thread Health

A review thread is healthy when it ends. Signs of an unhealthy thread:

- The same point is stated multiple times with increasing emphasis (both sides have stopped listening)
- The discussion is about who is right, not what the code should do
- The author is explaining intent rather than fixing code
- The reviewer is listing examples of how they would do it differently rather than identifying what is wrong

When a thread goes unhealthy, one person needs to end it: either "you've convinced me, I'll fix it" or "I'm not going to fix this one because [one sentence reason], marking resolved."

---

## PR Description as a Review Finding

If the PR description is missing or inadequate, it is a finding — not a meta-comment about process:

```
comprehensibility (minor): the PR description explains what changed but not why.
A future `git log` or `git blame` reader will land here without context for the decision.
Suggested addition: one sentence on why X approach was chosen over Y.
```

A good description contains:
1. What changed and what it does (the "what")
2. Why it was changed — what problem it solves (the "why")
3. What reviewers should pay most attention to (the "where to look")
4. What was explicitly NOT changed and why, if relevant (reduces scope questions)
