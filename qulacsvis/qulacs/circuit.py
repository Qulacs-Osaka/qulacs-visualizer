from qulacs import QuantumCircuit

from ..models.circuit import CircuitData, ControlQubitInfo, GateData


def to_model(circuit: QuantumCircuit) -> CircuitData:
    qubit_count = circuit.get_qubit_count()
    gates = []

    for position in range(circuit.get_gate_count()):
        gate = circuit.get_gate(position)
        target_index_list = gate.get_target_index_list()
        control_index_value_list = [
            ControlQubitInfo(index, control_value)
            for index, control_value in gate.get_control_index_value_list()
        ]
        gate_name = gate.get_name()
        gates.append(GateData(gate_name, target_index_list, control_index_value_list))

    return CircuitData.from_gate_sequence(gates, qubit_count)
