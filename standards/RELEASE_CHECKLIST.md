# Release Checklist

## Before release

- [ ] Scope, owner, risk classification, and approvals are current.
- [ ] Changed contracts and migrations are backward compatible.
- [ ] Unit, integration, contract, security, and recovery tests pass.
- [ ] Dependencies are pinned and audited.
- [ ] Secrets are externally managed and rotation is verified.
- [ ] Observability, SLOs, alerts, audit events, and dashboards are validated.
- [ ] Capacity, quotas, rate limits, timeouts, and retry budgets are reviewed.
- [ ] Runbook, rollback, reconciliation, and manual continuity are tested.
- [ ] Artifact digest and configuration version are recorded.

## Release

- [ ] Deploy through the approved pipeline using least-privileged identity.
- [ ] Use staged rollout when blast radius is material.
- [ ] Run smoke checks and verify expected telemetry.
- [ ] Reconcile a bounded sample of outcomes.
- [ ] Record approval, artifact, configuration, operator, and result.

## After release

- [ ] Observe the agreed stabilization window.
- [ ] Confirm no unexpected manual work, duplicate actions, or audit gaps.
- [ ] Close or assign release findings.
- [ ] Update documentation and known limitations.
