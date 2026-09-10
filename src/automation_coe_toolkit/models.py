from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DataSensitivity(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class AssessmentDecision(StrEnum):
    CANDIDATE = "candidate"
    DISCOVERY = "discovery"
    NEEDS_EVIDENCE = "needs_evidence"
    NOT_RECOMMENDED = "not_recommended"
    RISK_REVIEW = "risk_review"


class GateStatus(StrEnum):
    CONDITIONAL = "conditional"
    FAIL = "fail"
    PASSED = "passed"


class ControlPriority(StrEnum):
    RECOMMENDED = "recommended"
    REQUIRED = "required"


class ProcessMetrics(StrictModel):
    monthly_volume: int = Field(ge=1, le=10_000_000)
    average_handling_minutes: Decimal = Field(gt=0, le=1_440)
    manual_hourly_cost: Decimal = Field(ge=0, le=10_000)
    error_rate_percent: Decimal = Field(ge=0, le=100)
    sla_hours: Decimal = Field(gt=0, le=8_760)


class ProcessCharacteristics(StrictModel):
    rules_stability: int = Field(ge=1, le=5)
    input_structure: int = Field(ge=1, le=5)
    process_standardization: int = Field(ge=1, le=5)
    human_judgment: int = Field(ge=1, le=5)
    exception_rate_percent: Decimal = Field(ge=0, le=100)
    systems_count: int = Field(ge=1, le=20)
    data_sensitivity: DataSensitivity
    privileged_access: bool
    regulatory_impact: bool
    customer_facing: bool


class FinancialAssumptions(StrictModel):
    implementation_cost: Decimal = Field(ge=0, le=100_000_000)
    annual_platform_cost: Decimal = Field(ge=0, le=100_000_000)
    expected_automation_percent: Decimal = Field(gt=0, le=100)
    risk_contingency_percent: Decimal = Field(ge=0, le=100)


class ProcessEvidence(StrictModel):
    process_owner_confirmed: bool
    current_process_documented: bool
    baseline_measured: bool
    sample_data_available: bool
    security_owner_identified: bool
    rollback_defined: bool


class AutomationIntake(StrictModel):
    intake_id: str = Field(pattern=r"^AUT-[0-9]{4,}$")
    name: str = Field(min_length=3, max_length=160)
    sponsor: str = Field(min_length=3, max_length=160)
    process_owner: str = Field(min_length=3, max_length=160)
    problem_statement: str = Field(min_length=20, max_length=2_000)
    desired_outcome: str = Field(min_length=20, max_length=2_000)
    metrics: ProcessMetrics
    characteristics: ProcessCharacteristics
    financial: FinancialAssumptions
    evidence: ProcessEvidence
    tags: list[str] = Field(default_factory=list, max_length=20)


class ScoreComponent(StrictModel):
    name: str
    score: Decimal = Field(ge=0, le=100)
    weight: Decimal = Field(gt=0, le=1)
    rationale: str


class RoiEstimate(StrictModel):
    annual_hours_saved: Decimal
    annual_gross_benefit: Decimal
    risk_adjusted_implementation_cost: Decimal
    year_one_total_cost: Decimal
    year_one_net_benefit: Decimal
    payback_months: Decimal | None
    three_year_roi_percent: Decimal | None


class AssessmentResult(StrictModel):
    intake_id: str
    value_score: Decimal
    feasibility_score: Decimal
    risk_score: Decimal
    priority_score: Decimal
    decision: AssessmentDecision
    components: list[ScoreComponent]
    evidence_gaps: list[str]
    roi: RoiEstimate


class GovernanceGate(StrictModel):
    name: str
    status: GateStatus
    rationale: str


class ControlRecommendation(StrictModel):
    category: str
    priority: ControlPriority
    control: str
    rationale: str


class GovernanceReview(StrictModel):
    gates: list[GovernanceGate]
    controls: list[ControlRecommendation]


class PortfolioEvaluation(StrictModel):
    intake: AutomationIntake
    assessment: AssessmentResult
    governance: GovernanceReview
