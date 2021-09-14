import subprocess
import tempfile


class LatexCompiler:
    """
    Compile latex code to pdf.
    """

    def __init__(self) -> None:
        """
        Initialize the latex compiler.
        """
        if not self.has_pdflatex():
            raise Exception("pdflatex not found.")

    def compile(self, code: str, filename: str) -> None:
        """
        Compile the latex code.

        Parameters
        ----------
        code : str
            The latex code to compile.
        filename : str
            The filename of the latex code.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(tmpdir + "/" + filename + ".tex", "w") as f:
                f.write(code)
            try:
                subprocess.run(
                    [
                        "pdflatex",
                        "-halt-on-error",
                        "-interaction=nonstopmode",
                        f"-output-directory={tmpdir}",
                        tmpdir + "/" + filename + ".tex",
                    ],
                    check=True,
                    text=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                print(e.output)
                raise Exception("pdflatex failed.")

    def has_pdflatex(self) -> bool:
        """
        Check if latex is installed.
        """
        try:
            subprocess.run(
                ["pdflatex", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except FileNotFoundError:
            return False
