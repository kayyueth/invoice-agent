"""End-to-end: read expenses.json + notes.md, compute totals, render docx+pdf."""
import json
import sys
from datetime import date, datetime
from pathlib import Path

from fx import convert
from numbering import next_invoice_number
from render import render

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "invoice_template.docx"
MONTHS = ROOT / "months"

SALARY_USD = 6000  # fixed monthly salary


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def build(month: str, invoice_date_str: str):
    mdir = MONTHS / month
    expenses = json.loads((mdir / "expenses.json").read_text())
    invoice_date = parse_date(invoice_date_str)

    # Convert each expense to USD using the invoice-date rate.
    total_usd_expenses = 0.0
    for e in expenses:
        usd = convert(e["amount"], e["currency"], "USD", invoice_date)
        e["usd"] = round(usd, 2)
        total_usd_expenses += usd
    total_usd_expenses = round(total_usd_expenses, 2)
    total_due = round(SALARY_USD + total_usd_expenses, 2)

    inv_no = next_invoice_number(MONTHS)
    due = invoice_date.replace(day=min(28, invoice_date.day))  # placeholder; user can edit

    mapping = {
        "{{invoice_number}}": f"{inv_no:03d}",
        "{{invoice_date}}": invoice_date.strftime("%Y.%m"),
        "{{engagement_date}}": invoice_date.strftime("%B %d, %Y"),
        "{{due_date}}": invoice_date.strftime("%B %d, %Y"),
        "{{salary_usd}}": f"{SALARY_USD:.2f}",
        "{{expense_total_usd}}": f"{total_usd_expenses:.2f}",
        "{{total_due}}": f"{total_due:.2f}",
    }

    detail_items = expenses

    out_name = (
        f"{invoice_date.strftime('%Y%m%d')} Consultancy fee kayyu_invoice_"
        f"{invoice_date.strftime('%b%d')} (USD{total_due:.2f}).docx"
    )
    out_docx = mdir / "out" / out_name
    render(TEMPLATE, out_docx, mapping, detail_items)
    print(f"Rendered: {out_docx}")
    return {"invoice_no": inv_no, "total_due": total_due, "out": str(out_docx)}


if __name__ == "__main__":
    # usage: build.py 2026-06 2026-06-28
    print(json.dumps(build(sys.argv[1], sys.argv[2]), indent=2))
