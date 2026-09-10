from decimal import ROUND_HALF_UP, Decimal

from automation_coe_toolkit.models import AutomationIntake, RoiEstimate

MONEY = Decimal("0.01")
RATIO = Decimal("0.1")
MONTHS = Decimal("12")


def calculate_roi(intake: AutomationIntake) -> RoiEstimate:
    metrics = intake.metrics
    assumptions = intake.financial
    automation_rate = assumptions.expected_automation_percent / Decimal(100)
    contingency_rate = assumptions.risk_contingency_percent / Decimal(100)

    annual_hours_saved = (
        Decimal(metrics.monthly_volume)
        * MONTHS
        * metrics.average_handling_minutes
        / Decimal(60)
        * automation_rate
    )
    annual_gross_benefit = annual_hours_saved * metrics.manual_hourly_cost
    risk_adjusted_implementation_cost = assumptions.implementation_cost * (
        Decimal(1) + contingency_rate
    )
    year_one_total_cost = (
        risk_adjusted_implementation_cost + assumptions.annual_platform_cost
    )
    year_one_net_benefit = annual_gross_benefit - year_one_total_cost

    monthly_operating_benefit = (
        annual_gross_benefit - assumptions.annual_platform_cost
    ) / MONTHS
    payback_months = (
        risk_adjusted_implementation_cost / monthly_operating_benefit
        if monthly_operating_benefit > 0
        else None
    )

    three_year_cost = (
        risk_adjusted_implementation_cost
        + assumptions.annual_platform_cost * Decimal(3)
    )
    three_year_roi_percent = (
        (
            (annual_gross_benefit * Decimal(3) - three_year_cost)
            / three_year_cost
            * Decimal(100)
        )
        if three_year_cost > 0
        else None
    )

    return RoiEstimate(
        annual_hours_saved=annual_hours_saved.quantize(RATIO, ROUND_HALF_UP),
        annual_gross_benefit=annual_gross_benefit.quantize(MONEY, ROUND_HALF_UP),
        risk_adjusted_implementation_cost=risk_adjusted_implementation_cost.quantize(
            MONEY,
            ROUND_HALF_UP,
        ),
        year_one_total_cost=year_one_total_cost.quantize(MONEY, ROUND_HALF_UP),
        year_one_net_benefit=year_one_net_benefit.quantize(MONEY, ROUND_HALF_UP),
        payback_months=(
            payback_months.quantize(RATIO, ROUND_HALF_UP)
            if payback_months is not None
            else None
        ),
        three_year_roi_percent=(
            three_year_roi_percent.quantize(RATIO, ROUND_HALF_UP)
            if three_year_roi_percent is not None
            else None
        ),
    )
