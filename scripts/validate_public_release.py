#!/usr/bin/env python3
"""Validate artifacts produced by ``export_public.py``.

These checks are intentionally conservative:
- Export files must exist in ``public_release/exports``.
- Exported claim rows must only use public-safe protocol status values.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = ROOT / "public_release" / "exports"

REQUIRED_EXPORT_FILES = (
    "contributors.csv",
    "sources.csv",
    "claims.csv",
    "claim_sources.csv",
    "evidence.csv",
    "claim_evidence.csv",
    "protocol_decisions.csv",
)

PUBLIC_SAFE_PROTOCOL_STATUSES = {
    "public-safe",
    "public_safe",
    "public-language-safe",
    "public_language_safe",
}


def _is_public_safe_protocol_status(value: str) -> bool:
    normalized = (value or "").strip().lower().replace("_", "-")
    return normalized in PUBLIC_SAFE_PROTOCOL_STATUSES


def _validate_claim_rows(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        for row_number, row in enumerate(reader, start=2):
            status = row.get("protocol_status", "")
            if status and not _is_public_safe_protocol_status(status):
                raise SystemExit(
                    f"Non-public-safe claim row in {path.name}: row={row_number}, claim_id={row.get('claim_id')}, protocol_status={status}"
                )


def main() -> int:
    if not EXPORT_DIR.exists():
        raise SystemExit(f"Public export directory missing: {EXPORT_DIR}")

    for filename in REQUIRED_EXPORT_FILES:
        path = EXPORT_DIR / filename
        if not path.exists():
            raise SystemExit(f"Missing expected public export file: {path}")

    _validate_claim_rows(EXPORT_DIR / "claims.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
