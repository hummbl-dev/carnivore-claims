import os
import subprocess
import csv
from pathlib import Path


FORBIDDEN_FIELDS = {
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


def _write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=header)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _make_fixture_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir(parents=True)

    _write_csv(
        root / "data" / "contributors.csv",
        ["contributor_id", "display_name", "type", "status", "source_posture", "priority", "domains", "risk_domains", "notes"],
        [
            {
                "contributor_id": "C001",
                "display_name": "Source A",
                "type": "person",
                "status": "public_surface_verified",
                "source_posture": "nutrition_epistemology",
                "priority": "P1",
                "domains": "[]",
                "risk_domains": "[]",
                "notes": "Internal profile note.",
            }
        ],
    )

    _write_csv(
        root / "data" / "sources.csv",
        [
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
        [
            {
                "source_id": "SRC001",
                "title": "Source Title",
                "source_type": "video",
                "url": "https://example.org/source",
                "archive_url": "https://example.org/source/archive",
                "published_date": "2024-01-01",
                "accessed_date": "2024-01-02",
                "contributors": "[\"C001\"]",
                "source_quality": "SQ4_full_source_with_transcript_timestamp",
                "transcript_status": "available",
                "claim_extraction_status": "pending",
                "copyright_status": "metadata_and_short_quotes_only",
                "notes": "Transcript timestamp notes.",
            }
        ],
    )

    _write_csv(
        root / "data" / "claims.csv",
        [
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
        [
            {
                "claim_id": "CCL-CLM-000001",
                "normalized_claim": "Fiber is not required for everyone.",
                "claim_family": "fiber",
                "claim_type": "nutrient_essentiality",
                "risk_class": "R1_medium",
                "diet_context": "[]",
                "specificity": "[]",
                "duration_context": "lifetime",
                "evidence_status": "not_reviewed",
                "protocol_status": "public_language_safe",
                "created_at": "",
                "updated_at": "",
            },
            {
                "claim_id": "CCL-CLM-000002",
                "normalized_claim": "Unsafe claim.",
                "claim_family": "fiber",
                "claim_type": "clinical_outcome",
                "risk_class": "R4_unsafe_or_forbidden",
                "diet_context": "[]",
                "specificity": "[]",
                "duration_context": "lifetime",
                "evidence_status": "not_reviewed",
                "protocol_status": "research_only",
                "created_at": "",
                "updated_at": "",
            },
        ],
    )

    _write_csv(
        root / "data" / "claim_sources.csv",
        [
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
        [
            {
                "claim_source_id": "CST001",
                "claim_id": "CCL-CLM-000001",
                "contributor_id": "C001",
                "source_id": "SRC001",
                "verbatim_quote": "Exact long quote text",
                "timestamp_start": "00:01:00",
                "timestamp_end": "00:01:30",
                "receipt_url": "https://example.org/receipt",
                "rhetoric_strength": "assertive",
                "claim_strength": "moderate",
                "source_quality": "SQ4_full_source_with_transcript_timestamp",
                "do_not_infer": "[\"Do not infer...\"]",
            }
        ],
    )

    _write_csv(
        root / "data" / "evidence.csv",
        [
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
        [
            {
                "evidence_id": "EVD001",
                "title": "Trial",
                "authors": "[]",
                "year": "2025",
                "evidence_type": "systematic_review",
                "url": "https://example.org/evidence",
                "doi": "",
                "institution_or_journal": "",
                "evidence_maturity": "M0_no_evidence_located",
                "domains": "[]",
                "notes": "Private evidence notes.",
            }
        ],
    )

    _write_csv(
        root / "data" / "claim_evidence.csv",
        [
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
        [
            {
                "claim_evidence_id": "CEV001",
                "claim_id": "CCL-CLM-000001",
                "evidence_id": "EVD001",
                "relationship": "bounds_claim",
                "direction": "mixed",
                "strength": "moderate",
                "notes": "Internal note.",
                "reviewer": "agent",
                "review_date": "2026-07-04",
            }
        ],
    )

    _write_csv(
        root / "data" / "protocol_decisions.csv",
        [
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
        [
            {
                "protocol_decision_id": "PD001",
                "claim_id": "CCL-CLM-000001",
                "protocol_status": "public_language_safe",
                "approved_wording": "Example approved wording.",
                "not_approved_wording": "[\"do not...\"]",
                "subgroups": "[]",
                "contraindications": "[]",
                "monitoring": "[]",
                "review_date": "",
                "next_review_due": "",
            }
        ],
    )

    (root / "public_release").mkdir(parents=True, exist_ok=True)
    return root


def test_export_scrubs_forbidden_fields_from_public_outputs(tmp_path: Path):
    repo = _make_fixture_repo(tmp_path)
    env = os.environ.copy()
    env["CCL_REPO_ROOT"] = str(repo)
    repo_root = Path(__file__).resolve().parents[2]

    export_result = subprocess.run(
        ["python", "scripts/export_public.py"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
    )
    assert export_result.returncode == 0, export_result.stderr

    for filename in [
        "contributors.csv",
        "sources.csv",
        "claims.csv",
        "claim_sources.csv",
        "evidence.csv",
        "claim_evidence.csv",
        "protocol_decisions.csv",
    ]:
        with (repo / "public_release" / "exports" / filename).open(newline="", encoding="utf-8") as fp:
            headers = next(csv.reader(fp))
        for field in FORBIDDEN_FIELDS.get(filename, set()):
            assert field not in headers, f"{filename} leaked forbidden field {field}"

    with (repo / "public_release" / "exports" / "claims.csv").open(newline="", encoding="utf-8") as fp:
        rows = list(csv.DictReader(fp))
    assert len(rows) == 1
    assert rows[0]["claim_id"] == "CCL-CLM-000001"


def test_validation_detects_forbidden_export_fields(tmp_path: Path):
    repo = _make_fixture_repo(tmp_path)
    bad_exports = repo / "public_release" / "exports"
    bad_exports.mkdir(parents=True, exist_ok=True)
    _write_csv(
        bad_exports / "contributors.csv",
        ["contributor_id", "display_name", "notes"],
        [{"contributor_id": "C001", "display_name": "bad", "notes": "leak"}],
    )
    for filename in [
        "sources.csv",
        "claims.csv",
        "claim_sources.csv",
        "evidence.csv",
        "claim_evidence.csv",
        "protocol_decisions.csv",
    ]:
        _write_csv(
            bad_exports / filename,
            ["claim_id"] if filename != "claims.csv" else ["claim_id", "protocol_status"],
            [{} if filename != "claims.csv" else {"claim_id": "CCL-CLM-000001", "protocol_status": "public_language_safe"}],
        )
    repo_root = Path(__file__).resolve().parents[2]

    validate_result = subprocess.run(
        ["python", "scripts/validate_public_release.py"],
        cwd=repo_root,
        env={**os.environ, "CCL_REPO_ROOT": str(repo)},
        capture_output=True,
        text=True,
    )
    assert validate_result.returncode != 0
    assert "Forbidden fields in public export contributors.csv" in validate_result.stderr
