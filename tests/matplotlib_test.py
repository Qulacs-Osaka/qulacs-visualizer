import sys
from pathlib import Path

import matplotlib
import pytest
from packaging.version import Version
from qulacs import QuantumCircuit
from qulacsvis.visualization import MPLCircuitlDrawer

from .circuit_test_data import load_circuit_data

MPL_VERSION = Version(matplotlib.__version__)

baseline_dir = "baseline"

ftv = matplotlib.ft2font.__freetype_version__.replace(".", "")
hash_filename = f"mpl{MPL_VERSION.major}{MPL_VERSION.minor}_ft{ftv}.json"
hash_library = Path(__file__).parent / "baseline" / "hashes" / hash_filename
print(hash_library)

WIN = sys.platform.startswith("win")

# In some cases, the fonts on Windows can be quite different
# https://github.com/matplotlib/pytest-mpl/blob/2611bd020b523ab4fff1c9fa7db936b68dad7113/tests/test_pytest_mpl.py#L39 # noqa
DEFAULT_TOLERANCE = 10 if WIN else 2

"""
generate hash_library
poetry run pytest --mpl-generate-hash-library=tests/baseline/hashes/mpl34_ft261.json
"""

testdatas = load_circuit_data()


@pytest.mark.parametrize(
    "circuit", list(testdatas.values()), ids=list(testdatas.keys())
)
@pytest.mark.mpl_image_compare(hash_library=hash_library)
def test_draw_with_mpl(circuit: QuantumCircuit) -> matplotlib.figure.Figure:
    drawer = MPLCircuitlDrawer(circuit)
    fig = drawer.draw()
    return fig
