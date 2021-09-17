import os
import tempfile
from typing import Optional, Union

from PIL import Image
from qulacsvis.utils.latex import _LatexCompiler, _PDFtoImage


def circuit_drawer(
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
            latex_source = _generate_latex_source()
            latex = _LatexCompiler()
            pdftoimage = _PDFtoImage()

            latex.compile(latex_source, tmpdir, "circuit_drawer")
            pdftoimage.convert(os.path.join(tmpdir, "circuit_drawer"), ppi=ppi)

            image = Image.open(os.path.join(tmpdir, "circuit_drawer.png"))
            return image

    elif output_method == "latex_source":
        return _generate_latex_source()

    else:
        raise ValueError(
            "Invalid output_method. Valid options are: 'text', 'latex', 'latex_source'."
        )


def _generate_latex_source() -> str:
    """
    Generates a latex source code of a circuit.

    Returns
    -------
    str
        The latex source code of the circuit.
    """

    generated_latex_code = r"""
\documentclass[12pt,border={25pt 5pt 5pt 5pt}]{standalone}

\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[cmex10]{amsmath}

\usepackage{qcircuit}
\usepackage{braket}

\begin{document}

\Qcircuit @C=1em @R=.7em {
  \lstick{\ket{0}} & \gate{H} & \ctrl{1} & \qw          & \qw      & \meter \\
  \lstick{\ket{0}} & \qw      & \targ    & \ctrl{1}     & \qw      & \meter \\
  \lstick{\ket{0}} & \qw      & \gate{H} & \control \qw & \gate{H} & \meter
}

\end{document}
    """
    return generated_latex_code
