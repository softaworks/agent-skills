---
name: soar-purple-team
description: ATT&CK technique → SOAR playbook coverage matrix. Use when validating whether a specific ATT&CK technique ID is detected and contained by existing pb_* playbooks across all 7 SOAR platforms, or when performing purple-team coverage gap analysis. Seeded from penetration-tester agent knowledge + all 85 pb_* playbooks.
---

# SOAR Purple Team — ATT&CK Coverage Validator

## Purpose
Map ATT&CK technique IDs to the pb_* playbooks that claim to detect or contain them, then surface coverage gaps where no playbook handles a given technique.

## Coverage Matrix (pb_01–pb_85, key techniques)

| ATT&CK Technique | Sub-technique | Primary Playbook(s) | Platforms | Gap? |
|-----------------|--------------|---------------------|-----------|------|
| T1566 | T1566.001 Spearphishing | pb_01_phishing, pb_17_bec | All 7 | No |
| T1486 | — Ransomware/Encrypt | pb_02_ransomware | All 7 | No |
| T1059 | T1059.001 PowerShell | pb_11_suspicious_script, pb_39_lolbin | All 7 | No |
| T1110 | T1110.001/003/004 Brute Force | pb_04_brute_force | All 7 | No |
| T1078 | — Valid Accounts | pb_05_account_compromise, pb_06_impossible_travel | All 7 | No |
| T1548 | T1548.002 UAC Bypass | pb_07_privilege_escalation | All 7 | No |
| T1041 | — Exfil over C2 | pb_08_data_exfiltration | All 7 | No |
| T1071 | T1071.001 Web Protocol C2 | pb_13_c2_communication | All 7 | No |
| T1558 | T1558.003 Kerberoasting | pb_70_large_scale_compromise, pb_79_kerberoast_admin | All 7 | No |
| T1003 | T1003.006 DCSync | pb_70_large_scale_compromise, pb_85_ad_full_assessment | All 7 | No |
| T1556 | T1556.006 SID History | pb_77_ad_sid_history_backdoor | All 7 | No |
| T1484 | T1484.001 GPO Modification | pb_80_gpo_acl_tampering | All 7 | No |
| T1543 | T1543.003 Windows Service | pb_65_persistence_investigation | All 7 | No |
| T1190 | — Exploit Public-Facing | pb_18_exploit, pb_24_zero_day | All 7 | No |
| T1195 | T1195.002 Supply Chain SW | pb_32_supply_chain_attack | All 7 | No |
| T1040 | — Network Sniffing | pb_34_network_discovery | All 7 | No |
| T1071 | T1071.004 DNS C2 | pb_25_dns_tunneling | All 7 | No |
| T1134 | T1134.001 Token Impersonation | pb_70_large_scale_compromise | All 7 | Partial |
| T1562 | T1562.001 Disable Security Tools | pb_20_log_clearing | All 7 | Partial |
| T1601 | T1601.001 Patch System Image | pb_45_rootkit_bootkit | All 7 | Partial |
| T1657 | — Financial Theft | **NONE** | — | **GAP** |
| T1611 | — Escape to Host (container) | pb_61_container_k8s | All 7 | No |
| T1588 | T1588.006 Vulnerabilities | pb_55_vulnerability_triage | All 7 | No |
| T1046 | — Network Service Discovery | pb_50_unauthorized_scanning | All 7 | No |

## Gap Categories

### Confirmed Coverage Gaps (no pb_* handles)
- **T1657 Financial Theft** — no playbook covers fraudulent wire transfer / payment manipulation
- **T1649 Steal or Forge Authentication Certificates** — ADCS abuse; partially related to pb_79/pb_85 but no dedicated playbook
- **T1621 MFA Request Generation** (MFA fatigue/push bombing) — pb_26 covers MFA bypass but not fatigue specifically

### Partial Coverage (1 platform or 1 phase only)
- **T1134.001 Token Impersonation** — only in pb_70 large-scale; no dedicated standalone playbook
- **T1562.001 Disable Security Tools** — pb_20 covers log clearing but not EDR/AV disabling

## Usage
1. Look up technique ID in matrix above
2. If covered: load the named pb_* playbook design IR for detection/containment specifics
3. If **GAP**: this is a candidate for new playbook authorship — use `soar-ir-engineer` with technique ID as seed
4. For purple-team exercise: run the uncovered technique; confirm no alert fires; prioritize for new pb_* authorship

## NEVER
- NEVER claim coverage based on MITRE tags in `metadata.mitre_techniques` alone — verify the playbook has actual detection and containment tasks for the technique, not just the tag
- NEVER treat "partial coverage" as full coverage in a compliance report
- NEVER add a technique to this matrix without confirming the named playbook's `workflow_ir.json` contains tasks aligned to that technique's attack pattern
