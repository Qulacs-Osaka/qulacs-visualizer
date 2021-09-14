from typing import Optional


def circuit_drawer(output_method: Optional[str] = None) -> None:
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

    if output_method == "latex":
        raise NotImplementedError("Latex output_method is not implemented yet.")

    if output_method == "latex_source":
        raise NotImplementedError("Latex source output_method is not implemented yet.")
