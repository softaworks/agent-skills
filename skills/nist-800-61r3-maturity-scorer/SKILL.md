---
name: nist-800-61r3-maturity-scorer
description: "Score an organization's IR program maturity against the NIST SP 800-61r3 CSF 2.0 Community Profile using a weighted scoring model tied to element priority (High/Medium/Low). Produces a per-function heatmap, weighted overall score, maturity level (1-5), and the highest-leverage improvement actions. Use when asked to 'score this against NIST', 'maturity assessment', 'how mature is our IR program', 'NIST compliance score', 'IR program score', or 'benchmark our security program'."
user-invocable: true
---

# NIST SP 800-61r3 Maturity Scorer

Score an organization's IR program maturity against the complete CSF 2.0 Community Profile from NIST SP 800-61r3 (April 2025).

---

## Mindset

Expert scoring heuristics that distinguish accurate assessments from flattering ones:

1. **Weight the operational core, not the paperwork.** Table 3 elements (DE/RS/RC) get 3x weight because an org that can't detect or respond is genuinely dangerous regardless of governance maturity. A perfect GV score with a weak DE score is Level 2 at best.

2. **Evidence beats claims.** "We have a process" is 0.5. "Here is the documented process with test results from the last 12 months" is 1.0. Self-attestation without artifacts cannot score above 0.5 on any element.

3. **The improvement loop breaks the ceiling.** No program reaches Level 4 without ID.IM-01 through ID.IM-04 fully addressed. Orgs that don't measure their IR performance cannot improve it — they are, by definition, not Managed.

4. **Parent elements are aggregates, not bonuses.** DE.CM scores 1.0 only if all DE.CM-* children are 1.0. Never score a parent element independently of its children.

5. **Partial is not progress.** A 0.5 on a weight-3 element is 1.5 points. Upgrading it to 1.0 adds 1.5 points more. Always surface these "half-finished" high-weight elements as the cheapest wins available.

---

## Navigation

**Use this skill when:**
- Asked for a maturity score, maturity level, or capability rating against NIST 800-61r3
- Benchmarking an IR program across assessment cycles (trend tracking)
- Preparing board/executive reporting on IR program state
- Input is a coverage map from `nist-800-61r3-csf-mapper` or gap report from `nist-800-61r3-gap-analyzer`

**Do NOT use this skill when:**
- The ask is about mapping coverage (use `nist-800-61r3-csf-mapper`)
- The ask is about finding specific gaps (use `nist-800-61r3-gap-analyzer`)
- The ask is about auditing specific recommendations (use `nist-800-61r3-recommendation-auditor`)

**Input decision tree:**

```
Input available?
├── Raw document only
│   └── Perform inline mapping first (Step 1), then score
├── Coverage map from csf-mapper
│   └── Read coverage scores directly → skip to Step 2
├── Gap report from gap-analyzer
│   └── Infer coverage from gaps → assign 0.0 for gaps, 1.0 for non-gaps, 0.5 for partials
├── Multiple inputs
│   └── Program mode: merge coverage maps, take minimum score per element across sources
└── No coverage data at all
    └── Prompt user for at minimum: IR policy, IR plan, detection tool inventory, incident logs
```

---

## Philosophy

The score is a navigation tool, not a destination. Its purpose is to direct finite improvement resources toward the elements with the highest operational impact — not to satisfy an auditor. A Level 3 organization that knows exactly which five elements to fix next is more valuable than a Level 4 organization that achieved the score through paperwork compliance.

---

## Goal

Produce a quantitative maturity score grounded in SP 800-61r3's own priority system. High-priority elements (all Table 3 elements) have the most weight; Medium-priority elements (Table 2 selected) have moderate weight; Low-priority elements contribute minimally. Output a score, maturity level, per-function heatmap, and the top improvement actions by ROI.

---

## Inputs

- Coverage data from any of:
  - Raw document (will map inline)
  - Coverage map from `nist-800-61r3-csf-mapper`
  - Gap report from `nist-800-61r3-gap-analyzer`
  - Recommendation audit from `nist-800-61r3-recommendation-auditor`
  - Combined inputs from multiple documents (whole-program assessment)
- Assessment mode: **Document** (single doc) or **Program** (entire IR program across multiple docs)

---

## Workflow

```
1. Determine Element Coverage
   ↓
2. Apply Weighted Scoring Model
   ↓
3. Compute Per-Function Scores
   ↓
4. Compute Overall Weighted Score
   ↓
5. Assign Maturity Level
   ↓
6. Identify High-ROI Improvements
   ↓
7. Generate Maturity Report
```

### Step 1: Determine Element Coverage

