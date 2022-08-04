from typing import List

import numpy as np
from qulacs import QuantumCircuit

from qulacsvis.utils.gate import grouping_adjacent_gates, to_latex_style
from qulacsvis.visualization.circuit_parser import CircuitParser, GateData


class LatexSourceGenerator:
    """Generate latex source from QuantumCircuit

    Parameters
    ----------
    circuit : QuantumCircuit
        A quantum circuit to be drawn.

    Attributes
    ----------
    _quantum_circuit : QuantumCircuit
        A quantum circuit to be drawn.
    _parser : CircuitParser
        The parser of the quantum circuit.
    _circuit_data : CircuitData
        The data of the quantum circuit after parsing by CircuitParser.
    _circuit : numpy.ndarray
        A matrix containing strings converted from CircuitData for Qcircuit.
        Each element and its position corresponds to one of GateData.
        Quantum circuit only, input values are not contained.
    _head : str
        The head of the latex source containing preamble.
    _tail : str
        The tail of the latex source.

    Examples
    --------
    >>> from qulacs import QuantumCircuit
    >>> from qulacsvis.visualization import LatexSourceGenerator
    >>>
    >>> circuit = QuantumCircuit(3)
    >>> circuit.add_X_gate(0)
    >>> circuit.add_Y_gate(1)
    >>> circuit.add_Z_gate(2)
    >>>
    >>> generator = LatexSourceGenerator(circuit)
    >>> latex_source = generator.generate()
    >>> print(latex_source)
    """

    def __init__(self, circuit: QuantumCircuit):
        self._quantum_circuit = circuit
        self._parser = CircuitParser(circuit)
        self._circuit_data = self._parser.gate_info
        self._circuit = np.array([[]])
        self._head = r"""
\documentclass[border={-2pt 5pt 5pt -7pt}]{standalone}
\usepackage[braket, qm]{qcircuit}
\usepackage{graphicx}

\begin{document}
    \Qcircuit @C=1.0em @R=0.7em @!R{ \\
"""
        self._tail = r"    }" + "\n" + r"\end{document}"

    def generate(self) -> str:
        """Generate latex source from QuantumCircuit

        Returns
        -------
        latex_source : str
            String of latex source generated
        """
        qubit_count = self._parser.qubit_count
        circuit_layer_count = len(self._circuit_data[0])

        input_label = np.array(
            [
                [
                    # nghost reserves drawing area for input label,
                    # adjusts the spacing between rows.
                    r"\nghost{ q_{" + str(i) + "} : }",
                    r"\lstick{ q_{" + str(i) + "} : }",
                ]
                for i in range(qubit_count)
            ]
        )

        self._circuit = np.array([[] for _ in range(qubit_count)])
        for layer in range(circuit_layer_count):
            # This is an array containing strings.
            # The string for each element is the string for the Qcircuit of the gate corresponding to each qubit row of the layer currently of interest.
            current_layer_latex = [to_latex_style("wire") for _ in range(qubit_count)]
            for qubit in range(qubit_count):
                gate = self._circuit_data[qubit][layer]

                if gate.name == "ghost":
                    continue
                elif gate.name == "wire":
                    continue
                elif gate.name == "CNOT":
                    self._cnot(current_layer_latex, gate)
                elif gate.name == "SWAP":
                    self._swap(current_layer_latex, gate)
                elif len(gate.target_bits) > 1:
                    self._multi_gate(current_layer_latex, gate)
                else:
                    self._gate(current_layer_latex, gate)

            self._circuit = np.column_stack([self._circuit, current_layer_latex])
        wires = np.array([[r"\qw"] for _ in range(qubit_count)])
        circuit_with_label = np.column_stack([input_label, self._circuit, wires])
        body = self._matrix_to_qcircuit_style(circuit_with_label)  # type: ignore

        return self._head + body + self._tail

    def _matrix_to_qcircuit_style(self, matrix: List[List[str]]) -> str:
        """Generate from matrix to string for Qcircuit

        Parameters
        ----------
        matrix : List[List[str]]
            A matrix containing strings converted from CircuitData for Qcircuit.
        Returns
        -------
        res : str
            Generated string for Qcircuit from matrix
        """
        lines = [" & ".join(line) for line in matrix]
        # add indent for latex source file
        indent = "        "
        lines = [indent + line for line in lines]
        res = (r"\\" + "\n").join(lines)
        res += r"\\" + "\n"
        return res

    def _cnot(self, layer_latex: List[str], gate: GateData) -> None:
        """Generate CNOT gate for Qcircuit

        Parameters
        ----------
        layer_latex : List[str]
            Array containing the string of the gate of the layer currently of interest
        gate : GateData
            The gate data to be drawn.
        """
        cnot_qcircuit_style = to_latex_style(gate.name)
        target_bit = gate.target_bits[0]
        layer_latex[target_bit] = cnot_qcircuit_style
        self._control_bits(layer_latex, gate.control_bits, target_bit)

    def _control_bits(
        self, layer_latex: List[str], control_bits: List[int], target_bit: int
    ) -> None:
        """Generate control bits for Qcircuit

        Parameters
        ----------
        layer_latex : List[str]
            Array containing the string of the gate of the layer currently of interest
        control_bits : List[int]
            The control bits of the gate to be drawn.
        target_bit : int
            A target bit of the gate.
            This value is used to generate the line connecting the target bit and control bits.
        """
        for control_bit in control_bits:
            layer_latex[control_bit] = r"\ctrl{" + str(target_bit - control_bit) + "}"

    def _swap(self, layer_latex: List[str], gate: GateData) -> None:
        """Generate SWAP gate for Qcircuit

        Parameters
        ----------
        layer_latex : List[str]
            Array containing the string of the gate of the layer currently of interest
        gate : GateData
            The gate data to be drawn.
        """
        swap_qcircuit_style = to_latex_style(gate.name)
        target_index_list = gate.target_bits
        swap = (target_index_list[0], target_index_list[-1])
        layer_latex[swap[0]] = swap_qcircuit_style
        layer_latex[swap[0]] += r" \qwx[" + str(swap[1] - swap[0]) + r"]"
        layer_latex[swap[1]] = swap_qcircuit_style

    def _multi_gate(self, layer_latex: List[str], gate: GateData) -> None:
        """Generate multi gate for Qcircuit (e.g., DensityMatrixGate)

        Parameters
        ----------
        layer_latex : List[str]
            Array containing the string of the gate of the layer currently of interest
        gate : GateData
            The gate data to be drawn.
        """
        gate_name_qcircuit_style = to_latex_style(gate.name)
        groups_adjacent_gates = grouping_adjacent_gates(gate.target_bits)

        self._control_bits(layer_latex, gate.control_bits, gate.target_bits[0])

        for adjacent_gates in groups_adjacent_gates:
            size = len(adjacent_gates) - 1
            target_bit = adjacent_gates[0]
            # The "\multi_gate" should be placed in one location and "\ghost" in the other.
            layer_latex[target_bit] = (
                r"\multigate{" + str(size) + "}{" + gate_name_qcircuit_style + "}"
            )

            for target_bit in adjacent_gates[1:]:
                layer_latex[target_bit] = r"\ghost{" + gate_name_qcircuit_style + "}"

        if len(groups_adjacent_gates) > 1:
            # Generate the line connecting the each group
            for group1, group2 in zip(groups_adjacent_gates, groups_adjacent_gates[1:]):
                from_ = group1[-1]
                to_ = group2[0]
                size = to_ - from_
                layer_latex[from_] += r" \qwx[" + str(size) + "]"

    def _gate(self, layer_latex: List[str], gate: GateData) -> None:
        """Generate a gate for Qcircuit

        Parameters
        ----------
        layer_latex : List[str]
            Array containing the string of the gate of the layer currently of interest
        gate : GateData
            The gate data to be drawn.
        """
        gate_qcircuit_style = r"\gate{" + to_latex_style(gate.name) + "}"
        target_bit = gate.target_bits[0]
        layer_latex[target_bit] = gate_qcircuit_style
        self._control_bits(layer_latex, gate.control_bits, target_bit)
