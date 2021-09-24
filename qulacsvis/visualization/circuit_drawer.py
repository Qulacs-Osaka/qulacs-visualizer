import os
import tempfile
from typing import Optional, Union

from PIL import Image
from qulacs import QuantumCircuit
from qulacsvis.utils.latex import _LatexCompiler, _PDFtoImage

from .latex import _generate_latex_source
from .text import TextCircuitDrawer


def circuit_drawer(
    circuit: QuantumCircuit,
    output_method: Optional[str] = None,
    *,
    ppi: int = 150,
    verbose: bool = False,
    dot: str = "large"
) -> Union[str, Image.Image, None]:
    """
    Draws a circuit diagram of a circuit.

    Parameters
    ----------
    circuit : qulacs.QuantumCircuit
        The quantum circuit to be drawn.
    output_method : Optional[str]
        Set the output method for the drawn circuit.
        If None, the output method is set to 'text'.
    ppi : int
        The pixels per inch of the output image.
    verbose : bool
        If True, a number will be added to the gate.
        Gates are numbered in the order in which they are added to the circuit.
    dot: str
        Dot style to mean control qubit(default="large")

    Returns
    -------
    Union[str, Image.Image, None]
        The output of the circuit drawer.
        If output_method is 'text', the output is a None. Circuit is output to stdout.
        If output_method is 'latex', the output is an Image.Image object.
        If output_method is 'latex_source', the output is a string.

    Raises
    ------
    ValueError
        If the output_method is not 'text', 'latex', or 'latex_source'.

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
    --|   |---|   |---|   |-----x----
      |___|   |   |   |___|     |
       ___    |   |     |       |
      | Y |   |   |     |       |
    --|   |---|   |-----|-------x----
      |___|   |___|     |
       ___              |      ___
      | Z |             |     | X |
    --|   |-------------●-----|   |--
      |___|                   |___|
    """

    if output_method is None:
        output_method = "text"

    if output_method == "text":
        drawer = TextCircuitDrawer(circuit, dot=dot)  # type: ignore
        drawer.draw(verbose=verbose)  # type: ignore
        return None

    elif output_method == "latex":
        with tempfile.TemporaryDirectory() as tmpdir:
            latex_source = _generate_latex_source(circuit)
            latex = _LatexCompiler()
            pdftoimage = _PDFtoImage()

            latex.compile(latex_source, tmpdir, "circuit_drawer")
            pdftoimage.convert(os.path.join(tmpdir, "circuit_drawer"), ppi=ppi)

            image = Image.open(os.path.join(tmpdir, "circuit_drawer.png"))
            return image

    elif output_method == "latex_source":
        return _generate_latex_source(circuit)

    else:
        raise ValueError(
            "Invalid output_method. Valid options are: 'text', 'latex', 'latex_source'."
        )
