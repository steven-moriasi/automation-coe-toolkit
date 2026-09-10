# Naming Conventions

Names should reveal ownership, environment, function, and type without embedding confidential
business data.

## Identifiers

| Item | Convention | Example |
|---|---|---|
| Intake | `AUT-<sequence>` | `AUT-1042` |
| Repository | lower kebab case | `invoice-exception-router` |
| Service | `<domain>-<capability>` | `identity-access-review` |
| Queue/topic | `<env>.<domain>.<event>.v<major>` | `prod.invoice.received.v1` |
| Metric | `<service>_<noun>_<unit>` | `access_review_duration_seconds` |
| Secret reference | `<ENV>_<SERVICE>_<PURPOSE>` | `PROD_REVIEW_PROVIDER_TOKEN` |
| Runbook | `RB-<service>-<scenario>` | `RB-access-review-backlog` |
| Incident | `INC-YYYY-<sequence>` | `INC-2026-0042` |

## Rules

- Use stable business capabilities, not team names that may change.
- Put environment in deployment resources, not source package names.
- Version externally consumed contracts.
- Avoid personal names, customer names, credentials, or ticket descriptions.
- Use the same correlation ID across workflow boundaries.
- Define reason codes as stable machine-readable enums.