For each SP 800-61r3 element, assign a coverage score:
- **1.0** — Fully addressed (evidence is explicit and complete)
- **0.5** — Partially addressed (element present but key sub-requirements missing)
- **0.0** — Not found or absent

If working from a raw document, perform inline mapping before scoring.

### Step 2: Weighted Scoring Model

SP 800-61r3's own priority system drives the weights:

| Priority | Source | Weight |
|----------|--------|--------|
| High     | Table 3 (all DE/RS/RC elements) | 3 |
| Medium   | Table 2 selected GV/ID/PR elements | 2 |
| Low      | Table 2 remaining GV/ID/PR elements | 1 |

**Score formula per function:**
```
Function_score = Σ(element_coverage × element_weight) / Σ(element_weight)
```

**Overall weighted score:**
```
Overall = Σ(all element_coverage × element_weight) / Σ(all element_weight)
```

Full element registry with weights: `../nist-800-61r3-shared/references/csf-element-registry.md`

### Step 3: Per-Function Scores

Compute a score for each of the 6 CSF Functions independently, using only the elements belonging to that function.

Convert to percentage and render a visual bar:
```
DE (Detect)  [████████░░]  80%
RS (Respond) [██████░░░░]  60%
RC (Recover) [████████░░]  80%
GV (Govern)  [██████░░░░]  55%
ID (Identify)[████░░░░░░]  45%
PR (Protect) [████░░░░░░]  40%
```

### Step 4: Maturity Level Assignment

Map the overall weighted score to a maturity level:

| Score | Level | Name | Characterization |
|-------|-------|------|-----------------|
| 0–29% | 1 | Initial | No consistent IR practices; ad hoc and reactive |
| 30–49% | 2 | Developing | Basic IR exists but undocumented or inconsistently applied |
| 50–69% | 3 | Defined | Documented IR program; key processes established |
| 70–84% | 4 | Managed | Measured IR program; performance tracked; continuous improvement in place |
| 85–100% | 5 | Optimizing | IR integrated into all cybersecurity risk management; lessons feed back continuously |

These levels correspond loosely to CSF 2.0 Implementation Tiers 1–4 and the maturity concepts from ID.IM.

### Step 5: High-ROI Improvements

Identify the top 5 improvements with highest score impact.

For each Not Met or Partial element, compute:
- **Score uplift**: (1.0 - current_coverage) × weight / total_weighted_points
- **Dependencies unlocked**: how many other elements improve if this one is addressed

Rank by (score_uplift × 3) + (dependencies_unlocked × 2).

Common high-ROI improvements (based on typical IR programs):
1. **DE.AE-08** (incident declaration criteria) — weight 3; enables RS.MA-01 through RS.MA-05
2. **ID.IM-04** (IR plan maintenance) — weight 2; foundational for all Table 3 elements
3. **RS.AN-03** (root cause analysis) — weight 3; enables ID.IM-03 improvement loop
4. **RS.CO-02** (stakeholder notifications) — weight 3; legal/regulatory exposure reduction
5. **PR.PS-04** (log records) — weight 2; enables DE.AE-02/03/07 detection capabilities

---

## Output Format

