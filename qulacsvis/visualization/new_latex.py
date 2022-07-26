from typing import List

from qulacs import QuantumCircuit

from qulacsvis.utils.gate import to_latex_style
from qulacsvis.visualization.circuit_parser import CircuitParser, GateData


def to_qcircuit_style(gate_name: str) -> str:
    return "{" + to_latex_style(gate_name) + "}"


class LatexSourceGenerator:
    def __init__(self, circuit: QuantumCircuit):
        self.__quantum_circuit = circuit
        self.__parser = CircuitParser(circuit)
        self.__circuit_data = self.__parser.gate_info
        self.circuit: List[List[str]] = []

    def generate(self) -> str:
        qubit_count = self.__parser.qubit_count
        circuit_layer_count = len(self.__circuit_data[0])

        input_label = [
            [
                # nghost reserves drawing area for input label,
                # adjusts the spacing between rows.
                r"\nghost{ q_{" + str(i) + "} : }",
                r"\lstick{ q_{" + str(i) + "} : }",
            ]
            for i in range(qubit_count)
        ]

        # TODO Add wire
        # self.circuit = [[r"\qw"] for _ in range(qubit_count)]
        self.circuit = [[] for _ in range(qubit_count)]
        for layer in range(circuit_layer_count):
            for qubit in range(qubit_count):
                current_layer_latex = [
                    to_latex_style("wire") for _ in range(qubit_count)
                ]
                gate = self.__circuit_data[qubit][layer]

                if gate.name == "ghost":
                    current_layer_latex[qubit] = "ghost"
                elif gate.name == "wire":
                    current_layer_latex[qubit] = to_latex_style(gate.name)
                elif gate.name == "CNOT":
                    self.cnot(current_layer_latex, gate)
                elif gate.name == "SWAP":
                    self.swap(current_layer_latex, gate)
                elif len(gate.target_bits) > 1:
                    self.multi_gate(current_layer_latex, gate)
                else:
                    self.gate(current_layer_latex, gate)

        return "TODO generate latex code"

    def cnot(self, layer_latex: List[str], gate: GateData) -> None:
        raise NotImplementedError

    def swap(self, layer_latex: List[str], gate: GateData) -> None:
        swap_qcircuit_style = to_latex_style(gate.name)
        target_index_list = gate.target_bits
        swap = (target_index_list[0], target_index_list[-1])
        layer_latex[swap[0]] = swap_qcircuit_style
        layer_latex[swap[0]] += r" \qwx[" + str(swap[1] - swap[0]) + r"]"
        layer_latex[swap[1]] = swap_qcircuit_style

    def multi_gate(self, layer_latex: List[str], gate: GateData) -> None:
        raise NotImplementedError

    def gate(self, layer_latex: List[str], gate: GateData) -> None:
        raise NotImplementedError
