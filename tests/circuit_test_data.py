from typing import List

import numpy as np
from qulacs import QuantumCircuit
from qulacs.gate import CNOT, SWAP, TOFFOLI, DenseMatrix, to_matrix_gate


def load_circuit_data() -> List[QuantumCircuit]:
    circuits = []
    circuits.append(simple_circuit1())
    circuits.append(simple_circuit2())
    circuits.append(circuit_with_CZgate())
    circuits.append(circuit_with_DenseMatrix_SWAP())
    circuits.append(circuit_with_DeM_with_multiple_target_bits())
    return circuits


def simple_circuit1() -> QuantumCircuit:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_Z_gate(2)
    circuit.add_dense_matrix_gate(
        [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    circuit.add_CNOT_gate(2, 0)
    circuit.add_X_gate(2)
    return circuit


def simple_circuit2() -> QuantumCircuit:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_dense_matrix_gate(
        [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    circuit.add_Z_gate(2)
    circuit.add_CNOT_gate(2, 0)
    circuit.add_X_gate(2)
    return circuit


def circuit_with_CZgate() -> QuantumCircuit:
    # Example3
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(1)
    circuit.add_CZ_gate(0, 2)
    circuit.add_X_gate(1)
    return circuit


def circuit_with_DenseMatrix_SWAP() -> QuantumCircuit:
    # Example4
    circuit = QuantumCircuit(4)
    # CCX0,2, 3
    cx_gate = CNOT(2, 3)
    cx_mat_gate = to_matrix_gate(cx_gate)
    control_index = 0
    control_with_value = 1
    cx_mat_gate.add_control_qubit(control_index, control_with_value)
    circuit.add_gate(cx_mat_gate)
    # CCX1,2, 3
    ccx = TOFFOLI(1, 2, 3)
    circuit.add_gate(ccx)
    # CCX1,2, 0
    ccx = TOFFOLI(1, 2, 0)
    circuit.add_gate(ccx)
    # CCX1,3, 0
    ccx = TOFFOLI(1, 3, 0)
    circuit.add_gate(ccx)
    # CCX1,3, 2
    ccx = TOFFOLI(1, 3, 2)
    circuit.add_gate(ccx)
    # SWAP0,1
    circuit.add_SWAP_gate(0, 1)
    # SWAP0,2
    circuit.add_SWAP_gate(0, 2)
    # SWAP1,3
    circuit.add_SWAP_gate(1, 3)
    return circuit


def circuit_with_DeM_with_multiple_target_bits() -> QuantumCircuit:
    # Example5
    circuit = QuantumCircuit(5)
    # 3-qubit gate applied to [0,1,2]
    mat = np.identity(2 ** 3)
    circuit.add_dense_matrix_gate([0, 1, 2], mat)
    # 3-qubit gate applied to [0,3,4], and [1] qubit is control-qubit
    c_dense_gate = DenseMatrix([0, 3, 4], mat)
    control_index = 1
    control_with_value = 1
    c_dense_gate.add_control_qubit(control_index, control_with_value)
    circuit.add_gate(c_dense_gate)
    # 3-qubit gate applied to [0,2,4]
    circuit.add_dense_matrix_gate([0, 2, 4], mat)
    # SWAP gate aplied to [1,3], and [2] qubit is control-qubit
    swp_gate = to_matrix_gate(SWAP(1, 3))
    control_index = 2
    control_with_value = 1
    swp_gate.add_control_qubit(control_index, control_with_value)
    circuit.add_gate(swp_gate)
    return circuit
