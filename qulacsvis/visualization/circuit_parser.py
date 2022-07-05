import copy
import dataclasses
from typing import List

from qulacs import QuantumCircuit

GATE_DEFAULT_WIDTH = 1.0
GATE_DEFAULT_HEIGHT = 1.5


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
    gate_dict : Dict[str, str]
        A dictionary mapping gate names to their latex representation.
    """

    def __init__(self, circuit: QuantumCircuit):
        self.qubit_count = circuit.get_qubit_count()
        self.gate_info: CircuitData = [[] for _ in range(self.qubit_count)]
        self.layer_width = []

        self.gate_dict = {
            "I": r"$I$",
            "X": r"$X$",
            "Y": r"$Y$",
            "Z": r"$Z$",
            "H": r"$H$",
            "S": r"$S$",
            "Sdag": r"$S^\dag$",
            "T": r"$T$",
            "Tdag": r"$T^\dag$",
            "sqrtX": r"$\sqrt{X}$",
            "sqrtXdag": r"$\sqrt{X^\dag}$",
            "sqrtY": r"$\sqrt{Y}$",
            "sqrtYdag": r"$\sqrt{Y^\dag}$",
            "Projection-0": r"$P0$",
            "Projection-1": r"$P1$",
            "U1": r"$U1$",
            "U2": r"$U2$",
            "U3": r"$U3$",
            "X-rotation": r"$RX$",
            "Y-rotation": r"$RY$",
            "Z-rotation": r"$RZ$",
            "Pauli": r"$Pauli$",
            "Pauli-rotation": r"$PR$",
            "CZ": r"$CZ$",
            "CNOT": r"$\targ$",
            "SWAP": r"$SWAP$",
            "Reflection": r"$Ref$",
            "ReversibleBoolean": r"$ReB$",
            "DenseMatrix": r"$DeM$",
            "DinagonalMatrix": r"$DiM$",
            "SparseMatrix": r"$SpM$",
            "Generic gate": r"$GeG$",
            "ParametricRX": r"$pRX$",
            "ParametricRY": r"$pRY$",
            "ParametricRZ": r"$pRZ$",
            "ParametricPauliRotation": r"$pPR$",
        }

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
