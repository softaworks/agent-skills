# NIST SP 800-61r3 — Canonical CSF 2.0 Element Registry

Full element set from NIST SP 800-61r3 (April 2025), Tables 2 and 3.
This is the single authoritative reference for all skills in the nist-800-61r3 cluster.

Consuming skills:
- `nist-800-61r3-csf-mapper` — uses element list and Document Type scope table
- `nist-800-61r3-gap-analyzer` — uses element list, severity mapping, dependency graph
- `nist-800-61r3-maturity-scorer` — uses element list with weights and scoring summary

---

## TABLE 3 — Incident Response (HIGH Priority / Weight 3)

These are the primary IR operational elements. A missing or partial status for any of these
is a gap. The weight column is used by the maturity scorer; severity mapping is used by the
gap analyzer.

### DE — Detect

| CSF ID | Weight | Description |
|--------|--------|-------------|
| DE.CM | 3 | Assets are monitored to find anomalies, IoCs, and other potential adverse events |
| DE.CM-01 | 3 | Networks and network services are monitored to find potentially adverse events |
| DE.CM-02 | 3 | Physical environment is monitored |
| DE.CM-03 | 3 | Personnel activity and technology usage are monitored to find potentially adverse events |
| DE.CM-06 | 3 | External service provider activities and services are monitored to find potentially adverse events |
| DE.CM-09 | 3 | Computing hardware and software, runtime environments, and their data are monitored |
| DE.AE | 3 | Anomalies, indicators of compromise, and other potentially adverse events are analyzed to characterize the events and detect cybersecurity incidents |
| DE.AE-02 | 3 | Potentially adverse events are analyzed to better understand associated activities |
| DE.AE-03 | 3 | Information correlated from multiple sources |
| DE.AE-04 | 3 | The estimated impact and scope of adverse events are understood |
| DE.AE-06 | 3 | Information on adverse events is provided to authorized staff and tools |
| DE.AE-07 | 3 | Cyber threat intelligence and other contextual information are integrated into the analysis of adverse events |
| DE.AE-08 | 3 | Incidents are declared when adverse events meet the defined incident criteria |

### RS — Respond

| CSF ID | Weight | Description |
|--------|--------|-------------|
| RS.MA | 3 | Incidents are contained, eradicated, and recovered from |
| RS.MA-01 | 3 | The incident response plan is executed in coordination with relevant third parties once an incident is declared |
| RS.MA-02 | 3 | Incident reports are triaged to validate the incident, categorize the incident, and prioritize incident handling |
| RS.MA-03 | 3 | Incidents are categorized and prioritized |
| RS.MA-04 | 3 | Incidents are escalated or elevated as needed |
| RS.MA-05 | 3 | Criteria for initiating incident recovery are applied |
| RS.AN | 3 | Investigations are conducted to understand what occurred and support recovery and law enforcement |
| RS.AN-03 | 3 | Analysis is performed to establish what has occurred during an incident and the root cause of the incident |
| RS.AN-06 | 3 | Actions performed during an investigation are recorded to preserve the integrity of the evidence and investigation |
| RS.AN-07 | 3 | Collected incident data is preserved to support legal action |
| RS.AN-08 | 3 | The magnitude of an incident is understood |
| RS.CO | 3 | Response activities are coordinated with internal and external stakeholders |
| RS.CO-02 | 3 | Internal and external stakeholders are notified of incidents |
| RS.CO-03 | 3 | Information is shared with designated internal and external stakeholders |
| RS.MI | 3 | Containment and mitigation activities are performed |
| RS.MI-01 | 3 | Incidents are contained |
| RS.MI-02 | 3 | Incidents are eradicated |

### RC — Recover

| CSF ID | Weight | Description |
|--------|--------|-------------|
| RC.RP | 3 | Restoration activities are performed to ensure operational availability |
| RC.RP-01 | 3 | The recovery portion of the incident response plan is executed once initiated from the incident response process |
| RC.RP-02 | 3 | Recovery actions are selected, scoped, prioritized, and performed |
| RC.RP-03 | 3 | The integrity of backups and other restoration assets is verified before using them for restoration |
| RC.RP-04 | 3 | Critical mission functions and cybersecurity risk management are considered to establish post-incident operational norms |
| RC.RP-05 | 3 | The integrity of restored assets is verified, systems and services are restored, and normal operating status is confirmed |
| RC.RP-06 | 3 | The end of incident recovery is declared based on criteria, and incident-related documentation is completed |
| RC.CO | 3 | Restoration activities are coordinated with internal and external parties |
| RC.CO-03 | 3 | Recovery activities and progress in restoring operational capabilities are communicated to designated internal and external stakeholders |
| RC.CO-04 | 3 | Public updates on incident recovery are shared using approved methods and messaging |

