from typing import Dict

import numpy as np
from qulacs import QuantumCircuit
from qulacs.gate import CNOT, TOFFOLI, DenseMatrix, to_matrix_gate


def load_circuit_data() -> Dict[str, QuantumCircuit]:
    circuits = {}
    circuits["empty_circuit"] = empty_circuit()
    circuits["x_gate_circuit"] = x_gate_circuit()
    circuits["y_gate_circuit"] = y_gate_circuit()
    circuits["z_gate_circuit"] = z_gate_circuit()
    circuits["cz_gate_circuit"] = cz_gate_circuit()
    circuits["cnot_gate_circuit"] = cnot_gate_circuit()
    circuits["ctl_wire_should_not_overlap"] = ctl_wire_should_not_overlap()
    circuits["swap_circuit"] = swap_circuit()
    circuits[
        "multiple_swap_gates_should_not_overlap"
    ] = multiple_swap_gates_should_not_overlap()
    circuits["dense_matrix_gate_circuit"] = dense_matrix_gate_circuit()
    circuits[
        "dense_matrix_gate_with_target_bits"
    ] = dense_matrix_gate_with_target_bits()
    circuits[
        "dense_matrix_gate_with_separated_target_bits"
    ] = dense_matrix_gate_with_separated_target_bits()
    circuits[
        "dense_matrix_gate_should_not_overlap"
    ] = dense_matrix_gate_should_not_overlap()
    circuits["toffoli_gate_circuit"] = toffoli_gate_circuit()
    circuits["xyz_horizontal_circuit"] = xyz_horizontal_circuit()
    circuits["xyz_vertical_circuit"] = xyz_vertical_circuit()
    return circuits


def empty_circuit() -> QuantumCircuit:
    return QuantumCircuit(3)


def x_gate_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(1)
    circuit.add_X_gate(0)
    return circuit


def y_gate_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(1)
    circuit.add_Y_gate(0)
    return circuit


def z_gate_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(1)
    circuit.add_Z_gate(0)
    return circuit


def cz_gate_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(2)
    circuit.add_CZ_gate(0, 1)
    circuit.add_CZ_gate(1, 0)
    return circuit


def cnot_gate_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(2)
    circuit.add_CNOT_gate(0, 1)
    circuit.add_CNOT_gate(1, 0)
    return circuit


def ctl_wire_should_not_overlap() -> QuantumCircuit:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(1)
    circuit.add_CZ_gate(0, 2)
    circuit.add_X_gate(1)
    circuit.add_CNOT_gate(0, 2)
    circuit.add_X_gate(1)
    return circuit


def swap_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(2)
    circuit.add_SWAP_gate(0, 1)
    circuit.add_SWAP_gate(1, 0)
    return circuit


def multiple_swap_gates_should_not_overlap() -> QuantumCircuit:
    circuit = QuantumCircuit(4)
    circuit.add_SWAP_gate(0, 2)
    circuit.add_SWAP_gate(1, 3)
    return circuit


def dense_matrix_gate_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(2)
    circuit.add_dense_matrix_gate(
        [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    return circuit


def dense_matrix_gate_with_target_bits() -> QuantumCircuit:
    circuit = QuantumCircuit(3)
    # CCX0,1, 2
    cx_gate = CNOT(1, 2)
    cx_mat_gate = to_matrix_gate(cx_gate)
    control_index = 0
    control_with_value = 1
    cx_mat_gate.add_control_qubit(control_index, control_with_value)
    circuit.add_gate(cx_mat_gate)
    return circuit


def dense_matrix_gate_with_separated_target_bits() -> QuantumCircuit:
    circuit = QuantumCircuit(5)
    mat = np.identity(2 ** 3)
    # 3-qubit gate applied to [0,3,4], and [1] qubit is control-qubit
    c_dense_gate = DenseMatrix([0, 3, 4], mat)
    control_index = 1
    control_with_value = 1
    c_dense_gate.add_control_qubit(control_index, control_with_value)
    circuit.add_gate(c_dense_gate)
    return circuit


def dense_matrix_gate_should_not_overlap() -> QuantumCircuit:
    circuit = QuantumCircuit(5)
    mat = np.identity(2 ** 3)
    # 3-qubit gate applied to [0,2,4]
    circuit.add_dense_matrix_gate([0, 2, 4], mat)
    # 2-qubit gate applied to [1,3]
    mat = np.identity(2 ** 2)
    circuit.add_dense_matrix_gate([1, 3], mat)
    return circuit


def toffoli_gate_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(3)
    ccx = TOFFOLI(0, 1, 2)
    circuit.add_gate(ccx)
    ccx = TOFFOLI(1, 2, 0)
    circuit.add_gate(ccx)
    ccx = TOFFOLI(0, 2, 1)
    circuit.add_gate(ccx)
    return circuit


def xyz_horizontal_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(1)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(0)
    circuit.add_Z_gate(0)
    return circuit


def xyz_vertical_circuit() -> QuantumCircuit:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_Z_gate(2)
    return circuit
