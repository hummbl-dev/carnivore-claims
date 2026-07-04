import subprocess
from pathlib import Path


def test_export_and_public_release_validation():
    repo = Path(__file__).resolve().parents[2]
    export_result = subprocess.run(
        ["python", "scripts/export_public.py"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert export_result.returncode == 0, export_result.stderr

    validate_result = subprocess.run(
        ["python", "scripts/validate_public_release.py"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert validate_result.returncode == 0, validate_result.stderr
