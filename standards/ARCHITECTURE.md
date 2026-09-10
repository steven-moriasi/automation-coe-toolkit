# Architecture Standards

## Required characteristics

Every production automation must document:

- business owner, service owner, users, and support boundary;
- inputs, outputs, data classification, retention, and system-of-record rules;
- authentication, authorization, credential rotation, and least privilege;
- synchronous, asynchronous, scheduled, and human-interaction boundaries;
- idempotency, ordering, timeout, retry, dead-letter, reconciliation, and rollback behavior;
- expected load, quotas, rate limits, and scaling constraints;
- telemetry, audit events, SLOs, alerts, and runbook links;
- dependency lifecycle, versioning, deployment, and retirement.

## Preferred patterns

- API-first integration over fragile UI automation where supported.
- Event-driven handoff for long-running or failure-prone work.
- Explicit state machines for multi-step workflows.
- Typed contracts at system boundaries.
- Durable idempotency keys for side effects.
- Bounded retries with jitter only for retry-safe operations.
- Human approval for privilege, material financial action, or ambiguous judgment.
- Stateless workers with durable external state.

## Prohibited shortcuts

- credentials in source, configuration examples, logs, or screenshots;
- unbounded loops, retries, queues, payloads, or concurrency;
- silent exception swallowing;
- production writes from development environments;
- shared personal accounts for workloads;
- mutable manual production changes without versioned evidence;
- claims of exactly-once processing without a proven end-to-end contract.

## Architecture review triggers

Review is mandatory for restricted data, privileged access, customer-facing actions, regulatory
impact, artificial intelligence decisioning, new public endpoints, new vendors, cross-region data,
or changes to recovery and identity boundaries.
