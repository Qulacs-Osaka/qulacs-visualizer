import pytest
from qulacs import QuantumCircuit

from qulacsvis import circuit_drawer


def test_output_method_None() -> None:
    circuit = QuantumCircuit(2)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_Z_gate(2)
    circuit.add_dense_matrix_gate(
        [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    circuit.add_CNOT_gate(2, 0)
    circuit.add_X_gate(2)

    circuit_drawer(circuit, output_method=None)
    # TODO: check if text is generated


def test_output_method_text() -> None:
    circuit = QuantumCircuit(2)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_Z_gate(2)
    circuit.add_dense_matrix_gate(
        [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    circuit.add_CNOT_gate(2, 0)
    circuit.add_X_gate(2)

    circuit_drawer(circuit, output_method="text")
    # TODO: check if text is generated


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
