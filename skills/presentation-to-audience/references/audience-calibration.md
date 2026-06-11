# Audience Calibration

## The Single-Question Test

Before writing a single slide, answer this:

> **"What decision does this audience need to make, and when?"**

Every piece of content in the presentation is either moving toward that answer or it is not. Content that does not serve the decision is not "nice to have" — it is a tax on the audience's attention that they will charge against your credibility.

If you cannot answer the single-question test, you are not ready to build the deck. You need more information about the audience or the context, not more slides.

---

## Audience Type Diagnostics

Use these questions when the user hasn't clearly identified their audience type:

**1. What authority does this audience have?**
- Approval authority over budget, headcount, or direction → Executive arc
- Technical validation authority (they can say "this won't work") → Technical arc
- Political or stakeholder authority (they can block but not build) → SCR arc
- No formal authority, informational only → Use whatever arc fits their background

**2. What is their information diet?**
- They read dashboards and summaries → lead with conclusion (Executive arc)
- They read technical specs and primary data → lead with problem and methodology (Technical arc)
- They read reports with competing perspectives → build shared ground first (SCR arc)

**3. What is their prior disposition toward your conclusion?**
- Aligned or neutral → any arc works; use Executive or Technical based on (1) and (2)
- Mildly skeptical → Technical arc with strong proof section
- Actively hostile or politically opposed → SCR is mandatory; all other arcs give them a foothold to reject the premise

**4. How much time do they have?**
- Under 20 minutes → Executive arc; maximum 7 slides; appendix for everything else
- 30–60 minutes with Q&A → Technical or SCR arc; 12–18 slides; Q&A budget = 1/3 of total time
- Workshop or working session → Not a presentation, different tool; break into segments

---

## Multi-Stakeholder Presentations

When one presentation must serve multiple audience types simultaneously (e.g., a CPO and a principal engineer in the same room):

**The layered deck technique**:
- Slides 1–5: Vision/conclusion layer (serves the exec; tolerates technical skepticism)
- Slides 6–12: Evidence/methodology layer (serves the technical audience; provides the proof that makes the exec comfortable)
- Appendix: Deep technical detail (available if asked; never shown unless requested)

The exec exits after slide 5 satisfied. The technical audience stays for slides 6–12. This only works if the layers are explicitly separated — mixing them produces a deck that satisfies neither.

**Seating-aware delivery**: In a room with mixed stakeholders, make eye contact toward executives when delivering conclusion slides; shift to technical peers when delivering evidence slides. Both audiences feel the deck was built for them.

---

## The Content Triage Matrix

Apply to every candidate slide before including it:

| Does this slide... | If YES | If NO |
|-------------------|--------|-------|
| Directly answer the audience's core decision question? | Include | Evaluate further |
| Create necessary context for a later slide that does answer the question? | Include (but minimize) | Delete |
| Provide evidence the audience will ask for in Q&A? | Move to appendix | Delete |
| Show your work in a way the audience isn't qualified to evaluate? | Delete | N/A |
| Exist because you feel proud of the analysis? | Delete | N/A |

**The hardest deletion**: Slides that represent genuine analytical effort but don't serve the audience's decision. These are the slides the presenter most wants to keep and the audience least wants to see. Delete them. Move them to the appendix if you can't let go.

---

## Calibrating Data Density

Different audiences have different signal/noise thresholds for quantitative content:

**Executive audience**: 1–2 numbers per slide maximum. Each number needs a unit, a comparison point (vs. last period, vs. target, vs. competitor), and a one-line "what this means" statement. Raw data tables are never appropriate.

**Technical audience**: Can handle 4–6 data points per slide if they are organized and labeled. Still applies the cognitive load rule — the organization must be instantly parseable (grouped, ranked, or sequenced), not left to the viewer to sort.

**Mixed audience**: Calibrate to the technical floor, not the executive floor. Executives can skim data they don't need; non-technical stakeholders cannot extrapolate from data they lack the context to interpret.

---

## Visualization Selection Guide

Choosing the wrong chart type is not an aesthetic error — it is a communication error that forces the audience to do work you should have done.

| You want to show | Use | Never use |
|-----------------|-----|-----------|
| Comparison across categories | Bar chart (horizontal for long labels) | Pie chart |
| Change over time | Line chart | Bar chart (implies discrete, not continuous) |
| Relationship between two variables | Scatter plot | Line chart (implies time) |
| Part-to-whole (max 3 parts, none under 10%) | Pie chart | Stacked bar with many segments |
| Distribution | Histogram or box plot | Average alone (hides variance) |
| Single number that matters | Large typographic call-out | Any chart |
| Geographic variation | Choropleth map | Bar chart (loses spatial relationships) |

**The common pie chart mistake**: Pie charts are only valid when the parts sum to a meaningful whole, there are at most 3 segments, and no segment is under ~10%. A 5-segment pie chart with a 4% sliver requires a legend, cannot be read from a screen, and should always be replaced with a ranked bar chart.

**The common bar chart mistake**: Using a bar chart for time-series data implies the values are discrete (Q1, Q2, Q3) rather than continuous. If the underlying reality is continuous change over time, a line chart is accurate; a bar chart is technically a misrepresentation.
