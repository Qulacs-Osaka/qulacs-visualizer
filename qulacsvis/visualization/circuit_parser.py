import dataclasses
from collections import deque
from typing import Deque, List

import dataclasses_json
from qulacs import QuantumCircuit

GATE_DEFAULT_WIDTH = 1.0
GATE_DEFAULT_HEIGHT = 1.5


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class ControlQubitInfo:
    index: int
    control_value: int


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class GateData:
    name: str
    target_bits: List[int] = dataclasses.field(default_factory=list)
    control_bit_infos: List[ControlQubitInfo] = dataclasses.field(default_factory=list)


CircuitData = List[List[GateData]]
QueueCircuitData = List[Deque[GateData]]


class CircuitParser:
    """
    Parse quantum circuit into a list of gate data.

    Parameters
    ----------
    circuit : QuantumCircuit
        Quantum circuit to be parsed.

    Attributes
    ----------
    qubit_count : int
        Number of qubits in the circuit.
    gate_info : CircuitData
        List of gate data.
    layer_width : List[float]
        Width of each layer.
    """

    def __init__(self, circuit: QuantumCircuit):
        self.qubit_count = circuit.get_qubit_count()
        self.layer_width: List[float] = []
        self.__temp_parsed_circuit: QueueCircuitData = [
            deque() for _ in range(self.qubit_count)
        ]
        self.parsed_circuit: CircuitData = [[]]

        for position in range(circuit.get_gate_count()):
            gate = circuit.get_gate(position)
            target_index_list = gate.get_target_index_list()
            control_index_list = gate.get_control_index_list()
            control_index_value_list = [
                ControlQubitInfo(index, control_value)
                for index, control_value in gate.get_control_index_value_list()
            ]
            gate_name = gate.get_name()

            if len(target_index_list) == 0:
                print(
                    f"WARNING: The {position}-th Gate you added is skipped."
                    'This gate does not have "target_qubit_list".'
                )
                continue

            merged_index = target_index_list + control_index_list
            min_merged_index = min(merged_index)
            max_merged_index = max(merged_index)
            self._align_layers(min_merged_index, max_merged_index)

            for index in range(min_merged_index, max_merged_index + 1):
                if index == target_index_list[0]:
                    self.__temp_parsed_circuit[index].append(
                        GateData(gate_name, target_index_list, control_index_value_list)
                    )
                elif index in target_index_list:
                    self.__temp_parsed_circuit[index].append(GateData("ghost"))
                else:
                    self.__temp_parsed_circuit[index].append(GateData("wire"))

        self._align_layers(0, self.qubit_count)
        self.parsed_circuit = [list(queue) for queue in self.__temp_parsed_circuit]
        self.layer_width = [
            GATE_DEFAULT_WIDTH for _ in range(len(self.parsed_circuit[0]))
        ]

    def _align_layers(self, min_line_index: int, max_line_index: int) -> None:
        """
        Align layer sizes for a specified range of rows.

        Parameters
        ----------
        min_line_index : int
            Minimum row index to be aligned.
        max_line_index : int
            Maximum row index to be aligned.
        """
        if min_line_index > max_line_index:
            min_line_index, max_line_index = max_line_index, min_line_index
        lines = self.__temp_parsed_circuit[min_line_index : max_line_index + 1]
        layer_counts = [len(queue) for queue in lines]
        max_layer_count = max(layer_counts)

        for queue, layer_count in zip(lines, layer_counts):
            for _ in range(max_layer_count - layer_count):
                queue.append(GateData("wire"))
