# Environment Strategy

## Separation

| Environment | Purpose | Data | Side effects |
|---|---|---|---|
| Local | Fast developer feedback | Synthetic | Mocked or disabled |
| Test | Automated integration and contract tests | Synthetic | Isolated test systems |
| Staging | Production-like release validation | Masked/synthetic | Approved staging systems |
| Production | Business operation | Approved production data | Approved production systems |

Production credentials must never be available to lower environments. Network, identity, storage,
and telemetry boundaries should be separate where practical.

## Promotion

- Build once and promote the same immutable artifact.
- Pin runtime and dependencies.
- Apply configuration through validated environment-specific values.
- Require migrations to be backward compatible with rollback strategy.
- Record artifact digest, approvals, configuration version, and deployment result.
- Run post-deployment smoke checks and reconciliation.

## Access

- Federated identity and short-lived credentials are preferred.
- Human access is role-based, time-bound, and audited.
- Workloads use dedicated identities per service and environment.
- Break-glass access has a named owner, alert, expiry, and retrospective.

## Data

Use synthetic data by default. Masking must be irreversible for lower environments. Test fixtures
must not include copied customer, employee, credential, or regulated data.
