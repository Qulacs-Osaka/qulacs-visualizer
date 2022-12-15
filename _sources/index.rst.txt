.. qulacsvis documentation master file, created by
   sphinx-quickstart on Mon Sep  6 22:48:05 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. Hidden TOCs

.. toctree::
   :caption: Contents
   :maxdepth: 2
   :hidden:

   options
   modules

Welcome to qulacsvis's documentation!
=====================================

qulacs-visualizer is a quantum circuit drawing library for `qulacs <https://github.com/qulacs/qulacs>`_. This library only supports Python. Not available in C/C++.

============
Installation
============

Install using pip from PyPI:

.. code-block:: bash

      pip install qulacsvis

=======
Example
=======

For more information, see the `documentation <https://qulacs-osaka.github.io/qulacs-visualizer/qulacsvis.visualization.circuit_drawer.html>`_ of the ``circuit_drawer()`` function. The documentation describes the other options available.
Or See also :ref:`how_to_use_options`.

******************
Text-Based Drawing
******************

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


******************
Matplotlib Drawing
******************

To use another drawing method, you can specify it by setting a value to the ``output_method`` argument of the ``circuit_drawer()`` function. For matplotlib drawing, set ``output_method="mpl"``.

>>> import matplotlib.pyplot as plt
>>>
>>> circuit_drawer(circuit, "mpl")
>>> plt.show()

.. figure:: _static/circuit_matplotlib_drawing.png
    :alt: circuit_matplotlib_drawing.png


*************
LaTeX Drawing
*************

For LaTeX drawing, set ``output_method="latex"``.

>>> circuit_drawer(circuit, "latex")

.. figure:: _static/circuit_latex_drawing.png
    :alt: circuit_latex_drawing.png

If you want to output LaTeX code, set ``output_method="latex_source"``.

>>> print(circuit_drawer(circuit, "latex_source"))

.. code-block:: latex

  \documentclass[border={-2pt 5pt 5pt -7pt}]{standalone}
  \usepackage[braket, qm]{qcircuit}
  \usepackage{graphicx}

  \begin{document}
      \Qcircuit @C=1.0em @R=0.7em @!R{ \\
          \nghost{ q_{0} : } & \lstick{ q_{0} : } & \gate{X} & \multigate{1}{DeM} & \targ & \qw & \qw\\
          \nghost{ q_{1} : } & \lstick{ q_{1} : } & \gate{Y} & \ghost{DeM} & \qw & \qw & \qw\\
          \nghost{ q_{2} : } & \lstick{ q_{2} : } & \gate{Z} & \qw & \ctrl{-2} & \gate{X} & \qw\\
      }
  \end{document}


-----------
Requirement
-----------

If you want to use LaTeX for drawing, you need to have a local environment where you can run LaTeX (pdflatex).
You will also need the `qcircuit package <https://github.com/CQuIC/qcircuit>`_.
`TeX Live <https://www.tug.org/texlive/>`_ and `MiKTeX <https://miktex.org/>`_ have the qcircuit package installed by default.
