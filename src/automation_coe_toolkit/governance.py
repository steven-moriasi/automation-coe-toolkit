from automation_coe_toolkit.models import (
    AutomationIntake,
    ControlPriority,
    ControlRecommendation,
    DataSensitivity,
    GateStatus,
    GovernanceGate,
    GovernanceReview,
)


def review_governance(intake: AutomationIntake) -> GovernanceReview:
    return GovernanceReview(
        gates=[
            _process_gate(intake),
            _baseline_gate(intake),
            _data_gate(intake),
            _security_gate(intake),
            _continuity_gate(intake),
        ],
        controls=_controls(intake),
    )


def _process_gate(intake: AutomationIntake) -> GovernanceGate:
    passed = (
        intake.evidence.process_owner_confirmed
        and intake.evidence.current_process_documented
    )
    return GovernanceGate(
        name="process_accountability",
        status=GateStatus.PASSED if passed else GateStatus.FAIL,
        rationale=(
            "An accountable owner and current-state process are documented."
            if passed
            else "Confirm ownership and document the current process before design."
        ),
    )


def _baseline_gate(intake: AutomationIntake) -> GovernanceGate:
    passed = intake.evidence.baseline_measured
    return GovernanceGate(
        name="measured_baseline",
        status=GateStatus.PASSED if passed else GateStatus.FAIL,
        rationale=(
            "The value case is supported by measured baseline data."
            if passed
            else "Validate volume, handling time, quality, and SLA assumptions."
        ),
    )


def _data_gate(intake: AutomationIntake) -> GovernanceGate:
    passed = intake.evidence.sample_data_available
    return GovernanceGate(
        name="representative_data",
        status=GateStatus.PASSED if passed else GateStatus.FAIL,
        rationale=(
            "Representative redacted data is available for discovery and testing."
            if passed
            else "Obtain representative redacted data before solution validation."
        ),
    )


def _security_gate(intake: AutomationIntake) -> GovernanceGate:
    characteristics = intake.characteristics
    requires_review = (
        characteristics.data_sensitivity
        in {DataSensitivity.CONFIDENTIAL, DataSensitivity.RESTRICTED}
        or characteristics.privileged_access
        or characteristics.regulatory_impact
    )
    if not requires_review:
        status = GateStatus.PASSED
        rationale = "No elevated data, privilege, or regulatory trigger was declared."
    elif intake.evidence.security_owner_identified:
        status = GateStatus.CONDITIONAL
        rationale = (
            "An identified security owner must approve the elevated risk controls."
        )
    else:
        status = GateStatus.FAIL
        rationale = (
            "Identify a security owner before processing elevated-risk data or access."
        )
    return GovernanceGate(
        name="security_and_privacy",
        status=status,
        rationale=rationale,
    )


def _continuity_gate(intake: AutomationIntake) -> GovernanceGate:
    passed = intake.evidence.rollback_defined
    return GovernanceGate(
        name="operational_continuity",
        status=GateStatus.PASSED if passed else GateStatus.FAIL,
        rationale=(
            "Rollback and manual continuity procedures are defined."
            if passed
            else "Define rollback, reconciliation, and manual continuity procedures."
        ),
    )


def _controls(intake: AutomationIntake) -> list[ControlRecommendation]:
    characteristics = intake.characteristics
    controls = [
        ControlRecommendation(
            category="delivery",
            priority=ControlPriority.REQUIRED,
            control=(
                "Use version control, peer review, automated tests, and "
                "traceable releases."
            ),
            rationale=(
                "Every automation needs reproducible change and release evidence."
            ),
        ),
        ControlRecommendation(
            category="operations",
            priority=ControlPriority.REQUIRED,
            control=(
                "Emit correlation IDs, outcome metrics, failure alerts, "
                "and audit events."
            ),
            rationale=(
                "Operators need bounded evidence for diagnosis and reconciliation."
            ),
        ),
        ControlRecommendation(
            category="resilience",
            priority=ControlPriority.REQUIRED,
            control=(
                "Document idempotency, retry, timeout, recovery, and "
                "rollback behavior."
            ),
            rationale="Failure semantics must be explicit before unattended execution.",
        ),
    ]

    if characteristics.data_sensitivity in {
        DataSensitivity.CONFIDENTIAL,
        DataSensitivity.RESTRICTED,
    }:
        controls.append(
            ControlRecommendation(
                category="data_protection",
                priority=ControlPriority.REQUIRED,
                control=(
                    "Minimize retained data, encrypt it in transit and at rest, "
                    "and redact sensitive fields from logs."
                ),
                rationale="The intake declares elevated data sensitivity.",
            )
        )
    if characteristics.privileged_access:
        controls.append(
            ControlRecommendation(
                category="identity",
                priority=ControlPriority.REQUIRED,
                control=(
                    "Use workload identity, least privilege, short-lived "
                    "credentials, and human approval for privileged actions."
                ),
                rationale="The automation requests privileged access.",
            )
        )
    if characteristics.regulatory_impact:
        controls.append(
            ControlRecommendation(
                category="compliance",
                priority=ControlPriority.REQUIRED,
                control=(
                    "Capture decision provenance, retention rules, control "
                    "ownership, and evidence export."
                ),
                rationale="The process has declared regulatory impact.",
            )
        )
    if characteristics.human_judgment >= 4:
        controls.append(
            ControlRecommendation(
                category="human_oversight",
                priority=ControlPriority.REQUIRED,
                control=(
                    "Route ambiguous decisions to a named human queue with "
                    "response SLAs."
                ),
                rationale="The process relies heavily on contextual human judgment.",
            )
        )
    if characteristics.customer_facing:
        controls.append(
            ControlRecommendation(
                category="release",
                priority=ControlPriority.RECOMMENDED,
                control=(
                    "Use canary release, customer-safe errors, and a "
                    "tested kill switch."
                ),
                rationale="Customer-facing failures can create direct external impact.",
            )
        )
    if characteristics.systems_count > 5:
        controls.append(
            ControlRecommendation(
                category="integration",
                priority=ControlPriority.RECOMMENDED,
                control=(
                    "Contract-test every integration and monitor dependency health."
                ),
                rationale="The process spans more than five system boundaries.",
            )
        )
    return controls
