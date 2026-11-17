"""
@file export_pdf.py
@brief Exports the circuit as a TikZ pdf.
@author Evan Roe
@date 2026-11-16
"""
from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

COMPILE_TIMEOUT_S = 60

@dataclass(frozen=True)
class PdfExportResult:
    """Defines the result of the pdf export."""
    pdf_path: Path | None
    log_tail: str
    reason: str
    
    
def pdflatex_available() -> bool:
    """Checks if a pdflatex executable is on PATH."""
    return shutil.which('pdflatex') is not None

def tex_to_pdf(tex: str, output_pdf: Path, timeout_s: int = COMPILE_TIMEOUT_S) -> PdfExportResult:
    """Compiles to tex to pdf to output_pdf."""
    if not pdflatex_available:
        return PdfExportResult(
            pdf_path=None, log_tail='',
            reason="pdflatex not found on PATH",
            )
    exe = shutil.which('pdflatex')
    with tempfile.TemporaryDirectory(prefix="circuit_pdf_") as tmp:
        tmp_dir = Path(tmp)
        tex_file = tmp_dir / 'circuit.tex'
        tex_file.write_text(tex, encoding='utf-8')

        cmd = [
            exe,
            '-interaction=nonstopmode',
            '-halt-on-error',
            f'-output-directory={tmp_dir}',
            str(tex_file),
        ]
        try:
            proc = subprocess.run(
                cmd,
                cwd=tmp_dir,
                capture_output=True,
                timeout=timeout_s,
                text=True,
            )
        except subprocess.TimeoutExpired:
            return PdfExportResult(
                pdf_path=None, log_tail='',
                reason=f"Pdflatex timed out after {timeout_s}s",
            )
        except OSError as exc:
            return PdfExportResult(
                pdf_path=None, log_tail='',
                reason=f"Pdflatex could not be run, error: {exc}",
            )

        produced = tmp_dir / 'circuit.pdf'

        if proc.returncode != 0 or not produced.exists():
            return PdfExportResult(
                pdf_path=None, log_tail=_log_tail(tmp_dir, proc),
                reason=f"Pdflatex was unsuccessful, code: {proc.returncode}", 
            )
        if output_pdf.parent is None:
            return PdfExportResult(
                pdf_path=None, log_tail='',
                reason="Output pdf parent folder does not exist", 
            )
        shutil.copyfile(produced, output_pdf)
        return PdfExportResult(
            pdf_path=output_pdf, log_tail='', reason='',
        )

def _log_tail(tmp_dir: Path, proc: subprocess.CompletedProcess[str]) -> str:
    """Returns the useful end of the LaTeX log for debugging."""
    log_file = tmp_dir / 'circuit.log'
    text = log_file.read_text(encoding='utf-8', errors='replace')
    if not log_file.exists():
        return proc.stdout + proc.stderr
    lines = [ln for ln in text.splitlines() if ln.strip()]
    errors = [ln for ln in lines if ln.startswith('!')]
    return '\n'.join((errors or lines)[-25:])
        
        








    