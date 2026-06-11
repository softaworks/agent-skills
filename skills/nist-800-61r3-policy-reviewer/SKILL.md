---
name: nist-800-61r3-policy-reviewer
description: "Evaluate IR policy and procedure documents against NIST SP 800-61r3 Section 2.3 required policy elements and the GV.PO/GV.RR/ID.IM-04 CSF categories. Checks for all 8 required policy elements, role authority designations, and plan maintenance requirements. Use when asked to 'review this IR policy', 'check our incident response policy', 'is this policy complete', 'policy completeness check', or 'audit our IR policy'."
user-invocable: true
---

# NIST SP 800-61r3 Policy Reviewer

Evaluate IR policies, plans, and procedure documents against the requirements defined in NIST SP 800-61r3 Section 2.3 and the associated CSF 2.0 GV/ID elements.

---

## Mindset

1. **Explicit over implied.** A policy element is either explicitly stated or it is Missing — "we do this operationally" does not count. The document must speak for itself, because during an actual incident nobody reads the CSIRT wiki.

2. **Authority gaps are the most dangerous finding.** Organizations routinely list roles without designating *who can act*. A handler who doesn't know if they're authorized to yank a production server from the network will hesitate. That hesitation has measurable cost.

3. **Generic templates are a warning signal, not a pass.** If §3 of the scope says "all company assets and personnel" and nothing in the document references cloud environments, OT/ICS, remote workers, or contractors, the policy was never tailored — it's theater. Flag it.

4. **Performance measures absent = no improvement loop.** Element 7 is the most commonly missing element. Its absence means the org cannot demonstrate IR program effectiveness and cannot satisfy ID.IM-01.R1. Treat it as a critical gap regardless of how good everything else looks.

5. **The definitions section propagates errors.** If Element 4 is wrong or absent, every handler interprets "incident" differently. Misclassifications cascade into wrong escalation paths, wrong notifications, and wrong recovery decisions. Always check definitions first after scope.

---

## Navigation

### When to use this skill
- Reviewing an IR policy, IR plan, or IR procedures document for NIST SP 800-61r3 compliance
- Auditing whether a policy is ready for operational use
- Generating findings for an IR policy revision task list
- Feeding input to `nist-800-61r3-maturity-scorer`

### When NOT to use this skill
- Reviewing an IR *plan's operational procedures* or playbooks (use `nist-800-61r3-lifecycle-reviewer` instead)
- Assessing incident response *capability maturity* across the PICERL lifecycle (use `nist-800-61r3-maturity-scorer`)
- Reviewing a tabletop exercise design (different skill)

### Pre-Flight Decision Tree

```
Is the document provided a policy/plan/procedure?
├─ No → Ask the user for the IR policy document before proceeding
└─ Yes
   │
   Is the document more than a paragraph long?
   ├─ No (stub/template placeholder only) → Flag as "Policy shell only — no reviewable content"
   └─ Yes
      │
      What is the organization type?
      ├─ Federal agency   → Check FISMA + OMB notification requirements (GV.OC-03)
      ├─ Healthcare       → Check HIPAA Breach Notification Rule timing
      ├─ Financial        → Check GLBA / NY DFS Part 500 / SEC Rule 10-D1
      ├─ Critical infra   → Check CISA CIRCIA 72-hour / 24-hour ransom payment rule
      └─ Private sector   → Check applicable state breach laws; skip FISMA
         │
         Does the org use MSSPs, CSPs, or ISPs?
         ├─ Yes → Element 8 (shared responsibility) is required, not optional
         └─ No  → Element 8 is N/A; note in report

Run all 8 element checks → Roles & Authorities deep check → Plan framework → Generate report
```

---

## Philosophy

A policy that cannot be picked up by a new hire on day one of an incident and followed without explanation is not a policy — it is a compliance artifact. Every gap in this checklist represents a decision that will be made ad hoc under pressure, with no documented authority backing it.

---

## Workflow

```
1. Pre-flight: confirm document + org type (decision tree above)
   ↓
2. Load references/policy-checklist.md
   ↓
3. Check all 8 Required Policy Elements (§2.3)
   ↓
4. Check Roles & Authorities deep check (GV.RR-02.R1, R2)
   ↓
5. Check Plan Framework (ID.IM-04 R1–R4)
   ↓
6. Check Regulatory/Notification requirements (GV.OC-03) — org-type dependent
   ↓
7. Generate Policy Review Report (format below)
```

Full element-by-element checklists, GV.RR-02 role checks, ID.IM-04 plan framework checks, and org-type regulatory tables are in:
`references/policy-checklist.md`

---

## Inputs

- The IR policy, IR plan, or procedures document (text or file path)
- Organization type (federal agency, private sector, healthcare, financial, MSSP) — determines regulatory notification requirements

---

## Output Format

