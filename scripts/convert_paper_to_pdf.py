"""Typeset the paper with a native TeX engine, including math and references."""
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
TEX = PAPER / "when-communication-amplifies-error.tex"


def build():
    tectonic = shutil.which("tectonic")
    local_engine = ROOT / "output/tools/tectonic/tectonic.exe"
    if not tectonic and local_engine.exists():
        tectonic = str(local_engine)
    if tectonic:
        subprocess.run([tectonic, "--keep-logs", TEX.name], cwd=PAPER, check=True)
    elif shutil.which("latexmk"):
        subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", TEX.name], cwd=PAPER, check=True)
    elif shutil.which("pdflatex") and shutil.which("bibtex"):
        latex = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", TEX.name]
        subprocess.run(latex, cwd=PAPER, check=True)
        subprocess.run(["bibtex", TEX.stem], cwd=PAPER, check=True)
        subprocess.run(latex, cwd=PAPER, check=True)
        subprocess.run(latex, cwd=PAPER, check=True)
    else:
        raise SystemExit("Install Tectonic or a TeX distribution with latexmk/pdflatex and BibTeX, then rerun this script.")
    print(f"Built {TEX.with_suffix('.pdf').relative_to(ROOT)}")


if __name__ == "__main__":
    build()
