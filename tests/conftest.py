import json
from pathlib import Path

import pytest

from automation_coe_toolkit.models import AutomationIntake


@pytest.fixture
def sample_intake() -> AutomationIntake:
    path = Path("examples/sample-intake.json")
    return AutomationIntake.model_validate(json.loads(path.read_text(encoding="utf-8")))
