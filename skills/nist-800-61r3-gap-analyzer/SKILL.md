---
name: nist-800-61r3-gap-analyzer
description: "Identify and prioritize gaps in any cybersecurity document against the NIST SP 800-61r3 CSF 2.0 Community Profile. Accepts raw document content or a coverage map from nist-800-61r3-csf-mapper and outputs a priority-ranked gap list (High/Medium/Low) with specific SP 800-61r3 citation anchors. Use when asked to 'find gaps in this IR plan', 'what's missing from this playbook', or 'gap analysis against 800-61r3'. Trigger keywords: gap analysis, missing coverage, IR plan review, NIST compliance gaps, 800-61r3 gaps."
user-invocable: true
---

# NIST SP 800-61r3 Gap Analyzer

Identify and prioritize gaps in any cybersecurity document against the CSF 2.0 Community Profile defined in NIST SP 800-61r3 (April 2025).

---

## Mindset

Expert gap analysts do not mechanically check boxes — they reason about *consequence chains* and *operational reality*:

1. **Think in dependency chains, not isolated elements.** A gap in DE.AE-08 (incident declaration) is not just one missing item — it propagates as implied failure risk to RS.MA-01 through RS.MA-04. Always trace upstream: one missing foundational element can account for three or four apparent gaps. Identify the root gap, note the implied gaps, and remediate the root first.

2. **Score presence by operational evidence, not prose claims.** A policy that says "we monitor our networks" does not satisfy DE.CM-01 — it must describe *what* is monitored, *how*, and at what frequency. Treat unsupported assertions as Partial at best. The question is not "does this mention monitoring?" but "can a new analyst execute this tomorrow with only this document?"

3. **Prioritize remediation by unblocking downstream, not by severity label alone.** When two gaps both score Critical, order the one that unblocks more downstream elements first. A triage procedure (RS.MA-02) unblocks categorization (RS.MA-03), escalation (RS.MA-04), and every downstream analysis step — it ranks above RS.AN-06 even if both are Critical.

4. **Treat "Partial" as a signal, not a conclusion.** When something is Partial, ask: what specifically is present and what is absent? A good gap entry for a Partial element surfaces the specific sub-requirement (R/C/N item) that is missing, not a generic "needs improvement" note. This transforms the output from an audit finding into an actionable work item.

5. **Match remediation specificity to document type.** A tactical runbook gap gets a concrete, one-step remediation ("add urgency SLA table"). A program-level policy gap gets a structural fix ("create a formal supplier IR coordination annex"). Never suggest an enterprise framework overhaul for a single playbook's gap.

---

## Navigation

**Use this skill when:**
- Performing a gap analysis of an IR plan, playbook, runbook, or cybersecurity policy
- Reviewing an output from `nist-800-61r3-csf-mapper` and need prioritized action items
- An auditor or customer asks what the document is missing against 800-61r3
- Building a program improvement backlog from a compliance baseline

**Do NOT use this skill when:**
- The goal is to *map* what the document covers (use `nist-800-61r3-csf-mapper` first)
- The goal is to score overall maturity (use `nist-800-61r3-maturity-scorer` after gap analysis)
- The document is scoped to a single technology or tool — narrow scope means many Table 3 elements structurally cannot apply; note them as Out of Scope rather than gaps

**Document type decision tree:**

```
What kind of document is being analyzed?
│
├── Full IR Program / Policy
│     → Analyze ALL three priority tiers (High + Medium + Low)
│     → Expect 15-30+ gaps; group by functional area
│
├── Incident Playbook / Runbook (threat-specific or scenario-specific)
│     → Focus on HIGH priority (Table 3) only
│     → Many GV/ID/PR elements are Out of Scope — note, don't flag
│     → Typical output: 3-10 gaps
│
├── Subset / Annex / Supporting Procedure
│     → Identify the parent document scope first
│     → Flag gaps relative to what THIS document is responsible for
│     → Note: "element owned by parent document" ≠ gap
│
└── Unknown / Composite
      → Ask user for scope clarification before classifying gaps
      → If unavailable, default to playbook-tier analysis and note assumption
```

