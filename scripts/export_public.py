#!/usr/bin/env python3
"""Create a safe public export subset from reviewed claims.

The current export policy intentionally limits public claims to protocol
statuses that have been explicitly marked as safely publishable.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data"
OUTPUT = ROOT / "public_release" / "exports"

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


def _redact_row(row: dict[str, str], filename: str) -> dict[str, str]:
    redacted = row.copy()
    for field in FORBIDDEN_PUBLIC_FIELDS.get(filename, set()):
        redacted.pop(field, None)
    return redacted


def _copy_csv(root: Path, src_name: str, dst_name: str, keep_rows: bool = False):
    input_dir = root / "data"
    output_dir = root / "public_release" / "exports"
    src = input_dir / src_name
    dst = output_dir / dst_name
    if not src.exists():
        return

    with src.open("r", encoding="utf-8", newline="") as sf, dst.open("w", encoding="utf-8", newline="") as df:
        reader = csv.DictReader(sf)
        source_fields = reader.fieldnames or []
        fieldnames = [name for name in source_fields if name not in FORBIDDEN_PUBLIC_FIELDS.get(src_name, set())]
        writer = csv.DictWriter(df, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if not keep_rows:
                writer.writerow(_redact_row(row, src_name))
                continue
            if not _is_public_safe_protocol_status(row.get("protocol_status", "")):
                continue
            writer.writerow(_redact_row(row, src_name))


def main() -> int:
    root = _resolve_root(os.environ.get("CCL_REPO_ROOT"))
    output_dir = root / "public_release" / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)
    _copy_csv(root, "contributors.csv", "contributors.csv")
    _copy_csv(root, "sources.csv", "sources.csv")
    _copy_csv(root, "claims.csv", "claims.csv", keep_rows=True)
    _copy_csv(root, "claim_sources.csv", "claim_sources.csv")
    _copy_csv(root, "evidence.csv", "evidence.csv")
    _copy_csv(root, "claim_evidence.csv", "claim_evidence.csv")
    _copy_csv(root, "protocol_decisions.csv", "protocol_decisions.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
