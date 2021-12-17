from qulacs import QuantumCircuit

from qulacsvis.visualization.circuit_parser import CircuitParser


def _generate_latex_source(circuit: QuantumCircuit) -> str:
    gate_dict = {
        "I": r"{I}",
        "X": r"{X}",
        "Y": r"{Y}",
        "Z": r"{Z}",
        "H": r"{H}",
        "S": r"{S}",
        "Sdag": r"{S^\dag}",
        "T": r"{T}",
        "Tdag": r"{T^\dag}",
        "sqrtX": r"{\sqrt{X}}",
        "sqrtXdag": r"{\sqrt{X^\dag}}",
        "sqrtY": r"{\sqrt{Y}}",
        "sqrtYdag": r"{\sqrt{Y^\dag}}",
        "Projection-0": r"{P0}",
        "Projection-1": r"{P1}",
        "U1": r"{U1}",
        "U2": r"{U2}",
        "U3": r"{U3}",
        "X-rotation": r"{RX}",
        "Y-rotation": r"{RY}",
        "Z-rotation": r"{RZ}",
        "Pauli": r"{Pauli}",
        "Pauli-rotation": r"{PR}",
        "CZ": r"{CZ}",
        "CNOT": r"\targ",
        "SWAP": r"{SWAP}",
        "Reflection": r"{Ref}",
        "ReversibleBoolean": r"{ReB}",
        "DenseMatrix": r"{DeM}",
        "DinagonalMatrix": r"{DiM}",
        "SparseMatrix": r"{SpM}",
        "Generic gate": r"{GeG}",
        "ParametricRX": r"{pRX}",
        "ParametricRY": r"{pRY}",
        "ParametricRZ": r"{pRZ}",
        "ParametricPauliRotation": r"{pPR}",
        "wire": r"¥qw",
        "ghost": "ghost",
    }
    parser = CircuitParser(circuit)
    qubit_count = parser.qubit_count

    gate_latex = [
        [
            r"        \nghost{ {q}_{" + str(i) + r"} : }",
            r"\lstick{ {q}_{" + str(i) + r"} :  }",
        ]
        for i in range(qubit_count)
    ]

    for i in range(len(parser.gate_info[0])):
        gate_latex_part = [r"\qw" for _ in range(qubit_count)]
        for j in range(qubit_count):
            gate_data = parser.gate_info[j][i]
            name_latex_part = gate_dict[gate_data["raw_text"]]
            target_index_list = gate_data["target_bit"]
            control_index_list = gate_data["control_bit"]

            for target_index in target_index_list:
                name_latex = ""
                if len(target_index_list) == 1:
                    if name_latex_part == r"\targ":
                        name_latex = name_latex_part
                    else:
                        name_latex = r"\gate" + name_latex_part
                else:
                    if target_index == target_index_list[0]:
                        name_latex = r"\multigate{" + str(len(target_index_list)) + r"}"
                        name_latex += name_latex_part
                    else:
                        name_latex = r"\ghost" + name_latex_part
                gate_latex_part[target_index] = name_latex

            for control_index in control_index_list:
                gate_latex_part[control_index] = (
                    r"\ctrl{" + str(target_index_list[0] - control_index) + r"}"
                )

        for qubit in range(qubit_count):
            gate_latex[qubit].append(gate_latex_part[qubit])

    circuit_latex_part = [" & ".join(gate_latex[i]) for i in range(qubit_count)]
    circuit_latex = (r" \\" + "\n").join(circuit_latex_part)

    res = r"""
\documentclass[border=2px]{standalone}
\usepackage[braket, qm]{qcircuit}
\usepackage{graphicx}

\begin{document}
    \scalebox{1.0}{
    \Qcircuit @C=1.0em @R=0.2em @!R { \\
"""
    res += circuit_latex
    res += r""" \\
    }}
\end{document}"""

    return res
