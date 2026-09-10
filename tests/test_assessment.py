from decimal import Decimal

import pytest
from pydantic import ValidationError

from automation_coe_toolkit.models import (
    AssessmentDecision,
    AutomationIntake,
    DataSensitivity,
    FinancialAssumptions,
    ProcessCharacteristics,
    ProcessEvidence,
    ProcessMetrics,
)
from automation_coe_toolkit.roi import calculate_roi
from automation_coe_toolkit.scoring import assess


def test_assessment_scores_value_feasibility_risk_and_roi(
    sample_intake: AutomationIntake,
) -> None:
    result = assess(sample_intake)

    assert result.decision is AssessmentDecision.CANDIDATE
    assert result.model_version == "1.0.0"
    assert result.value_score == Decimal("76.0")
    assert result.feasibility_score == Decimal("87.9")
    assert result.risk_score == Decimal("55.0")
    assert result.priority_score == Decimal("74.0")
    assert result.roi.annual_hours_saved == Decimal("8100.0")
    assert result.roi.year_one_net_benefit == Decimal("270600.00")
    assert result.roi.payback_months == Decimal("2.1")
    assert result.roi.three_year_roi_percent == Decimal("990.4")


def test_missing_discovery_evidence_blocks_candidate_recommendation(
    sample_intake: AutomationIntake,
) -> None:
    intake = sample_intake.model_copy(
        update={
            "evidence": ProcessEvidence(
                process_owner_confirmed=False,
                current_process_documented=False,
                baseline_measured=False,
                sample_data_available=True,
                security_owner_identified=True,
                rollback_defined=True,
            )
        }
    )

    result = assess(intake)

    assert result.decision is AssessmentDecision.NEEDS_EVIDENCE
    assert len(result.evidence_gaps) == 3


def test_elevated_risk_requires_risk_review(
    sample_intake: AutomationIntake,
) -> None:
    characteristics = sample_intake.characteristics.model_copy(
        update={
            "data_sensitivity": DataSensitivity.RESTRICTED,
            "privileged_access": True,
            "customer_facing": True,
        }
    )
    intake = sample_intake.model_copy(update={"characteristics": characteristics})

    result = assess(intake)

    assert result.risk_score == Decimal(100)
    assert result.decision is AssessmentDecision.RISK_REVIEW


def test_low_value_complex_process_is_not_recommended() -> None:
    intake = AutomationIntake(
        schema_version="1.0",
        intake_id="AUT-9001",
        name="Low-value exception handling",
        sponsor="Example Operations",
        process_owner="Example Process Owner",
        problem_statement=(
            "A rare exception is manually reviewed using contextual judgment."
        ),
        desired_outcome=(
            "Assess whether automation is proportionate to the limited recurring value."
        ),
        metrics=ProcessMetrics(
            monthly_volume=1,
            average_handling_minutes=Decimal(1),
            manual_hourly_cost=Decimal(20),
            error_rate_percent=Decimal(0),
            sla_hours=Decimal(168),
        ),
        characteristics=ProcessCharacteristics(
            rules_stability=1,
            input_structure=1,
            process_standardization=1,
            human_judgment=5,
            exception_rate_percent=Decimal(100),
            systems_count=20,
            data_sensitivity=DataSensitivity.PUBLIC,
            privileged_access=False,
            regulatory_impact=False,
            customer_facing=False,
        ),
        financial=FinancialAssumptions(
            currency="USD",
            implementation_cost=Decimal(100_000),
            annual_platform_cost=Decimal(10_000),
            expected_automation_percent=Decimal(10),
            risk_contingency_percent=Decimal(20),
        ),
        evidence=ProcessEvidence(
            process_owner_confirmed=True,
            current_process_documented=True,
            baseline_measured=True,
            sample_data_available=True,
            security_owner_identified=True,
            rollback_defined=True,
        ),
    )

    result = assess(intake)

    assert result.decision is AssessmentDecision.NOT_RECOMMENDED
    assert result.roi.payback_months is None


def test_zero_cost_roi_avoids_division_by_zero(
    sample_intake: AutomationIntake,
) -> None:
    intake = sample_intake.model_copy(
        update={
            "financial": sample_intake.financial.model_copy(
                update={
                    "implementation_cost": Decimal(0),
                    "annual_platform_cost": Decimal(0),
                }
            )
        }
    )

    roi = calculate_roi(intake)

    assert roi.payback_months == Decimal("0.0")
    assert roi.three_year_roi_percent is None


def test_intake_rejects_unknown_fields(
    sample_intake: AutomationIntake,
) -> None:
    payload = sample_intake.model_dump(mode="json")
    payload["unreviewed_override"] = True

    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        AutomationIntake.model_validate(payload)


def test_intake_rejects_unknown_schema_version(
    sample_intake: AutomationIntake,
) -> None:
    payload = sample_intake.model_dump(mode="json")
    payload["schema_version"] = "2.0"

    with pytest.raises(ValidationError, match="Input should be '1.0'"):
        AutomationIntake.model_validate(payload)
