import pytest
from qulacsvis import circuit_drawer


def test_output_method_None() -> None:
    with pytest.raises(Exception):
        circuit_drawer(output_method=None)


def test_output_method_text() -> None:
    with pytest.raises(Exception):
        circuit_drawer(output_method="text")


def test_output_method_latex() -> None:
    with pytest.raises(Exception):
        circuit_drawer(output_method="latex")


def test_output_method_latex_source() -> None:
    with pytest.raises(Exception):
        circuit_drawer(output_method="latex_source")
