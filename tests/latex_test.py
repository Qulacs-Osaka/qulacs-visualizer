import os
import tempfile

import pytest
from qulacsvis.utils.latex import LatexCompiler


@pytest.mark.runlatex
def test_has_pdflatex() -> None:
    latex = LatexCompiler()
    assert latex.has_pdflatex()


@pytest.mark.runlatex
def test_compile() -> None:
    code = r"""
    \documentclass{article}
    \begin{document}
    Test Document Body
    \end{document}
    """

    latex = LatexCompiler()
    with tempfile.TemporaryDirectory() as tmpdir:
        latex = LatexCompiler()
        latex.compile(code, tmpdir, "test")
        assert os.path.exists(os.path.join(tmpdir, "test.pdf"))


@pytest.mark.runlatex
def test_fail_compile() -> None:
    code = r"""
    \documentclass{article}
    \begin{document}
    % missing end
    """

    latex = LatexCompiler()
    with pytest.raises(Exception):
        with tempfile.TemporaryDirectory() as tmpdir:
            latex = LatexCompiler()
            latex.compile(code, tmpdir, "test")
