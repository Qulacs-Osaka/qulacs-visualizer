import os
import tempfile
from typing import Optional, Union

import matplotlib.pyplot as plt
from PIL import Image
from qulacs import QuantumCircuit

from qulacsvis.utils.latex import _LatexCompiler, _PDFtoImage

from .latex import LatexSourceGenerator
from .matplotlib import MPLCircuitlDrawer
from .text import TextCircuitDrawer


def circuit_drawer(
    circuit: QuantumCircuit,
    output_method: Optional[str] = None,
    *,
    verbose: bool = False,
    dot: str = "large",
    ppi: int = 150,
    dpi: int = 72,
    scale: float = 0.6,
) -> Union[str, Image.Image, None]:
    """
    Draws a circuit diagram of a circuit.

    Parameters
    ----------
    circuit : qulacs.QuantumCircuit
        The quantum circuit to be drawn.
    output_method : Optional[str], optional
        Set the output method for the drawn circuit.
        If None, the output method is set to 'text'.
    verbose : bool optional default=False
        (output_method='text')
        If True, a number will be added to the gate.
        Gates are numbered in the order in which they are added to the circuit.
    dot: str optional default='large'
        (output_method='text')
        Dot style to mean control qubit(default="large")
    ppi : int optional default=150
        (output_method='latex')
        The pixels per inch of the output image.
    dpi : int optional default=72
        (output_method='mpl')
        The dots per inch of the output image.
    scale : float optional default=0.6
        (output_method='mpl')
        The scale of the output image.

    Returns
    -------
    Union[str, Image.Image, None]
        The output of the circuit drawer.
        If output_method is 'text', the output is a None. Circuit is output to stdout.
        If output_method is 'latex', the output is an Image.Image object.
        If output_method is 'latex_source', the output is a string.
        If output_method is 'mpl', the output is a None.
        Circuit is drawn to a matplotlib figure.

    Raises
    ------
    ValueError
        If output_method is not 'text', 'latex', 'latex_source', or 'mpl'.

    Examples
    --------
    >>> from qulacs import QuantumCircuit
    >>> from qulacsvis.visualization import circuit_drawer
    >>> circuit = QuantumCircuit(3)
    >>> circuit.add_X_gate(0)
    >>> circuit.add_Y_gate(1)
    >>> circuit.add_Z_gate(2)
    >>> circuit.add_dense_matrix_gate(
    >>>     [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    >>> )
    >>> circuit.add_CNOT_gate(2, 0)
    >>> circuit.add_X_gate(2)
    >>> circuit_drawer(circuit, output_method='text')
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
    """

    if output_method is None:
        output_method = "text"

    if output_method == "text":
        text_drawer = TextCircuitDrawer(circuit, dot=dot)
        text_drawer.draw(verbose=verbose)  # type: ignore
        return None

    elif output_method == "latex":
        with tempfile.TemporaryDirectory() as tmpdir:
            generator = LatexSourceGenerator(circuit)
            latex_source = generator.generate()
            latex = _LatexCompiler()
            pdftoimage = _PDFtoImage()

            latex.compile(latex_source, tmpdir, "circuit_drawer")
            pdftoimage.convert(os.path.join(tmpdir, "circuit_drawer"), ppi=ppi)

            image = Image.open(os.path.join(tmpdir, "circuit_drawer.png"))
            return image

    elif output_method == "latex_source":
        generator = LatexSourceGenerator(circuit)
        latex_source = generator.generate()
        return latex_source

    elif output_method == "mpl":
        mpl_drawer = MPLCircuitlDrawer(circuit, dpi=dpi, scale=scale)
        mpl_drawer.draw()
        plt.show()
        return None

    else:
        raise ValueError(
            "Invalid output_method. Valid options are: 'text', 'latex', 'latex_source', 'mpl'."
        )
