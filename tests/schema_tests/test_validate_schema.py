from pathlib import Path
import subprocess


def test_validate_schema_runs():
    repo = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        ["python", "scripts/validate_schema.py"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
