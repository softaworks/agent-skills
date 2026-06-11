# RC.RP-06 — After-Action Report Completeness Checklist

Load this file when performing Step 1 of the AAR review workflow.

---

## Component A — The Incident

- [ ] Incident type and classification (per RS.MA-03 categorization)
- [ ] Initial detection method and timestamp (links to DE.AE)
- [ ] Timeline of significant events from first indicator to recovery completion
- [ ] Systems, data, and services affected (with asset identifiers)
- [ ] Estimated or confirmed impact (financial, operational, reputational, regulatory)
- [ ] Threat actor characterization if known (TTPs, attribution confidence level)

**Gap signal:** Report says "attacker gained access" without complete chain of events — fails RC.RP-06.R1.

---

## Component B — Response and Recovery Actions

- [ ] Triage and validation actions (RS.MA-02)
- [ ] Incident management decisions and rationale (RS.MA-03, RS.MA-04)
- [ ] Containment measures applied with timestamps (RS.MI-01)
- [ ] Eradication actions taken with verification (RS.MI-02)
- [ ] Recovery steps executed in documented order (RC.RP-02, RC.RP-04)
- [ ] Recovery completion declaration with date/time (RC.RP-06)
- [ ] Notifications sent (RS.CO-02, RS.CO-03) — timestamps AND recipients required

**Gap signal:** Recovery noted as "completed" without sequence or owner sign-off — fails RC.RP-04.R1 and RC.RP-04.R2.

---

## Component C — Lessons Learned

- [ ] What worked well (specific, not generic)
- [ ] What did not work or was delayed (with contributing factors)
- [ ] Root cause(s) — systemic, not proximate (see RS.AN-03 checklist)
- [ ] Specific, assignable improvement actions (not vague "improve monitoring")
- [ ] Owner name and deadline for each improvement action
- [ ] Which CSF Function/outcome each improvement targets

**Actionability scoring:**
- Count total lessons identified
- Count lessons with assigned owner AND specific deadline
- Actionability ratio = assigned / total (target: 100%; below 50% = critical finding)

**Gap signal:** Lessons like "improve communication" with no owner, no deadline, no measurable outcome — fails ID.IM-03.N3.
