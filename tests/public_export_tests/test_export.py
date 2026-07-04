from pathlib import Path


def test_public_release_exists():
    root = Path(__file__).resolve().parents[2]
    assert (root / "public_release" / "claims.csv").exists()
    assert (root / "public_release" / "README_PUBLIC.md").exists()
