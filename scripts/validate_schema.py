#!/usr/bin/env python3
"""Minimal repository validation.

Checks:
- presence of expected CSV files
- required headers in each CSV
- valid JSON syntax in all schema files
"""

from __future__ import annotations

import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

CSV_EXPECTED_HEADERS = {
    ROOT / "data" / "contributors.csv": [
        "contributor_id",
        "display_name",
        "type",
        "status",
        "source_posture",
        "priority",
        "domains",
        "risk_domains",
        "notes",
    ],
    ROOT / "data" / "sources.csv": [
        "source_id",
        "title",
        "source_type",
        "url",
        "archive_url",
        "published_date",
        "accessed_date",
        "contributors",
        "source_quality",
        "transcript_status",
        "claim_extraction_status",
        "copyright_status",
        "notes",
    ],
    ROOT / "data" / "claims.csv": [
        "claim_id",
        "normalized_claim",
        "claim_family",
        "claim_type",
        "risk_class",
        "diet_context",
        "specificity",
        "duration_context",
        "evidence_status",
        "protocol_status",
        "created_at",
        "updated_at",
    ],
    ROOT / "data" / "claim_sources.csv": [
        "claim_source_id",
        "claim_id",
        "contributor_id",
        "source_id",
        "verbatim_quote",
        "timestamp_start",
        "timestamp_end",
        "receipt_url",
        "rhetoric_strength",
        "claim_strength",
        "source_quality",
        "do_not_infer",
    ],
    ROOT / "data" / "evidence.csv": [
        "evidence_id",
        "title",
        "authors",
        "year",
        "evidence_type",
        "url",
        "doi",
        "institution_or_journal",
        "evidence_maturity",
        "domains",
        "notes",
    ],
    ROOT / "data" / "claim_evidence.csv": [
        "claim_evidence_id",
        "claim_id",
        "evidence_id",
        "relationship",
        "direction",
        "strength",
        "notes",
        "reviewer",
        "review_date",
    ],
    ROOT / "data" / "protocol_decisions.csv": [
        "protocol_decision_id",
        "claim_id",
        "protocol_status",
        "approved_wording",
        "not_approved_wording",
        "subgroups",
        "contraindications",
        "monitoring",
        "review_date",
        "next_review_due",
    ],
}


def validate_schema_json():
    for path in (ROOT / "schema").glob("*.json"):
        with path.open("r", encoding="utf-8") as fp:
            json.load(fp)


def validate_csv_headers():
    for path, expected in CSV_EXPECTED_HEADERS.items():
        if not path.exists():
            raise SystemExit(f"Missing required CSV file: {path}")
        with path.open("r", encoding="utf-8", newline="") as fp:
            reader = csv.DictReader(fp)
            headers = reader.fieldnames or []
            if headers != expected:
                raise SystemExit(
                    f"Header mismatch in {path.name}. Expected {expected}, got {headers}"
                )


def main() -> int:
    validate_schema_json()
    validate_csv_headers()
    return 0


if __name__ == "__main__":
    sys.exit(main())
