from typing import List

import numpy as np
from qulacs import QuantumCircuit

from qulacsvis.utils.gate import grouping_adjacent_gates, to_latex_style
from qulacsvis.visualization.circuit_parser import CircuitParser, GateData


class LatexSourceGenerator:
    def __init__(self, circuit: QuantumCircuit):
        self.__quantum_circuit = circuit
        self.__parser = CircuitParser(circuit)
        self.__circuit_data = self.__parser.gate_info
        self.circuit = np.array([[]])
        self.head = r"""
\documentclass[border={-2pt 5pt 5pt -7pt}]{standalone}
\usepackage[braket, qm]{qcircuit}
\usepackage{graphicx}

\begin{document}
    \Qcircuit @C=1.0em @R=0.7em @!R{ \\
"""
        self.tail = r"    }" + "\n" + r"\end{document}"

    def generate(self) -> str:
        qubit_count = self.__parser.qubit_count
        circuit_layer_count = len(self.__circuit_data[0])

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

        self.circuit = np.array([[r"\qw"] for _ in range(qubit_count)])
        for layer in range(circuit_layer_count):
            current_layer_latex = [to_latex_style("wire") for _ in range(qubit_count)]
            for qubit in range(qubit_count):
                gate = self.__circuit_data[qubit][layer]

                if gate.name == "ghost":
                    continue
                elif gate.name == "wire":
                    continue
                elif gate.name == "CNOT":
                    self.cnot(current_layer_latex, gate)
                elif gate.name == "SWAP":
                    self.swap(current_layer_latex, gate)
                elif len(gate.target_bits) > 1:
                    self.multi_gate(current_layer_latex, gate)
                else:
                    self.gate(current_layer_latex, gate)

            self.circuit = np.column_stack([self.circuit, current_layer_latex])
        circuit_with_label = np.column_stack([input_label, self.circuit])
        body = self.array_to_qcircuit_style(circuit_with_label)  # type: ignore

        return self.head + body + self.tail

    def array_to_qcircuit_style(self, array: List[List[str]]) -> str:
        lines = [" & ".join(line) for line in array]
        # add indent for latex source file
        indent = "        "
        lines = [indent + line for line in lines]
        res = (r"\\" + "\n").join(lines)
        res += r"\\" + "\n"
        return res

    def cnot(self, layer_latex: List[str], gate: GateData) -> None:
        cnot_qcircuit_style = to_latex_style(gate.name)
        target_bit = gate.target_bits[0]
        layer_latex[target_bit] = cnot_qcircuit_style
        self.control_bits(layer_latex, gate.control_bits, target_bit)

    def control_bits(
        self, layer_latex: List[str], control_bits: List[int], target_bit: int
    ) -> None:
        for control_bit in control_bits:
            layer_latex[control_bit] = r"\ctrl{" + str(target_bit - control_bit) + "}"

    def swap(self, layer_latex: List[str], gate: GateData) -> None:
        swap_qcircuit_style = to_latex_style(gate.name)
        target_index_list = gate.target_bits
        swap = (target_index_list[0], target_index_list[-1])
        layer_latex[swap[0]] = swap_qcircuit_style
        layer_latex[swap[0]] += r" \qwx[" + str(swap[1] - swap[0]) + r"]"
        layer_latex[swap[1]] = swap_qcircuit_style

    def multi_gate(self, layer_latex: List[str], gate: GateData) -> None:
        gate_name_qcircuit_style = to_latex_style(gate.name)
        groups_adjacent_gates = grouping_adjacent_gates(gate.target_bits)

        self.control_bits(layer_latex, gate.control_bits, gate.target_bits[0])

        for adjacent_gates in groups_adjacent_gates:
            size = len(adjacent_gates) - 1
            target_bit = adjacent_gates[0]
            layer_latex[target_bit] = (
                r"\multigate{" + str(size) + "}{" + gate_name_qcircuit_style + "}"
            )

            for target_bit in adjacent_gates[1:]:
                layer_latex[target_bit] = r"\ghost{" + gate_name_qcircuit_style + "}"

        if len(groups_adjacent_gates) > 1:
            for group1, group2 in zip(groups_adjacent_gates, groups_adjacent_gates[1:]):
                from_ = group1[-1]
                to_ = group2[0]
                size = to_ - from_
                layer_latex[from_] += r" \qwx[" + str(size) + "]"

    def gate(self, layer_latex: List[str], gate: GateData) -> None:
        gate_qcircuit_style = r"\gate{" + to_latex_style(gate.name) + "}"
        target_bit = gate.target_bits[0]
        layer_latex[target_bit] = gate_qcircuit_style
        self.control_bits(layer_latex, gate.control_bits, target_bit)
