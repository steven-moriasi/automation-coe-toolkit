import hashlib
import json
from datetime import date
from enum import StrEnum
from pathlib import Path

from pydantic import Field, RootModel

from automation_coe_toolkit.models import StrictModel


class AccessTier(StrEnum):
    PRIVILEGED = "privileged"
    STANDARD = "standard"


class AccessDecision(StrEnum):
    MANUAL_REVIEW = "manual_review"
    RETAIN = "retain"
    REVOKE = "revoke"


class AccessReviewRequest(StrictModel):
    request_id: str = Field(pattern=r"^ARQ-[0-9]{4,}$")
    subject_ref: str = Field(pattern=r"^subject-[0-9]{4,}$")
    employment_active: bool
    access_tier: AccessTier
    last_login_date: date | None
    manager_attested: bool


class AccessReviewRequests(RootModel[list[AccessReviewRequest]]):
    pass


class DecisionRecord(StrictModel):
    request_id: str
    subject_ref: str
    decision: AccessDecision
    reason_code: str


class AuditEvent(StrictModel):
    sequence: int
    event_type: str
    request_id: str
    payload_digest: str
    previous_hash: str
    event_hash: str


class AccessReviewPlan(StrictModel):
    plan_id: str
    as_of: date
    side_effects_executed: bool = False
    decisions: list[DecisionRecord]
    audit_events: list[AuditEvent]


def run_access_review(
    requests: list[AccessReviewRequest],
    *,
    as_of: date,
) -> AccessReviewPlan:
    request_ids = [request.request_id for request in requests]
    if len(request_ids) != len(set(request_ids)):
        raise ValueError("request IDs must be unique")

    decisions = [_decide(request, as_of=as_of) for request in requests]
    audit_events = _audit(decisions)
    plan_digest = hashlib.sha256(
        "".join(event.event_hash for event in audit_events).encode()
    ).hexdigest()
    return AccessReviewPlan(
        plan_id=f"ARP-{plan_digest[:12]}",
        as_of=as_of,
        decisions=decisions,
        audit_events=audit_events,
    )


def run_access_review_file(path: Path, *, as_of: date) -> AccessReviewPlan:
    requests = AccessReviewRequests.model_validate_json(
        path.read_text(encoding="utf-8")
    )
    return run_access_review(requests.root, as_of=as_of)


def _decide(request: AccessReviewRequest, *, as_of: date) -> DecisionRecord:
    if not request.employment_active:
        decision = AccessDecision.REVOKE
        reason_code = "employment_inactive"
    elif request.access_tier is AccessTier.PRIVILEGED:
        decision = AccessDecision.MANUAL_REVIEW
        reason_code = "privileged_access"
    elif not request.manager_attested:
        decision = AccessDecision.MANUAL_REVIEW
        reason_code = "manager_attestation_missing"
    elif request.last_login_date is not None and request.last_login_date > as_of:
        decision = AccessDecision.MANUAL_REVIEW
        reason_code = "future_login_date"
    elif (
        request.last_login_date is None
        or (as_of - request.last_login_date).days > 90
    ):
        decision = AccessDecision.MANUAL_REVIEW
        reason_code = "stale_or_missing_login"
    else:
        decision = AccessDecision.RETAIN
        reason_code = "controls_satisfied"

    return DecisionRecord(
        request_id=request.request_id,
        subject_ref=request.subject_ref,
        decision=decision,
        reason_code=reason_code,
    )


def _audit(decisions: list[DecisionRecord]) -> list[AuditEvent]:
    previous_hash = "0" * 64
    events: list[AuditEvent] = []
    for sequence, decision in enumerate(decisions, start=1):
        payload = json.dumps(
            decision.model_dump(mode="json"),
            separators=(",", ":"),
            sort_keys=True,
        )
        payload_digest = hashlib.sha256(payload.encode()).hexdigest()
        event_material = (
            f"{sequence}|decision_recorded|{decision.request_id}|"
            f"{payload_digest}|{previous_hash}"
        )
        event_hash = hashlib.sha256(event_material.encode()).hexdigest()
        events.append(
            AuditEvent(
                sequence=sequence,
                event_type="decision_recorded",
                request_id=decision.request_id,
                payload_digest=payload_digest,
                previous_hash=previous_hash,
                event_hash=event_hash,
            )
        )
        previous_hash = event_hash
    return events
