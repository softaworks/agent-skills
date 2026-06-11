# Worked Example: Invoice Detail Screen

This is a realistic, complete example of a backend requirements document. Notice:
- No field names, endpoint paths, or JSON structures
- Every data need has a "why"
- States are fully specified
- Business rules are flagged even when uncertain
- Open questions are specific and invite real discussion

---

```markdown
# Backend Requirements: Invoice Detail Screen

**Author**: Frontend team
**Date**: 2025-03-14
**Status**: Draft — awaiting backend review

## Context

We're building an invoice detail view for billing administrators. When a billing admin
clicks an invoice in the invoice list, they land here. The goal is to let them review
what was charged, why, and take action (download, dispute, mark as paid). This is
admin-only — regular users can't reach this screen.

## Screens / Components

### Invoice Detail Page

**Purpose**: Show a single invoice in full, with enough context to understand and act on it.

**Data I need to display**:

- Invoice identity: something that lets the admin identify this invoice at a glance — a
  number, a date range, and who it's for (account name)
- Line items: each thing being charged — a human-readable description of what it is,
  the quantity, the unit price, and the line total. There could be anywhere from 1 to
  ~50 line items.
- Subtotal, any taxes or fees, and the total. I'm not sure if taxes are stored per line
  or per invoice — flagged in Uncertainties.
- Invoice status: whether it's paid, overdue, disputed, or pending. The UI changes
  significantly based on this.
- Payment history: if payments have been made against this invoice (partial payments are
  allowed, I think?), I need to show those with dates and amounts.
- Who issued the invoice (the org/entity on our side) and who it was issued to (the
  customer). Both need enough info to appear on a legal document — name, address,
  possibly tax ID.

**Actions the user can perform**:

- Download as PDF → User sees a "downloading" spinner, then browser download starts.
  The PDF should look like a formal invoice (assume backend generates it).
- Dispute invoice → Opens a confirmation modal, user submits a reason. After submit:
  invoice status changes to "disputed" and admin sees a success toast. Not sure if this
  triggers an email automatically — flagged below.
- Mark as paid (only if status is "pending" or "overdue") → Confirmation modal with
  payment date picker. After confirm: status updates to "paid", payment record appears
  in payment history.
- Download payment receipts (per payment, if payments exist) → Similar to PDF download.

**States I need to handle**:

- **Loading**: Full page skeleton while invoice loads. Line items area is the slowest
  part visually — consider if line items can be deferred.
- **Empty (no line items)**: Shouldn't happen, but if it does, show a message rather
  than an empty table.
- **Error**: If the invoice fails to load, show an error with a retry button. Don't
  show a partial invoice — that's worse than an error.
- **Not found**: If the invoice ID is invalid or the admin doesn't have access, show
  a 404-style message. Don't expose whether the invoice exists but is inaccessible.
- **Disputed state**: Most actions are disabled. Admin can only see the invoice and
  contact support. I need to know what "disputed" blocks.
- **Partial payment**: Invoice shows as partially paid. Payment history shows multiple
  entries. Remaining balance visible. I'm not sure what the status label should be —
  "partially paid"? Flagged.

**Business rules affecting UI**:

- Only billing admins can reach this page — assume auth is enforced server-side, but I
  need the API to return a clear "unauthorized" vs "not found" so I can show the right
  message.
- Dispute action should only be available within 30 days of invoice date (I think?).
  Not sure — please confirm. If correct, I need to know the invoice date to compute this
  client-side, or I'd prefer the API tell me whether the action is available.
- Mark-as-paid should only appear for "pending" and "overdue" statuses. I'll hide it
  for others.
- Tax line may only appear in certain jurisdictions — I'll conditionally render it, but
  I need to know if "no tax" means zero or means the field is absent.

---

## Uncertainties

- [ ] Are taxes stored per line item or as a single invoice-level value? I'm building
  the UI assuming invoice-level, but it may need to change.
- [ ] Can invoices be partially paid? I'm assuming yes based on product context but
  haven't confirmed. If yes, what's the status label for a partially paid invoice?
- [ ] Does disputing an invoice trigger a notification to the customer automatically,
  or does the admin need to do that separately? Affects the confirmation modal copy.
- [ ] Is the 30-day dispute window enforced server-side (API rejects it) or do I need
  to compute it client-side and hide the button? Prefer server-side enforcement so the
  UI can't get out of sync.
- [ ] What does "not authorized to view this invoice" look like from the API — a 403
  or a 404? I need to know to show the right message.

## Questions for Backend

- The line items table could have up to 50 rows. Is there a case where it could be
  hundreds? If so, should I plan for pagination or virtualization?
- Would it be possible to include an "available actions" list in the invoice response
  (e.g., `["download", "dispute"]`) rather than me computing action availability from
  status + date? It would make the UI more resilient to rule changes.
- Is the PDF generated on the fly or pre-generated and stored? Affects loading UX — if
  it's generated on the fly, I need a longer loading indicator for large invoices.
- Is payment history always inline with the invoice, or is it a separate resource?
  Would prefer it inline if possible to avoid a second request.

## Discussion Log

| Date | From | Note |
|------|------|------|
| 2025-03-15 | Backend (Sam) | Taxes are invoice-level, not per-line. Zero tax = field present with value 0, not absent. |
| 2025-03-15 | Backend (Sam) | Partial payments supported. Status for partial = "partially_paid" — we can add that label. |
| 2025-03-16 | Frontend | Updated states section to include partially_paid. Removed uncertainty. |
| 2025-03-16 | Backend (Sam) | Dispute window enforced server-side. API returns 409 with reason if window has passed. Available actions list is a good idea — will include in response. |
```

---

## What Makes This Good

- **No field names** — "invoice identity" not "invoice_number". "Who it was issued to" not "customer_id".
- **Every data need has context** — "enough info to appear on a legal document" tells backend why it matters.
- **States are fully specified** — including what to do when invoice loads but is in an unusual state.
- **Business rules are flagged even when uncertain** — "I think?" is better than assuming.
- **Questions are specific and invite real decisions** — "would it be possible to include an available actions list?" is a design suggestion, not a demand.
- **Discussion Log is populated** — shows the document is a living negotiation, not a one-way spec.
