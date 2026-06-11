# NIST SP 800-61r3 R-Item Catalog (April 2025)

Full catalog of Recommendation (R) items from the SP 800-61r3 CSF 2.0 Community Profile.
R-items represent "the organization **should** do this" — highest obligation level.
C-items ("should consider") are tracked separately; N-items are informational only.

---

## HIGH PRIORITY — Table 3 (Respond/Recover functions)

### DE.CM (Continuous Monitoring)

| ID | Requirement |
|----|-------------|
| `DE.CM.R1` | Continuous monitoring must cover: networks/network services; computing HW/SW/runtime/data; physical environment; personnel activity and technology usage; external service provider activities |
| `DE.CM.R2` | Tune monitoring technologies to reduce false positives and false negatives to acceptable levels |
| `DE.CM-01.R1` | Monitoring must include wired/wireless networks, network communications/flows, network services (DNS, BGP), and unauthorized/rogue networks |
| `DE.CM-02.R1` | Physical environment monitoring must include all access attempts, movement of people/equipment, and tampering signs |
| `DE.CM-03.R1` | Personnel activity monitoring must include anomalous user activity, authentication attempts, and deception technology |
| `DE.CM-06.R1` | External provider monitoring must include remote/on-site admin, maintenance activities, deviations from expected cloud/ISP behavior |
| `DE.CM-09.R1` | Monitor email, web, file sharing, collaboration services for malware/phishing/exfil |
| `DE.CM-09.R2` | Monitor authentication attempts for credential attacks and unauthorized credential use |
| `DE.CM-09.R3` | Monitor software/hardware configurations for deviations from security baselines |
| `DE.CM-09.R4` | Monitor hardware/software including cybersecurity protection mechanisms for tampering/failure/compromise |
| `DE.CM-09.R5` | Monitor endpoints for cyber health issues (missing patches, malware, unauthorized software) |

### DE.AE (Adverse Event Analysis)

| ID | Requirement |
|----|-------------|
| `DE.AE.R1` | Rely on technical solutions to filter large event datasets to human-viewable subsets |
| `DE.AE.R2` | Proactively find incidents earlier in the attack life cycle |
| `DE.AE-02.R1` | Use SIEM/SOAR to continuously monitor log events for known malicious/suspicious activity |
| `DE.AE-02.R2` | Use up-to-date CTI in log analysis tools to improve detection accuracy |
| `DE.AE-02.R3` | Regularly conduct manual reviews for technologies that cannot be sufficiently auto-monitored |
| `DE.AE-03.R1` | Constantly transfer log data from sources to a small number of log servers |
| `DE.AE-03.R2` | Use event correlation technology (SIEM/SOAR) to gather related data from multiple sources |
| `DE.AE-03.R3` | Use CTI to correlate events among log sources |
| `DE.AE-04.R1` | Estimate impact/scope through automated (SIEM/SOAR) and/or manual means; review and refine estimates |
| `DE.AE-06.R1` | Generate alerts and provide to cybersecurity/IR tools and staff (SOC, incident responders) |
| `DE.AE-06.R2` | Make log analysis findings accessible to incident responders at all times |
| `DE.AE-07.R1` | Integrate up-to-date CTI and asset inventories into adverse event analysis |
| `DE.AE-07.R2` | Rapidly acquire and analyze vulnerability disclosures from suppliers/vendors/advisories |
| `DE.AE-08.R1` | Apply incident criteria to analyzed activity; consider known false positives to determine incident declaration |

### RS.MA (Incident Management)

| ID | Requirement |
|----|-------------|
| `RS.MA.R1` | Do not handle incidents on first-come, first-served basis — use risk evaluation factors |
| `RS.MA.R2` | Base triage/prioritization/escalation/recovery on risk evaluation factors |
| `RS.MA.R3` | Track incident response status with: summary, IoCs, status/timeframe per action, next steps |
| `RS.MA-01.R1` | Detection technologies should automatically report confirmed incidents |
| `RS.MA-02.R1` | Perform preliminary review to verify incident occurred, estimate severity and urgency |
| `RS.MA-02.R2` | Have mechanisms for third parties to report possible incidents; monitor reports seriously |
| `RS.MA-03.R1` | Perform detailed review to categorize by incident type (data breach, ransomware, account takeover, DoS) |
| `RS.MA-03.R2` | Prioritize based on scope, likely impact, time-critical nature, resource availability |
| `RS.MA-03.R3` | Select incident response strategies balancing recovery speed vs. investigation need |
| `RS.MA-04.R1` | Track and validate status of all ongoing incidents to identify escalation needs |
| `RS.MA-05.R1` | Apply incident recovery criteria to determine when recovery should be initiated |
| `RS.MA-05.R2` | Consider operational disruption of recovery activities when deciding recovery timing |

