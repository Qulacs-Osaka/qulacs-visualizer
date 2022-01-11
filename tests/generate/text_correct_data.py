import os
import sys
from io import StringIO
from typing import Any, List

from qulacsvis import circuit_drawer

sys.path.append(os.path.join("tests"))

from circuit_test_data import load_circuit_data  # noqa

BASELINE_DIR = os.path.join("tests", "baseline", "text_circuit_drawer")


class Capturing(List[str]):
    def __enter__(self) -> "Capturing":
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args: Any) -> None:
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


if __name__ == "__main__":
    test_data = load_circuit_data()
    test_data.pop("empty_circuit")

    for name, circuit in test_data.items():
        with Capturing() as output:
            circuit_drawer(circuit, "text")
        with open(os.path.join(BASELINE_DIR, name + ".txt"), "w") as f:
            f.write("\n".join(output))
            f.write("\n")
