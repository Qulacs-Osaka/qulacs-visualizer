import os
import tempfile
from typing import Optional, Union

from PIL import Image
from qulacsvis.utils.latex import LatexCompiler, PDFtoImage


def circuit_drawer(
    output_method: Optional[str] = None,
) -> Union[str, Image.Image]:
    """
    Draws a circuit diagram of a circuit.

    Parameters
    ----------
    output_method : Optional[str]
        Set the output method for the drawn circuit.
    """

    if output_method is None:
        output_method = "text"

    if output_method == "text":
        raise NotImplementedError("Text output_method is not implemented yet.")

    elif output_method == "latex":
        with tempfile.TemporaryDirectory() as tmpdir:
            latex_source = generate_latex_source()
            latex = LatexCompiler()
            pdftoimage = PDFtoImage()

            latex.compile(latex_source, tmpdir, "circuit_drawer")
            pdftoimage.convert(os.path.join(tmpdir, "circuit_drawer"))

            image = Image.open(os.path.join(tmpdir, "circuit_drawer.png"))
            return image

    elif output_method == "latex_source":
        return generate_latex_source()

    else:
        raise ValueError(
            "Invalid output_method. Valid options are: 'text', 'latex', 'latex_source'."
        )


def generate_latex_source() -> str:
    """
    Generates a latex source code of a circuit.

    Returns
    -------
    str
        The latex source code of the circuit.
    """

    generated_latex_code = r"""
    \documentclass{article}
    \begin{document}
    Circuit diagram goes here.
    \end{document}
    """
    return generated_latex_code
