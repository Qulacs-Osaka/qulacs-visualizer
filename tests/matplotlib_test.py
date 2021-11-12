import pytest
from matplotlib import figure
from qulacs import QuantumCircuit
from qulacsvis.visualization import MPLCircuitlDrawer

from .circuit_test_data import load_circuit_data


@pytest.mark.parametrize("circuit", [*load_circuit_data()])
def test_draw_with_matplotlib(circuit: QuantumCircuit) -> None:
    drawer = MPLCircuitlDrawer(circuit)
    fig = drawer.draw()
    assert isinstance(fig, figure.Figure)
