---
description: Draft a professional email using the What-Why-How framework. Use when you need to compose emails to colleagues, stakeholders, or leadership.
argument-hint: [context or paste existing draft]
allowed-tools: Read, AskUserQuestion
---

# Draft Professional Email

Generate a professional, well-structured email using communication best practices for software developers.

## Arguments

`$ARGUMENTS` - Optional context, topic, or existing draft to refine

## Workflow

### Step 1: Gather Context

If `$ARGUMENTS` is empty or insufficient, use AskUserQuestion to gather:

**Question 1: Recipient Type** (header: "Audience")

- Technical peer (developer, engineer)
- Non-technical stakeholder (PM, executive, customer)
- Cross-functional team (mixed audience)
- Manager or leadership

**Question 2: Email Purpose** (header: "Purpose")

- Status update or progress report
- Request (review, approval, resources)
- Information sharing (FYI, announcement)
- Escalation or raising concern
- Following up on prior conversation

**Question 3: Urgency** (header: "Urgency")

- Urgent - needs response today
- Standard - within 1-2 days
- Low priority - for awareness only

### Step 2: Apply Communication Framework

Use the **What-Why-How** structure:

1. **WHAT** (Opening - 1-2 sentences)
   - Lead with the key message or request
   - State the purpose immediately
   - No throat-clearing ("I hope this email finds you well...")

2. **WHY** (Context - 2-3 sentences)
   - Provide necessary background
   - Explain relevance to the recipient
   - Include only essential context

3. **HOW** (Action - clear next steps)
   - Specific call-to-action
   - Clear deadline if applicable
   - Who needs to do what

### Step 3: Apply Email Best Practices

**Subject Line:**

- Specific and scannable (5-8 words ideal)
- Include action needed: "[Action Required]", "[FYI]", "[Decision Needed]"
- Include deadline if urgent: "[Due Friday]"

**Body Structure:**

- Bullets for multiple points (3-5 max)
- Bold key information
- One topic per email
- Short paragraphs (2-3 sentences max)

**Tone Calibration by Audience:**

| Audience | Tone | Jargon Level |
| --- | --- | --- |
| Technical peer | Direct, precise | High (use technical terms) |
| Non-technical | Business-focused | Low (translate jargon) |
| Cross-functional | Balanced | Medium (explain as needed) |
| Leadership | Concise, impact-focused | Low (focus on outcomes) |

### Step 4: Generate Draft

Produce a complete email with:

```markdown
## Email Draft

**Subject:** [Clear, specific subject line]

---

[Opening - WHAT: Key message/request]

[Context - WHY: Background and relevance]

[Body - Details as needed, use bullets for lists]

[Closing - HOW: Clear call-to-action]

[Sign-off]
```

### Step 5: Offer Refinements

After presenting the draft, offer:

1. **Tone adjustment** - Make more/less formal
2. **Length adjustment** - Expand or condense
3. **Jargon translation** - Adjust technical language level
4. **Format change** - Different structure for different medium (Slack, Teams)

## Example Usage

```bash
# With context
/soft-skills:draft-email Need to ask team lead for deadline extension on API migration

# Refine existing draft
/soft-skills:draft-email "Hi team, wanted to let you know about the deployment..."

# Start fresh
/soft-skills:draft-email
```

## Output

Present the draft in a clear format showing:

1. **Subject line** with rationale
2. **Email body** with WHAT/WHY/HOW sections labeled
3. **Refinement options** for iteration

## Anti-Patterns to Avoid

- Generic subjects ("Quick question", "Update", "FYI")
- Burying the request at the end
- Wall of text without structure
- Missing clear call-to-action
- Over-apologizing or excessive hedging
- CC'ing unnecessarily
