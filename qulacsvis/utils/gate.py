from typing import List

__DEFAULT_GATESTR_MAP = {
    "": "",
    "I": "I",
    "X": "X",
    "Y": "Y",
    "Z": "Z",
    "H": "H",
    "S": "S",
    "Sdag": "Sdg",
    "T": "T",
    "Tdag": "Tdg",
    "sqrtX": "sqX",
    "sqrtXdag": "sXd",
    "sqrtY": "sqY",
    "sqrtYdag": "sYd",
    "Projection-0": "P0",
    "Projection-1": "P1",
    "U1": "U1",
    "U2": "U2",
    "U3": "U3",
    "X-rotation": "RX",
    "Y-rotation": "RY",
    "Z-rotation": "RZ",
    "Pauli": "Pau",
    "Pauli-rotation": "PR",
    "CZ": "CZ",
    "CNOT": "CX",
    "SWAP": "SWP",
    "Reflection": "Ref",
    "ReversibleBoolean": "ReB",
    "DenseMatrix": "DeM",
    "DinagonalMatrix": "DiM",
    "SparseMatrix": "SpM",
    "Generic gate": "GeG",
    "ParametricRX": "pRX",
    "ParametricRY": "pRY",
    "ParametricRZ": "pRZ",
    "ParametricPauliRotation": "pPR",
}

__TO_LATEX_STYLE_GATESTR_MAP = dict(
    __DEFAULT_GATESTR_MAP,
    **{
        "Sdag": r"S^\dag",
        "Tdag": r"T^\dag",
        "sqrtX": r"\sqrt{X}",
        "sqrtXdag": r"\sqrt{X^\dag}",
        "sqrtY": r"\sqrt{Y}",
        "sqrtYdag": r"\sqrt{Y^\dag}",
        "CNOT": r"\targ",
        "SWAP": r"\qswap",
        "wire": r"\qw",
        "ghost": "ghost",
    },
)


def to_text_style(gate_name: str) -> str:
    return __DEFAULT_GATESTR_MAP[gate_name].center(3)


def to_latex_style(gate_name: str) -> str:
    """Get string for latex from gate name.

    Parameters
    ----------
    gate_name : str
        Gate name.

    Returns
    -------
    str
        string for LaTex.

    Raises
    ------
    KeyError
        If gate name is not found.
    """
    return __TO_LATEX_STYLE_GATESTR_MAP[gate_name]


def grouping_adjacent_gates(target_bits: List[int]) -> List[List[int]]:
    """
    Grouping adjacent gates.

    Parameters
    ----------
    target_bit : List[int]
        The target bit list.

    Returns
    -------
    List[List[int]]
        The grouped target bit list.

    Examples
    --------
    >>> target_bits = [1, 2, 3, 5, 7, 8]
    >>> print(grouping_adjacent_gates(target_bits))
    >>> [[1, 2, 3], [5], [7, 8]]
    """

    target_bits.sort()
    groups = []
    adjacent_gates: List[int] = []
    for target_bit in target_bits:
        if adjacent_gates == []:
            adjacent_gates.append(target_bit)
            continue

        if target_bit - 1 in adjacent_gates:
            adjacent_gates.append(target_bit)
        else:
            groups.append(adjacent_gates)
            adjacent_gates = [target_bit]

    groups.append(adjacent_gates)
    return groups
