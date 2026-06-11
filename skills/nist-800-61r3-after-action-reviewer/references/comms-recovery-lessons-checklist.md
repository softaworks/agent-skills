# RS.CO / RC.RP / ID.IM-03 — Communications, Recovery & Lessons Checklists

Load this file when performing Steps 4–6 of the AAR review workflow.

---

## RS.CO-02/03 — Communication Retrospective

### RS.CO-02.R2 — Internal Notifications
"Follow established procedures concerning incident coordination: what must be reported, to whom, and at what times."

- [ ] Required internal notifications made: leadership, legal, HR, asset owners, privacy officer
- [ ] Notification timestamps documented for each recipient group
- [ ] Any missed or delayed notifications acknowledged with reason

### RS.CO-02.R3 — Regulatory Notifications
"Perform notifications in compliance with incident notification laws/regulations."

- [ ] Regulatory/legal notification obligations assessed (HIPAA, GDPR, PCI-DSS, state breach laws, SEC, CISA, etc.)
- [ ] If triggered: notifications sent within required timeframes with timestamps
- [ ] If not triggered: decision explicitly documented with rationale (not just silence)

**Practitioner trap:** An AAR that is silent on regulatory notification is not compliant — the decision must be documented either way.

### RS.CO-02.R5 — Law Enforcement
"Notify law enforcement and regulatory bodies per criteria in IR plan."

- [ ] Law enforcement notification considered and decision documented
- [ ] If notified: agency, date, case number documented
- [ ] If not notified: rationale documented (not critical infrastructure, no criminal nexus, etc.)

### RS.CO-03.R2 — Senior Leadership Updates (Major Incidents)
"Regularly update senior leadership on status of major incidents."

- [ ] (Major incidents only) Leadership update log exists with dates and content summary
- [ ] Escalation criteria from IR plan referenced

---

## RC.RP-04/05 — Recovery Verification

### RC.RP-04.R1 — Restoration Sequence
"Validate that essential services are restored in the appropriate order."

- [ ] Restoration sequence documented with prioritization rationale
- [ ] Critical services confirmed restored before non-critical
- [ ] Sequence matches BCP/DRP priority tiers if those exist

### RC.RP-04.R2 — Owner Confirmation
"Work with system owners to confirm successful restoration and return to normal operations."

- [ ] System owner sign-off documented (written, not just verbal)
- [ ] Each restored system has a named owner confirmation

### RC.RP-04.R3 — Post-Recovery Monitoring
"Monitor performance of restored systems to verify adequacy of restoration."

- [ ] Post-recovery monitoring period defined and executed
- [ ] Anomalies detected post-restoration documented (or explicit "none detected")

### RC.RP-05.R1 — Pre-Production IoC Scan
"Check restored assets for IoCs; remediate root causes before production use."

- [ ] Restored systems scanned for IoCs before going back online
- [ ] Root causes confirmed remediated before production restoration
- [ ] Scan results documented

### RC.RP-05.R2 — Pre-Production Verification
"Verify correctness and adequacy of restoration actions before putting restored system online."

- [ ] Pre-production verification step explicitly documented
- [ ] Verification method (automated scan, manual inspection, integrity check) noted

---

## ID.IM-03 — Lessons-Learned Loop Closure

### ID.IM-03.N3 — Meeting and Follow-Up
"Creating follow-up reports or holding 'lessons learned' meetings when an incident's recovery efforts are concluding, especially if the incident was major."

- [ ] Lessons-learned meeting held: date, attendees, facilitator documented
- [ ] Follow-up report or this AAR serves as the documented output

### ID.IM-03.N2 — Program Improvement Scope
"Improvements that affect IR can be made to the IR program itself or to other aspects of cybersecurity risk management."

- [ ] At least one improvement targets IR program changes (plan, policy, procedures) — not only technical fixes
- [ ] At least one lesson feeds back to Preparation functions (GV, ID, PR)
- [ ] All improvement actions are SMART: Specific, Measurable, Assignable, Realistic, Time-bound
- [ ] Tracking mechanism identified for improvement actions (ticket system, roadmap item, etc.)

**Actionability scoring formula:**
- Actionability % = (lessons with owner AND deadline) / (total lessons) × 100
- 100% = fully actionable
- 50–99% = partially actionable (note unassigned items)
- Below 50% = critical finding (lessons captured but not actioned)
- 0% = AAR will not improve the program — this is the most common critical finding
