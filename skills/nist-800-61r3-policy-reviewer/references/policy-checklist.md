# NIST SP 800-61r3 §2.3 Policy Element Checklist

Full checklist used by the policy reviewer. Load this when conducting element-by-element reviews.

---

## Section 2.3 — Required Policy Elements

| # | Element | CSF Anchor | Common Failure Mode |
|---|---------|-----------|-------------------|
| 1 | Statement of management commitment | GV.RR-01 | Signature present but no resource commitment referenced |
| 2 | Purpose and objectives | GV.PO | Generic boilerplate with no org-specific mission tie |
| 3 | Scope (who/what/when it applies) | GV.PO | Omits cloud environments or contractor systems |
| 4 | Definitions: event, adverse event, cybersecurity incident, investigation | DE.AE-08 | "Incident" used generically without CIA-jeopardy distinction |
| 5 | Roles, responsibilities, and authorities (including confiscation/disconnect/shutdown) | GV.RR-02 | Roles named but authority to act never explicitly designated |
| 6 | Prioritization, severity, recovery, and key action guidelines | RS.MA-03, RS.MA-05 | Severity tiers defined but recovery initiation criteria absent |
| 7 | Performance measures | ID.IM-01 | Entirely absent — most common critical gap |
| 8 | Shared responsibility with third parties (if applicable) | GV.SC-08, GV.RR-02 | Acknowledged but no authority limits on MSSP actions |

### Element-by-Element Detailed Checks

**Element 1 — Management Commitment**
- Is there a signed/dated endorsement from executive leadership?
- Does it reference resource allocation for IR (FTE, budget, tools)?
- CSF: GV.RR-01 — "Organizational leadership is responsible and accountable for cybersecurity risk"

**Element 2 — Purpose and Objectives**
- Does the policy state why it exists (impact reduction, effectiveness improvement)?
- Does it align to the org's mission or regulatory obligations?

**Element 3 — Scope**
- Who is in scope? (employees, contractors, third parties)
- What environments? (cloud, on-prem, OT/ICS, mobile, remote work)
- Are exclusions documented and reasoned?

**Element 4 — Definitions**
- Are "event," "adverse event," and "cybersecurity incident" defined per SP 800-61r3 Appendix B?
- Is "incident" clearly distinguished from "event" (incidents jeopardize CIA or constitute policy violations)?
- Are investigation-related terms (evidence, chain of custody) defined?
- CSF: DE.AE-08

**Element 5 — Roles, Responsibilities, and Authorities**
- Are IR roles explicitly named: incident lead, handlers, legal, HR, comms, leadership?
- Does the policy designate which specific roles have authority to:
  - Confiscate assets
  - Disconnect systems from the network
  - Shut down technology assets
  - Engage law enforcement
  - Invoke BCP/DRP
- Are third-party roles (MSSP, CSP, law enforcement) addressed?
- CSF: GV.RR-02.R1, GV.RR-02.R2

**Element 6 — Prioritization, Severity, and Recovery Guidelines**
- Are severity/priority tiers defined (e.g., P1–P4 or Critical/High/Medium/Low)?
- Are risk evaluation factors listed? SP 800-61r3 RS.MA.N2 factors: asset criticality, functional impact, data impact, stage of observed activity, threat actor characterization, recoverability
- Are recovery initiation criteria defined? (RS.MA-05.R1)
- Are time-based response SLAs included?

**Element 7 — Performance Measures**
- Are IR program performance metrics defined?
- Minimum acceptable metrics: MTTD, MTTR, % incidents within SLA, % staff IR-trained annually
- Is there a review cycle for measuring performance against these metrics?
- CSF: ID.IM-01.R1 — "Periodically evaluate IR program performance to identify problems"

**Element 8 — Shared Responsibility Model**
- If the org uses MSSPs/CSPs/ISPs: are their responsibilities documented?
- Are contracts/SLAs referenced?
- Are information flow and coordination authorities defined?
- Are restrictions on third-party actions documented (e.g., MSSP cannot share sanitized incident data with other customers)?
- CSF: GV.SC-08, GV.RR-02.R3

---

## Roles & Authorities Deep Check (GV.RR-02)

**R1 — All IR roles documented in organizational policies:**
- [ ] Incident Response Team / SOC roles documented
- [ ] Legal counsel role in IR documented
- [ ] HR role documented — specifically scoped to insider threat (RS.CO-03.R3)
- [ ] Public affairs / media relations role documented
- [ ] Physical security and facilities role documented
- [ ] Asset owners role documented
- [ ] Leadership decision authority documented

**R2 — All appropriate individuals designated the authority to fulfill IR responsibilities:**
- [ ] Named or role-titled individuals with authority to isolate/disconnect systems
- [ ] Named or role-titled individuals with authority to invoke BCP
- [ ] Named or role-titled individuals with authority to engage law enforcement
- [ ] Escalation/elevation triggers and authority chain documented (RS.MA-04)

---

## Plan Framework Check (ID.IM-04)

SP 800-61r3 ID.IM-04 has four requirements for all cybersecurity plans:

| Req | Check | Common Finding |
|-----|-------|----------------|
| R1 | BCP/DRP aligned with IR plan | "Referenced" but not formally linked or exercised together |
| R2 | Plans reviewed/updated periodically or post-significant-change | Annual cycle stated but no post-incident trigger |
| R3 | Plans tailored to org's unique requirements, mission, size | Generic NIST template with org name substituted |
| R4 | Plans identify resources and management support needed | "Resources as needed" boilerplate — no specifics |

---

## Regulatory & Notification Check (GV.OC-03)

GV.OC-03.R1 — Cybersecurity requirements include all IR-related requirements (incident notification, data breach reporting).

**By organization type:**

| Org Type | Key Regulations to Check |
|----------|--------------------------|
| Federal agency | FISMA 2014, OMB M-22-01 (72-hour CISA notification), US-CERT mandatory reporting |
| Healthcare | HIPAA Breach Notification Rule (60-day), HHS reporting |
| Financial | GLBA, NY DFS Part 500 (72-hour), SEC Rule 10-D1 |
| Critical infrastructure | CISA CIRCIA (72-hour report / 24-hour ransom payment) |
| EU operations | GDPR Article 33 (72-hour supervisory authority) |
| Payment card | PCI-DSS 12.10.7 — immediate notification to brands |

- [ ] Breach notification timelines addressed (RS.CO-02.R3)
- [ ] Law enforcement notification criteria defined (RS.CO-02.R5)
- [ ] Regulatory body notification criteria defined
