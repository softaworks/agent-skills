---
name: nist-800-61r3-recommendation-auditor
description: "Audit whether a cybersecurity document satisfies the R-tagged (Recommendation) items from NIST SP 800-61r3's CSF 2.0 Community Profile (April 2025). R-items are the highest-obligation findings — 'should do' requirements. Outputs Met/Partial/Not Met per R-item with direct quotes. Use when asked to 'check all the recommendations', 'audit R items', 'what recommendations aren't met', 'NIST 800-61 compliance check', or 'SP 800-61r3 gap analysis'."
user-invocable: true
---

# NIST SP 800-61r3 Recommendation Auditor

Audit whether a document satisfies the R-tagged recommendations from NIST SP 800-61r3's CSF 2.0 Community Profile (April 2025). The full 89-item R-item catalog is in `references/r-item-catalog.md` — load it before beginning any audit.

---

## Mindset

Expert auditors apply these heuristics before touching a single R-item:

1. **Burden of proof is on the document, not the auditor.** If the document doesn't explicitly state a requirement is addressed, it is Not Met. Assume absence of evidence is evidence of absence — don't infer from organizational context.

2. **Partial beats Not Met only when sub-requirements are enumerable.** An R-item like `RS.MA-02.R1` requires *both* severity AND urgency. If the document has one but not the other, that's Partial. If it has neither, it's Not Met. Don't split Partials on vague grounds.

3. **Scope discipline prevents false negatives.** An IR Plan must satisfy all Table 3 R-items — not just the ones obviously addressed. Unsatisfied R-items that aren't in scope for the document type are N/A, not Not Met. Document-type scope is in `references/r-item-catalog.md`.

4. **Sequence matters: detect → triage → contain → analyze → communicate → recover.** R-items are structured along this kill-chain-aligned lifecycle. Gaps in early-phase items (DE.AE, RS.MA) cascade — an organization that can't declare an incident (DE.AE-08.R1) can't satisfy any RS.MA item correctly.

5. **Cross-reference for coherence gaps.** If a document claims RS.CO-02.R2 is met ("we follow established reporting procedures") but those procedures aren't named or referenced, flag as Partial — citing a phantom document is not evidence.

---

## Navigation

**Use this skill when:**
- A user provides an IR plan, playbook, incident report, after-action report, or policy document and asks for gap analysis against NIST SP 800-61r3
- The user explicitly mentions "R-items", "SP 800-61r3 recommendations", "CSF 2.0 Community Profile", or "audit"
- Feeding results into `nist-800-61r3-maturity-scorer`

**Do NOT use this skill when:**
- The document is pre-2025 and references NIST SP 800-61 Rev. 2 only — the R/C/N annotation system did not exist in Rev. 2; use a different mapping
- The user wants NIST CSF 2.0 *Core* compliance (not 800-61r3 Community Profile) — different catalog
- The document is a vendor product brochure — R-items apply to *organizational* processes, not tool capabilities

**Scope decision tree:**

```
Is scope specified? ──Yes──► Use specified CSF Functions
       │
       No
       │
What document type?
  IR Plan          ──► All Table 3 + Table 2 governance items
  Playbook         ──► RS.MA + RS.AN + RS.MI + RC.RP + DE.AE-08.R1
  Incident Report  ──► RS.MA-02-05 + RS.AN-03/06/07/08 + RS.CO-02/03 + RC.RP-06
  After-Action     ──► RS.AN-03 + RC.RP-06.R1 + RS.AN-06.R1 + RS.AN-07.R1
  IR Policy        ──► GV.PO.R1 + GV.RR-02 + ID.IM-04 + GV.OC-03.R1
  Unknown          ──► Ask user to clarify; default to Table 3 full scope
```

---

## Philosophy

The auditor's single function is to determine whether written, documented evidence satisfies each NIST recommendation — not whether the organization *probably* does the right thing. A well-intentioned organization with no written artifact scores Not Met, because the R-item requires the practice to be expressible, communicable, and auditable.

---

## Workflow

**Before auditing: load the catalog**

Read `references/r-item-catalog.md` to get the full 89-item R-item list and the document-type scope map. Do not rely on memory for R-item text — always quote from the catalog verbatim.

```
1. Load R-item Catalog (references/r-item-catalog.md)
   ↓
2. Classify Document & Set Scope (scope map in catalog)
   ↓
3. Audit Each In-Scope R-item (Met / Partial / Not Met / N/A)
   ↓
4. Score Results (formula in catalog)
   ↓
5. Generate Audit Report (format below)
```

