import os
import sys

from qulacsvis import circuit_drawer

sys.path.append(os.path.join("tests"))

from circuit_test_data import load_circuit_data  # noqa

BASELINE_DIR = os.path.join("tests", "baseline", "latex_source_circuit_drawer")

if __name__ == "__main__":
    test_data = load_circuit_data()

    for name, circuit in test_data.items():
        src = circuit_drawer(circuit, "latex_source")
        with open(os.path.join(BASELINE_DIR, name + ".txt"), "w") as f:
            if isinstance(src, str):
                f.write(src)
            else:
                print("Error: `src` is not a string", file=sys.stderr)
