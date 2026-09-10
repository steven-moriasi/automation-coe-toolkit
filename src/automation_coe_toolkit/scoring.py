from decimal import ROUND_HALF_UP, Decimal

from automation_coe_toolkit.models import (
    AssessmentDecision,
    AssessmentResult,
    AutomationIntake,
    DataSensitivity,
    ProcessEvidence,
    ScoreComponent,
)
from automation_coe_toolkit.roi import calculate_roi

SCORE = Decimal("0.1")
ASSESSMENT_MODEL_VERSION = "1.0.0"


def assess(intake: AutomationIntake) -> AssessmentResult:
    value_components = _value_components(intake)
    feasibility_components = _feasibility_components(intake)
    value_score = _weighted_score(value_components)
    feasibility_score = _weighted_score(feasibility_components)
    risk_score = _risk_score(intake)
    priority_score = (
        value_score * Decimal("0.45")
        + feasibility_score * Decimal("0.35")
        + (Decimal(100) - risk_score) * Decimal("0.20")
    ).quantize(SCORE, ROUND_HALF_UP)
    evidence_gaps = _evidence_gaps(intake.evidence)
    roi = calculate_roi(intake)

    return AssessmentResult(
        model_version=ASSESSMENT_MODEL_VERSION,
        intake_id=intake.intake_id,
        value_score=value_score,
        feasibility_score=feasibility_score,
        risk_score=risk_score,
        priority_score=priority_score,
        decision=_decision(
            priority_score=priority_score,
            risk_score=risk_score,
            evidence_gaps=evidence_gaps,
            year_one_net_benefit=roi.year_one_net_benefit,
        ),
        components=[*value_components, *feasibility_components],
        evidence_gaps=evidence_gaps,
        roi=roi,
    )


def _value_components(intake: AutomationIntake) -> list[ScoreComponent]:
    metrics = intake.metrics
    return [
        ScoreComponent(
            name="transaction_volume",
            score=_bounded(Decimal(metrics.monthly_volume) / Decimal(10)),
            weight=Decimal("0.40"),
            rationale="Higher recurring volume increases addressable manual effort.",
        ),
        ScoreComponent(
            name="handling_time",
            score=_bounded(metrics.average_handling_minutes * Decimal(2)),
            weight=Decimal("0.30"),
            rationale="Longer handling time increases potential capacity recovery.",
        ),
        ScoreComponent(
            name="quality_exposure",
            score=_bounded(metrics.error_rate_percent * Decimal(5)),
            weight=Decimal("0.30"),
            rationale="Measured error rates indicate potential rework reduction.",
        ),
    ]


def _feasibility_components(intake: AutomationIntake) -> list[ScoreComponent]:
    characteristics = intake.characteristics
    return [
        ScoreComponent(
            name="rules_stability",
            score=_five_point(characteristics.rules_stability),
            weight=Decimal("0.22"),
            rationale="Stable rules reduce maintenance and decision ambiguity.",
        ),
        ScoreComponent(
            name="input_structure",
            score=_five_point(characteristics.input_structure),
            weight=Decimal("0.20"),
            rationale="Structured inputs reduce extraction uncertainty.",
        ),
        ScoreComponent(
            name="process_standardization",
            score=_five_point(characteristics.process_standardization),
            weight=Decimal("0.20"),
            rationale="Standardized processes require fewer variants.",
        ),
        ScoreComponent(
            name="judgment_fit",
            score=Decimal(100) - _five_point(characteristics.human_judgment),
            weight=Decimal("0.18"),
            rationale="Lower human judgment needs favor deterministic automation.",
        ),
        ScoreComponent(
            name="exception_fit",
            score=Decimal(100) - characteristics.exception_rate_percent,
            weight=Decimal("0.12"),
            rationale="Lower exception rates increase straight-through processing.",
        ),
        ScoreComponent(
            name="integration_complexity",
            score=_bounded(Decimal(110 - characteristics.systems_count * 10)),
            weight=Decimal("0.08"),
            rationale="Each system boundary adds delivery and operational complexity.",
        ),
    ]


def _risk_score(intake: AutomationIntake) -> Decimal:
    characteristics = intake.characteristics
    sensitivity = {
        DataSensitivity.PUBLIC: Decimal(0),
        DataSensitivity.INTERNAL: Decimal(15),
        DataSensitivity.CONFIDENTIAL: Decimal(40),
        DataSensitivity.RESTRICTED: Decimal(65),
    }[characteristics.data_sensitivity]
    risk = sensitivity
    if characteristics.privileged_access:
        risk += Decimal(20)
    if characteristics.regulatory_impact:
        risk += Decimal(15)
    if characteristics.customer_facing:
        risk += Decimal(10)
    if characteristics.systems_count > 5:
        risk += Decimal(10)
    if characteristics.human_judgment >= 4:
        risk += Decimal(10)
    return _bounded(risk).quantize(SCORE, ROUND_HALF_UP)


def _evidence_gaps(evidence: ProcessEvidence) -> list[str]:
    evidence_labels = {
        "process_owner_confirmed": "Confirm the accountable process owner.",
        "current_process_documented": "Document the current process and variants.",
        "baseline_measured": "Measure volume, handling time, error, and SLA baselines.",
        "sample_data_available": "Provide representative redacted sample data.",
        "security_owner_identified": "Identify the security and privacy reviewer.",
        "rollback_defined": "Define rollback and manual continuity procedures.",
    }
    evidence_values = evidence.model_dump()
    return [
        label
        for field_name, label in evidence_labels.items()
        if evidence_values[field_name] is False
    ]


def _decision(
    *,
    priority_score: Decimal,
    risk_score: Decimal,
    evidence_gaps: list[str],
    year_one_net_benefit: Decimal,
) -> AssessmentDecision:
    if len(evidence_gaps) >= 3:
        return AssessmentDecision.NEEDS_EVIDENCE
    if risk_score >= Decimal(70):
        return AssessmentDecision.RISK_REVIEW
    if priority_score >= Decimal(65) and year_one_net_benefit > 0:
        return AssessmentDecision.CANDIDATE
    if priority_score >= Decimal(45):
        return AssessmentDecision.DISCOVERY
    return AssessmentDecision.NOT_RECOMMENDED


def _weighted_score(components: list[ScoreComponent]) -> Decimal:
    return sum(
        (component.score * component.weight for component in components),
        start=Decimal(0),
    ).quantize(SCORE, ROUND_HALF_UP)


def _five_point(value: int) -> Decimal:
    return Decimal(value - 1) / Decimal(4) * Decimal(100)


def _bounded(value: Decimal) -> Decimal:
    return min(Decimal(100), max(Decimal(0), value))
