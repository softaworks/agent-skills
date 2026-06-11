---
name: nist-800-61r3-incident-coordinator
description: "Coordinate live, active security incidents using the NIST SP 800-61r3 (April 2025) framework. Guides triage, PICERL phase management, stakeholder notification timing, evidence preservation, escalation decisions, and containment/eradication sequencing during an ongoing incident. Use when asked to 'help coordinate this incident', 'walk me through incident response', 'we have an active incident', 'guide containment steps', or 'should we escalate this'. NOT for post-incident review — use nist-800-61r3-after-action-reviewer for that."
user-invocable: true
---

# NIST SP 800-61r3 Incident Coordinator

Guide active, live security incident response using NIST SP 800-61r3 (April 2025) framework structures — from initial triage through declared recovery, including phase management, escalation decisions, evidence preservation, and stakeholder communication timing.

---

## Mindset

1. **Stop the bleeding first; understand the wound second.** Containment precedes root cause analysis. Teams that pause containment to conduct thorough forensics while the attacker still has an active foothold consistently achieve worse outcomes than teams that limit the attacker's options first. You can investigate a preserved, contained environment. You cannot un-exfiltrate data while you were still doing log analysis.

2. **Parallel evidence preservation is a real tension, not a luxury.** NIST SP 800-61r3 RS.AN-06 requires preserving evidence, but containment actions (isolation, account revocation, firewall blocks) inevitably alter or terminate forensic artifacts. The sequencing decision — preserve memory/logs before or after isolation — must be made explicitly and documented, not made accidentally by whoever acts fastest.

3. **PICERL phases are states, not a waterfall.** Preparation, Identification, Containment, Eradication, Recovery, and Lessons Learned overlap and recurse in real incidents. An organization can be in Containment on one lateral movement vector while simultaneously in Identification on a newly discovered second foothold. Treat phases as labels for current dominant activity, not as sequential gates.

4. **Communication cadence is a decision, not a default.** Too frequent updates create noise that desensitizes stakeholders and consumes responder time. Too infrequent updates create fear, generate inbound calls that disrupt response, and cause leadership to lose confidence. The right cadence is calibrated to incident velocity: fast-moving incidents need hourly executive pulses; stable, contained incidents need 4-hour updates. State your chosen cadence and the reasoning explicitly.

5. **Escalation to CIRT is a decision point, not a failure.** Internal handlers should not resist CIRT escalation to protect team reputation. The escalation criteria are objective: complexity exceeds team capability, a second concurrent incident is active, legal/regulatory exposure is confirmed, the incident has crossed into a major incident threshold per RS.MA-04. When any criterion is met, escalate — delay is the actual failure.

6. **Legal hold begins at the moment of suspected regulatory exposure, not at confirmed breach.** Organizations routinely wait for incident confirmation before engaging legal counsel. This is backwards: the trigger for legal hold is the moment there is reasonable belief that regulated data (PII, PHI, financial records) *may* have been accessed. RS.AN-07 evidence retention requirements and legal hold are parallel processes, not sequential ones. If legal hold is missed, no amount of good IR work recovers it.

7. **Every containment decision has a business cost and a security cost — document both.** Isolating a production system stops attacker lateral movement but also stops business operations. The correct decision requires knowing both costs and documenting the trade-off explicitly. An undocumented isolation that causes business harm becomes a liability; a documented, authorized isolation becomes a defensible decision.

---

## Navigation

### When to use this skill
- An active, declared security incident is in progress
- User needs guidance on sequencing PICERL phases for a specific incident type
- Triage is complete and user is deciding between Containment strategies
- Escalation decision needs a structured framework
- Stakeholder communication timing is in question during an active event
- Evidence preservation vs. containment trade-off requires a documented decision
- Legal hold trigger conditions need to be assessed mid-incident

### When NOT to use this skill
- The incident is over — use `nist-800-61r3-after-action-reviewer` for post-incident review
- User wants to check whether their IR policy is complete — use `nist-800-61r3-policy-reviewer`
- User wants to find gaps in a playbook or procedure document — use `nist-800-61r3-gap-analyzer`
- User is running a tabletop exercise — apply exercise facilitation, not live incident coordination
- No incident has been declared — if in pre-declaration ambiguity, guide through DE.AE-08 criteria first

