import json
import os
import sys

from qulacsvis.visualization import CircuitParser

sys.path.append(os.path.join("tests"))

from circuit_test_data import load_circuit_data  # noqa

BASELINE_DIR = os.path.join("tests", "baseline", "circuit_parser")

if __name__ == "__main__":
    test_data = load_circuit_data()

    for name, circuit in test_data.items():
        parser = CircuitParser(circuit)
        with open(os.path.join(BASELINE_DIR, name + ".txt"), "w") as f:
            json.dump(parser.gate_info, f, sort_keys=True, indent=4)
            print(f'Saved output to {os.path.join(BASELINE_DIR, name + ".txt")}')
