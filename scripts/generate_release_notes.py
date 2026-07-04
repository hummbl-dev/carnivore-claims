#!/usr/bin/env python3
"""Generate simple release-note summary from row counts."""

from __future__ import annotations

import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "public_release" / "CHANGELOG.md"


def _count(path: pathlib.Path) -> int:
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8", newline="") as fp:
        return max(0, sum(1 for _ in csv.reader(fp)) - 1)


def main() -> int:
    rows = {
        "contributors": _count(DATA / "contributors.csv"),
        "sources": _count(DATA / "sources.csv"),
        "claims": _count(DATA / "claims.csv"),
        "evidence": _count(DATA / "evidence.csv"),
    }
    OUT.write_text(
        "# Changelog\n\n- Contributors: {contributors}\n- Sources: {sources}\n- Claims: {claims}\n- Evidence artifacts: {evidence}\n".format(
            **rows
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