### Auditing Each R-item

For each in-scope R-item:
1. Search document for direct evidence satisfying the requirement
2. Assign status:
   - **Met** — document clearly satisfies all sub-requirements; quote the supporting text
   - **Partial** — document addresses the concept but misses named sub-requirements; specify the gap
   - **Not Met** — no evidence found
   - **N/A** — not applicable to this document type per scope map

---

## Output Format

```
=== NIST SP 800-61r3 Recommendation Audit ===
Document: [name/type]
Scope: [Full / Table 3 / targeted function]
R-items audited: [N]

━━━ NOT MET — High Priority (Table 3) ━━━

[✗] DE.AE-08.R1 — Incident Declaration Criteria
    Requirement: "Apply incident criteria to known and assumed characteristics
    of analyzed activity, and consider known false positives to determine
    whether an incident should be declared."
    Finding: No incident declaration criteria or thresholds defined.
    Severity: Critical — incidents may be declared inconsistently or too late.

━━━ PARTIAL — High Priority (Table 3) ━━━

[~] RS.MA-02.R1 — Triage and Validation
    Requirement: "Perform preliminary review... estimate severity AND urgency."
    Finding: Severity tiers (P1–P4) defined but no urgency/SLA criteria present.
    Gap: Add time-to-respond criteria alongside severity classification.

━━━ MET — High Priority (Table 3) ━━━

[✓] RS.MI-01.R1 — Manual Containment Selection
    Evidence: §5.2 "Incident handlers may override automated containment."

━━━ MEDIUM PRIORITY (Table 2) ━━━
[✗] GV.PO.R1 — IR policy not referenced in document
[✓] ID.IM-04.R2 — Review cycle stated as annual in §1.3

━━━ SCORECARD ━━━
High-priority R-items:   Met: 14  Partial: 6  Not Met: 8  (Total: 28)
Medium-priority R-items: Met: 8   Partial: 3  Not Met: 7  (Total: 18)
High compliance: 57%  |  Weighted composite: 53%

Top 3 highest-impact Not Met items:
1. DE.AE-08.R1 — Incident declaration criteria (blocks all RS.MA)
2. RS.CO-02.R3 — Regulatory notification compliance (legal exposure)
3. RC.RP-06.R1 — After-action report requirement (no lessons-learned loop)
```

---

## NEVER

- **NEVER mark an R-item Met without a direct quote from the document** — inference, organizational reputation, or "they probably do this" does not count; a reviewer must be able to turn to the page and see it
- **NEVER conflate C-items (should consider) with R-items (should do)** — they have different obligation weights; mixing them inflates compliance scores and masks real gaps; if both apply to an element, surface the R-item first
- **NEVER omit verbatim R-item text from SP 800-61r3 in any Not Met or Partial finding** — without the exact requirement, remediation authors can't write to the standard; the finding becomes unactionable
- **NEVER assess a document at a scope broader than its stated purpose** — an incident playbook is Not Applicable for GV.PO.R1 (IR Policy), not Not Met; marking it Not Met creates false negatives that distort program-level scoring
- **NEVER skip RS.MA.R1 (risk-based prioritization) when RS.MA-03.R2 or RS.MA-03.R3 appears met** — organizations frequently document categorization criteria but fail to document the risk *weighting* mechanism; these are different requirements
- **NEVER accept a reference to an external document as Met without verifying the external document was provided** — "see our SOP-IR-001" is Partial at best; the R-item is met only if the SOP is in scope and its content is evidenced
- **NEVER conflate RC.RP-05.R1 (pre-production IoC check) with RS.AN-08.R1 (ongoing persistence check)** — similar language, different lifecycle stage; conflating them produces duplicate Mets and hidden Not Mets

---

## When Things Go Wrong

