from qulacs import QuantumCircuit

from qulacsvis.visualization.circuit_parser import CircuitParser


def test_matplotlib_init() -> None:
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