### RS.AN (Incident Analysis)

| ID | Requirement |
|----|-------------|
| `RS.AN-03.R1` | Determine sequence of events and which assets/resources were involved in each event |
| `RS.AN-03.R2` | Determine which vulnerabilities, threats, and threat actors were involved (direct/indirect) |
| `RS.AN-03.R3` | Analyze incident for underlying or systemic root causes |
| `RS.AN-03.R4` | Check any deployed cyber deception technology for additional attacker behavior info |
| `RS.AN-06.R1` | Safeguard confidentiality and integrity of IR records; restrict to authorized personnel only |
| `RS.AN-07.R1` | Collect and retain evidence per evidence preservation procedures and data retention policies; consider prosecution possibility |
| `RS.AN-08.R1` | Look for IoCs, evidence of persistence, and other signs on both targeted and potential target assets |

### RS.CO (Incident Reporting and Communication)

| ID | Requirement |
|----|-------------|
| `RS.CO.R1` | Have mechanisms in place in advance to coordinate with affected parties about incidents |
| `RS.CO-02.R1` | When incident analyzed/prioritized, coordinate with appropriate individuals inside and outside the organization |
| `RS.CO-02.R2` | Follow established procedures: what must be reported, to whom, at what times |
| `RS.CO-02.R3` | Perform notifications in compliance with incident notification laws/regulations for organization's sectors and geographies |
| `RS.CO-02.R4` | Notify affected third parties of data breaches per regulatory, legal, contractual requirements |
| `RS.CO-02.R5` | Notify law enforcement and regulatory bodies per criteria in IR plan and management approval |
| `RS.CO-03.R1` | Securely share information consistent with response plans and information sharing agreements |
| `RS.CO-03.R2` | Regularly update senior leadership on status of major incidents |
| `RS.CO-03.R3` | Notify human resources when malicious insider activity has occurred |
| `RS.CO-03.R4` | Establish and follow media communications procedures for IR that comply with org policies |

### RS.MI (Incident Mitigation)

| ID | Requirement |
|----|-------------|
| `RS.MI-01.R1` | Allow incident handlers to manually select and perform containment actions in addition to or instead of automated measures |
| `RS.MI-02.R1` | Identify all affected hosts and services so all flaws and weaknesses can be remediated |

### RC.RP (Recovery Plan Execution)

| ID | Requirement |
|----|-------------|
| `RC.RP-01.R1` | Begin recovery procedures during or after incident response processes |
| `RC.RP-01.R2` | Inform all individuals with recovery responsibilities about plans and required authorizations |
| `RC.RP-02.R1` | Recovery actions must account for timeliness, precision, and reliability |
| `RC.RP-02.R2` | Select recovery actions based on IR plan criteria and available resources |
| `RC.RP-02.R3` | Change planned recovery actions based on reassessment of needs/resources |
| `RC.RP-03.R1` | Check restoration assets for indicators of compromise, file corruption, and integrity issues before use |
| `RC.RP-04.R1` | Validate that essential services are restored in the appropriate order |
| `RC.RP-04.R2` | Work with system owners to confirm successful restoration and return to normal operations |
| `RC.RP-04.R3` | Monitor performance of restored systems to verify adequacy of restoration |
| `RC.RP-05.R1` | Check restored assets for IoCs; remediate root causes before production use |
| `RC.RP-05.R2` | Verify correctness and adequacy of restoration actions before putting restored system online |
| `RC.RP-06.R1` | Prepare an after-action report documenting the incident, response/recovery actions, and lessons learned |

### RC.CO (Recovery Communication)

