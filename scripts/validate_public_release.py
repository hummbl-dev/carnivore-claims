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


def _load_claim_ids(path: Path) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        return {row.get("claim_id", "") for row in reader if row.get("claim_id")}


def _load_related_ids(path: Path, key: str) -> set[str]:
    with path.open("r", encoding="utf-8", newline="") as fp:
        reader = csv.DictReader(fp)
        return {row.get(key, "") for row in reader if row.get(key)}


def _validate_export_scope(root: Path) -> None:
    claims_path = root / "public_release" / "exports" / "claims.csv"
    claim_ids = _load_claim_ids(claims_path)

    source_rows = root / "public_release" / "exports" / "sources.csv"
    if source_rows.exists():
        source_ids = _load_related_ids(root / "public_release" / "exports" / "claim_sources.csv", "source_id")
        if source_rows.exists() and source_ids:
            with source_rows.open("r", encoding="utf-8", newline="") as fp:
                for line_number, row in enumerate(csv.DictReader(fp), start=2):
                    source_id = row.get("source_id")
                    if source_id and source_id not in source_ids:
                        raise SystemExit(f"Public source not referenced by safe claims: {source_id} (row={line_number})")

    for filename, key in (
        ("contributors.csv", "contributor_id"),
        ("claim_sources.csv", "claim_id"),
        ("claim_evidence.csv", "claim_id"),
        ("protocol_decisions.csv", "claim_id"),
    ):
        path = root / "public_release" / "exports" / filename
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8", newline="") as fp:
            reader = csv.DictReader(fp)
            rows = list(reader)
            if filename == "contributors.csv":
                claim_sources = _load_related_ids(root / "public_release" / "exports" / "claim_sources.csv", "contributor_id")
                for row_number, row in enumerate(rows, start=2):
                    contributor_id = row.get(key, "")
                    if contributor_id and contributor_id not in claim_sources:
                        raise SystemExit(
                            f"Public contributor not referenced by safe claims: "
                            f"{contributor_id} (row={row_number}, file={filename})"
                        )
            elif filename in {"claim_sources.csv", "claim_evidence.csv", "protocol_decisions.csv"}:
                for row_number, row in enumerate(rows, start=2):
                    claim_id = row.get(key, "")
                    if claim_id and claim_id not in claim_ids:
                        raise SystemExit(
                            f"Non-safe claim leaked in public export {filename}: "
                            f"claim_id={claim_id}, row={row_number}"
                        )

    evidence_rows = root / "public_release" / "exports" / "evidence.csv"
    if evidence_rows.exists():
        claim_evidence_path = root / "public_release" / "exports" / "claim_evidence.csv"
        allowed_evidence = _load_related_ids(claim_evidence_path, "evidence_id") if claim_evidence_path.exists() else set()
        if allowed_evidence:
            with evidence_rows.open("r", encoding="utf-8", newline="") as fp:
                for row_number, row in enumerate(csv.DictReader(fp), start=2):
                    evidence_id = row.get("evidence_id", "")
                    if evidence_id and evidence_id not in allowed_evidence:
                        raise SystemExit(
                            f"Public evidence not linked to safe claim: "
                            f"{evidence_id} (row={row_number})"
                        )


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
    _validate_export_scope(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
