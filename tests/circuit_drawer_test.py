import pytest
from qulacsvis import circuit_drawer


def test_output_method_None() -> None:
    with pytest.raises(Exception):
        circuit_drawer(output_method=None)


def test_output_method_text() -> None:
    with pytest.raises(Exception):
        circuit_drawer(output_method="text")


@pytest.mark.runlatex
def test_output_method_latex() -> None:
    circuit_drawer(output_method="latex")
    # TODO: check if pdf file is generated


def test_output_method_latex_source() -> None:
    circuit_drawer(output_method="latex_source")
    # TODO: check if latex file is generated
