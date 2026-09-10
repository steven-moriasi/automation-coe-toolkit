from automation_coe_toolkit.governance import review_governance
from automation_coe_toolkit.models import (
    AutomationIntake,
    ControlPriority,
    DataSensitivity,
    GateStatus,
    PortfolioEvaluation,
)
from automation_coe_toolkit.reporting import render_markdown
from automation_coe_toolkit.scoring import assess


def test_elevated_data_produces_conditional_gate_and_controls(
    sample_intake: AutomationIntake,
) -> None:
    review = review_governance(sample_intake)

    security_gate = next(
        gate for gate in review.gates if gate.name == "security_and_privacy"
    )
    assert security_gate.status is GateStatus.CONDITIONAL
    assert {
        control.category
        for control in review.controls
        if control.priority is ControlPriority.REQUIRED
    } >= {"compliance", "data_protection", "delivery", "operations", "resilience"}


def test_missing_security_owner_fails_elevated_risk_gate(
    sample_intake: AutomationIntake,
) -> None:
    intake = sample_intake.model_copy(
        update={
            "evidence": sample_intake.evidence.model_copy(
                update={"security_owner_identified": False}
            )
        }
    )

    review = review_governance(intake)

    security_gate = next(
        gate for gate in review.gates if gate.name == "security_and_privacy"
    )
    assert security_gate.status is GateStatus.FAIL


def test_low_risk_process_passes_security_gate_without_data_control(
    sample_intake: AutomationIntake,
) -> None:
    characteristics = sample_intake.characteristics.model_copy(
        update={
            "data_sensitivity": DataSensitivity.PUBLIC,
            "regulatory_impact": False,
        }
    )
    intake = sample_intake.model_copy(update={"characteristics": characteristics})

    review = review_governance(intake)

    security_gate = next(
        gate for gate in review.gates if gate.name == "security_and_privacy"
    )
    assert security_gate.status is GateStatus.PASSED
    assert "data_protection" not in {
        control.category for control in review.controls
    }


def test_governance_adds_context_specific_controls(
    sample_intake: AutomationIntake,
) -> None:
    characteristics = sample_intake.characteristics.model_copy(
        update={
            "privileged_access": True,
            "human_judgment": 5,
            "customer_facing": True,
            "systems_count": 6,
        }
    )
    intake = sample_intake.model_copy(update={"characteristics": characteristics})

    categories = {
        control.category for control in review_governance(intake).controls
    }

    assert {"human_oversight", "identity", "integration", "release"} <= categories


def test_markdown_report_escapes_table_content(
    sample_intake: AutomationIntake,
) -> None:
    intake = sample_intake.model_copy(
        update={"name": "Evidence | preparation\nworkflow"}
    )
    evaluation = PortfolioEvaluation(
        intake=intake,
        assessment=assess(intake),
        governance=review_governance(intake),
    )

    report = render_markdown(evaluation)

    assert "# Automation assessment: Evidence \\| preparation workflow" in report
    assert "Recommendation: **candidate**" in report
