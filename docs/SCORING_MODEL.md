# Scoring and ROI Model

## Purpose

The model creates a consistent first-pass comparison across proposed automations. It is not a
precision forecast. Discovery must validate every baseline and financial input.

## Value score

Value is a weighted score from 0 to 100:

| Component | Weight | Normalization |
|---|---:|---|
| Monthly transaction volume | 40% | `min(volume / 10, 100)` |
| Average handling time | 30% | `min(minutes × 2, 100)` |
| Error rate | 30% | `min(error percent × 5, 100)` |

These thresholds are transparent defaults, not universal economic truths. Organizations should
version calibrated thresholds rather than silently changing historical scores.

## Feasibility score

Feasibility combines:

- rules stability: 22%;
- input structure: 20%;
- process standardization: 20%;
- low human-judgment dependence: 18%;
- low exception rate: 12%;
- low integration complexity: 8%.

Five-point inputs are converted linearly to 0–100. Human judgment is inverted because highly
contextual decisions are less suited to deterministic unattended automation.

## Risk score

Risk starts with data sensitivity and adds bounded triggers:

| Trigger | Risk points |
|---|---:|
| Internal data | 15 |
| Confidential data | 40 |
| Restricted data | 65 |
| Privileged access | 20 |
| Regulatory impact | 15 |
| Customer-facing behavior | 10 |
| More than five systems | 10 |
| High human judgment | 10 |

The final score is capped at 100. A score of 70 or more requires explicit risk review even if the
economic case is attractive.

## Priority and recommendation

```text
priority =
  value × 45%
  + feasibility × 35%
  + (100 - risk) × 20%
```

Decision order:

1. Three or more missing evidence items → `needs_evidence`.
2. Risk score of at least 70 → `risk_review`.
3. Priority of at least 65 and positive year-one net benefit → `candidate`.
4. Priority of at least 45 → `discovery`.
5. Otherwise → `not_recommended`.

This ordering prevents an attractive score from bypassing weak evidence or elevated risk.

## ROI formulas

```text
annual hours saved =
  monthly volume × 12 × handling minutes ÷ 60 × automation rate

annual gross benefit =
  annual hours saved × manual hourly cost

risk-adjusted implementation cost =
  implementation cost × (1 + contingency rate)

year-one total cost =
  risk-adjusted implementation cost + annual platform cost

year-one net benefit =
  annual gross benefit - year-one total cost
```

Payback uses monthly gross benefit after annual platform cost. Three-year ROI includes one
risk-adjusted implementation cost and three years of platform cost. Zero or negative denominators
return no ratio instead of misleading infinity.

## Model governance

- Store intake and evaluation together.
- Record the model version used for portfolio decisions.
- Re-score when assumptions or scope change.
- Compare forecasts with realized outcomes after release.
- Investigate systematic optimism by process type.
- Require finance validation before using results as an approved business case.