```
╔══════════════════════════════════════════════════════════════════╗
║     NIST SP 800-61r3 IR Maturity Assessment                     ║
║     Standard: NIST SP 800-61r3 (April 2025), CSF 2.0            ║
╚══════════════════════════════════════════════════════════════════╝

Assessment Mode: [Document / Program]
Document(s): [list]
Assessment Date: [date]

━━━ MATURITY SCORE ━━━

Overall Weighted Score: 61%
┌─────────────────────────────┐
│  MATURITY LEVEL 3: DEFINED  │
│  Score range: 50–69%        │
└─────────────────────────────┘
Documented IR program exists with key processes established.
Gaps remain in continuous improvement loop and detection coverage.

━━━ PER-FUNCTION SCORES ━━━

Function     Coverage  Score  Bar
──────────── ───────── ────── ──────────────────────
DE (Detect)   11/14 el   74%  ████████████████░░░░░
RS (Respond)  15/25 el   58%  ████████████░░░░░░░░░
RC (Recover)  10/12 el   80%  ████████████████░░░░
GV (Govern)    9/18 el   50%  ██████████░░░░░░░░░░░
ID (Identify)  8/18 el   44%  █████████░░░░░░░░░░░░
PR (Protect)   7/15 el   47%  █████████░░░░░░░░░░░░

Strongest function:  RC (Recover) — 80%
Weakest function:    ID (Identify) — 44%
Table 3 (IR) score:  67%  ← primary operational readiness indicator
Table 2 (Prep) score: 47%  ← preparation and prevention readiness

━━━ ELEMENT COVERAGE DETAIL ━━━

High Priority (Table 3):  24/40 elements addressed (3 partial)
Medium Priority (Table 2): 9/17 elements addressed (2 partial)
Low Priority (Table 2):   11/48 elements addressed

━━━ TOP 5 HIGH-ROI IMPROVEMENTS ━━━

Rank  Element        Score Uplift  Dependencies  Action
────  ─────────────  ────────────  ────────────  ──────────────────────────────
 1    DE.AE-08        +3.2%         5 unlocked    Define incident declaration
                                                  criteria with false-positive
                                                  guidance
 2    RS.AN-03        +2.8%         3 unlocked    Implement RCA methodology
                                                  (5-Whys or fishbone) in all
                                                  AAR procedures
 3    ID.IM-04        +1.6%         2 unlocked    Establish formal IR plan
                                                  review cycle (annual +
                                                  post-major-incident trigger)
 4    RS.CO-02        +2.4%         0 unlocked    Document regulatory
                                                  notification obligations by
                                                  jurisdiction and sector
 5    PR.PS-04        +1.8%         4 unlocked    Implement centralized log
                                                  management covering all
                                                  SP 800-61r3 DE.CM asset types

Implementing all 5 would raise score to approximately 72% (Level 4: Managed).

━━━ BENCHMARKING ━━━

Level 3 (Defined) organizations typically:
✓ Have documented IR policies and procedures
✓ Have incident classification and triage processes
✗ Lack continuous improvement mechanisms
✗ Have gaps in detection coverage (DE elements)
✗ Do not systematically measure IR program performance

This assessment is consistent with a Level 3 organization.

━━━ TREND (if prior assessment available) ━━━
Prior score: N/A
Change: N/A
```

---

## NEVER

- **NEVER report a score without showing the per-function breakdown** — an overall score hides inverse function scores that cancel each other out; a 65% overall can mask a 30% RS score that indicates an IR program that cannot respond
- **NEVER assign Maturity Level 4 or 5 without verifying the ID.IM improvement loop (ID.IM-01 through ID.IM-04)** — measurement and continuous improvement are definitional to "Managed"; their absence makes the level assignment technically invalid regardless of score arithmetic
- **NEVER accept self-attestation as 1.0 coverage** — "we have a process" is 0.5 until documented evidence exists; inflating coverage rewards mature-sounding language over actual capability
- **NEVER round up partial coverage** — 0.5 is 0.5; upgrading a weight-3 element from 0.5 to 1.0 adds 1.5 points to the score; collapsing this difference destroys the uplift calculation
- **NEVER score parent elements independently of their children** — DE.CM is 1.0 only when all DE.CM-* children are 1.0; scoring the parent header as a bonus double-counts coverage
- **NEVER use the score as a compliance checkbox** — maturity scores measure program capability, not regulatory compliance; state explicitly that Level 4 does not equal FISMA compliance, SOC 2 readiness, or any specific regulatory posture
- **NEVER omit the Table 3 sub-score** — the Table 3 (IR operational) score is the single most important indicator of actual incident response readiness and must always be surfaced separately from the overall score

---

## When Things Go Wrong

| Situation | What It Usually Means | What to Do |
|-----------|----------------------|------------|
| Overall score is Level 4+ but Table 3 sub-score is below 70% | Governance and prep are strong, but actual IR execution is weak — the program looks good on paper but cannot respond | Flag the inversion explicitly; the Table 3 score is the operative one for operational risk |
| All elements score 0.5 (org claims partial for everything) | Assessor or org is hedging; 0.5 across the board usually means no artifacts were reviewed | Push for specific evidence artifacts; if none exist, those elements are 0.0 |
| Score drops significantly vs. prior assessment | Either the prior assessment was inflated, or a capability genuinely regressed (staff turnover, tool decommission) | Compare element-level deltas; regression in DE.CM or RS.MA elements is the most operationally dangerous |
| Input is a polished IR policy document only | Policy alone covers GV and some ID elements; DE/RS/RC will score near 0.0 without operational evidence | State clearly that a policy-only assessment reflects program design intent, not operational capability |
| ID.IM elements all score 1.0 but program is clearly Level 2 | ID.IM is self-referential — an org can write improvement policies without implementing them | Require evidence of at least one completed improvement cycle (before/after data from an AAR) |

---

## References

- `../nist-800-61r3-shared/references/csf-element-registry.md` — Full weighted element registry (High/Medium/Low), element counts, max points table. Load when computing element-level scores or presenting coverage detail.
