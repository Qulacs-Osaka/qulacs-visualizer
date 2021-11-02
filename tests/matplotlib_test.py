from qulacs import QuantumCircuit
from qulacsvis.visualization.matplotlob import MatplotlibDrawer


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
    mlp_drawer = MatplotlibDrawer(circuit)
    expected = [
        [
            {
                "raw_text": "X",
                "width": 0.65,
                "height": 0.65,
                "text": "$X$",
                "target_bit": [0],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "DenseMatrix",
                "width": 1.173,
                "height": 0.65,
                "text": "$DeM$",
                "target_bit": [0, 1],
                "control_bit": [],
            },
            {
                "raw_text": "CNOT",
                "width": 0.65,
                "height": 0.65,
                "text": "$\\targ$",
                "target_bit": [0],
                "control_bit": [2],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "Y",
                "width": 0.65,
                "height": 0.65,
                "text": "$Y$",
                "target_bit": [1],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "ghost",
                "width": 1.173,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
        ],
        [
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "Z",
                "width": 0.65,
                "height": 0.65,
                "text": "$Z$",
                "target_bit": [2],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 1.173,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "wire",
                "width": 0.65,
                "height": 0.65,
                "text": "",
                "target_bit": [],
                "control_bit": [],
            },
            {
                "raw_text": "X",
                "width": 0.65,
                "height": 0.65,
                "text": "$X$",
                "target_bit": [2],
                "control_bit": [],
            },
        ],
    ]
    for i in range(len(mlp_drawer.gate_info[0])):
        for j in range(mlp_drawer.qubit_count):
            assert mlp_drawer.gate_info[j][i] == expected[j][i]
