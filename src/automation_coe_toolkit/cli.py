import argparse
from pathlib import Path

from automation_coe_toolkit import __version__
from automation_coe_toolkit.evaluation import evaluate_file
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
    return command_parser


def main() -> None:
    arguments = parser().parse_args()
    if arguments.command != "evaluate":
        parser().print_help()
        return

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
