#!/usr/bin/env python3
"""Simple duplicate detector for normalized claims."""

from __future__ import annotations

import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "data" / "claims.csv"


def main() -> int:
    seen = {}
    duplicates = []
    with CLAIMS.open("r", encoding="utf-8", newline="") as fp:
        for row in csv.DictReader(fp):
            key = (row.get("normalized_claim", "").strip().lower(), row.get("claim_family", "").strip().lower())
            if not key[0]:
                continue
            prior = seen.get(key)
            if prior:
                duplicates.append((prior, row.get("claim_id", "")))
            else:
                seen[key] = row.get("claim_id", "")

    if duplicates:
        lines = [f"{a} <-> {b}" for a, b in duplicates]
        raise SystemExit("Duplicate normalized claims detected: " + "; ".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