**Edge case: the document explicitly disclaims scope**

If the document says "this playbook covers detection and containment only," then RC.RP-* elements are Out of Scope. Still note them as "not covered by this document — verify in parent program," but do not classify them as gaps for severity scoring.

---

## Philosophy

A gap analysis is a *consequence map*, not a compliance checklist. Every finding must answer: if this gap is never fixed, what breaks during an actual incident? Findings that cannot answer that question are noise, not signal.

---

## Workflow

```
1. Obtain Coverage Map (run mapper if not already done)
   ↓
2. Load SP 800-61r3 Element Baseline (../nist-800-61r3-shared/references/csf-element-registry.md)
   ↓
3. Identify Gaps — check each element, classify Missing vs. Partial
   ↓
4. Classify & Prioritize — apply severity and dependency-chain reasoning
   ↓
5. Generate Gap Report
```

### Step 1: Obtain Coverage Map

If a coverage map exists from `nist-800-61r3-csf-mapper`, use it directly. Otherwise, perform inline mapping against the document before gap analysis.

### Step 2: Load Element Baseline

Load `../nist-800-61r3-shared/references/csf-element-registry.md` for the full element set, severity mapping, and dependency graph. Do not embed the full table inline in your response — reference it by CSF ID.

### Step 3: Identify Gaps

For each element in the baseline (scoped to document type per Navigation):
- `Not Found` → Gap (Missing)
- `Partial` → Gap (Incomplete) — identify the specific absent sub-requirement
- `Addressed` → No gap
- `Out of Scope` → Note but do not count in severity totals

### Step 4: Classify & Prioritize

Assign severity using the Severity Mapping in `../nist-800-61r3-shared/references/csf-element-registry.md`.

Apply the dependency-chain rule: when remediating Critical gaps, sequence the one
that unblocks the most downstream elements first (see dependency graph in reference).

### Step 5: Generate Gap Report

---

## Output Format

```
=== NIST SP 800-61r3 Gap Analysis Report ===
Document: [name/type]
Standard: NIST SP 800-61r3 (April 2025)
Analysis date: [date]
Scope tier: [Full Program | Playbook/Runbook | Subset | Unknown]

━━━ CRITICAL GAPS (High Priority — Table 3) ━━━

[C1] DE.AE-08 — Incident Declaration Criteria
     Status: Missing
     Requirement: "Apply incident criteria to known and assumed characteristics
     of analyzed activity, and consider known false positives to determine
     whether an incident should be declared." (DE.AE-08.R1)
     Impact: Without defined declaration criteria, incident response may start
     too late or on false positives — undermining RS.MA-02 triage.
     Downstream risk: RS.MA-01 through RS.MA-04 all depend on a declared incident.
     Remediation: Define specific observable thresholds (e.g., confirmed C2
     beacon, lateral movement detected, data staged for exfil) that constitute
     an incident declaration trigger.

[C2] RS.MA-02 — Incident Triage and Validation
     Status: Partial (severity categories present, no urgency criteria)
     Requirement: "Perform a preliminary review of a new incident report to
     verify that a cybersecurity incident has occurred, then estimate the
     severity and urgency needed to respond to it." (RS.MA-02.R1)
     Missing sub-requirement: Urgency/SLA criteria absent; only severity tiers present.
     Impact: Teams cannot determine response SLAs — P1/P2/P3 differentiation impossible.
     Remediation: Add urgency criteria alongside severity (e.g., P1 = respond
     within 1hr, P2 = 4hr, P3 = 24hr).

...

━━━ SIGNIFICANT GAPS (High Priority) ━━━

[S1] RS.CO-02 — Stakeholder Notification
     ...

━━━ MEDIUM PRIORITY GAPS (Table 2) ━━━

[M1] ID.IM-04 — IR Plans Maintained and Improved
     ...

━━━ OUT OF SCOPE (noted, not scored) ━━━

RC.CO-04 — Public updates: document scope excludes public communications.

━━━ SUMMARY ━━━

Critical gaps:    3  (must address before next incident)
Significant gaps: 5  (address within 30 days)
Minor gaps:       4  (address in next program review cycle)
Medium gaps:      6
Low gaps:         2  (if full program scope)
Out of scope:     3

Highest-impact single fix: Adding DE.AE-08 incident declaration criteria would
immediately resolve implied gaps in RS.MA-01 through RS.MA-04 (5 items, one fix).
```

