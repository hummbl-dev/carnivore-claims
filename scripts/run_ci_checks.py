#!/usr/bin/env python3
"""Run lightweight CI checks for this repo without external dependencies."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _check_non_empty_dirs():
    required = [
        ROOT / "schema",
        ROOT / "data",
        ROOT / "claim_families",
        ROOT / "contributors",
        ROOT / "scripts",
    ]
    for path in required:
        if not any(path.iterdir()):
            raise SystemExit(f"Directory has no files: {path}")


def main() -> int:
    for script in ["validate_schema.py", "check_receipts.py", "dedupe_claims.py"]:
        module_path = ROOT / "scripts" / script
        if not module_path.exists():
            raise SystemExit(f"Missing required check script: {module_path}")
    _check_non_empty_dirs()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
