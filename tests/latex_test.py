from qulacsvis.visualization.latex import LatexCompiler


def test_has_pdflatex() -> None:
    latex = LatexCompiler()
    assert latex.has_pdflatex()


def test_compile() -> None:
    code = r"""
    \documentclass{article}
    \begin{document}
    \end{document}
    """

    latex = LatexCompiler()
    latex.compile(code, "test.tex")
