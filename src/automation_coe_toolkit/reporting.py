from automation_coe_toolkit.models import PortfolioEvaluation


def render_markdown(evaluation: PortfolioEvaluation) -> str:
    intake = evaluation.intake
    assessment = evaluation.assessment
    roi = assessment.roi
    lines = [
        f"# Automation assessment: {_safe(intake.name)}",
        "",
        f"- Intake: `{intake.intake_id}`",
        f"- Sponsor: {_safe(intake.sponsor)}",
        f"- Process owner: {_safe(intake.process_owner)}",
        f"- Assessment model: `{assessment.model_version}`",
        f"- Recommendation: **{assessment.decision.value}**",
        "",
        "## Scorecard",
        "",
        "| Dimension | Score |",
        "|---|---:|",
        f"| Value | {assessment.value_score} |",
        f"| Feasibility | {assessment.feasibility_score} |",
        f"| Risk | {assessment.risk_score} |",
        f"| Priority | {assessment.priority_score} |",
        "",
        "Scores are comparative decision support, not a substitute for discovery.",
        "",
        "## Financial model",
        "",
        f"- Annual hours saved: {roi.annual_hours_saved}",
        (
            f"- Annual gross benefit: {roi.annual_gross_benefit} "
            f"{intake.financial.currency}"
        ),
        (
            "- Risk-adjusted implementation cost: "
            f"{roi.risk_adjusted_implementation_cost} {intake.financial.currency}"
        ),
        f"- Year-one total cost: {roi.year_one_total_cost} {intake.financial.currency}",
        (
            f"- Year-one net benefit: {roi.year_one_net_benefit} "
            f"{intake.financial.currency}"
        ),
        f"- Payback months: {_optional(roi.payback_months)}",
        f"- Three-year ROI percent: {_optional(roi.three_year_roi_percent)}",
        "",
        "All financial outputs inherit the intake assumptions and require validation.",
        "",
        "## Governance gates",
        "",
        "| Gate | Status | Rationale |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| {_safe(gate.name)} | {gate.status.value} | {_safe(gate.rationale)} |"
        for gate in evaluation.governance.gates
    )
    lines.extend(["", "## Required evidence", ""])
    if assessment.evidence_gaps:
        lines.extend(f"- {gap}" for gap in assessment.evidence_gaps)
    else:
        lines.append("- No intake evidence gaps were identified.")
    lines.extend(["", "## Recommended controls", ""])
    lines.extend(
        (
            f"- **{control.priority.value} / {control.category}:** "
            f"{control.control} _{control.rationale}_"
        )
        for control in evaluation.governance.controls
    )
    lines.extend(["", "## Scoring rationale", ""])
    lines.extend(
        (
            f"- **{component.name} ({component.score}, "
            f"weight {component.weight}):** {component.rationale}"
        )
        for component in assessment.components
    )
    return "\n".join(lines) + "\n"


def _optional(value: object | None) -> str:
    return "not available" if value is None else str(value)


def _safe(value: str) -> str:
    return value.replace("\n", " ").replace("|", "\\|")
