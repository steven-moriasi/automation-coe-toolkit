# Roadmap

## Priority 1: Model governance

- Add model-version migration, dual-running, and historical re-scoring workflows.
- Store calibration datasets without sensitive process data.
- Add sensitivity analysis and confidence ranges.
- Compare forecast with realized outcomes by automation type.
- Add migration and re-scoring policy for model changes.

## Priority 2: Portfolio registry

- Persist intake, evaluation, decision, owner, stage, approvals, and review dates.
- Track exceptions with approver, rationale, expiry, and remediation.
- Record realized benefit, interventions, incidents, and retirement.
- Provide role-based portfolio views and exportable evidence.

## Priority 3: Enforced assurance workflow

- Convert governance gates into policy-as-code.
- Integrate authenticated approvals and separation of duties.
- Require signed release artifacts and provenance.
- Block promotion on expired exceptions or missing operational evidence.

## Priority 4: Production reference connector

- Add a mock-first provider contract.
- Use workload identity and least privilege.
- Add durable idempotency, bounded retry, rate limiting, and reconciliation.
- Store signed audit evidence and test rollback.

## Priority 5: Organizational feedback

- Pilot the templates with delivery teams.
- Measure intake quality, review lead time, exception volume, and rework.
- Simplify controls that add friction without reducing material risk.
- Publish calibrated defaults only after evidence supports them.
