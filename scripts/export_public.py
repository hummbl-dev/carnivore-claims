#!/usr/bin/env python3
"""Create a safe public export subset from reviewed claims.

The current export policy intentionally limits public claims to protocol
statuses that have been explicitly marked as safely publishable.
"""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Callable

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


def _read_csv_rows(root: Path, filename: str) -> list[dict[str, str]]:
    src = root / "data" / filename
    if not src.exists():
        return []
    with src.open("r", encoding="utf-8", newline="") as sf:
        return list(csv.DictReader(sf))


def _extract_public_safe_claim_ids(root: Path) -> set[str]:
    claims = _read_csv_rows(root, "claims.csv")
    safe_claim_ids: set[str] = set()
    for row in claims:
        if _is_public_safe_protocol_status(row.get("protocol_status", "")):
            safe_claim_ids.add(row.get("claim_id", ""))
    return {claim_id for claim_id in safe_claim_ids if claim_id}


def _extract_safe_claim_sources(root: Path, safe_claim_ids: set[str]) -> tuple[set[str], set[str], set[str]]:
    source_ids: set[str] = set()
    contributor_ids: set[str] = set()
    evidence_ids: set[str] = set()

    for row in _read_csv_rows(root, "claim_sources.csv"):
        if row.get("claim_id") not in safe_claim_ids:
            continue
        claim_source_id = row.get("source_id", "").strip()
        claim_contributor_id = row.get("contributor_id", "").strip()
        if claim_source_id:
            source_ids.add(claim_source_id)
        if claim_contributor_id:
            contributor_ids.add(claim_contributor_id)

    for row in _read_csv_rows(root, "claim_evidence.csv"):
        if row.get("claim_id") not in safe_claim_ids:
            continue
        evidence_id = row.get("evidence_id", "").strip()
        if evidence_id:
            evidence_ids.add(evidence_id)

    return source_ids, contributor_ids, evidence_ids


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


def _copy_csv(
    root: Path,
    src_name: str,
    dst_name: str,
    row_filter: Callable[[dict[str, str]], bool] | None = None,
):
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
            if row_filter is not None and not row_filter(row):
                continue
            writer.writerow(_redact_row(row, src_name))


def main() -> int:
    root = _resolve_root(os.environ.get("CCL_REPO_ROOT"))
    safe_claim_ids = _extract_public_safe_claim_ids(root)
    safe_source_ids, safe_contributor_ids, safe_evidence_ids = _extract_safe_claim_sources(
        root,
        safe_claim_ids,
    )

    output_dir = root / "public_release" / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)

    _copy_csv(root, "contributors.csv", "contributors.csv",
              row_filter=lambda row: row.get("contributor_id", "") in safe_contributor_ids)
    _copy_csv(root, "sources.csv", "sources.csv",
              row_filter=lambda row: row.get("source_id", "") in safe_source_ids)
    _copy_csv(root, "claims.csv", "claims.csv", row_filter=lambda row: _is_public_safe_protocol_status(row.get("protocol_status", "")))
    _copy_csv(root, "claim_sources.csv", "claim_sources.csv", row_filter=lambda row: row.get("claim_id", "") in safe_claim_ids)
    _copy_csv(root, "evidence.csv", "evidence.csv", row_filter=lambda row: row.get("evidence_id", "") in safe_evidence_ids)
    _copy_csv(root, "claim_evidence.csv", "claim_evidence.csv", row_filter=lambda row: row.get("claim_id", "") in safe_claim_ids)
    _copy_csv(root, "protocol_decisions.csv", "protocol_decisions.csv", row_filter=lambda row: row.get("claim_id", "") in safe_claim_ids)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
