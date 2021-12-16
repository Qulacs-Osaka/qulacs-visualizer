import numpy as np
from qulacs import QuantumCircuit
from qulacs.gate import CNOT, SWAP, TOFFOLI, DenseMatrix, to_matrix_gate

from qulacsvis.visualization.circuit_parser import CircuitParser


def circuit_parser_test1() -> None:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_Z_gate(2)
    circuit.add_dense_matrix_gate(
        [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    circuit.add_CNOT_gate(2, 0)
    circuit.add_X_gate(2)
    parser = CircuitParser(circuit)
    expected = [
        [
            {
                "raw_text": "X",
                "width": 1.0,
                "height": 1.5,
                "text": "$X$",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [0, 1],
                "control_bit": [],
            },
            {
                "raw_text": "CNOT",
                "width": 1.0,
                "height": 1.5,
                "text": "$\\targ$",
                "target_bit": [0],
                "control_bit": [2],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "Y",
                "width": 1.0,
                "height": 1.5,
                "text": "$Y$",
                "target_bit": [1],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "Z",
                "width": 1.0,
                "height": 1.5,
                "text": "$Z$",
                "target_bit": [2],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "X",
                "width": 1.0,
                "height": 1.5,
                "text": "$X$",
                "target_bit": [2],
                "control_bit": [],
            },
        ],
    ]
    for i in range(len(parser.gate_info[0])):
        for j in range(parser.qubit_count):
            assert parser.gate_info[j][i] == expected[j][i]


def circuit_parser_test2() -> None:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_dense_matrix_gate(
        [0, 1], [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    )
    circuit.add_Z_gate(2)
    circuit.add_CNOT_gate(2, 0)
    circuit.add_X_gate(2)
    parser = CircuitParser(circuit)

    expected = [
        [
            {
                "raw_text": "X",
                "width": 1.0,
                "height": 1.5,
                "text": "$X$",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [0, 1],
                "control_bit": [],
            },
            {
                "raw_text": "CNOT",
                "width": 1.0,
                "height": 1.5,
                "text": "$\\targ$",
                "target_bit": [0],
                "control_bit": [2],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "Y",
                "width": 1.0,
                "height": 1.5,
                "text": "$Y$",
                "target_bit": [1],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "Z",
                "width": 1.0,
                "height": 1.5,
                "text": "$Z$",
                "target_bit": [2],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "X",
                "width": 1.0,
                "height": 1.5,
                "text": "$X$",
                "target_bit": [2],
                "control_bit": [],
            },
        ],
    ]

    for i in range(len(parser.gate_info[0])):
        for j in range(parser.qubit_count):
            assert parser.gate_info[j][i] == expected[j][i]


def circuit_parser_test3() -> None:
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(1)
    circuit.add_CZ_gate(0, 2)
    circuit.add_X_gate(1)
    parser = CircuitParser(circuit)

    expected = [
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "X",
                "width": 1.0,
                "height": 1.5,
                "text": "$X$",
                "target_bit": [1],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "X",
                "width": 1.0,
                "height": 1.5,
                "text": "$X$",
                "target_bit": [1],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "CZ",
                "width": 1.0,
                "height": 1.5,
                "text": "$CZ$",
                "target_bit": [2],
                "control_bit": [0],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
    ]

    for i in range(len(parser.gate_info[0])):
        for j in range(parser.qubit_count):
            assert parser.gate_info[j][i] == expected[j][i]


def circuit_parser_test4() -> None:
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
    parser = CircuitParser(circuit)

    expected = [
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [0],
                "control_bit": [1, 2],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [0],
                "control_bit": [1, 3],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "SWAP",
                "width": 1.0,
                "height": 1.5,
                "text": "$SWAP$",
                "target_bit": [0, 1],
                "control_bit": [],
            },
            {
                "raw_text": "SWAP",
                "width": 1.0,
                "height": 1.5,
                "text": "$SWAP$",
                "target_bit": [0, 2],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "SWAP",
                "width": 1.0,
                "height": 1.5,
                "text": "$SWAP$",
                "target_bit": [1, 3],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [2],
                "control_bit": [1, 3],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [3],
                "control_bit": [2, 0],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [3],
                "control_bit": [1, 2],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
    ]

    for i in range(len(parser.gate_info[0])):
        for j in range(parser.qubit_count):
            assert parser.gate_info[j][i] == expected[j][i]


def circuit_parser_test5() -> None:
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
    parser = CircuitParser(circuit)

    expected = [
        [
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [0, 1, 2],
                "control_bit": [],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [0, 3, 4],
                "control_bit": [1],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [0, 2, 4],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.0,
                "height": 1.5,
                "text": "$DeM$",
                "target_bit": [1, 3],
                "control_bit": [2],
            },
        ],
        [
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.0,
                "height": 1.5,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
    ]

    for i in range(len(parser.gate_info[0])):
        for j in range(parser.qubit_count):
            assert parser.gate_info[j][i] == expected[j][i]
