# Automation CoE Operating Model

## Mandate

The CoE provides a paved road for safe automation without becoming a centralized delivery
bottleneck. It owns standards, portfolio transparency, reusable controls, assurance, and
capability development. Business process owners remain accountable for outcomes and controls.

## Lifecycle

| Stage | Accountable role | Required evidence | Exit |
|---|---|---|---|
| Intake | Process owner | Problem, outcome, baseline, owner | Validated intake |
| Triage | Portfolio lead | Score, ROI assumptions, risk triggers | Discovery decision |
| Discovery | Product + engineering | Current state, variants, data, controls | Approved option |
| Design | Solution owner | ADRs, threat model, failure semantics | Architecture approval |
| Build | Engineering lead | Versioned code, tests, review | Release candidate |
| Release | Service owner | Checklist, runbook, rollback, approvals | Controlled deployment |
| Operate | Service owner | SLOs, telemetry, incidents, reconciliations | Stable service |
| Improve/retire | Process owner | Outcome review, control evidence | Updated or retired |

## Decision rights

- **Process owner:** accepts process change and residual business risk.
- **Product/portfolio lead:** prioritizes capacity and benefits.
- **Solution owner:** owns technical design and lifecycle.
- **Security/privacy:** approves triggered controls and exceptions.
- **Operations:** accepts supportability, telemetry, and recovery.
- **Finance:** validates business-case assumptions when funding depends on them.
- **CoE:** defines the standard, assures evidence, and tracks exceptions.

No score overrides a required approver.

## Portfolio cadence

- Weekly intake triage for evidence gaps and ownership.
- Fortnightly discovery and architecture review.
- Monthly portfolio review for delivery health, benefit confidence, incidents, and technical debt.
- Quarterly model calibration using forecast-versus-realized outcomes.

## Federated delivery

Teams can deliver automations when they:

1. use the shared lifecycle and templates;
2. meet architecture and release standards;
3. expose required telemetry and audit evidence;
4. register the service owner and support path;
5. document approved deviations with expiry dates.

Reusable components should be treated as products with owners, versions, tests, and compatibility
policies—not copied snippets.

## Measures

Track decision-quality and service-health measures rather than vanity counts:

- intake lead time and evidence completeness;
- forecast confidence and forecast-versus-realized benefit;
- automation exception and manual-intervention rate;
- change failure and rollback rate;
- incident frequency and recovery time;
- control exceptions and overdue remediation;
- component reuse with version adoption;
- retirement of obsolete automations.

Raw "bots built" or "hours saved" without a measured baseline and reconciliation are insufficient.
