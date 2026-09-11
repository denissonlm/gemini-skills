#!/usr/bin/env python3
"""Print the communication HTML to PDF with Chrome/Chromium for pixel-perfect fidelity."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
]

WEASYPRINT_PYTHON = Path(
    "/Users/denisson/Documents/Codex/tools/sesmt-html-pdf/bin/python"
)


def find_browser() -> Optional[str]:
    for candidate in CANDIDATES:
        if candidate.is_file():
            return str(candidate)
    for name in (
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
        "microsoft-edge",
        "chrome",
    ):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None


def get_page_count(pdf_path: Path) -> Optional[int]:
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        pass

    if WEASYPRINT_PYTHON.is_file():
        try:
            check = subprocess.run(
                [
                    str(WEASYPRINT_PYTHON),
                    "-c",
                    (
                        "from pypdf import PdfReader; "
                        "import sys; "
                        "print(len(PdfReader(sys.argv[1]).pages))"
                    ),
                    str(pdf_path),
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            return int(check.stdout.strip())
        except Exception:
            pass
    return None


def render_with_browser(browser_bin: str, source: Path, destination: Path) -> None:
    # Try modern --headless=new first, fallback to --headless
    for headless_flag in ("--headless=new", "--headless"):
        command = [
            browser_bin,
            headless_flag,
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--allow-file-access-from-files",
            "--log-level=3",
            f"--print-to-pdf={destination}",
            source.as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if destination.is_file() and destination.stat().st_size > 0:
            return
    raise RuntimeError(f"O navegador falhou ao produzir o PDF: {result.stderr or result.stdout}")


def render_with_weasyprint(source: Path, destination: Path) -> None:
    command = [
        str(WEASYPRINT_PYTHON),
        "-c",
        (
            "from weasyprint import HTML; "
            "import sys; "
            "HTML(filename=sys.argv[1]).write_pdf(sys.argv[2])"
        ),
        str(source),
        str(destination),
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Converte comunicado HTML em PDF A4 de página única com alta fidelidade."
    )
    parser.add_argument("input_html", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()

    source = args.input_html.resolve()
    destination = args.output_pdf.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)

    if not source.is_file():
        raise SystemExit(f"Arquivo HTML de entrada não encontrado: {source}")

    browser_bin = find_browser()
    if browser_bin:
        render_with_browser(browser_bin, source, destination)
    elif WEASYPRINT_PYTHON.is_file():
        print(
            "AVISO: Chrome/Chromium não encontrado. Usando WeasyPrint como contingência "
            "(emojis e flexbox podem sofrer desvios visuais).",
            file=sys.stderr,
        )
        render_with_weasyprint(source, destination)
    else:
        raise SystemExit(
            "Nenhum renderizador compatível encontrado (Chrome/Chromium ou ambiente WeasyPrint). "
            "Instale o Google Chrome para renderização com fidelidade total."
        )

    if not destination.is_file() or destination.stat().st_size == 0:
        raise SystemExit("Erro: o arquivo PDF final não foi gerado ou está vazio.")

    pages = get_page_count(destination)
    if pages is not None and pages != 1:
        raise SystemExit(
            f"Comunicado bloqueado: esperado exatamente 1 página A4, obtido {pages} página(s)."
        )

    print(destination)


if __name__ == "__main__":
    main()

