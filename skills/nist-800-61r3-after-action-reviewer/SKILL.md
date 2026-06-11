---
name: nist-800-61r3-after-action-reviewer
description: "Evaluate post-incident reports, after-action reports (AARs), and lessons-learned documents against NIST SP 800-61r3's post-incident activity requirements — specifically RS.AN-03, RS.AN-06/07/08, RC.RP-06, and ID.IM-03. Checks root cause completeness, evidence integrity, magnitude validation, stakeholder communications, recovery verification, and whether lessons are actionable. Use when asked to 'review this after-action report', 'evaluate our lessons learned', 'post-incident review check', or 'does this AAR meet NIST requirements'."
user-invocable: true
---

# NIST SP 800-61r3 After-Action Reviewer

Evaluate post-incident reports, AARs, and lessons-learned documents against NIST SP 800-61r3 (April 2025) post-incident requirements.

---

## Mindset

1. **Proximate cause is never the root cause.** "User clicked a link" describes what happened. The root cause is always structural: the control that was absent, the process that failed, the architecture that permitted it. Treat any single-sentence root cause as incomplete by default.

2. **Lessons captured ≠ lessons actionable.** A 10-item lessons list with zero owners and zero deadlines is an observation log, not an improvement plan. Score actionability ruthlessly — it's the single best predictor of whether the program actually improves.

3. **Scope validation is not optional.** Unverified scope is the top cause of re-infection. If an AAR covers only the initially identified host without documenting adjacent-asset checks, treat this as a critical finding regardless of how thorough the rest of the document is.

4. **Silence on regulatory notification is non-compliant.** An AAR that doesn't mention regulatory notification assessment is not silent — it's missing a required element. The decision must be documented even when the answer is "not applicable."

5. **Document quality predicts program maturity.** An AAR that reads like a chronology but lacks systemic analysis, owner assignments, or cross-function improvement actions signals a team that responds to incidents but doesn't learn from them.

---

## Navigation

### When to use this skill
- User presents a completed or draft after-action report, post-incident report, or lessons-learned document for review
- User asks whether an AAR "meets NIST," "passes a compliance audit," or "is complete"
- User wants to improve an AAR before submitting to leadership, auditors, or regulators
- Checking output from `nist-800-61r3-incident-coordinator` or similar

### When NOT to use this skill
- User is conducting an active incident — use `nist-800-61r3-incident-coordinator` instead
- User wants general NIST 800-61r3 guidance without a specific document to review — provide framework overview directly
- Document is a tabletop exercise report (different standard; not a live-incident AAR)

### Pre-flight decision tree for incomplete documents

```
Is a document provided?
├── No → Ask: "Please share the AAR text or file path to review."
│
└── Yes → Is it clearly labeled as an AAR, post-incident report, or lessons-learned doc?
    ├── No → Confirm: "Is this a post-incident report for a [live/past] security incident?"
    │         If yes, proceed. If tabletop/drill, note different standard applies.
    │
    └── Yes → Does the document have at least a basic incident description + some lessons?
        ├── No (e.g., single paragraph stub) →
        │   State: "This document is too incomplete to score against RC.RP-06.
        │   Identifying what's missing: [list missing components A/B/C].
        │   Recommend completing these sections before formal review."
        │   Provide the Component A/B/C checklist from references/aar-completeness-checklist.md.
        │
        └── Yes → Proceed with full 6-step review workflow.
```

---

## Philosophy

An after-action report that chronicles what happened but fails to drive change is documentation theater. The standard of review is not "did they write it down" but "will reading this cause the program to be meaningfully different tomorrow."

---

## Workflow

```
1. RC.RP-06  — After-Action Report Completeness     [load: references/aar-completeness-checklist.md]
   ↓
2. RS.AN-03  — Root Cause Analysis Quality          [load: references/root-cause-evidence-checklist.md]
   ↓
3. RS.AN-06/07/08 — Evidence & Records Integrity    [load: references/root-cause-evidence-checklist.md]
   ↓
4. RS.CO-02/03 — Communication Retrospective        [load: references/comms-recovery-lessons-checklist.md]
   ↓
5. RC.RP-04/05 — Recovery Verification              [load: references/comms-recovery-lessons-checklist.md]
   ↓
6. ID.IM-03  — Lessons-Learned Loop Closure         [load: references/comms-recovery-lessons-checklist.md]
   ↓
7. Generate AAR Review Report (output format below)
```

