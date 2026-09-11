#!/usr/bin/env python3
"""Check a generated DOCX for template residue, third-case leakage, and routing."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TEXT = ("23/02/2026", "Cleber Edmar")
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stale_media_hashes() -> set[str]:
    hashes: set[str] = set()
    for name in ("template-rat.dotx", "template-trajeto.dotx"):
        with zipfile.ZipFile(ROOT / "assets" / name) as zf:
            try:
                hashes.add(sha256(zf.read("word/media/image2.png")))
            except KeyError:
                pass
    return hashes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("case_json", type=Path)
    args = parser.parse_args()
    data = json.loads(args.case_json.read_text(encoding="utf-8"))
    errors: list[str] = []
    with zipfile.ZipFile(args.docx) as zf:
        xml_names = [
            name
            for name in zf.namelist()
            if name == "word/document.xml"
            or re.fullmatch(r"word/(header|footer)\d+\.xml", name)
        ]
        text_parts = []
        for name in xml_names:
            root = etree.fromstring(zf.read(name))
            text_parts.extend(root.xpath(".//w:t/text()", namespaces=NS))
        text = " ".join(" ".join(text_parts).split())
        media_hashes = {
            sha256(zf.read(name)) for name in zf.namelist() if name.startswith("word/media/")
        }

    for value in FORBIDDEN_TEXT:
        if value in text:
            errors.append(f"resíduo do template encontrado: {value}")
    if "{{" in text or "}}" in text:
        errors.append("placeholder não preenchido encontrado")
    for expected in (
        data["victim"]["name"],
        str(data["victim"]["re"]),
        data["incident"]["rat_number"],
        data["incident"]["date"],
    ):
        if expected not in text:
            errors.append(f"valor esperado ausente: {expected}")
    expected_title = (
        "INVESTIGAÇÃO DE ACIDENTE DO TRABALHO"
        if data["classification"] == "trabalho"
        else "INVESTIGAÇÃO DE ACIDENTE DE TRAJETO"
    )
    if expected_title not in text:
        errors.append("template incompatível com a classificação")
    if media_hashes & stale_media_hashes():
        errors.append("imagem histórica residual do template encontrada")

    if errors:
        print("REPROVADO")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(2)
    print("APROVADO: sem resíduos conhecidos e com roteamento correto.")


if __name__ == "__main__":
    main()
