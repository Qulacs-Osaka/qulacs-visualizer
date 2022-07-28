import os
import subprocess


class _LatexCompiler:
    """
    Compile latex code to pdf.
    """

    def __init__(self) -> None:
        """
        Initialize the latex compiler.
        """
        if not self.has_pdflatex():
            raise Exception("pdflatex not found.")

    def compile(self, code: str, output_dir: str, filename: str) -> None:
        """
        Compile the latex code.

        Parameters
        ----------
        code : str
            The latex code to compile.
        output_dir : str
            The directory to save the pdf file.
        filename : str
            The filename of the latex code (No extension).
        """
        filename_with_ext = filename + ".tex"
        texfile_path = os.path.join(output_dir, filename_with_ext)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(texfile_path, "w") as f:
            f.write(code)
        try:
            subprocess.run(
                [
                    "pdflatex",
                    "-halt-on-error",
                    "-interaction=nonstopmode",
                    f"-output-directory={output_dir}",
                    filename_with_ext,
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as err:
            with open("latex_error.log", "wb") as error_file:
                error_file.write(err.stdout)
            with open("circuit_drawer.tex", "w") as tex_file:
                tex_file.write(code)
            raise Exception(
                "`pdflatex` failed. See `latex_error.log`, `circuit_drawer.tex`"
            ) from err

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


class _PDFtoImage:
    """
    Convert pdf to image with pdftocairo.
    """

    def __init__(self) -> None:
        """
        Initialize the pdf to image converter.
        """
        if not self.has_pdftocairo():
            raise Exception("pdftocairo not found.")

    def convert(self, filename: str, *, ppi: int = 150) -> None:
        """
        Convert the pdf to image.
        <filename>.pdf -> <filename>.png

        Parameters
        ----------
        filename : str
            The filename of the pdf file (No extension).
        ppi : int
            The pixels per inch of the output image.
        """
        pdf_path = filename + ".pdf"

        if not os.path.exists(pdf_path):
            raise Exception("pdf file not found.")

        try:
            subprocess.run(
                [
                    "pdftocairo",
                    "-singlefile",
                    "-png",
                    "-r",
                    f"{ppi}",
                    pdf_path,
                    filename,
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as err:
            with open("pdftocairo_error.log", "wb") as error_file:
                error_file.write(err.stdout)
            raise Exception("`pdftocairo` failed. See `pdftocairo_error.log`") from err

    def has_pdftocairo(self) -> bool:
        """
        Check if pdftocairo is installed.
        """
        try:
            subprocess.run(
                ["pdftocairo", "-v"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except FileNotFoundError:
            return False