Load the referenced checklist file for each step group. Do not reproduce checklist items inline — use the reference files to drive analysis, then report findings in the output format.

---

## Inputs

- The after-action report, post-incident report, or lessons-learned document (text or file path)
- Incident type (data breach, ransomware, account takeover, DoS, insider, etc.) — affects scope
- Was this a major incident? (affects whether senior leadership update requirements apply under RS.CO-03.R2)

---

## Output Format

```
=== NIST SP 800-61r3 After-Action Review ===
Document: [AAR name/incident reference]
Incident type: [ransomware / data breach / etc.]
Severity: [major / significant / minor]
Standard: NIST SP 800-61r3 (April 2025)

━━━ RC.RP-06 — AFTER-ACTION REPORT COMPLETENESS ━━━

Component A — Incident Documentation
[✓] Incident type and classification: Present (§1)
[✓] Detection method and timestamp: Present (§2.1 — DE alert at 14:23 UTC)
[~] Event timeline: Partial — gaps between 16:00–19:00 UTC unexplained
[✗] Threat actor characterization: Missing — vector identified but no TTP analysis
Gap: RC.RP-06.R1 requires documenting the incident itself; threat actor info
needed for ID.IM-03 improvement loop.

Component B — Response and Recovery Actions
[✓] Triage and validation: Present (§3)
[✓] Containment measures: Present (§4.1)
[✗] Recovery steps: Missing — report notes systems restored but no sequence
documented. RC.RP-04.R1 requires restoration order validation.

Component C — Lessons Learned
[~] What worked: Present (§7)
[✗] Actionable improvements: 3 lessons identified, 0 have assigned owners or
deadlines. ID.IM-03 requires SMART improvement actions.

━━━ RS.AN-03 — ROOT CAUSE ANALYSIS ━━━

[✓] R1 — Event sequence: Complete timeline from initial access to containment
[~] R2 — Vulnerability identification: Phishing vector identified; no analysis
of why MFA bypass was possible or why phishing bypassed email filtering
[✗] R3 — Systemic root cause: "Employee clicked phishing link" = proximate cause.
No 5-Whys or structural analysis. Missing: why MFA not enforced, why email
filtering failed this variant, whether this reflects a pattern.
[N/A] R4 — No deception technology deployed per §1.3

━━━ RS.AN-06/07/08 — EVIDENCE & RECORDS ━━━
[✓] RS.AN-06.R1 — IR records access control referenced (§6.2)
[~] RS.AN-07.R1 — Evidence collected but no retention timeline documented
[✗] RS.AN-08.R1 — Scope validation missing: no evidence adjacent systems
were checked for lateral movement or IoC presence

━━━ RS.CO COMMUNICATIONS RETROSPECTIVE ━━━
[✓] Internal notifications made with timestamps (§5.1)
[~] RS.CO-02.R3 — Regulatory notification: HIPAA applicability not assessed;
decision not documented (silence = non-compliant)
[✓] RS.CO-03.R2 — Senior leadership received 3 updates during incident

━━━ RC.RP RECOVERY VERIFICATION ━━━
[~] RC.RP-04.R2 — System owner confirmations: verbal only, not documented
[✗] RC.RP-05.R1 — No pre-production IoC scan of restored systems documented

━━━ ID.IM-03 — LESSONS LEARNED LOOP ━━━
Lessons identified: 3
Lessons with owner + deadline: 0
Actionability score: 0% — all lessons are observations, none are assigned actions
Program improvement scope: No lessons target IR plan/policy changes (all technical)

━━━ SUMMARY ━━━
Critical gaps: RS.AN-03.R3 (systemic root cause), RC.RP-05.R1 (IoC scan),
              ID.IM-03 actionability (0% — no assigned owners or deadlines)
Significant gaps: RS.AN-08.R1 (scope validation), RC.RP-04.R2 (owner sign-off),
                 RS.CO-02.R3 (regulatory decision not documented)
Assessment: AAR captures what happened but will not improve the IR program.
The absence of systemic root cause analysis means the same incident is likely
to recur. The 0% actionability on lessons means no improvements will be tracked.
```

---

## NEVER