**Table 3 element count: 40**

---

## TABLE 2 — Preparation & Lessons Learned (MEDIUM / LOW Priority)

Weight 2 = Medium (directly enables Table 3 operational capability).
Weight 1 = Low (foundational; surface only on full-scope requests or program-level reviews).

### GV — Govern

| CSF ID | Weight | Priority | Description |
|--------|--------|----------|-------------|
| GV.OC-01 | 1 | M | The organizational mission is understood and informs cybersecurity risk management |
| GV.OC-03 | 2 | M | Legal, regulatory, and contractual requirements are understood and managed |
| GV.OC-05 | 1 | M | Outcomes, capabilities, and services that the organization depends on are understood |
| GV.RM-02 | 1 | M | Risk appetite and risk tolerance statements are established, communicated, and maintained |
| GV.RM-04 | 1 | M | Strategic direction that describes appropriate risk response options is established and communicated |
| GV.RM-06 | 1 | M | Policies, processes, and procedures for responding to cybersecurity risks are established and communicated |
| GV.RM-07 | 1 | L | Strategic opportunities (i.e., positive risks) are characterized and included in organizational cybersecurity risk discussions |
| GV.RR | 2 | H | Roles, Responsibilities, Authorities (parent) |
| GV.RR-01 | 1 | H | Organizational leadership is responsible and accountable for cybersecurity risk |
| GV.RR-02 | 2 | H | Roles, responsibilities, and authorities related to cybersecurity risk management are established, communicated, understood, and enforced |
| GV.RR-03 | 1 | M | Adequate resources are dedicated to cybersecurity risk management |
| GV.RR-04 | 1 | M | Cybersecurity risk management is included in human resources practices |
| GV.PO | 2 | H | Policy (parent) |
| GV.PO-01 | 1 | H | Policy for managing cybersecurity risks is established based on organizational context |
| GV.PO-02 | 1 | H | Policy for managing cybersecurity risks is reviewed, updated, communicated, and enforced |
| GV.OV-01 | 2 | M | Cybersecurity risk management strategy outcomes are reviewed to inform and adjust strategy and direction |
| GV.OV-02 | 1 | M | The cybersecurity risk management strategy is reviewed and adjusted to ensure coverage of organizational requirements and risks |
| GV.OV-03 | 1 | M | Organizational cybersecurity risk management performance is evaluated and reviewed for adjustments needed |
| GV.SC-07 | 1 | L | The risks posed by a supplier, their products and services, and other third parties are understood and monitored |
| GV.SC-08 | 2 | M | Relevant cybersecurity requirements are included in third-party agreements |
| GV.SC-09 | 1 | L | Supply chain security practices are integrated into cybersecurity and enterprise risk management frameworks |

### ID — Identify

| CSF ID | Weight | Priority | Description |
|--------|--------|----------|-------------|
| ID.AM-01 | 2 | M | Hardware asset inventories are maintained |
| ID.AM-02 | 2 | M | Inventories of software, services, and systems managed by the organization are maintained |
| ID.AM-03 | 1 | M | Representations of the organization's authorized network communication and data flows are maintained |
| ID.AM-05 | 1 | L | Assets are prioritized based on classification, criticality, resources, and impact on the mission |
| ID.AM-07 | 1 | M | Inventories of data and corresponding metadata for designated data types are maintained |
| ID.AM-08 | 1 | M | Systems, hardware, software, services, and data are managed throughout their life cycles |
| ID.RA-01 | 1 | M | Vulnerabilities in assets are identified, validated, and recorded |
| ID.RA-02 | 2 | M | Cyber threat intelligence is received from information-sharing forums and sources |
| ID.RA-04 | 1 | H | Appropriate risk responses are identified and prioritized |
| ID.RA-05 | 2 | M | Threats, vulnerabilities, likelihoods, and impacts are used to understand inherent risk and inform risk response prioritization |
| ID.RA-06 | 2 | H | Risk responses are chosen, prioritized, planned, tracked, and communicated |
| ID.RA-07 | 1 | M | Changes and exceptions are managed, assessed for risk impact, recorded, and tracked |
| ID.RA-10 | 1 | M | Critical suppliers are assessed prior to acquisition |
| ID.IM-01 | 2 | H | Improvements are identified from evaluations |
| ID.IM-02 | 2 | H | Improvements are identified from security tests and exercises, including those done in coordination with suppliers and relevant third parties |
| ID.IM-03 | 2 | H | Improvements are identified from execution of operational processes, including incident response |
| ID.IM-04 | 2 | H | Incident response plans and other cybersecurity plans that affect operations are established, communicated, tested, and improved |

