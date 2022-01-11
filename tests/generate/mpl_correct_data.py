import os
import sys

import matplotlib.pyplot as plt
from qulacsvis.visualization import MPLCircuitlDrawer

sys.path.append(os.path.join("tests"))

from circuit_test_data import load_circuit_data  # noqa

OUTPUT_DIR = os.path.join("tests", "images", "matplotlib")

if __name__ == "__main__":
    test_data = load_circuit_data()

    for name, circuit in test_data.items():
        drawer = MPLCircuitlDrawer(circuit)
        fig = drawer.draw()
        plt.savefig(os.path.join(OUTPUT_DIR, name + ".png"))
