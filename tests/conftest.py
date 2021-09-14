from typing import List

import pytest
from _pytest import nodes
from _pytest.config import Config
from _pytest.config.argparsing import Parser


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--runlatex",
        action="store_true",
        default=False,
        help="Run the LaTeX code compilation with pdflatex.",
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "runlatex: Mark pdflatex as a required test.")


def pytest_collection_modifyitems(config: Config, items: List[nodes.Item]) -> None:
    if config.getoption("--runlatex"):
        return
    skip_latex = pytest.mark.skip(reason="need --runlatex option to run")
    for item in items:
        if "runlatex" in item.keywords:
            item.add_marker(skip_latex)
