# Monitoring Standards

## Required telemetry

Every automation should expose bounded, non-sensitive signals for:

- work received, started, succeeded, failed, retried, deferred, and dead-lettered;
- end-to-end and dependency latency;
- backlog age and depth;
- exception and human-intervention rate;
- dependency errors, quotas, and circuit state;
- reconciliation mismatch;
- deployment and configuration version;
- audit-event delivery health.

Never use customer IDs, email addresses, free-form error text, or correlation IDs as metric labels.

## Service objectives

Define objectives for the business outcome, not only process uptime. Examples:

- 99% of eligible work receives a terminal outcome within the agreed time;
- fewer than 0.1% of completed items have a reconciliation mismatch;
- 100% of privileged actions have approval and audit evidence.

Targets require measured baselines and business approval. Example values are not portfolio claims.

## Alerts

Alerts must be actionable and linked to a runbook. Page on sustained outcome failure, stale backlog,
missing audit evidence, security-control failure, or reconciliation breach. Ticket lower urgency
capacity trends and non-customer-impacting degradations.

Every alert has an owner, severity, threshold rationale, test, and review date.
