from qulacs import QuantumCircuit
from qulacsvis.visualization.matplotlib import MPLCircuitlDrawer

if __name__ == "__main__":
    circuit = QuantumCircuit(3)
    circuit.add_X_gate(0)
    circuit.add_Y_gate(1)
    circuit.add_Z_gate(2)

    mpl_drawer = MPLCircuitlDrawer(circuit)
    mpl_drawer.draw()  # type: ignore
