import argparse
from datetime import date
from pathlib import Path

from automation_coe_toolkit import __version__
from automation_coe_toolkit.evaluation import evaluate_file
from automation_coe_toolkit.example_automation import run_access_review_file
from automation_coe_toolkit.reporting import render_markdown


def parser() -> argparse.ArgumentParser:
    command_parser = argparse.ArgumentParser(
        prog="coe-toolkit",
        description="Executable governance toolkit for automation portfolios.",
    )
    command_parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subcommands = command_parser.add_subparsers(dest="command")
    evaluate_parser = subcommands.add_parser(
        "evaluate",
        help="Evaluate a JSON automation intake.",
    )
    evaluate_parser.add_argument("intake", type=Path)
    evaluate_parser.add_argument(
        "--json-output",
        type=Path,
        help="Write the full typed evaluation as JSON.",
    )
    evaluate_parser.add_argument(
        "--report-output",
        type=Path,
        help="Write the decision report as Markdown instead of standard output.",
    )
    example_parser = subcommands.add_parser(
        "run-access-review",
        help="Build a governed access-review decision plan without side effects.",
    )
    example_parser.add_argument("requests", type=Path)
    example_parser.add_argument("--as-of", type=date.fromisoformat, required=True)
    example_parser.add_argument("--output", type=Path)
    return command_parser


def main() -> None:
    arguments = parser().parse_args()
    if arguments.command == "evaluate":
        evaluation = evaluate_file(arguments.intake)
        report = render_markdown(evaluation)
        if arguments.report_output is None:
            print(report, end="")
        else:
            arguments.report_output.write_text(report, encoding="utf-8")
        if arguments.json_output is not None:
            arguments.json_output.write_text(
                evaluation.model_dump_json(indent=2),
                encoding="utf-8",
            )
    elif arguments.command == "run-access-review":
        plan = run_access_review_file(arguments.requests, as_of=arguments.as_of)
        serialized = plan.model_dump_json(indent=2)
        if arguments.output is None:
            print(serialized)
        else:
            arguments.output.write_text(serialized, encoding="utf-8")
    else:
        parser().print_help()
