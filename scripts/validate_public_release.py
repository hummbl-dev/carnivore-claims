#!/usr/bin/env python3
"""Validate artifacts produced by ``export_public.py``.

These checks are intentionally conservative:
- Export files must exist in ``public_release/exports``.
- Exported claim rows must only use public-safe protocol status values.
"""

from __future__ import annotations

import csv
import os
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

FORBIDDEN_PUBLIC_FIELDS = {
    "contributors.csv": {"notes", "risk_domains", "source_posture"},
    "sources.csv": {"notes", "archive_url"},
    "claim_sources.csv": {
        "verbatim_quote",
        "timestamp_start",
        "timestamp_end",
        "receipt_url",
        "do_not_infer",
    },
    "evidence.csv": {"notes"},
    "claim_evidence.csv": {"notes"},
    "protocol_decisions.csv": {"not_approved_wording"},
}


def _is_public_safe_protocol_status(value: str) -> bool:
    normalized = (value or "").strip().lower().replace("_", "-")
    return normalized in PUBLIC_SAFE_PROTOCOL_STATUSES


def _resolve_root(root_override: str | None = None) -> Path:
    if root_override:
        return Path(root_override).expanduser().resolve()
    env_root = os.environ.get("CCL_REPO_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return ROOT


def _validate_claim_rows(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        for row_number, row in enumerate(reader, start=2):
            status = row.get("protocol_status", "")
            if status and not _is_public_safe_protocol_status(status):
                raise SystemExit(
                    f"Non-public-safe claim row in {path.name}: "
                    f"row={row_number}, claim_id={row.get('claim_id')}, "
                    f"protocol_status={status}"
                )


def _validate_forbidden_fields(path: Path) -> None:
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        fieldnames = reader.fieldnames or []
        forbidden = FORBIDDEN_PUBLIC_FIELDS.get(path.name, set())
        leaked = sorted(set(fieldnames) & forbidden)
        if leaked:
            raise SystemExit(f"Forbidden fields in public export {path.name}: {leaked}")


def main() -> int:
    root = _resolve_root(os.environ.get("CCL_REPO_ROOT"))
    export_dir = root / "public_release" / "exports"
    if not export_dir.exists():
        raise SystemExit(f"Public export directory missing: {export_dir}")

    for filename in REQUIRED_EXPORT_FILES:
        path = export_dir / filename
        if not path.exists():
            raise SystemExit(f"Missing expected public export file: {path}")
        _validate_forbidden_fields(path)

    _validate_claim_rows(export_dir / "claims.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
