#!/usr/bin/env python3
"""Check that every claim has at least one claim-source receipt."""

from __future__ import annotations

import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "data" / "claims.csv"
CLAIM_SOURCES = ROOT / "data" / "claim_sources.csv"


def _read_ids(path: pathlib.Path):
    with path.open("r", encoding="utf-8", newline="") as fp:
        return {row["claim_id"] for row in csv.DictReader(fp) if row.get("claim_id")}


def main() -> int:
    all_claims = _read_ids(CLAIMS)
    sourced = _read_ids(CLAIM_SOURCES)
    missing = sorted(all_claims - sourced)
    if missing:
        raise SystemExit(f"Claims missing receipts: {', '.join(missing)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
