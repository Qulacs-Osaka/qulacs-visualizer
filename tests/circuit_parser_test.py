import json
import os

import pytest
from qulacs import QuantumCircuit

from qulacsvis.visualization import CircuitParser

from .circuit_test_data import load_circuit_data

BASELINE_DIR_PATH = "tests/baseline/circuit_parser/"

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
def test_circuit_parser(circuit: QuantumCircuit, expected_path: str) -> None:
    parser = CircuitParser(circuit)
    with open(expected_path, "r") as f:
        expected = json.load(f)
    assert parser.gate_info == expected
