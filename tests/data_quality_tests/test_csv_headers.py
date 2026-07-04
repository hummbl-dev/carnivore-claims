import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_csv_headers_non_empty():
    csv_files = [
        ROOT / "data" / "contributors.csv",
        ROOT / "data" / "sources.csv",
        ROOT / "data" / "claims.csv",
        ROOT / "data" / "claim_sources.csv",
        ROOT / "data" / "evidence.csv",
        ROOT / "data" / "claim_evidence.csv",
        ROOT / "data" / "protocol_decisions.csv",
    ]
    for path in csv_files:
        with path.open() as fp:
            header = next(csv.reader(fp))
            assert header
