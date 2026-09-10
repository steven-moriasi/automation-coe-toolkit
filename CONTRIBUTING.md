# Contributing

## Development contract

Use Python 3.12 and keep scoring, controls, and examples deterministic and explainable.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip==26.2.1
python -m pip install -e ".[dev]"
ruff check src tests
mypy src tests
pytest --cov=automation_coe_toolkit --cov-report=term-missing --cov-fail-under=80
pip-audit
docker build .
```

## Change requirements

Every scoring or governance change must include:

1. a stated decision objective;
2. bounded typed inputs;
3. visible weights, thresholds, or conditions;
4. tests for ordinary and boundary decisions;
5. documentation of model and approval consequences;
6. backward-compatibility or re-scoring guidance.

Reference automations must remain side-effect free unless a production-grade connector boundary,
authorization model, durable idempotency, reconciliation, and explicit approval flow are added.

Do not add proprietary process maps, customer names, copied employee data, production metrics,
credentials, or confidential business cases. Examples must remain clearly fictional.
