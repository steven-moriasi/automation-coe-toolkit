# ADR 0003: Plan Rather Than Execute Reference Side Effects

## Status

Accepted.

## Context

A public portfolio example cannot safely assume access to a real identity provider or demonstrate
privileged production changes.

## Decision

The reference automation emits a deterministic, pseudonymous decision plan with hash-chained audit
records and an explicit false side-effect flag. It does not call an identity system.

## Consequences

- The safety and decision boundary is inspectable without credentials.
- Connector authorization, durable state, reconciliation, and production rollback remain explicit
  future work.
- The example demonstrates governance behavior without implying a live deployment.
