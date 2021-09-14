import tempfile
from typing import Optional

from qulacsvis.utils.latex import LatexCompiler


def circuit_drawer(output_method: Optional[str] = None):  # type: ignore
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
            latex.compile(latex_source, tmpdir, "circuit_drawer")

    elif output_method == "latex_source":
        return generate_latex_source()


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
    \end{document}
    """
    return generated_latex_code