### Pre-flight: Is this actually a declared incident?

```
Has an incident been declared per DE.AE-08 criteria?
│
├── No — observable activity only, no declaration yet
│     → Run through DE.AE-08 decision criteria:
│         Is there confirmed malicious activity OR high-confidence indicator?
│         Does the activity meet any severity threshold in your tier definitions?
│         ↳ If yes → guide declaration (RS.MA-01) then continue coordination
│         ↳ If no → document as potential incident, set monitoring checkpoint,
│                   do not initiate containment actions prematurely
│
└── Yes — incident declared, severity assigned
      → Confirm current PICERL phase
      → Confirm whether major incident threshold (RS.MA-04) applies
      → Proceed with phase-appropriate workflow below
```

---

## Philosophy

Active incident response is not documentation work — it is a time-critical sequence of decisions made under uncertainty with incomplete information. The coordinator's job is not to know all the answers but to ensure the right questions are asked in the right order, that decisions are made explicitly rather than by default, and that the organization does not create new problems while solving the original one. Every minute of an active incident, the attacker is either moving or waiting; your decisions are real-time responses to their actions.

---

## PICERL Phase Workflows

### Phase: Identification (RS.MA-02 / RS.MA-03)

**Objective:** Validate the incident is real, assign severity, establish initial scope.

```
1. Validate the alert or report (RS.MA-02.R1)
   └── Confirm: true positive vs. false positive
   └── Estimate scope: single host, subnet, domain, or cross-environment?

2. Assign severity tier (RS.MA-03.R1)
   └── P1 — critical: data exfiltration confirmed or imminent, ransomware active,
              major-incident criteria met → escalation review required (RS.MA-04)
   └── P2 — high: confirmed malicious access, scope uncertain, containment needed
   └── P3 — medium: suspicious activity, unconfirmed, monitoring + analysis mode

3. Apply major incident criteria (RS.MA-04) — escalate if:
   └── Estimated business impact exceeds defined threshold
   └── Regulatory data exposure is plausible
   └── Multiple systems or environments involved
   └── Team capability is outpaced by incident complexity
   └── A second concurrent incident is active

4. Assign and confirm Incident Handler authority (GV.RR-02)
   └── Who is authorized to: isolate hosts? revoke accounts? engage legal?
   └── If authority is unclear, STOP and get explicit authorization before acting
```

### Phase: Containment (RS.MA-05)

**Objective:** Limit attacker's ability to move, escalate, or exfiltrate further.

```
Evidence Preservation Decision (RS.AN-06) — make this BEFORE containment:
├── Can memory forensics be captured in <15 minutes?
│   └── Yes → capture memory, running process list, active network connections FIRST
│   └── No → proceed to containment; document decision and rationale
├── Are logs being forwarded to SIEM/immutable store?
│   └── Yes → proceed to containment
│   └── No → snapshot/export logs from affected systems BEFORE isolation
└── Document the preserve/contain sequencing decision explicitly

Containment Actions (sequence by attacker opportunity cost):
1. Network isolation (highest priority if lateral movement is active)
2. Credential revocation for compromised accounts
3. C2 blocking at perimeter (coordinate with network team)
4. Privileged access review — disable accounts with admin rights near affected systems
5. Cloud resource isolation if cloud footprint is involved

Containment verification — do NOT proceed to Eradication until:
└── No new lateral movement events in [defined time window]
└── All known ingress paths are blocked
└── Attacker's known access mechanisms are severed
└── Network/endpoint telemetry confirms quiescence
```

### Phase: Eradication (RS.MA-05.R2)

**Objective:** Remove all attacker artifacts from confirmed-contained environment.

```
PREREQUISITE CHECK — eradication starts only after:
[ ] Containment verified (no active attacker movement)
[ ] Scope validated (RS.AN-08 — adjacent systems checked)
[ ] Evidence preserved for forensic use

Eradication sequence:
1. Remove all identified malware, tools, and persistence mechanisms
2. Patch or mitigate the exploited vulnerability
3. Rotate ALL credentials in attacker's confirmed or suspected reach
4. Rebuild compromised hosts if integrity cannot be verified (preferred over "clean")
5. Validate eradication completeness with IoC scan before proceeding
```