| ID | Requirement |
|----|-------------|
| `RC.CO-03.R1` | Securely share recovery information including restoration progress |
| `RC.CO-03.R2` | Regularly update senior leadership on recovery status and restoration progress for major incidents |
| `RC.CO-03.R3` | Follow contract rules for incident information sharing between org and suppliers |
| `RC.CO-03.R4` | Coordinate crisis communication between the organization and its critical suppliers |
| `RC.CO-04.R1` | Follow org's breach notification procedures for recovering from a data breach incident |
| `RC.CO-04.R2` | Explain the steps being taken to recover and to prevent recurrence |

---

## MEDIUM PRIORITY — Table 2 (Govern/Identify/Protect functions)

| ID | Requirement |
|----|-------------|
| `GV.OC-03.R1` | Cybersecurity requirements include all IR-related requirements (incident notification, data breach reporting) |
| `GV.RM-03.R1` | Incident-related decision-making informed by other risk types (privacy, operational, safety, reputational, AI) |
| `GV.RM-06` | Have a standardized method for calculating, documenting, categorizing, and prioritizing cybersecurity risks |
| `GV.RR.R1` | Cybersecurity roles/responsibilities/authorities should include incident response |
| `GV.RR-02.R1` | All roles/responsibilities involving IR should be documented in organizational policies |
| `GV.RR-02.R2` | All appropriate individuals/parties should be designated the authority to fulfill IR responsibilities |
| `GV.PO.R1` | Cybersecurity policies should include an incident response policy |
| `GV.SC-05.R1` | Supply chain risk management requirements include cybersecurity performance, vulnerability/threat/incident disclosure/sharing |
| `GV.SC-08` | Relevant suppliers included in incident planning, response, and recovery activities |
| `ID.AM-01.R1` | Make current, auto-updated inventories of internal/external hardware available for vulnerability finding, monitoring, and shadow IT detection |
| `ID.AM-02.R1` | Make current, auto-updated inventories of internal/external SW/services available |
| `ID.RA-01.R1` | Understand current vulnerabilities to make informed risk decisions (all types: FW, misconfigs, design weaknesses, physical, integrity violations) |
| `ID.RA-03.R1` | Identify internal/external threats during routine operations and from CTI |
| `ID.RA-05.R1` | Use existing risk estimation mechanisms for incident response purposes |
| `ID.IM-01.R1` | Periodically evaluate IR program performance to identify problems and deficiencies |
| `ID.IM-04.R1` | Synchronize business continuity plans with incident response plans |
| `ID.IM-04.R2` | Review and update all cybersecurity plans periodically or when significant improvements are needed |
| `ID.IM-04.R3` | Base each cybersecurity plan on the organization's unique requirements, mission, size, structure |
| `ID.IM-04.R4` | Each plan identifies resources and management support needed |
| `PR.AT-02.R1` | Role-based training includes incident-related responsibilities |
| `PR.DS-11` | Backups created, protected, maintained, and tested (particularly important for recovery) |

---

## Quick Count

- **High-priority R-items (Table 3):** 68 items across 8 control families
- **Medium-priority R-items (Table 2):** 21 items across 6 control families
- **Total auditable R-items:** 89

---

## Document-Type Scope Map

| Document Type | Primary R-item Scope |
|---------------|----------------------|
| IR Plan | All Table 3 R-items + ID.IM-04.R1–R4 + GV.PO.R1 + GV.RR-02.R1/R2 |
| Playbook | RS.MA, RS.AN, RS.MI, RC.RP R-items + DE.AE-08.R1 |
| Incident Report | RS.MA-02–05, RS.AN-03, RS.AN-06/07/08, RS.CO-02/03, RC.RP-06 |
| After-Action Report | RS.AN-03, RC.RP-06.R1, RS.AN-06.R1, RS.AN-07.R1 |
| IR Policy | GV.PO.R1, GV.RR-02.R1/R2, ID.IM-04.R1–R4, GV.OC-03.R1 |
| Detection Runbook | DE.CM-01–09, DE.AE-02/03/04/06/07/08 |
| BCP/DRP | RC.RP-01–06, ID.IM-04.R1, ID.IM-04.R4 |

---

## Scoring Formula

**High-priority compliance rate:**
`(Met + Partial×0.5) ÷ Total_High × 100`

**Weighted composite:**
`(High_met × 3 + Med_met × 2) ÷ (High_total × 3 + Med_total × 2) × 100`

**Tier thresholds:**
- 90%+ High = Strong compliance
- 75–89% High = Adequate with gaps
- 60–74% High = Significant gaps
- <60% High = Non-compliant
