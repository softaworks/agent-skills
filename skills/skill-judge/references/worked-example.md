# Worked Example: Evaluating a Real Skill

This walks through a complete evaluation of a hypothetical `pdf-processor` skill to calibrate scoring judgment.

---

## Skill Under Evaluation (excerpt)

```markdown
---
name: pdf-processor
description: Process PDF files
---

# PDF Processor

This skill helps you work with PDF files.

## What is a PDF?
PDF (Portable Document Format) is a file format developed by Adobe...

## Installation
Install PyMuPDF: pip install PyMuPDF

## Step by Step
1. Open the PDF file
2. Read the contents
3. Extract what you need
4. Save results

## NEVER
- Don't break things
- Be careful with large files
```

---

## Evaluation Walk-Through

### Step 1: Knowledge Delta Scan

Mark each section:
- "What is a PDF?" → **[R] Redundant** — Claude definitely knows this
- "Installation: pip install PyMuPDF" → **[A] Activation** — acceptable reminder
- "Step by Step: Open, Read, Extract, Save" → **[R] Redundant** — generic, Claude knows
- "NEVER: Don't break things" → **[R] Redundant** — vague, no value

Knowledge ratio: E:0 / A:1 / R:3 — catastrophic ratio

### Step 2: Structure Analysis
```
[ ] frontmatter validity — PASS (valid YAML)
[ ] line count — 18 lines (good length, bad content)
[ ] reference files — none
[ ] pattern — attempts Tool but lacks decision trees
[ ] loading triggers — N/A
```

### Step 3: Dimension Scores

| Dimension | Score | Justification |
|-----------|-------|---------------|
| D1: Knowledge Delta | 2/20 | "What is PDF" section, generic steps — pure redundancy |
| D2: Mindset + Procedures | 3/15 | No thinking frameworks; generic file I/O steps only |
| D3: Anti-Pattern Quality | 1/15 | "Don't break things" — maximum vagueness, zero expert insight |
| D4: Spec Compliance | 5/15 | Valid frontmatter; description "Process PDF files" has WHAT but no WHEN, no keywords |
| D5: Progressive Disclosure | 12/15 | Short file; no references needed at this size (bonus for brevity, penalty for no triggers) |
| D6: Freedom Calibration | 6/15 | Tool-type skill should have low freedom; vague guidance is wrong direction |
| D7: Pattern Recognition | 3/10 | Attempts Tool pattern but lacks the defining element: decision trees |
| D8: Practical Usability | 2/15 | No decision trees, no fallbacks, no error handling, no edge cases |

**Total: 34/120 (28%) — F**

---

## What a Fixed Version Looks Like

### Fixed description:
```yaml
description: "Extract text, tables, and images from PDF files using PyMuPDF and
camelot-py. Use when processing scanned PDFs (needs OCR), extracting tables,
handling encrypted files, or preserving layout information from .pdf documents."
```

### Fixed D1 content (expert knowledge, not basics):
```markdown
## Tool Selection Decision Tree

| Task | Primary Tool | Fallback | When to Use Fallback |
|------|-------------|----------|----------------------|
| Extract text | pdftotext | PyMuPDF | Need page coordinates |
| Extract tables | camelot-py | tabula-py | camelot fails on lattice |
| Scanned PDF | pytesseract | easyocr | tesseract accuracy <70% |
| Encrypted | PyMuPDF + password | pikepdf | unknown encryption type |
```

### Fixed D3 content (expert anti-patterns):
```markdown
## NEVER
- NEVER use pdftotext on scanned PDFs — it returns empty strings silently;
  you won't know it failed until you see blank output downstream
- NEVER use camelot on borderless tables — it requires visible grid lines;
  use tabula-py instead which handles whitespace-delimited tables
- NEVER decrypt a PDF then re-encrypt with the same password and assume
  it preserved permissions — re-encryption resets all permission flags
- NEVER call text extraction on password-protected files without catching
  PdfReadError — the error message varies by library version
- NEVER assume page count from filename — multi-part PDFs often have
  misleading names; always call len(doc) before iterating
```

---

## Calibration Notes

This example demonstrates:
- A 2/20 D1 score (pure redundancy)
- A 1/15 D3 score (vague warnings)
- How specific, experience-derived anti-patterns look vs vague warnings
- How a decision tree transforms D8 from 2 to 13+

Use this as your anchor when uncertain whether a real skill's content qualifies as Expert vs Redundant.