### Phase: Recovery (RC.RP-03 / RC.RP-04)

**Objective:** Restore affected systems to verified, operational state.

```
Recovery sequencing (RC.RP-03):
1. Restore from known-good backup (verify backup integrity first)
2. OR rebuild from golden image + apply required configs
3. Pre-production IoC scan of all systems to be restored (RC.RP-05.R1)
4. System owner authorization before returning to production (RC.RP-04.R2)
5. Monitor restored systems with elevated telemetry for [defined window]

Recovery completion criteria (RC.RP-06 prerequisite):
└── All affected systems restored and owner-verified
└── Business operations confirmed normal by system owners
└── No recurrence events detected in monitoring window
└── Lessons-learned process initiated (hand off to after-action-reviewer)
```

---

## Stakeholder Notification Timing

### Internal Notifications (RS.CO-02)

| Audience | Trigger | Cadence (active incident) | Cadence (stable/contained) |
|----------|---------|--------------------------|---------------------------|
| Incident Handler / SOC | Immediate on declaration | Continuous | Continuous |
| IR Team Lead | Within 15 minutes of P1/P2 declaration | Per incident activity | Per incident activity |
| CISO / Security Leadership | Within 1 hour of P1; within 4 hours of P2 | Hourly (P1), every 4hr (P2) | Every 4-8hr |
| Legal Counsel | Immediately if regulated data exposure possible | As needed | As needed |
| Executive Leadership | Within 2 hours of major incident (RS.CO-03.R2) | Hourly | Every 4-8hr |
| IT Operations | Before any containment action affecting infrastructure | Per action | Per action |

### External Notifications (RS.CO-02.R3)

Regulatory notification assessment must be documented for every incident, regardless of outcome. The decision is:

```
Does this incident involve data that is subject to breach notification law?
├── Yes (PII, PHI, PCI, FERPA, GLBA, etc.)
│   └── Legal hold triggered immediately
│   └── Regulatory clock starts at discovery (not confirmation)
│   └── Engage legal counsel NOW — they determine notification timing
│   └── Document: date/time of discovery, scope estimate, counsel engagement
│
└── No confirmed regulated data
    └── Document: what data types were in scope, why notification not required
    └── Reassess if scope expands
    └── Do not mark N/A without written rationale
```

### Communication Cadence Calibration

- **Fast-moving incidents (active exfiltration, spreading ransomware):** Hourly executive pulse; 15-minute responder sync
- **Contained incidents under active investigation:** 4-hour executive update; responder sync at shift transitions
- **Stable, low-risk incidents:** 8-hour or end-of-day update sufficient
- **Rule:** If stakeholders are calling *in* to ask for status, your cadence is too slow. If responders are spending >20% of time on updates, your cadence is too fast.

---

## Escalation Decision Tree (RS.MA-04)

```
Should this escalate to CIRT / external IR firm?

Criterion 1: Scope complexity
└── Affected environments: >2 business units OR cloud + on-prem + OT → ESCALATE

Criterion 2: Team capacity
└── Active incident requires >80% of available IR staff for >4 hours → ESCALATE
└── A second unrelated incident is declared concurrently → ESCALATE

Criterion 3: Threat sophistication
└── Evidence of APT TTPs, zero-day exploitation, or signed malware → ESCALATE
└── Attacker has demonstrated OPSEC (custom tools, living-off-the-land, no detectable C2) → ESCALATE

Criterion 4: Regulatory or legal exposure
└── Data breach notification law triggered → ESCALATE (legal team + IR firm with legal hold experience)
└── Law enforcement involvement likely → ESCALATE (FBI, CISA engagement requires case management)

Criterion 5: Business continuity
└── Incident threatens operational continuity for >24 hours → ESCALATE

→ If any criterion is met: escalate immediately, do not wait to see if the team can manage it.
→ If no criterion is met: document the assessment and reassess every 4 hours.
```