---

## NEVER

- **NEVER mark a gap as Critical unless it is in Table 3 AND directly impacts incident handling** — Critical inflation devalues the finding; a stakeholder who sees 20 Critical items stops prioritizing any of them. Reserve Critical for elements that *gate* other elements.
- **NEVER suggest remediation that adds bureaucracy** — "implement a governance committee to oversee..." is compliance theater. Remediation must be executable by a practitioner, not a PMO. Write the specific artifact or procedure they need to create.
- **NEVER conflate Missing with Partial** — partial coverage is operational progress and should be acknowledged. A "Partial" gap entry must name what *is* present, then what specific sub-requirement is absent. Collapsing both to "gap" erases useful signal.
- **NEVER omit citation anchors** — every finding must cite the specific CSF ID and R/C/N item from SP 800-61r3. An uncited finding cannot be traced to the standard and fails audit defensibility.
- **NEVER flag elements as gaps when they are explicitly out of scope for the document type** — a threat-specific playbook is not responsible for GV.PO (organizational policy). Mark Out of Scope and explain why; inflating scope inflates the gap count and undermines trust in the analysis.
- **NEVER skip the dependency-chain analysis for Critical gaps** — listing Critical gaps in arbitrary order misguides remediation sequencing. Always identify which fix unblocks the most downstream elements and say so explicitly.
- **NEVER treat an assertion in prose as operational evidence** — "We perform continuous monitoring" does not satisfy DE.CM unless the document describes what is monitored, by what mechanism, and at what cadence. Challenge unsupported prose claims.

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|-------------|----------|
| Gap count is suspiciously high (30+ Critical gaps in a short runbook) | Scope was not narrowed for document type — Table 2/3 applied wholesale to a narrow tactical doc | Re-run with Playbook/Runbook scope; reclassify GV/ID/PR elements as Out of Scope |
| Mapper output marks elements Addressed but analyst suspects false positives | Mapper may have matched on keyword proximity, not operational depth | Re-verify Addressed elements using the "operational evidence" test: can a new analyst execute this from the document alone? Downgrade to Partial if not. |
| User disputes a Critical finding — "we handle this informally" | Informal practices are not documentable evidence; they disappear when staff turns over | Note the informal practice in the finding; remediation is to document the informal process, not build a new one from scratch |
| Two Critical gaps rank equally — user wants one to fix first | Dependency chain not yet applied | Check `../nist-800-61r3-shared/references/csf-element-registry.md` dependency graph; the upstream element in the chain goes first |

---

## Reference Loading Guide

| Situation | Load |
|-----------|------|
| Performing gap analysis (always) | `../nist-800-61r3-shared/references/csf-element-registry.md` — full element set, severity mapping, dependency graph |
| Scope is uncertain | Re-read Navigation decision tree above before loading baseline |
| Dependency sequencing question | See "Element Dependency Graph" section in `../nist-800-61r3-shared/references/csf-element-registry.md` |

---

## Deliverable

A prioritized, citation-anchored gap report suitable for:
- Direct input to `nist-800-61r3-maturity-scorer`
- Action items for IR program improvement backlog
- Audit findings documentation
