import os

import pytest
from qulacs import QuantumCircuit

from qulacsvis import circuit_drawer

from .circuit_test_data import load_circuit_data

BASELINE_DIR_PATH = "tests/baseline/latex_source_circuit_drawer/"

circuit_data = load_circuit_data()

test_table = []

for key, circuit in circuit_data.items():
    test_table.append(
        (
            pytest.param(
                circuit,
                os.path.join(BASELINE_DIR_PATH, key + ".txt"),
                id=key,
            )
        )
    )


@pytest.mark.parametrize("circuit,expected_path", test_table)
def test_latex_circuit_drawer(circuit: QuantumCircuit, expected_path: str) -> None:
    out = circuit_drawer(circuit, output_method="latex_source")
    if isinstance(out, str):
        with open(expected_path, "r") as f:
            expected = f.read()
        assert out == expected
    else:
        raise Exception("Output is not a string")
