---
name: invoice-maker
description: >-
  Generates freelance instructor invoices from calendar and template. ON HOLD
  until user provides invoice template. Use only after template is added to
  config/invoicing/.
---

# Invoice Maker (on hold)

**Status:** Waiting for invoice template from user.

## When ready

1. User adds template to `config/invoicing/template.docx` (or `.xlsx`)
2. User adds rate card to `config/invoicing/rates.yaml`
3. Enable calendar read (Google Calendar export or manual session list)

## Planned workflow

```
- [ ] Pull teaching sessions from calendar (date, course, hours)
- [ ] Match to cohort config for client/billing entity
- [ ] Fill template fields
- [ ] Output PDF + tracking row in data/invoices.csv
```

## Placeholder config

```yaml
# config/invoicing/rates.yaml (future)
client: Scaler SST
hourly_rate: TBD
currency: INR
```

Do not run until user says template is ready.
