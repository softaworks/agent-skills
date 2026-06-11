---
name: nist-800-61r3-csf-mapper
description: "Map any cybersecurity document (IR plan, playbook, incident report, after-action report, IR policy, risk assessment) to NIST SP 800-61r3 CSF 2.0 elements. Produces a structured coverage table with Addressed/Partial/Not Found status and gap summary. Trigger phrases: 'map this to NIST', 'what CSF elements does this cover', 'tag this against 800-61r3', 'CSF 2.0 coverage', 'map to SP 800-61r3'."
user-invocable: true
---

# NIST SP 800-61r3 CSF Mapper

Map any cybersecurity document to the CSF 2.0 Community Profile defined in NIST SP 800-61r3 (April 2025).

---

## Mindset

1. **Document type determines expected scope — not the other way around.** An IR Plan that only covers RS elements is incomplete. A playbook that covers GV elements is bonus, not expected. Calibrate what "good coverage" means per type before scoring anything.

2. **Partial is harder to call than Addressed or Not Found.** Partial means the document touches the element but leaves a practitioner-actionable gap — missing a threshold, missing a named role, missing a frequency. Vague language that merely mentions a concept is Not Found, not Partial.

3. **Table 3 (DE/RS/RC) is always in scope; Table 2 (GV/ID/PR) is conditional.** For a single-incident playbook, mapping all 40+ Table 2 elements is noise. For an IR Program policy review, Table 2 is the primary deliverable. Know which table is load-bearing for the request.

4. **Subcategory ≠ Category.** Marking DE.CM as Addressed because the document mentions monitoring does not satisfy DE.CM-01, DE.CM-03, DE.CM-06, or DE.CM-09 individually. Always distinguish category-level coverage from subcategory-level evidence.

5. **Inference creep is the primary failure mode.** The worst mapping errors come from reading intent ("they probably have monitoring because they mention SOC") into coverage status. Only text that is explicitly present earns a status other than Not Found.

---

## Navigation

**Use this skill when**:
- Asked to "map this to NIST", "tag against 800-61r3", "what CSF elements does this cover"
- Producing a gap input for `nist-800-61r3-gap-analyzer` or a score input for `nist-800-61r3-maturity-scorer`
- Auditing whether an IR plan, playbook, policy, or report meets CSF 2.0 Community Profile expectations

**Do NOT use this skill when**:
- The request references SP 800-61r2 phases (Preparation / Detection & Analysis / etc.) — redirect to r3
- The user wants gap prioritization or remediation — hand off to `nist-800-61r3-gap-analyzer`
- The document is a vendor product datasheet — CSF mapping requires organizational process content

**Ambiguous input decision tree**:
```
Document provided?
├── Yes → Classify type (see ../nist-800-61r3-shared/references/csf-element-registry.md §Document Type table)
│         → Determine Table 3 vs Table 2 scope
│         → Map and output
└── No  → Ask: "Paste the document text, provide a file path, or describe what the document contains."

Document type unclear?
├── Has phases/steps/timeline → likely Playbook or Incident Report
├── Has policy language/shall/must → likely IR Policy or IR Plan
├── Has findings/recommendations/timeline of events → likely After-Action Report
└── Has risk scores/asset lists → likely Risk Assessment
```

---

## Philosophy

Every element earns its status from explicit document text — not from what the document implies, what the organization probably does, or what a reasonable reader would assume. The coverage table is forensic evidence of what is written, not an assessment of what is practiced.

---

## NEVER

- **NEVER mark Addressed based on category-level language alone** — "we monitor our environment" satisfies DE.AE at most; it does not satisfy DE.CM-01/03/06/09 individually. Each subcategory requires subcategory-level evidence.

- **NEVER use SP 800-61r2 element IDs** — r2 used phase names (Preparation, Detection & Analysis, Containment, Eradication, Recovery, Post-Incident). r3 uses CSF 2.0 Function/Category/Subcategory IDs. Mixing them produces an unmappable output.

- **NEVER skip Table 3 for any document type** — even an IR policy must be checked against Table 3 to confirm it references execution elements. A policy with no DE/RS/RC language is a policy gap, not a scope limitation.

- **NEVER inflate Partial to avoid showing gaps** — gaps are the deliverable's primary value. A coverage table that shows 90% Addressed for a sparse document has failed its purpose; the downstream gap-analyzer depends on honest Partial/Not Found signals.

- **NEVER load the full CSF baseline into context unless needed** — for a focused playbook, Table 3 alone suffices. Load `../nist-800-61r3-shared/references/csf-element-registry.md` only when the document type requires Table 2 coverage or when the user requests a full-scope map. Unnecessary loading wastes context.