| Situation | Diagnosis | Response |
|-----------|-----------|----------|
| Document is >100 pages (large IR program, full policy suite) | Full audit will be noisy; analyst loses thread | Ask user which CSF Function or Table to prioritize; audit one section at a time and aggregate |
| Document is ambiguous — could be an IR plan or a playbook | Scope map produces different R-item sets; wrong call invalidates the audit | Ask: "Is this a program-level plan or a procedural runbook?" before setting scope |
| R-item text partially satisfied by two different sections | Both sections are fragmented; individually each is Partial | Mark Partial, quote both sections, note that combined they approach Met but neither section is independently complete |
| User says "just give me a quick pass, skip the details" | Temptation to skip Not Met reasoning | Still assign Met/Partial/Not Met for every in-scope item; compress the rationale to one line, but do not omit the status |
| Document uses different terminology (e.g., "severity matrix" vs. NIST's "risk evaluation factors") | Terminology mismatch may mask genuine compliance | Map the term, quote it, mark Met or Partial based on whether the *content* satisfies the requirement — terminology difference alone is not a finding |
| Only a summary or excerpt is provided (not the full document) | Scope is necessarily incomplete | State clearly in the report header: "Audit based on excerpt — findings reflect visible content only; full document may satisfy additional R-items" |

---

## Deliverable

A citation-anchored audit report with Met/Partial/Not Met assessments for all in-scope R-items, suitable for:
- Direct input to `nist-800-61r3-maturity-scorer`
- Audit findings for compliance documentation
- IR program improvement backlog items

---

## Reference Files

| File | Purpose | Load When |
|------|---------|-----------|
| `references/r-item-catalog.md` | Complete 89-item R-item catalog with scope maps and scoring formula | Always — load before step 1 |

## Cross-Framework Delta Table (NIST CSF ↔ ISO 27001 ↔ SOC 2 Type II ↔ PCI-DSS)

Use this table when a client deliverable must map IR findings to multiple compliance frameworks simultaneously.

| NIST CSF Function | NIST 800-61r3 Phase | ISO 27001:2022 Control | SOC 2 Type II CC | PCI-DSS v4.0 Req |
|-------------------|--------------------|-----------------------|-----------------|-----------------|
| Identify (ID.RA) | Preparation | A.8.8 Vulnerability mgmt | CC3.2 Risk assessment | 6.3 Security vulnerabilities |
| Protect (PR.AT) | Preparation | A.6.3 Security awareness | CC1.4 Competence | 12.6 Security awareness |
| Detect (DE.AE) | Detection & Analysis | A.8.16 Monitoring | CC7.1 Threat detection | 10.7 Failure detection |
| Detect (DE.CM) | Detection & Analysis | A.8.15 Logging | CC7.2 Anomaly evaluation | 10.3 Log integrity |
| Respond (RS.RP) | Containment | A.5.26 IR planning | CC7.3 Response evaluation | 12.10.1 IR plan |
| Respond (RS.CO) | Eradication | A.5.29 Continuity IR | CC7.4 Incident response | 12.10.3 IR response |
| Respond (RS.AN) | Post-incident | A.5.28 Evidence collection | CC4.1 Monitoring activities | 12.10.4 Training |
| Recover (RC.RP) | Recovery | A.5.30 ICT readiness | CC7.5 Recovery | 12.10.5 Recovery alerts |
| Recover (RC.IM) | Post-incident | A.5.27 Lessons learned | CC4.2 Deficiency eval | 12.10.6 Process evolution |

### Breach Notification Deadlines by Framework

| Framework | Notification Deadline | Notify Whom | Trigger |
|-----------|----------------------|-------------|---------|
| GDPR Art. 33 | 72 hours | Supervisory Authority | Personal data breach |
| GDPR Art. 34 | Without undue delay | Affected individuals | High-risk to rights |
| HIPAA Breach Rule | 60 days (from discovery) | HHS + affected individuals | Unsecured PHI breach |
| HIPAA (>500 affected) | 60 days | HHS + media in affected state | Same |
| PCI-DSS v4.0 Req 12.10.2 | Immediately | Card brands + acquirer | Suspected or confirmed compromise |
| NY SHIELD / CCPA | 30–45 days (varies by state) | State AG + affected residents | Personal information breach |
| SEC (public companies) | 4 business days | SEC Form 8-K | Material cybersecurity incident |

### IR Maturity Mapping — Framework Equivalence

| Maturity Level | NIST CSF Tier | ISO 27001 Conformance | SOC 2 Opinion | PCI-DSS Compliance Level |
|---------------|--------------|----------------------|---------------|------------------------|
| 1 — Initial | Tier 1 (Partial) | Non-conformant | Qualified / Adverse | Non-compliant |
| 2 — Developing | Tier 2 (Risk-informed) | Partially conformant | Qualified | Compensating controls |
| 3 — Defined | Tier 3 (Repeatable) | Conformant | Unqualified | Compliant |
| 4 — Managed | Tier 4 (Adaptive) | Conformant + continual improvement | Clean + SOC 2+ | Compliant + validated |
