# ADR 0001: Use Explainable Deterministic Scoring

## Status

Accepted.

## Context

Portfolio triage needs consistency, but opaque ranking models make assumptions hard to challenge and
can conceal bias or score gaming.

## Decision

Use bounded, versioned, deterministic formulas with visible weights, rationales, evidence gaps, and
financial assumptions. Keep final decisions with accountable humans.

## Consequences

- Reviewers can reproduce and challenge every result.
- Thresholds need calibration against realized outcomes.
- The model cannot capture every strategic or qualitative factor.
- High risk and weak evidence remain explicit gates outside the aggregate priority score.
