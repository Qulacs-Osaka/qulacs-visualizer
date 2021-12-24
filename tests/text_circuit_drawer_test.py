import os
from typing import Any

import pytest
from qulacs import QuantumCircuit

from qulacsvis import circuit_drawer

from .circuit_test_data import empty_circuit, load_circuit_data

EXPECTED_STR_PATH = "tests/baseline/text_circuit_drawer/"

circuit_data = load_circuit_data()
# empty_circuit will throw an IndexError Exception
circuit_data.pop("empty_circuit")

test_table = []

for key, circuit in circuit_data.items():
    test_table.append(
        (
            pytest.param(
                circuit,
                os.path.join(EXPECTED_STR_PATH, key + ".txt"),
                id=key,
            )
        )
    )


def test_empty_circuit() -> None:
    circuit = empty_circuit()
    with pytest.raises(IndexError):
        circuit_drawer(circuit, output_method="text")


@pytest.mark.parametrize("circuit,expected_path", test_table)
def test_text_circuit_drawer(
    circuit: QuantumCircuit, expected_path: str, capfd: Any
) -> None:
    circuit_drawer(circuit, output_method="text")
    out, _ = capfd.readouterr()
    with open(expected_path, "r") as f:
        expected = f.read()

    assert out == expected
