"""Find next invoice number by scanning past months/*/out/ filenames."""
import re
from pathlib import Path


def next_invoice_number(months_dir: Path) -> int:
    max_n = 0
    for docx in months_dir.glob("*/out/*.docx"):
        m = re.search(r"invoice[_#-]?(\d{1,4})", docx.stem, re.IGNORECASE)
        if m:
            max_n = max(max_n, int(m.group(1)))
    # Also scan a sidecar meta file if present
    for meta in months_dir.glob("*/invoice_meta.txt"):
        try:
            n = int(meta.read_text().strip())
            max_n = max(max_n, n)
        except ValueError:
            pass
    return max_n + 1
