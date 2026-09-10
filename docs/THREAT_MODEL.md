# Threat Model

## Assets

- process and financial assumptions;
- portfolio prioritization decisions;
- approval and exception evidence;
- automation credentials and workload identities;
- business data processed by automations;
- audit records and operational telemetry;
- release artifacts and reusable components.

## Trust boundaries

1. Requestor-provided intake enters the assessment tool.
2. Portfolio reviewers consume generated reports.
3. Delivery pipelines turn approved designs into deployable artifacts.
4. Runtime automations cross identity, API, data, and human-approval boundaries.
5. Monitoring and incident systems receive operational evidence.

## Material threats and controls

| Threat | Impact | Control |
|---|---|---|
| Inflated volume or benefit assumptions | Misallocated funding | Measured baselines, finance validation, realized-benefit review |
| Score gaming | Risk bypass | Explainable components, immutable model version, approval gates |
| Malformed or oversized intake | Tool failure or distorted output | Strict schema, numeric bounds, forbidden extra fields |
| Sensitive intake in source control | Data exposure | Fictional examples, redaction, repository review |
| Spreadsheet or report tampering | Untraceable decisions | Store typed JSON with reviewed source and release evidence |
| Credential embedding | Account compromise | Workload identity, secret stores, scanning, short-lived access |
| Excessive runtime privilege | Broad blast radius | Least privilege, approval, scoped connectors, kill switch |
| Unsafe retries | Duplicate business actions | Idempotency contract and operation-specific retry policy |
| Log leakage | Sensitive-data exposure | Structured allowlisted fields and redaction |
| Audit deletion or mutation | Lost accountability | Append-only remote evidence and integrity verification |
| Automation of ambiguous judgment | Incorrect outcomes | Human review queues, confidence bounds, response SLAs |
| Compromised reusable component | Portfolio-wide impact | Pinned dependencies, signing, provenance, staged rollout |

## Reference automation boundary

The access review example does not call an identity provider. It produces pseudonymous decisions
and a hash-chained plan with `side_effects_executed: false`. A production connector would require:

- authenticated and authorized workload identity;
- stable provider idempotency behavior;
- approval before privileged revoke actions;
- durable audit storage outside the worker;
- reconciliation against source state;
- alerting, rollback, and emergency disablement.

Hash chaining demonstrates mutation detection within an exported sequence. It is not a substitute
for signed, access-controlled, append-only storage.
