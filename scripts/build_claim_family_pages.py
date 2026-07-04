#!/usr/bin/env python3
"""Generate public claim-family pages from templates and reviews."""

from __future__ import annotations

import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "claim_families"
DST = ROOT / "public_release" / "claim_families"


def main() -> int:
    DST.mkdir(parents=True, exist_ok=True)
    for path in SRC.glob("*.md"):
        shutil.copy(path, DST / path.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