- **NEVER omit the Evidence/Location column** — without a source reference (section number, paragraph quote, or "—" for Not Found), the table cannot be verified or challenged. An unattributed Addressed claim is indistinguishable from inference creep.

---

## When Things Go Wrong

| Situation | Likely Cause | Recovery |
|-----------|--------------|----------|
| Every element comes back Not Found | Document is too abstract (policy without procedures, or architecture diagram without process language) | Note document type mismatch; map what exists; flag that a companion procedures document is needed |
| Subcategories under same category disagree (one Addressed, siblings Not Found) | Normal and correct — subcategories are independent | Keep the split status; do not normalize upward to the category |
| User disputes a Partial rating | Criteria disagreement on what "fully satisfies" means | Quote the specific gap (missing threshold, missing role name, missing frequency) that prevents Addressed |
| Document covers r2 phases, not r3 elements | Legacy IR plan written pre-2024 | Note the r2 structure; attempt best-effort phase-to-subcategory crosswalk; flag document needs update to r3 structure |
| Document type is a hybrid (e.g., playbook embedded inside IR plan) | Compound document | Split into logical sections; map each section against the expected scope for its type |

---

## Workflow

### Step 1 — Classify Document

Identify document type. If unclear, use the Navigation decision tree above.
For expected scope per type, read: `../nist-800-61r3-shared/references/csf-element-registry.md` → §Document Type → Expected CSF Scope table.

### Step 2 — Set Scope

- **Playbook / Incident Report / After-Action Report**: Table 3 (DE/RS/RC) only, unless document explicitly addresses governance/prep content.
- **IR Plan / IR Policy / Risk Assessment**: Load full baseline from `../nist-800-61r3-shared/references/csf-element-registry.md`.
- Default: always start with Table 3 (all High priority).

### Step 3 — Scan and Tag

For each document section, identify the most specific subcategory satisfied. Apply these semantic anchors:

| Document language | Maps to |
|-------------------|---------|
| Anomaly detection, continuous monitoring | DE.CM |
| Incident declaration criteria, threshold to declare | DE.AE-08 |
| Triage, validate, severity scoring | RS.MA-02 |
| Incident categorization, incident type classification | RS.MA-03 |
| Escalation criteria, elevation, resource surge | RS.MA-04 |
| Criteria to begin recovery | RS.MA-05 |
| Root cause analysis, attack chain reconstruction | RS.AN-03 |
| Evidence log, chain of custody | RS.AN-06/07 |
| Incident scope, blast radius, IoC magnitude | RS.AN-08 |
| Stakeholder notification, breach notification | RS.CO-02 |
| ISAC sharing, threat intel sharing, external notification | RS.CO-03 |
| Containment, isolation, quarantine | RS.MI-01 |
| Eradication, persistence removal, patch | RS.MI-02 |
| Recovery execution, restore operations | RC.RP-01/02 |
| Backup integrity check, clean restore verification | RC.RP-03/05 |
| End-of-incident declaration, lessons learned, after-action | RC.RP-06, ID.IM-03 |
| IR policy, policy elements, policy review cycle | GV.PO-01/02 |
| Roles, responsibilities, RACI, authority | GV.RR-02 |

### Step 4 — Build Coverage Table

```
=== CSF 2.0 Coverage Map — [Document Name/Type] ===
Standard: NIST SP 800-61r3 (April 2025)
Document Type: [type]

TABLE 3 — INCIDENT RESPONSE (All High Priority)
─────────────────────────────────────────────────────────────
CSF ID     | Description (brief)               | Coverage  | Location
─────────────────────────────────────────────────────────────
DE.CM      | Asset monitoring for anomalies     | Partial   | §2.1
DE.CM-01   | Network monitoring                 | Addressed | §2.1.a
DE.CM-09   | Computing HW/SW/runtime monitoring | Not Found | —
DE.AE-08   | Incident declaration criteria      | Not Found | —
RS.MA-02   | Triage and validation              | Partial   | §4.2 (no severity criteria)
...

TABLE 2 — PREPARATION (load only if in scope)
[load ../nist-800-61r3-shared/references/csf-element-registry.md for full element list]

SUMMARY
────────
Table 3 coverage: X/23 Addressed, Y Partial, Z Not Found
Top gaps: [3–5 highest-priority Not Found elements]
Assessment: [does coverage match expected profile for this document type?]
```

### Step 5 — Flag Downstream

State whether output is ready for:
- `nist-800-61r3-gap-analyzer` (prioritized remediation)
- `nist-800-61r3-maturity-scorer` (maturity scoring)

---

## References

Load `../nist-800-61r3-shared/references/csf-element-registry.md` when:
- Full Table 2 (GV/ID/PR) subcategory list is needed
- Document type is IR Plan, IR Policy, or Risk Assessment
- User requests a complete element-by-element map
