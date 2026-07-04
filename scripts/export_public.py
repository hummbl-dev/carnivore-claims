#!/usr/bin/env python3
"""Create a safe public export subset from reviewed claims.

Includes only rows where protocol_status is public-safe.
"""

from __future__ import annotations

import csv
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
INPUT = ROOT / "data"
OUTPUT = ROOT / "public_release" / "exports"
OUTPUT.mkdir(parents=True, exist_ok=True)


def _copy_csv(src_name: str, dst_name: str, keep_rows: bool = False):
    src = INPUT / src_name
    dst = OUTPUT / dst_name
    if not src.exists():
        return
    with src.open("r", encoding="utf-8", newline="") as sf, dst.open("w", encoding="utf-8", newline="") as df:
        reader = csv.DictReader(sf)
        writer = csv.DictWriter(df, fieldnames=reader.fieldnames or [])
        writer.writeheader()
        for row in reader:
            if not keep_rows:
                writer.writerow(row)
                continue
            if row.get("protocol_status") == "public-language-safe":
                writer.writerow(row)


def main() -> int:
    _copy_csv("contributors.csv", "contributors.csv")
    _copy_csv("sources.csv", "sources.csv")
    _copy_csv("claims.csv", "claims.csv", keep_rows=True)
    _copy_csv("claim_sources.csv", "claim_sources.csv")
    _copy_csv("evidence.csv", "evidence.csv")
    _copy_csv("claim_evidence.csv", "claim_evidence.csv")
    _copy_csv("protocol_decisions.csv", "protocol_decisions.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
