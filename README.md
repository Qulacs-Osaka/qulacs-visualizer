# qulacs-visualizer

[![CI](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/ci.yml) [![Build and Deploy Documentation](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/doc.yml/badge.svg)](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/doc.yml) [![PyPI version](https://badge.fury.io/py/qulacsvis.svg)](https://badge.fury.io/py/qulacsvis) [![MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

qulacs-visualizer is a quantum circuit drawing library for [qulacs](https://github.com/qulacs/qulacs). This library only supports Python and is not available in C/C++.

qulacs-visualizer supports text-based drawing and drawing using [matplotlib](https://github.com/matplotlib/matplotlib). We plan to add support for drawing using LaTeX and outputting LaTeX code using the [qcircuit package](https://github.com/CQuIC/qcircuit).

## Quick Install

Install using `pip` from PyPI:

```
pip install qulacsvis
```

## Example


For more information, see the [documentation](https://qulacs-osaka.github.io/qulacs-visualizer/qulacsvis.visualization.circuit_drawer.html) of the `circuit_drawer()` function.
The documentation describes the other options available.

### Text-Based Drawing

In text-based mode, draws the circuit as ASCII art. This mode is the default behavior.

```py
from qulacs import QuantumCircuit
from qulacsvis import circuit_drawer

# Build a quantum circuit
circuit = QuantumCircuit(3)
circuit.add_X_gate(0)
circuit.add_Y_gate(1)
circuit.add_Z_gate(2)
circuit.add_dense_matrix_gate(
    [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
)
circuit.add_CNOT_gate(2, 0)
circuit.add_X_gate(2)

circuit_drawer(circuit)
```

### Matplotlib Drawing

To use another drawing method, you can specify it by setting a value to the `output_method` argument of the `circuit_drawer()` function.

The `output_method` can be omitted.

```py
# Matplotlib Drawing
circuit_drawer(circuit, output_method="mpl")
# or 
circuit_drawer(circuit, "mpl")
```

## License

[MIT License](LICENSE)

## Contributors

We use [qqcd](https://github.com/mf-22/qqcd) for text-based drawing, a drawing library developed by [@mf-22](https://github.com/mf-22). Thank you.
