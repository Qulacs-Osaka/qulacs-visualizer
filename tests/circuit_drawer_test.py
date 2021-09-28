import pytest
from qulacs import QuantumCircuit
from qulacsvis import circuit_drawer


def test_output_method_None() -> None:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_X_gate(1)

    with pytest.raises(Exception):
        circuit_drawer(circuit, output_method=None)


def test_output_method_text() -> None:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_X_gate(1)

    with pytest.raises(Exception):
        circuit_drawer(circuit, output_method="text")


@pytest.mark.runlatex
def test_output_method_latex() -> None:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_X_gate(1)

    circuit_drawer(circuit, output_method="latex")
    # TODO: check if pdf file is generated


def test_output_method_latex_source() -> None:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_X_gate(1)
    circuit_drawer(circuit, output_method="latex_source")
    # TODO: check if latex file is generated
