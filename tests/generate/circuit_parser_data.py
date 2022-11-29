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
        parsed_circuit = dataclasses_to_dict(parser.parsed_circuit)

        with open(os.path.join(BASELINE_DIR, name + ".txt"), "w") as f:
            json.dump(parsed_circuit, f, sort_keys=True, indent=4)
            print(f'Saved output to {os.path.join(BASELINE_DIR, name + ".txt")}')
