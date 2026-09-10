from datetime import date
from pathlib import Path

import pytest

from automation_coe_toolkit.example_automation import (
    AccessDecision,
    AccessReviewRequest,
    AccessTier,
    run_access_review,
    run_access_review_file,
)


def test_reference_automation_builds_side_effect_free_auditable_plan() -> None:
    plan = run_access_review_file(
        path=Path("examples/access-review-requests.json"),
        as_of=date(2026, 9, 1),
    )

    assert plan.side_effects_executed is False
    assert [record.decision for record in plan.decisions] == [
        AccessDecision.RETAIN,
        AccessDecision.REVOKE,
        AccessDecision.MANUAL_REVIEW,
        AccessDecision.MANUAL_REVIEW,
    ]
    assert plan.audit_events[0].previous_hash == "0" * 64
    assert all(
        event.previous_hash == plan.audit_events[index - 1].event_hash
        for index, event in enumerate(plan.audit_events[1:], start=1)
    )
    assert plan.plan_id == "ARP-4bc59e30be82"


def test_reference_automation_is_deterministic() -> None:
    request = _request()

    first = run_access_review([request], as_of=date(2026, 9, 1))
    second = run_access_review([request], as_of=date(2026, 9, 1))

    assert first == second


def test_duplicate_request_ids_are_rejected() -> None:
    request = _request()

    with pytest.raises(ValueError, match="request IDs must be unique"):
        run_access_review([request, request], as_of=date(2026, 9, 1))


@pytest.mark.parametrize(
    ("updates", "reason_code"),
    [
        ({"manager_attested": False}, "manager_attestation_missing"),
        ({"last_login_date": None}, "stale_or_missing_login"),
        ({"last_login_date": date(2026, 9, 2)}, "future_login_date"),
    ],
)
def test_ambiguous_records_route_to_manual_review(
    updates: dict[str, object],
    reason_code: str,
) -> None:
    request = _request().model_copy(update=updates)

    plan = run_access_review([request], as_of=date(2026, 9, 1))

    assert plan.decisions[0].decision is AccessDecision.MANUAL_REVIEW
    assert plan.decisions[0].reason_code == reason_code


def _request() -> AccessReviewRequest:
    return AccessReviewRequest(
        request_id="ARQ-9001",
        subject_ref="subject-9001",
        employment_active=True,
        access_tier=AccessTier.STANDARD,
        last_login_date=date(2026, 8, 15),
        manager_attested=True,
    )
