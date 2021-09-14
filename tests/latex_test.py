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
    \end{document}
    """

    latex = LatexCompiler()
    latex.compile(code, "test")


@pytest.mark.runlatex
def test_fail_compile() -> None:
    code = r"""
    \documentclass{article}
    \begin{document}
    % missing end
    """

    latex = LatexCompiler()
    with pytest.raises(Exception):
        latex.compile(code, "test")
