from typing import List

from qulacs import QuantumCircuit

from qulacsvis.utils.gate import to_latex_style, grouping_adjacent_gates
from qulacsvis.visualization.circuit_parser import CircuitParser, GateData

import numpy as np


def to_qcircuit_style(gate_name: str) -> str:
    return "{" + to_latex_style(gate_name) + "}"


class LatexSourceGenerator:
    def __init__(self, circuit: QuantumCircuit):
        self.__quantum_circuit = circuit
        self.__parser = CircuitParser(circuit)
        self.__circuit_data = self.__parser.gate_info
        self.circuit = np.array([[]])

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

        return self.array_to_qcircuit_style(circuit_with_label)  # type:ignore

    def array_to_qcircuit_style(self, array: List[List[str]]) -> str:
        liens = [" & ".join(line) for line in array]
        res = (r"\\" + "\n").join(liens)
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

    def gate(self, layer_latex: List[str], gate: GateData) -> None:
        gate_qcircuit_style = r"\gate{" + to_latex_style(gate.name) + "}"
        target_bit = gate.target_bits[0]
        layer_latex[target_bit] = gate_qcircuit_style
        self.control_bits(layer_latex, gate.control_bits, target_bit)
