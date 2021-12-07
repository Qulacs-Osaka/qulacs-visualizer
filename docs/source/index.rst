.. qulacsvis documentation master file, created by
   sphinx-quickstart on Mon Sep  6 22:48:05 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to qulacsvis's documentation!
=====================================

qulacs-visualizer is a quantum circuit drawing library for `qulacs <https://github.com/qulacs/qulacs>`_. This library only supports Python and is not available in C/C++.

************
Installation
************

Install using pip from PyPI:

.. code-block:: bash

      pip install qulacsvis

*******
Example
*******

For more information, see the `documentation <https://qulacs-osaka.github.io/qulacs-visualizer/qulacsvis.visualization.circuit_drawer.html>`_ of the ``circuit_drawer()`` function. The documentation describes the other options available.

------------------
Text-Based Drawing
------------------

In text-based mode, draws the circuit as ASCII art. This mode is the default behavior.

>>> from qulacs import QuantumCircuit
>>> from qulacsvis import circuit_drawer
>>>
>>> # Build a quantum circuit
>>> circuit = QuantumCircuit(3)
>>> circuit.add_X_gate(0)
>>> circuit.add_Y_gate(1)
>>> circuit.add_Z_gate(2)
>>> circuit.add_dense_matrix_gate(
...     [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
... )
>>> circuit.add_CNOT_gate(2, 0)
>>> circuit.add_X_gate(2)
>>>
>>> circuit_drawer(circuit)
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


------------------
Matplotlib Drawing
------------------

To use another drawing method, you can specify it by setting a value to the ``output_method`` argument of the ``circuit_drawer()`` function.

The ``output_method`` can be omitted.

>>> # Matplotlib Drawing
>>> circuit_drawer(circuit, output_method="mpl")
>>> # or
>>> circuit_drawer(circuit, "mpl")

.. figure:: _static/simple_circuit1.png
    :alt: simple_circuit1.png
