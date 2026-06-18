---
name: invoice
description: Generate monthly consultancy invoice + expense report from receipts and notes. Triggers when user runs /invoice <YYYY-MM>.
---

# Invoice generation flow

Input: a month folder under `months/<YYYY-MM>/` containing:
- `receipts/` — receipt images / PDFs
- `notes.md` — date-range work purposes, one per line, e.g. `2026-06-03 ~ 2026-06-09: SZ Hardware Scouting`

Output: filled `.docx` + `.pdf` under `months/<YYYY-MM>/out/`.

## Steps you (the agent) must follow

1. **Read every file in `receipts/`** using your vision capability. For each receipt extract:
   `{date: YYYY-MM-DD, category, amount, currency, payment_method, description}`
   Categories: Flight, Hotel, Taxi, Food, Meeting Room, Other. One row per receipt — do NOT pre-merge taxis.

2. **Read `notes.md`** and assign each expense a `work_purpose` by matching its date against the date ranges. Also set `unit: 1`.

3. **Write `months/<YYYY-MM>/expenses.json`** with the array. Show the user a compact table and pause: ask whether to merge any rows (e.g. taxis into one line) before rendering.

4. After user confirms, run:
   ```
   python lib/build.py <YYYY-MM> <invoice-date YYYY-MM-DD>
   ```
   Output is a `.docx` under `months/<YYYY-MM>/out/`. The user submits the docx directly — no PDF step.

## Salary
Fixed US$6000/month. Hard-coded in `lib/build.py` — change there if it changes.

## FX
Frankfurter (ECB), rate of the invoice date. Weekends fall back to the prior weekday automatically.

## Invoice numbering
Auto-incremented by scanning `months/*/out/*.docx` filenames for `invoice_NNN` patterns.