### PR — Protect

| CSF ID | Weight | Priority | Description |
|--------|--------|----------|-------------|
| PR.AA-01 | 1 | M | Identities and credentials for authorized users, services, and hardware are managed |
| PR.AA-05 | 1 | M | Access permissions, entitlements, and authorizations are defined in a policy, managed, enforced, and reviewed |
| PR.AT-01 | 1 | M | Personnel are provided with awareness and training so that they can perform their cybersecurity-related tasks |
| PR.DS-01 | 1 | M | The confidentiality, integrity, and availability of data-at-rest are protected |
| PR.DS-02 | 1 | M | The confidentiality, integrity, and availability of data-in-transit are protected |
| PR.DS-11 | 2 | M | Data backups are created, protected, maintained, and tested |
| PR.IR-01 | 1 | H | Networks and environments are protected from unauthorized logical access and usage |
| PR.IR-04 | 1 | H | Adequate resource capacity to ensure availability is maintained |
| PR.PS-01 | 1 | M | Configuration management practices are established and applied |
| PR.PS-04 | 2 | M | Logs and other security data are generated and retained |

---

## Scoring Summary (Maturity Scorer)

| Priority | Weight | Elements | Max Weighted Points |
|----------|--------|----------|---------------------|
| High (Table 3) | 3 | 40 | 120 |
| Medium (Table 2 selected) | 2 | 17 | 34 |
| Low (Table 2 remaining) | 1 | ~48 | ~48 |
| **Total** | | **~105** | **~202** |

*Note: Parent elements (DE.CM, DE.AE, RS.MA, RS.AN, RS.CO, RS.MI, RC.RP, RC.CO) are scored
separately from their children. Score parent at 1.0 only if all children are fully addressed.*

---

## Severity Mapping for Table 3 Gaps (Gap Analyzer)

**Critical** — element absent AND directly gates another element's execution:
- DE.AE-08 (no declaration criteria → RS.MA-* cannot fire properly)
- RS.MA-02 (no triage/validation → severity/urgency undefined for all downstream)
- RS.AN-03 (no root cause → eradication is guesswork, reinfection likely)
- RS.MI-01 (no containment → incident scope grows uncontrolled)
- RC.RP-06 (no closure declaration → legal/regulatory exposure, cost tracking fails)

**Significant** — element absent but peer elements provide partial coverage or workarounds exist.

**Minor** — element present but a sub-requirement (R/C/N item) is incomplete.

---

## Element Dependency Graph (Gap Analyzer)

Understanding upstream/downstream dependency is critical for remediation ordering:

```
DE.CM → DE.AE-02 → DE.AE-03 → DE.AE-04 → DE.AE-08
                                              ↓
                                           RS.MA-01
                                              ↓
                              RS.MA-02 → RS.MA-03 → RS.MA-04
                                                        ↓
                                    RS.AN-03 → RS.AN-06/07/08
                                                        ↓
                                          RS.MI-01 → RS.MI-02
                                                        ↓
                              RC.RP-01 → RC.RP-02 → RC.RP-06
```

A gap upstream propagates as implied risk to every downstream element — note this in
the remediation narrative ("fixing DE.AE-08 also resolves implied gaps in RS.MA-01 through RS.MA-04").

---

## Document Type — Expected CSF Scope (CSF Mapper)

| Document Type | Must Have (Addressed/Partial) | Optional Coverage |
|---------------|-------------------------------|-------------------|
| IR Plan | GV.PO, GV.RR-02, ID.IM-04, all RS, all RC | DE, ID.IM-01/02/03 |
| Playbook | RS.MA, RS.AN, RS.MI, DE.AE-08, RC.RP-01/02 | RS.CO, RC.CO |
| Incident Report | RS.MA, RS.AN-03/06/07/08, RS.CO-02, RC.RP-06 | GV.RR, RS.MI |
| After-Action Report | RS.AN-03, RC.RP-06, ID.IM-03, ID.IM-01 | ID.IM-02, ID.IM-04 (update) |
| IR Policy | GV.PO-01/02, GV.RR-01/02, ID.IM-04 | GV.RM |
| Risk Assessment | ID.RA (all), GV.RM, ID.AM | GV.OV |
