from qulacs import QuantumCircuit

from ..qulacs.circuit import to_model


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
    gate_info : GateDataSeq
        List of gate data.
    """

    def __init__(self, circuit: QuantumCircuit):
        circuit_data = to_model(circuit)
        self.qubit_count = circuit_data.qubit_count
        self.parsed_circuit = circuit_data.gates
