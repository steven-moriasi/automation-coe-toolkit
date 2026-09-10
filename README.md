# Automation CoE Toolkit

A portfolio/reference implementation for governing an enterprise automation portfolio from intake
through assessment, delivery, release, and operations.

The toolkit combines executable assessment logic with reusable governance standards. It makes
prioritization assumptions inspectable instead of hiding them in a spreadsheet and keeps
high-risk automations behind explicit review gates.

## What is implemented

- strict JSON intake schema with bounded process and financial inputs;
- explainable value, feasibility, risk, and priority scores;
- annual benefit, risk-adjusted cost, payback, and three-year ROI calculations;
- evidence, security, privacy, and continuity gates;
- context-specific control recommendations;
- Markdown and JSON decision reports;
- a side-effect-free access review reference automation with bounded inputs, deterministic
  decisions, and verifiable hash-chained audit records;
- standards, checklists, templates, tests, container packaging, and CI.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip==26.2.1
python -m pip install -e ".[dev]"

coe-toolkit evaluate examples/sample-intake.json
mkdir -p build
coe-toolkit evaluate examples/sample-intake.json \
  --report-output build/assessment.md \
  --json-output build/assessment.json
coe-toolkit run-access-review examples/access-review-requests.json \
  --as-of 2026-09-01 \
  --output build/access-review-plan.json
```

Create output directories before using output flags. Without them, commands write to standard
output.

## Decision flow

```text
Automation intake
    ↓
Schema and bounds validation
    ↓
Value + feasibility + risk + ROI
    ↓
Evidence and control gates
    ↓
Candidate / discovery / evidence / risk-review / not-recommended
    ↓
Human portfolio decision
```

The recommendation is decision support, not an autonomous funding decision. Financial results
inherit the supplied assumptions. A candidate can still have conditional governance gates that
must be approved before delivery.

## Reference automation

The access review example deliberately produces a plan rather than changing an identity system.
It demonstrates:

- pseudonymous subject references;
- explicit retain, revoke, and manual-review outcomes;
- human review for privilege, ambiguity, stale data, and missing attestation;
- duplicate request rejection;
- bounded batch and input-file sizes;
- deterministic output;
- locally verifiable hash chaining;
- a visible `side_effects_executed: false` safety boundary.

Production execution would require an approved identity connector, durable idempotency,
authorization, reconciliation, alerting, and change controls.

## Repository map

```text
src/automation_coe_toolkit/  Executable assessment and reference automation
examples/                    Fictional, non-production inputs
templates/                   Intake, design, risk, runbook, and incident templates
standards/                   Architecture, release, monitoring, and operating standards
docs/                        Methods, threat model, evidence, ADRs, and critical review
tests/                       Unit, integration, and CLI tests
```

## Verification

```bash
ruff check src tests
mypy src tests
pytest --cov=automation_coe_toolkit --cov-report=term-missing --cov-fail-under=80
pip-audit
docker build .
```

## Scope and non-claims

This repository demonstrates an Automation Center of Excellence operating model and executable
governance patterns. It does not claim:

- adoption by a specific enterprise;
- realized savings, delivery-time reduction, or production reliability;
- production identity changes by the reference automation;
- that sample financial values or scores represent actual business results;
- regulatory certification or replacement of legal, privacy, security, finance, or architecture
  approval.

See [Portfolio Evidence](docs/PORTFOLIO_EVIDENCE.md) for the exact evidence boundary.
