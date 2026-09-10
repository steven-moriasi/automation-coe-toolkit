# Incident Management Guidance

## Priorities

1. Protect people, data, credentials, money, and downstream systems.
2. Stop or contain unsafe side effects.
3. Preserve evidence and establish an incident channel and commander.
4. Restore a safe business process, including manual continuity.
5. Reconcile outcomes before resuming unattended execution.

## Initial actions

- identify affected automation, version, environment, and time window;
- disable triggers or revoke credentials if side effects are unsafe;
- preserve logs, audit events, queue state, deployment records, and approvals;
- classify data, privilege, customer, financial, and regulatory impact;
- assign incident commander, operations lead, communications lead, and scribe;
- use the runbook; document deviations.

## Recovery

Recovery is not complete when a process restarts. Verify:

- duplicates, omissions, and partial side effects;
- source and target reconciliation;
- queue and scheduler state;
- credential and control integrity;
- customer or stakeholder communication;
- increased monitoring during stabilization.

## Learning

Use a blameless timeline focused on system conditions and decision context. Track corrective actions
to owners and dates. Update tests, alerts, runbooks, architecture, training, and portfolio risk.
