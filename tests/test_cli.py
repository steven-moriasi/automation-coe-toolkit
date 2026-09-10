import json
import sys
from pathlib import Path

import pytest

from automation_coe_toolkit.cli import main


def test_evaluate_command_writes_json_and_markdown(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    report_path = tmp_path / "assessment.md"
    json_path = tmp_path / "assessment.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "coe-toolkit",
            "evaluate",
            "examples/sample-intake.json",
            "--report-output",
            str(report_path),
            "--json-output",
            str(json_path),
        ],
    )

    main()

    assert "Recommendation: **candidate**" in report_path.read_text()
    payload = json.loads(json_path.read_text())
    assert payload["assessment"]["decision"] == "candidate"


def test_access_review_command_writes_plan(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "plan.json"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "coe-toolkit",
            "run-access-review",
            "examples/access-review-requests.json",
            "--as-of",
            "2026-09-01",
            "--output",
            str(output_path),
        ],
    )

    main()

    payload = json.loads(output_path.read_text())
    assert payload["side_effects_executed"] is False
    assert len(payload["decisions"]) == 4


def test_cli_without_command_prints_help(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(sys, "argv", ["coe-toolkit"])

    main()

    assert "Executable governance toolkit" in capsys.readouterr().out