- **NEVER accept proximate cause as root cause** — "User clicked a link" is a behavior, not a cause. The standard requires systemic analysis (RS.AN-03.R3). Every proximate cause has at least 3–5 structural causes behind it; accepting the proximate answer lets all of them go unfixed.

- **NEVER mark lessons learned as sufficient without owner + deadline** — Unassigned lessons are observations that will never be acted on. An ID.IM-03 finding without a named human and a date is indistinguishable from not having the finding at all.

- **NEVER skip the scope validation check (RS.AN-08.R1)** — Failure to validate scope is the leading cause of re-infection on adjacent systems. Teams that validate only the initially identified host consistently experience follow-on incidents within 90 days.

- **NEVER treat regulatory notification silence as compliant** — RS.CO-02.R3 requires the decision to be documented, not just the action. An AAR that doesn't mention regulatory notification at all fails this requirement even if notification was correctly determined to be unnecessary.

- **NEVER accept verbal sign-offs as documentation** — RC.RP-04.R2 requires system owner confirmation of restoration. Verbal confirmation that was not recorded is legally and procedurally equivalent to no confirmation. Flag as a gap regardless of whether recovery was successful.

- **NEVER omit N/A documentation for deception technology (RS.AN-03.R4)** — Teams without honeypots or deception tokens still must document the absence explicitly. A blank field is ambiguous; an explicit "N/A — no deception technology deployed" is compliant.

- **NEVER score ID.IM-03 on meeting held alone** — The standard requires both a meeting AND actionable follow-up. Teams that hold thorough lessons-learned meetings but don't assign owners have satisfied the meeting requirement and violated the improvement requirement. Score both independently.

- **NEVER let technical-only improvements satisfy ID.IM-03.N2** — The standard explicitly requires that improvements can target the IR program itself (plan, policy, procedures) or other cybersecurity risk management areas. An AAR where every improvement is a patch or a tool purchase and none target process/program changes is non-compliant with the intent of ID.IM-03.

- **NEVER mark evidence handling complete without retention timeline** — RS.AN-07.R1 requires not just collection but retention policy compliance. Evidence collected without documented retention timelines may be improperly destroyed before litigation hold periods expire or preserved past required deletion dates.

- **NEVER skip the communications retrospective for minor incidents** — RS.CO-02.R2 notification requirements apply regardless of severity. Minor incidents still require documented internal notifications. The difference for major incidents is the addition of senior leadership updates (RS.CO-03.R2), not the elimination of other requirements.

---

## When Things Go Wrong

| Situation | Response |
|-----------|----------|
| AAR contains root cause analysis but it's a single paragraph with no method cited | Flag RS.AN-03.R3 as partial. Note analysis method is required (5-Whys, fishbone, fault tree). Ask whether a structured analysis was performed verbally and not documented — if so, that also fails the standard since it requires analysis to be in the record. |
| Lessons list is long (10+) but no owners or deadlines | Score actionability at 0% regardless of lesson count. A long observation list with no assignments is worse than a short actionable list — it creates false confidence that the team is learning. |
| Document is clearly a draft — author says "owners TBD" | Review for structural completeness but note that the actionability score cannot be assessed until owners and deadlines are assigned. Provide the SMART criteria from references/comms-recovery-lessons-checklist.md as a template. |
| Incident involved a vendor/third party and the AAR only covers the organization's response | Flag scope gap under RS.AN-08.R1: third-party incident scope validation is required. The AAR should document what visibility the organization had into the vendor environment and what compensating controls or contractual remedies apply. |
| Document is actually a tabletop/exercise after-action, not a live incident AAR | Note that NIST SP 800-61r3 applies to live incidents. Tabletop AARs are governed by exercise program standards (e.g., HSEEP). Offer to evaluate against tabletop AAR best practices instead, but do not apply live-incident scoring. |
| Regulatory notification section says "N/A" with no rationale | Flag as non-compliant — RS.CO-02.R3 requires the rationale for N/A determinations. Which regulation was considered? What criteria determined it didn't apply? Document the analysis, not just the conclusion. |

---

## Deliverable

A section-by-section AAR review with citation-anchored findings, a lessons-actionability score, and specific improvement recommendations. Suitable for:
- IR program quality assurance
- Compliance audit support
- AAR revision guidance
- Input to `nist-800-61r3-maturity-scorer`
