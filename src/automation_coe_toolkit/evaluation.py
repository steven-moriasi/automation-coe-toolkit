import json
from pathlib import Path

from automation_coe_toolkit.governance import review_governance
from automation_coe_toolkit.models import AutomationIntake, PortfolioEvaluation
from automation_coe_toolkit.scoring import assess


def evaluate_file(path: Path) -> PortfolioEvaluation:
    intake = AutomationIntake.model_validate(
        json.loads(path.read_text(encoding="utf-8"))
    )
    return PortfolioEvaluation(
        intake=intake,
        assessment=assess(intake),
        governance=review_governance(intake),
    )
