"""
generate_supplementary_tables.py

RSOS reproducibility helper (NON-SYNTHETIC).

What this script DOES:
- Locates the canonical supplementary workbook already included in the repository
  (Supplementary_Tables_S1-S12.xlsx).
- Copies it into the repository structure expected by README
  (Supplementary_Tables/Supplementary_Tables_S1-S12.xlsx).
- Optionally exports each sheet to CSV for transparency.

What this script DOES NOT do:
- It does NOT fabricate or simulate docking/QikProp/MM-GBSA data.
  (Those results should come from the deposited outputs.)

Usage:
    python generate_supplementary_tables.py
Optional:
    python generate_supplementary_tables.py --export-csv

Run from:
- Python_Scripts/ (recommended, matches README), or anywhere inside the repo.

Dependencies:
- pandas, openpyxl
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import pandas as pd


def _repo_root() -> Path:
    """Infer repository root from this file location."""
    return Path(__file__).resolve().parent.parent


def _find_source_workbook(root: Path) -> Path:
    """Find the canonical supplementary workbook in likely locations."""
    candidates = [
        root / "Supplementary_Tables_S1-S12.xlsx",
        root / "Supplementary_Tables" / "Supplementary_Tables_S1-S12.xlsx",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        "Could not find 'Supplementary_Tables_S1-S12.xlsx' in the repository root "
        "or in 'Supplementary_Tables/'. Please add it to the repo before running."
    )


def _copy_workbook(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _export_sheets_to_csv(xlsx_path: Path, csv_dir: Path) -> None:
    csv_dir.mkdir(parents=True, exist_ok=True)
    xls = pd.ExcelFile(xlsx_path)
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        safe_name = "".join(c if (c.isalnum() or c in "-_") else "_" for c in sheet)
        out_csv = csv_dir / f"{safe_name}.csv"
        df.to_csv(out_csv, index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--export-csv",
        action="store_true",
        help="Also export each sheet as CSV into Supplementary_Tables/CSV/.",
    )
    args = parser.parse_args()

    root = _repo_root()
    src = _find_source_workbook(root)

    dst = root / "Supplementary_Tables" / "Supplementary_Tables_S1-S12.xlsx"
    _copy_workbook(src, dst)

    print(f"✓ Copied canonical workbook:\n  {src}\n→ {dst}")

    if args.export_csv:
        csv_dir = root / "Supplementary_Tables" / "CSV"
        _export_sheets_to_csv(dst, csv_dir)
        print(f"✓ Exported sheets to CSV:\n  {csv_dir}")

    # Minimal validation summary
    xls = pd.ExcelFile(dst)
    print("\nWorkbook validation summary:")
    print(f"- Sheets: {len(xls.sheet_names)}")
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet)
        print(f"  - {sheet}: {df.shape[0]} rows × {df.shape[1]} columns")


if __name__ == "__main__":
    main()
