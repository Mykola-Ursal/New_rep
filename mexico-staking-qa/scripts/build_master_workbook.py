#!/usr/bin/env python3
"""Combine the Mexico Staking QA CSV checklists into a single Excel workbook.

Reads each checklist CSV from `mexico-staking-qa/csv/` (columns vary per file,
e.g. `Title;How to test;Expected Result` or `Title;Category;How to test;
Expected Result`) and produces `Mexico_Staking_QA_Master.xlsx` with:

- one worksheet per checklist, using each CSV's own columns plus added
  `Status` and `Priority` columns,
- a `Summary` worksheet with per-checklist case counts and an overall status
  breakdown once statuses are filled in.

Usage:
    python3 scripts/build_master_workbook.py
"""
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent.parent
CSV_DIR = ROOT / "csv"
OUTPUT_PATH = ROOT / "Mexico_Staking_QA_Master.xlsx"

CHECKLISTS = [
    ("Smoke Fast", "mexico_smoke_fast.csv"),
    ("Break It Tonight", "mexico_break_it_tonight.csv"),
    ("Solana Specific", "mexico_solana_specific.csv"),
    ("Unstake Deep Dive", "mexico_unstake_deep_dive.csv"),
]

STATUS_OPTIONS = ["Not tested", "Passed", "Failed", "Blocked", "Skipped"]
PRIORITY_OPTIONS = ["P0", "P1", "P2", "P3"]

HEADER_FILL = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True)
WRAP = Alignment(wrap_text=True, vertical="top")


def read_checklist(filename: str) -> tuple[list[str], list[dict]]:
    path = CSV_DIR / filename
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        return list(reader.fieldnames or []), list(reader)


def style_header(ws, ncols: int):
    for col in range(1, ncols + 1):
        cell = ws.cell(row=1, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = WRAP
    ws.freeze_panes = "A2"


DEFAULT_WIDTHS = {"#": 5, "Title": 38, "Category": 16, "How to test": 55, "Expected Result": 50}


def add_checklist_sheet(wb: Workbook, title: str, csv_headers: list[str], rows: list[dict]):
    ws = wb.create_sheet(title=title[:31])
    headers = ["#"] + csv_headers + ["Status", "Priority"]
    ws.append(headers)

    status_col = len(headers) - 1  # 1-indexed column of "Status"
    priority_col = len(headers)  # 1-indexed column of "Priority"
    status_letter = get_column_letter(status_col)
    priority_letter = get_column_letter(priority_col)

    status_dv = DataValidation(
        type="list", formula1=f'"{",".join(STATUS_OPTIONS)}"', allow_blank=True
    )
    priority_dv = DataValidation(
        type="list", formula1=f'"{",".join(PRIORITY_OPTIONS)}"', allow_blank=True
    )
    ws.add_data_validation(status_dv)
    ws.add_data_validation(priority_dv)

    for idx, row in enumerate(rows, start=1):
        ws.append([idx] + [row.get(h, "") for h in csv_headers] + ["Not tested", ""])
        status_dv.add(f"{status_letter}{idx + 1}")
        priority_dv.add(f"{priority_letter}{idx + 1}")
        for col in range(1, len(headers) + 1):
            ws.cell(row=idx + 1, column=col).alignment = WRAP

    style_header(ws, len(headers))

    for col_idx, header in enumerate(headers, start=1):
        col_letter = get_column_letter(col_idx)
        width = DEFAULT_WIDTHS.get(header, 14)
        ws.column_dimensions[col_letter].width = width

    return ws, len(rows), status_letter


def add_summary_sheet(wb: Workbook, counts: list[tuple[str, int, str]]):
    ws = wb.create_sheet(title="Summary", index=0)
    ws.append(["Mexico Staking (MEX) — QA Master Checklist"])
    ws["A1"].font = Font(bold=True, size=14)
    ws.append([])
    ws.append(["Checklist", "Case Count", "Not tested", "Passed", "Failed", "Blocked", "Skipped"])
    style_header(ws, 7)

    row_idx = 4
    for name, count, status_letter in counts:
        sheet_ref = f"'{name[:31]}'"
        col = status_letter
        ws.append(
            [
                name,
                count,
                f'=COUNTIF({sheet_ref}!{col}2:{col}{count + 1},"Not tested")',
                f'=COUNTIF({sheet_ref}!{col}2:{col}{count + 1},"Passed")',
                f'=COUNTIF({sheet_ref}!{col}2:{col}{count + 1},"Failed")',
                f'=COUNTIF({sheet_ref}!{col}2:{col}{count + 1},"Blocked")',
                f'=COUNTIF({sheet_ref}!{col}2:{col}{count + 1},"Skipped")',
            ]
        )
        row_idx += 1

    total_row = row_idx + 1
    ws.cell(row=total_row, column=1, value="Total").font = Font(bold=True)
    for col in range(2, 8):
        col_letter = get_column_letter(col)
        ws.cell(
            row=total_row,
            column=col,
            value=f"=SUM({col_letter}4:{col_letter}{row_idx - 1})",
        ).font = Font(bold=True)

    ws.append([])
    ws.append(["Open findings not part of the original checklists (see bug_reports/):"])
    ws.append(["BUG-001", "Helius RPC API key exposed in plain text query parameter on the front end", "Critical"])
    ws.append(["BUG-002", "Verify rounding behavior on small/frequent claims (dust)", "Medium — pending verification"])
    ws.append([])
    ws.append(["Note: 'Unstake Deep Dive' overlaps with unstake-related cases already present in the"])
    ws.append(["other three checklists; treat it as the authoritative, expanded source for unstake and"])
    ws.append(["avoid double-counting duplicate cases when tallying overall coverage."])

    widths = {"A": 26, "B": 60, "C": 14, "D": 12, "E": 12, "F": 12, "G": 12}
    for col_letter, width in widths.items():
        ws.column_dimensions[col_letter].width = width


def main():
    wb = Workbook()
    wb.remove(wb.active)

    counts = []
    for title, filename in CHECKLISTS:
        csv_headers, rows = read_checklist(filename)
        _, count, status_letter = add_checklist_sheet(wb, title, csv_headers, rows)
        counts.append((title, count, status_letter))

    add_summary_sheet(wb, counts)

    wb.save(OUTPUT_PATH)
    total = sum(c for _, c, _ in counts)
    print(f"Wrote {OUTPUT_PATH} with {total} test cases across {len(counts)} sheets.")


if __name__ == "__main__":
    main()
