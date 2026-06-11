# RS.AN-03 / RS.AN-06/07/08 — Root Cause & Evidence Checklists

Load this file when performing Steps 2–3 of the AAR review workflow.

---

## RS.AN-03 — Root Cause Analysis Quality

### R1 — Event Sequence (RS.AN-03.R1)
"Determine the sequence of events that have occurred during the incident and which assets and resources were involved in each of those events."

- [ ] Complete, timestamped event sequence exists
- [ ] Affected assets enumerated at each stage of the sequence
- [ ] Gaps in timeline are explicitly acknowledged with explanation

**Gap signal:** Report says "attacker gained access" without explaining the full chain — fails R1.

### R2 — Vulnerability and Threat Identification (RS.AN-03.R2)
"Determine what vulnerabilities, threats, and threat actors were directly or indirectly involved."

- [ ] Specific vulnerability or misconfiguration enabling the incident identified
- [ ] Indirect enablers noted (missing MFA, stale accounts, excessive permissions, monitoring gaps)
- [ ] Threat actor capability level characterized (opportunistic vs. targeted)

**Gap signal:** Report blames "phishing" without identifying which controls failed or were absent — fails R2.

### R3 — Systemic Root Cause (RS.AN-03.R3)
"Analyze the incident to find the underlying or systemic root causes."

- [ ] AAR goes beyond proximate cause to systemic causes
- [ ] At least one of these systemic categories addressed: patch management, training/awareness, monitoring gaps, access control architecture, process/procedure failure, vendor/supply chain, governance/policy gap
- [ ] Analysis method noted (5-Whys, fishbone/Ishikawa, fault tree, or equivalent)

**Practitioner trap:** "Employee clicked phishing link" = proximate cause. The systemic causes are: (1) why did email filtering not catch it, (2) why was MFA not enforced on that account class, (3) why did the user not recognize/report it, (4) why did detection not fire sooner. All four can be systemic findings.

**Gap signal:** Single-sentence root cause with no structural analysis — fails R3.

### R4 — Deception Technology Check (RS.AN-03.R4)
"Check any deployed cyber deception technology for additional information on attacker behavior."

- [ ] Honeypots, deception tokens, or canary files checked (or N/A if not deployed)
- [ ] N/A documented explicitly with statement that no deception tech is deployed

---

## RS.AN-06/07/08 — Evidence & Records Integrity

### RS.AN-06.R1 — Records Confidentiality
"Safeguard the confidentiality and integrity of incident response records; ensure only authorized personnel have access."

- [ ] AAR references how IR records were protected during and after incident
- [ ] Access control for incident data documented (who had access, role-based)
- [ ] Incident lead identified as accountable for records safeguarding

### RS.AN-07.R1 — Evidence Preservation
"Collect and retain evidence per evidence preservation procedures and data retention policies; consider factors including the possibility of prosecution."

- [ ] Forensic images, logs, or artifacts collected and itemized
- [ ] Chain of custody procedures referenced or attached
- [ ] Prosecution possibility explicitly considered and documented (even if decided no)
- [ ] Retention timelines for each evidence category documented

**Practitioner trap:** Teams that never intend to prosecute still must document the decision — the standard requires consideration, not prosecution.

### RS.AN-08.R1 — Scope Validation
"Look for indicators of compromise, evidence of persistence, and other signs of an incident on both the assets known to be targeted and other potential targets."

- [ ] Incident scope validated beyond initially identified systems
- [ ] Adjacent/related assets checked for IoCs (lateral movement paths enumerated)
- [ ] Persistence mechanism identified, confirmed removed, and removal verified
- [ ] Scope expansion findings documented (even if scope confirmed as initially assessed)

**Gap signal:** Report addresses only initial host without checking lateral spread — this is the top predictor of re-infection. Fails RS.AN-08.R1.
