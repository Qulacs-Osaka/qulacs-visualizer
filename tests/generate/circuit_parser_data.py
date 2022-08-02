import json
import os
import sys

from qulacsvis.visualization import CircuitParser

sys.path.append(os.path.join("tests"))

from circuit_test_data import load_circuit_data  # noqa
from test_utils import dataclasses_to_dict  # noqa

BASELINE_DIR = os.path.join("tests", "baseline", "circuit_parser")


if __name__ == "__main__":
    test_data = load_circuit_data()

    for name, circuit in test_data.items():
        parser = CircuitParser(circuit)
        gate_info = dataclasses_to_dict(parser.gate_info)

        with open(os.path.join(BASELINE_DIR, name + ".txt"), "w") as f:
            json.dump(gate_info, f, sort_keys=True, indent=4)
            print(f'Saved output to {os.path.join(BASELINE_DIR, name + ".txt")}')