---

## Legal Hold Trigger Conditions

Legal hold must be initiated before evidence is altered or destroyed. Triggers include:

- Any confirmed or suspected access to PII, PHI, financial records, or IP
- Receipt of external demand (ransom note, extortion communication)
- Any indication that law enforcement may be involved
- Evidence of data staging or exfiltration, even if exfiltration is unconfirmed
- Incident scope includes a third party or vendor whose data may be affected

**Legal hold actions (coordinate with legal counsel):**
1. Suspend any automated log rotation or data deletion for affected systems
2. Preserve all email communications related to the incident (including internal)
3. Document chain of custody for all forensic artifacts
4. Do NOT share evidence copies externally without legal sign-off

---

## NEVER

- **NEVER begin eradication before containment is verified** — if the attacker retains any active access path while you're removing artifacts, they simply reinstall. Every eradication step performed on an uncontained environment must be treated as ineffective and repeated after containment is confirmed. Premature eradication is the leading cause of "re-infection" that is actually the original infection continuing.

- **NEVER make containment decisions without explicit authority designation** — an IR handler who isolates a production payment system without documented authorization exposes the organization to operational liability equal to or greater than the incident itself. Authority to contain must be pre-established in the IR plan (GV.RR-02) and confirmed verbally/in-writing at incident start. If it isn't, STOP and get authorization before acting.

- **NEVER delay legal hold until breach is confirmed** — the legal hold trigger is *reasonable belief* that regulated data may have been accessed, not confirmed proof. Organizations that wait for forensic confirmation before engaging legal counsel routinely destroy evidence that would have been protected, miss regulatory notification clocks, and lose litigation defensibility. Engage legal counsel the moment regulated data is plausibly in scope.

- **NEVER skip the evidence preservation/containment sequencing decision** — acting on containment without first deciding whether to capture forensic artifacts (memory, logs, active connections) is not a decision — it is an accident. Every incident requires an explicit, documented choice: "we preserved X before containing because Y" or "we contained before preserving because Z." Undocumented sequencing is a scope and chain-of-custody failure.

- **NEVER communicate incident details to external parties (including vendors) without legal review** — even well-intentioned sharing of incident scope with a SaaS vendor or managed service provider can constitute unauthorized disclosure of a breach, complicate law enforcement investigations, or trigger unintended contractual notice obligations. All external communication must route through legal during an active incident.

- **NEVER validate containment based on absence of alerts alone** — alert silence is not containment confirmation. Sophisticated attackers suppress telemetry; misconfigured detection tools have blind spots; containment decisions based only on "we haven't seen new alerts" routinely fail. Containment is verified by positive evidence: confirmed network isolation, account revocation receipts, firewall rule confirmation, and endpoint telemetry showing no outbound connections from isolated hosts.

- **NEVER bypass the scope validation step (RS.AN-08) before declaring recovery** — teams that validate only the initially identified asset and declare recovery without checking adjacent systems are not in recovery, they are in a false sense of recovery. Lateral movement is the norm in advanced incidents, not the exception. Document what was checked, how, and the result before any recovery declaration.

---

## When Things Go Wrong

