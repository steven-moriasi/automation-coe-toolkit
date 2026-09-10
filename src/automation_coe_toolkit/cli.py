import argparse

from automation_coe_toolkit import __version__


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
    return command_parser


def main() -> None:
    parser().parse_args()
