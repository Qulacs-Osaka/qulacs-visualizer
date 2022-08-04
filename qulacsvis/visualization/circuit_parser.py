import copy
import dataclasses
from typing import List

import dataclasses_json
from qulacs import QuantumCircuit

GATE_DEFAULT_WIDTH = 1.0
GATE_DEFAULT_HEIGHT = 1.5


@dataclasses_json.dataclass_json
@dataclasses.dataclass
class GateData:
    name: str
    target_bits: List[int] = dataclasses.field(default_factory=list)
    control_bits: List[int] = dataclasses.field(default_factory=list)


CircuitData = List[List[GateData]]


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
        self.gate_info: CircuitData = [[] for _ in range(self.qubit_count)]
        self.layer_width = []

        default_value = GateData("wire")
        layer_info: List[GateData] = [
            copy.deepcopy(default_value) for _ in range(self.qubit_count)
        ]
        gate_num = circuit.get_gate_count()

        for i in range(gate_num):
            gate = circuit.get_gate(i)
            if len(gate.get_target_index_list()) == 0:
                print(
                    """CAUTION: The {}-th Gate you added is skipped.\
                    This gate does not have "target_qubit_list".""".format(
                        i
                    )
                )
                continue
            target_index_list = gate.get_target_index_list()
            control_index_list = gate.get_control_index_list()
            index_list = target_index_list + control_index_list
            gate_name = gate.get_name()

            conflict = False
            for index in range(min(index_list), max(index_list) + 1):
                if layer_info[index].name != "wire":
                    conflict = True
            if conflict:
                self.append_layer(layer_info, default_value)

            for index in range(min(index_list), max(index_list) + 1):
                layer_info[index].name = "used"
            for target_index in target_index_list:
                if target_index == target_index_list[0]:
                    layer_info[target_index].name = gate_name
                    layer_info[target_index].target_bits = target_index_list
                    layer_info[target_index].control_bits = control_index_list
                else:
                    layer_info[target_index].name = "ghost"

        self.append_layer(layer_info, default_value)

        self.layer_width = [GATE_DEFAULT_WIDTH for _ in range(len(self.gate_info[0]))]

    def append_layer(self, layer_info: List[GateData], default_value: GateData) -> None:
        """
        Append a layer to the layer_info.

        Parameters
        ----------
        layer_info : List[GateData]
            A list of gate data.
        default_value : GateData
            A default value of gate data.
        """
        is_blank = True
        for qubit in range(self.qubit_count):
            if layer_info[qubit].name != "wire":
                is_blank = False
        if not is_blank:
            for qubit in range(self.qubit_count):
                if layer_info[qubit].name == "used":
                    layer_info[qubit].name = "wire"
            for qubit in range(self.qubit_count):
                self.gate_info[qubit].append(layer_info[qubit])
                layer_info[qubit] = copy.deepcopy(default_value)