| Situation | Response |
|-----------|----------|
| Containment was executed before evidence was preserved | Document the decision retroactively with rationale; flag RS.AN-06 as compromised in the eventual AAR; salvage what evidence remains (SIEM logs, network flow data, cloud audit trails); note that forensic completeness is reduced and conclusions may be limited. |
| Legal counsel is unavailable at incident start | Designate an authorized internal contact (General Counsel backup, outside counsel on retainer) in the IR plan *before* incidents. If no one is available: assume legal hold applies, suspend all log rotation and deletion, do not make external disclosures, and document that counsel was sought but unavailable and when they were eventually reached. |
| Attacker re-establishes access after eradication | Restart at Containment — do not continue the current eradication pass. The re-access event means at least one persistence mechanism or access path was missed. Treat this as a new scope event: re-examine all systems, not just the one where re-access was detected. Document the timeline split (incident resumes at Containment, [timestamp]). |
| Executive demands recovery before containment is verified | This is a governance and authority decision, not an IR decision. Document the request, the responder's assessment, and the executive's direction in writing. If the executive overrides containment verification, note that RS.MA-05 was not fully completed and that the organization accepted that risk. Ensure the after-action-reviewer captures this as a process finding. |
| Stakeholder communication is generating more inbound calls than outbound updates can handle | Establish a single status page or bridge line for stakeholders; shift from push-notifications to pull-access (stakeholders check status board vs. receiving individual updates). Assign one communicator role solely responsible for stakeholder management so responders are not interrupted. |
| Scope expands mid-incident (new systems discovered in attacker's reach) | Do not restart the incident — extend it. Document the scope expansion as a new finding within the same incident, re-run the Identification phase for the newly in-scope assets, and reassess severity. If the expansion triggers major incident criteria, escalate immediately. Notify stakeholders of scope change at the next communication checkpoint. |
| Two simultaneous incidents with overlapping responder pool | Invoke CIRT escalation criteria immediately. Triage which incident has higher business impact and assign primary responders there. Assign secondary team or escalate the lower-priority incident. Do not attempt to run both incidents with the same team at full capacity — partial attention on two incidents consistently produces worse outcomes than full attention on one with escalation on the other. |

---

## Incident Coordination Checklist (Quick Reference)

```
IDENTIFICATION
[ ] DE.AE-08 — Incident declared, criteria documented
[ ] RS.MA-02 — Severity and urgency assigned
[ ] RS.MA-03 — Incident categorized (type, scope estimate)
[ ] RS.MA-04 — Major incident criteria evaluated
[ ] GV.RR-02 — Handler authority confirmed

CONTAINMENT
[ ] RS.AN-06 — Evidence preservation decision documented (before/after isolation)
[ ] Legal hold assessed and triggered if applicable
[ ] Containment actions executed and logged with timestamps
[ ] Containment verification completed (positive evidence, not absence of alerts)
[ ] Stakeholder notification sent (internal per RS.CO-02, external if RS.CO-02.R3 applies)

ERADICATION
[ ] Scope validation completed (RS.AN-08 — adjacent systems checked)
[ ] All artifacts removed; persistence mechanisms identified and severed
[ ] Vulnerability patched or mitigated
[ ] Credentials rotated for all accounts in attacker's reach

RECOVERY
[ ] Systems restored from verified clean state (RC.RP-03)
[ ] Pre-production IoC scan completed (RC.RP-05.R1)
[ ] System owner sign-off documented (RC.RP-04.R2)
[ ] Elevated monitoring in place for restored systems
[ ] Lessons-learned process initiated → hand off to nist-800-61r3-after-action-reviewer
```

---

## Related Skills

| Skill | When to use |
|-------|-------------|
| `nist-800-61r3-after-action-reviewer` | After the incident is closed — review the AAR for completeness and actionability |
| `nist-800-61r3-policy-reviewer` | Review the IR policy and plan that governs this incident coordination |
| `nist-800-61r3-gap-analyzer` | Identify what is missing from your IR playbooks before the next incident |
| `nist-800-61r3-maturity-scorer` | Score program maturity using this incident as evidence input |

---

## Deliverable

Real-time coordination guidance covering:
- PICERL phase status and sequencing decisions
- Evidence preservation vs. containment trade-off documentation
- Stakeholder notification timing and cadence decisions
- Escalation assessment with documented criteria
- Legal hold trigger evaluation
- Containment verification before eradication sign-off
- Recovery readiness checklist
- Handoff package for `nist-800-61r3-after-action-reviewer`

<!-- INJECT:B3:ir-coordination -->
<!-- Source: awesome-claude-code-subagents (MIT) — incident-responder.md (D-grade source; PATTERNS only) -->
## Track B / B3 — IR coordination patterns
Severity-tiered notification matrix, append-only evidence-bag manifest (chain of custody), and Lessons-Learned schema (no tracked-metric JSON). Full reference: `~/soar/splunk-soar-base/knowledgebase/ir-coordination-patterns.md`. SEV-1/SEV-2 with identity/mail implicated → coordinate out-of-band.
