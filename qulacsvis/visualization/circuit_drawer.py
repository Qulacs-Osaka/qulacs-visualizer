import os
import tempfile
from typing import Optional, Union

from PIL import Image
from qulacsvis.utils.latex import _LatexCompiler, _PDFtoImage

from .latex import _generate_latex_source


def circuit_drawer(
    circuit,
    output_method: Optional[str] = None,
    *,
    ppi: int = 150,
) -> Union[str, Image.Image]:
    """
    Draws a circuit diagram of a circuit.

    Parameters
    ----------
    output_method : Optional[str]
        Set the output method for the drawn circuit.
        If None, the output method is set to 'text'.
    ppi : int
        The pixels per inch of the output image.
    """

    if output_method is None:
        output_method = "text"

    if output_method == "text":
        raise NotImplementedError("Text output_method is not implemented yet.")

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
