# Automation CoE Toolkit

A portfolio/reference implementation for governing an enterprise automation portfolio from intake
through assessment, delivery, release, and operations.

The toolkit combines executable assessment logic with reusable governance standards. It is
designed to make prioritization assumptions inspectable rather than hiding them in a spreadsheet.

## Planned evidence

- typed automation intake and process assessment;
- explainable value, feasibility, and risk scoring;
- ROI and payback calculations;
- governance gates and control recommendations;
- architecture, environment, release, monitoring, and incident standards;
- reusable documentation templates;
- a small governed reference automation;
- tests, security checks, container packaging, and CI.

This repository demonstrates a governance model. It does not claim that its sample scores,
financial assumptions, or fictional process data represent a production organization.

## Development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip==26.2.1
python -m pip install -e ".[dev]"
coe-toolkit --version
```
