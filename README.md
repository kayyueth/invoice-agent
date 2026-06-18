# Invoice Agent

Personal tool for generating monthly consultancy invoice (salary + reimbursement) from receipts.

## Setup

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then put your Word template at `templates/invoice_template.docx` with these placeholders:

- `{{invoice_number}}`, `{{invoice_date}}`, `{{engagement_date}}`, `{{due_date}}`
- `{{salary_usd}}`, `{{expense_total_usd}}`, `{{total_due}}`
- Detail table: header row + **one sample row** (any values) — the sample row will be cloned and replaced with real expense rows.

## Monthly workflow

```
months/2026-06/
  receipts/   # drop screenshots / PDFs here
  notes.md    # 2026-06-03 ~ 2026-06-09: SZ Hardware Scouting
```

Then in Claude Code: `/invoice 2026-06`

The agent will:
1. OCR receipts → `expenses.json`
2. Pause for you to review / merge rows
3. Render `.docx`, then `.pdf` after you confirm
