# qulacs-visualizer

[![CI](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/ci.yml/badge.svg)](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/ci.yml) [![Build and Deploy Documentation](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/doc.yml/badge.svg)](https://github.com/Qulacs-Osaka/qulacs-visualizer/actions/workflows/doc.yml) [![PyPI version](https://badge.fury.io/py/qulacsvis.svg)](https://badge.fury.io/py/qulacsvis) [![MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

qulacs-visualizer is a quantum circuit drawing library for [qulacs](https://github.com/qulacs/qulacs). This library only supports Python. Not available in C/C++.

qulacs-visualizer supports the following methods.

- Text-Based Drawing
- Matplotlib Drawing
  - using [matplotlib](https://github.com/matplotlib/matplotlib)
- LaTeX Drawing
  - using LaTeX and the [qcircuit package](https://github.com/CQuIC/qcircuit)


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

# Draw a quantum circuit
circuit_drawer(circuit)
```
```
   ___     ___     ___
  | X |   |DeM|   |CX |
--|   |---|   |---|   |----------
  |___|   |   |   |___|
   ___    |   |     |
  | Y |   |   |     |
--|   |---|   |-----|------------
  |___|   |___|     |
   ___              |      ___
  | Z |             |     | X |
--|   |-------------●-----|   |--
  |___|                   |___|
```

### Matplotlib Drawing

To use another drawing method, you can specify it by setting a value to the `output_method` argument of the `circuit_drawer()` function. For matplotlib drawing, set `output_method="mpl"`.

```py
circuit_drawer(circuit, "mpl")
```

![circuit_matplotlib_drawing.png](doc/source/_static/circuit_matplotlib_drawing.png)

## LaTeX Drawing

For LaTeX drawing, set `output_method="latex"`.

```py
circuit_drawer(circuit, "latex")
```

![circuit_latex_drawing.png](doc/source/_static/circuit_latex_drawing.png)

### Requirement

If you want to use LaTeX for drawing, you need to have a local environment where you can run LaTeX (pdflatex).
You will also need the [qcircuit package](https://github.com/CQuIC/qcircuit).
[TeX Live](https://www.tug.org/texlive/) and [MiKTeX](https://miktex.org/) have the qcircuit package installed by default.

## License

[MIT License](LICENSE)

## Contributors

We use [qqcd](https://github.com/mf-22/qqcd) for text-based drawing, a drawing library developed by [@mf-22](https://github.com/mf-22). Thank you.