```
=== NIST SP 800-61r3 IR Policy Review ===
Document: [policy name/version]
Organization type: [federal / private / healthcare / financial / MSSP]
Standard: NIST SP 800-61r3 §2.3 + CSF 2.0 GV/ID elements

━━━ SECTION 2.3 REQUIRED ELEMENTS CHECKLIST ━━━

[✓] Element 1 — Management Commitment
    Found: Executive VP signature, dated 2025-01-15; §1.1
    Note: Does not reference specific resource commitments (FTE, budget)

[✗] Element 4 — Definitions
    Missing: "Event" and "adverse event" are not defined.
    The policy uses "incident" broadly without distinguishing security events
    from confirmed cybersecurity incidents per FISMA 2014 definition.
    Required by: DE.AE-08, SP 800-61r3 Appendix B
    Fix: Add a definitions section with SP 800-61r3 Appendix B terms at minimum.

[~] Element 5 — Roles, Responsibilities, and Authorities
    Partial: Roles listed (IR Team, Legal, HR) but authority to disconnect
    systems is not designated to any specific role.
    Required by: GV.RR-02.R2
    Fix: Add explicit authority table specifying who can isolate/disconnect/
    shut down each asset class.

[✓] Element 6 — Prioritization Guidelines
    Found: Four-tier severity model (P1-P4) with response SLAs; §3.2
    Note: Recovery initiation criteria (RS.MA-05.R1) are absent.

[✗] Element 7 — Performance Measures
    Missing: No IR performance metrics defined anywhere in the document.
    Required by: ID.IM-01.R1
    Fix: Define at minimum: MTTD, MTTR, % incidents within SLA,
    % staff completing IR training annually.

━━━ ROLES & AUTHORITIES (GV.RR-02) ━━━
[✓] IR Team roles documented
[✓] Legal counsel role documented
[~] HR role referenced but not scoped for insider threat (RS.CO-03.R3)
[✗] Physical security role not mentioned
[✗] No named authority to invoke BCP/DRP during incident

━━━ PLAN FRAMEWORK (ID.IM-04) ━━━
[~] R1 — BCP alignment mentioned in passing, not formally linked (§1.4)
[✓] R2 — Annual review cycle defined (§6.1)
[✗] R3 — Document appears to be a generic template; lacks org-specific context
[~] R4 — "Resources as needed" language present but no specifics

━━━ REGULATORY/NOTIFICATION (GV.OC-03) ━━━
[~] Notification obligations referenced but no specific laws cited
[✗] No breach notification timelines defined

━━━ SUMMARY ━━━
Present:  4 / 8 required elements fully addressed
Partial:  2 / 8 elements partially addressed
Missing:  2 / 8 required elements absent

Critical gaps: Element 4 (definitions) and Element 7 (performance measures)
Policy assessment: Not ready for operational use without addressing critical gaps.
Estimated effort to remediate: LOW — most gaps are additions, not rewrites.
```

---

## NEVER

- **NEVER accept "implied" policy elements** — if an element is not explicit in the document, mark it Missing. "We do this" verbal assurance does not make a policy compliant; auditors and incident handlers both read the document, not the culture.

- **NEVER skip the authority designations check** — GV.RR-02.R2 is the single most commonly missed requirement in real-world policy reviews. Listing roles without designating authority is operationally equivalent to having no policy: the handler still can't act without making an unauthorized judgment call.

- **NEVER mark Element 4 (definitions) as Partial when terms are absent** — if "event" and "incident" are not explicitly defined, downstream classification, escalation, and notification decisions will all be inconsistent. There is no meaningful "partial" state for a definitions section that omits the primary terms.

- **NEVER recommend creating a separate document for each gap** — all 8 elements belong in the policy document itself. Suggesting a separate "definitions annex" or "roles addendum" is a maintenance antipattern: separate documents drift apart, and handlers only read the policy they were trained on.

- **NEVER skip the definitions check when a policy has a severity model** — organizations frequently define a four-tier severity model but never define what constitutes an "incident" vs. an "event." The severity model is then applied inconsistently: one analyst escalates a phishing email to P1; another logs it as a ticket.

- **NEVER flag Element 8 (shared responsibility) as N/A without asking** — organizations routinely forget that their HR system, email, or endpoint management is SaaS. If the org runs any cloud services, Element 8 likely applies. Ask explicitly before marking N/A.

- **NEVER confuse a policy review with a maturity assessment** — this skill checks whether required elements exist, not whether they work well. A policy can pass all 8 elements and still represent a low-maturity program. Direct maturity questions to `nist-800-61r3-maturity-scorer`.

---

## When Things Go Wrong

| Situation | What it usually means | Recommended action |
|-----------|----------------------|-------------------|
| Policy is a vendor template with the org's name substituted | ID.IM-04.R3 failure; likely also fails Elements 3, 6, 8 | Flag the entire document as "not tailored" before element-by-element review; estimate remediation effort as HIGH |
| Document is labeled "IR Plan" but contains policy-level content | Org conflated policy and plan — common in SMBs | Review the elements present regardless of label; note the structural issue in the report |
| Policy references "Appendix X for roles" but appendix is not provided | Cannot complete GV.RR-02 check | Note the missing appendix; mark Element 5 as Incomplete Submission, not Partial |
| Policy was last updated more than 3 years ago | ID.IM-04.R2 violation likely; technology/regulatory references will be stale | Flag the date; check if CIRCIA (effective 2024), GDPR, or current CSF 2.0 references are missing |
| Org claims MSSP handles all IR and refuses to provide MSSP contract | Element 8 cannot be verified; GV.SC-08 likely fails | Document the gap as Unverifiable; note that undocumented MSSP authority scope is itself a compliance risk |

---

## Deliverable

A checklist-based policy review report with element-by-element findings, direct SP 800-61r3 citations, and specific remediation guidance. Suitable for:
- IR policy audit findings
- Input to `nist-800-61r3-maturity-scorer`
- Policy revision task list
