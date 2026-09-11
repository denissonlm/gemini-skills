#!/usr/bin/env python3
"""Fill the official two-page RAT or Trajeto template from validated JSON."""

from __future__ import annotations

import argparse
import json
import zipfile
from copy import deepcopy
from pathlib import Path
from typing import Any

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.table import _Cell
from docx.text.paragraph import Paragraph
from lxml import etree
from PIL import Image

from validate_case import validate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    "trabalho": ROOT / "assets" / "template-rat.dotx",
    "trajeto": ROOT / "assets" / "template-trajeto.dotx",
}
TEMPLATE_TYPE = b"application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml"
DOCUMENT_TYPE = b"application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"w": W, "a": A, "r": R, "pr": PR}


def clone_and_sanitize(template: Path, destination: Path) -> None:
    """Convert DOTX to DOCX and remove historical media and metadata."""
    with zipfile.ZipFile(template, "r") as src:
        entries = {info.filename: src.read(info.filename) for info in src.infolist()}
        infos = {info.filename: info for info in src.infolist()}

    entries["[Content_Types].xml"] = entries["[Content_Types].xml"].replace(
        TEMPLATE_TYPE, DOCUMENT_TYPE
    )
    document = etree.fromstring(entries["word/document.xml"])
    rel_path = "word/_rels/document.xml.rels"
    rels = etree.fromstring(entries[rel_path])
    stale_ids: set[str] = set()
    for rel in rels.xpath("./pr:Relationship", namespaces=NS):
        if rel.get("Target", "").endswith("media/image2.png"):
            stale_ids.add(rel.get("Id", ""))
            rels.remove(rel)
    for rid in stale_ids:
        for drawing in document.xpath(
            f'.//w:drawing[.//a:blip[@r:embed="{rid}"]]', namespaces=NS
        ):
            run = drawing.xpath("ancestor::w:r[1]", namespaces=NS)
            if run:
                run[0].getparent().remove(run[0])
            else:
                drawing.getparent().remove(drawing)
    entries["word/document.xml"] = etree.tostring(
        document, xml_declaration=True, encoding="UTF-8", standalone="yes"
    )
    entries[rel_path] = etree.tostring(
        rels, xml_declaration=True, encoding="UTF-8", standalone="yes"
    )
    entries.pop("word/media/image2.png", None)

    core_path = "docProps/core.xml"
    if core_path in entries:
        core = etree.fromstring(entries[core_path])
        for node in core.xpath(
            "//*[local-name()='lastPrinted' or local-name()='created' or local-name()='modified']"
        ):
            node.getparent().remove(node)
        replacements = {
            "creator": "SESMT - Grupo Açotubo",
            "lastModifiedBy": "SESMT - Grupo Açotubo",
            "keywords": "",
            "description": "",
        }
        for local_name, value in replacements.items():
            for node in core.xpath(f"//*[local-name()='{local_name}']"):
                node.text = value
        entries[core_path] = etree.tostring(
            core, xml_declaration=True, encoding="UTF-8", standalone="yes"
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as dst:
        for name, data in entries.items():
            info = infos.get(name)
            dst.writestr(info if info is not None else name, data)


def get_cell(doc: Document, table_index: int, row_index: int, physical_index: int) -> _Cell:
    table = doc.tables[table_index]
    tc = table._tbl.tr_lst[row_index].tc_lst[physical_index]
    return _Cell(tc, table)


def clear_paragraph(paragraph: Any) -> None:
    for child in list(paragraph._p):
        if child.tag != qn("w:pPr"):
            paragraph._p.remove(child)


def set_cell_text(
    cell: _Cell,
    text: Any,
    *,
    size: float = 7.5,
    bold: bool = False,
    italic: bool = True,
    align: WD_ALIGN_PARAGRAPH | None = None,
) -> None:
    paragraphs = cell.paragraphs
    paragraph = paragraphs[0] if paragraphs else cell.add_paragraph()
    clear_paragraph(paragraph)
    for extra in paragraphs[1:]:
        extra._element.getparent().remove(extra._element)
    lines = str(text).splitlines() or [""]
    for index, line in enumerate(lines):
        run = paragraph.add_run(line)
        run.font.name = "Arial Narrow"
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        if index < len(lines) - 1:
            run.add_break()
    if align is not None:
        paragraph.alignment = align
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.0
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_sdt_text(
    sdt: Any,
    value: Any,
    *,
    size: float = 7.5,
    bold: bool = False,
    italic: bool = True,
) -> None:
    texts = sdt.findall(".//" + qn("w:t"))
    if not texts:
        content = sdt.findall("./" + qn("w:sdtContent"))
        if not content:
            return
        paragraph = OxmlElement("w:p")
        run = OxmlElement("w:r")
        text = OxmlElement("w:t")
        run.append(text)
        paragraph.append(run)
        content[0].append(paragraph)
        texts = [text]
    texts[0].text = str(value)
    if str(value).startswith(" ") or str(value).endswith(" "):
        texts[0].set(qn("xml:space"), "preserve")
    for node in texts[1:]:
        node.text = ""
    # Style the run
    run_elem = texts[0].getparent()
    if run_elem is not None and run_elem.tag == qn("w:r"):
        rPr = run_elem.find(qn("w:rPr"))
        if rPr is None:
            rPr = OxmlElement("w:rPr")
            run_elem.insert(0, rPr)
        rFonts = rPr.find(qn("w:rFonts"))
        if rFonts is None:
            rFonts = OxmlElement("w:rFonts")
            rPr.append(rFonts)
        rFonts.set(qn("w:ascii"), "Arial Narrow")
        rFonts.set(qn("w:hAnsi"), "Arial Narrow")
        rFonts.set(qn("w:cs"), "Arial Narrow")
        sz = rPr.find(qn("w:sz"))
        if sz is None:
            sz = OxmlElement("w:sz")
            rPr.append(sz)
        sz.set(qn("w:val"), str(int(size * 2)))
        szCs = rPr.find(qn("w:szCs"))
        if szCs is None:
            szCs = OxmlElement("w:szCs")
            rPr.append(szCs)
        szCs.set(qn("w:val"), str(int(size * 2)))
        i_node = rPr.find(qn("w:i"))
        if italic:
            if i_node is None:
                rPr.append(OxmlElement("w:i"))
        else:
            if i_node is not None:
                rPr.remove(i_node)
        b_node = rPr.find(qn("w:b"))
        if bold:
            if b_node is None:
                rPr.append(OxmlElement("w:b"))
        else:
            if b_node is not None:
                rPr.remove(b_node)


def strip_data_bindings(doc: Document) -> None:
    """Keep the filled display text instead of stale custom-XML values."""
    for sdt in doc._element.xpath(".//w:sdt"):
        for binding in sdt.findall(".//" + qn("w:dataBinding")):
            binding.getparent().remove(binding)


def ensure_when_cell(doc: Document, row_index: int) -> _Cell:
    table = doc.tables[1]
    tr = table._tbl.tr_lst[row_index]
    if len(tr.tc_lst) < 6:
        new_tc = deepcopy(tr.tc_lst[-1])
        header_when = table._tbl.tr_lst[1].tc_lst[-1]
        for old_width in list(new_tc.tcPr.findall(qn("w:tcW"))):
            new_tc.tcPr.remove(old_width)
        if header_when.tcPr.tcW is not None:
            new_tc.tcPr.insert(0, deepcopy(header_when.tcPr.tcW))
        tr.append(new_tc)
        tr_pr = tr.trPr
        if tr_pr is not None:
            for tag in ("w:gridAfter", "w:wAfter"):
                for node in list(tr_pr.findall(qn(tag))):
                    tr_pr.remove(node)
    return _Cell(tr.tc_lst[5], table)


def fit_dimensions(path: Path, max_width: float, max_height: float) -> tuple[float, float]:
    with Image.open(path) as image:
        width, height = image.size
    ratio = min(max_width / width, max_height / height)
    return width * ratio, height * ratio


def add_picture(
    cell: _Cell,
    path_value: str,
    case_folder: Path,
    *,
    max_width: float,
    max_height: float,
    clear: bool = False,
) -> None:
    path = Path(path_value)
    if not path.is_absolute():
        path = case_folder / path
    if not path.is_file():
        raise FileNotFoundError(path)
    if clear:
        set_cell_text(cell, "", italic=False)
        paragraph = cell.paragraphs[0]
    else:
        paragraph = cell.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    width_px, height_px = fit_dimensions(path, max_width * 100, max_height * 100)
    run = paragraph.add_run()
    run.add_picture(
        str(path), width=Inches(width_px / 100), height=Inches(height_px / 100)
    )
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)


def add_caption(cell: _Cell, text: str, *, size: float = 6.2) -> None:
    paragraph = cell.add_paragraph()
    paragraph.paragraph_format.space_before = Pt(1)
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.0
    lines = str(text).splitlines() or [""]
    for index, line in enumerate(lines):
        run = paragraph.add_run(line)
        run.font.name = "Arial Narrow"
        run.font.size = Pt(size)
        run.bold = index == 0
        run.italic = index > 0
        if index < len(lines) - 1:
            run.add_break()


def center_cell(cell: _Cell) -> None:
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for paragraph in cell.paragraphs:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER


def center_sdt_cell(sdt: Any, table: Any) -> None:
    tc_nodes = sdt.xpath("ancestor::*[local-name()='tc'][1]")
    parent: Any = sdt
    if tc_nodes:
        parent = _Cell(tc_nodes[0], table)
        parent.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for paragraph in sdt.xpath(".//*[local-name()='p']"):
        Paragraph(paragraph, parent).alignment = WD_ALIGN_PARAGRAPH.CENTER


def rat_number_only(value: Any) -> str:
    text = str(value).strip()
    return text[3:].strip(" :-") if text.casefold().startswith("rat") else text


# Mapa de simplificação de unidades (case-insensitive substring → nome curto).
_UNIT_MAP = [
    ("tubos e acos", "TA Prod"),
    ("tubos e aços", "TA Prod"),
    ("inox producao", "Inox Prod"),
    ("inox produção", "Inox Prod"),
    ("incotep", "Incotep"),
    ("solucoes", "Soluções"),
    ("soluções", "Soluções"),
    ("joinville", "Joinville"),
    ("canoas", "Canoas"),
    ("caxias", "Caxias do Sul"),
    ("curitiba", "Curitiba"),
    ("sertaozinho", "Sertãozinho"),
    ("sertãozinho", "Sertãozinho"),
    ("minas gerais", "MG"),
    ("belo horizonte", "BH"),
    ("rio de janeiro", "RJ"),
    ("goiania", "Goiânia"),
    ("goiânia", "Goiânia"),
    ("brasilia", "Brasília"),
    ("brasília", "Brasília"),
    ("guarulhos", "Guarulhos"),
]


def format_unit(raw: str) -> str:
    """Simplifica o nome da unidade para exibição no formulário."""
    lower = str(raw).casefold()
    for pattern, short in _UNIT_MAP:
        if pattern in lower:
            return short
    return str(raw).strip()


def format_re(raw: Any) -> str:
    """Formata o RE com separador de milhar: 12553 → 12.553."""
    digits = "".join(filter(str.isdigit, str(raw)))
    if not digits:
        return str(raw)
    return f"{int(digits):,}".replace(",", ".")


def format_team(raw: str, supervisor: str = "") -> str:
    """Garante que o time inclua alguém da Produção.
    - Substitui 'Eng.º Denisson M.' por 'Denisson Monteiro'
    - Remove títulos/abreviações de engenheiro
    - Adiciona supervisor de produção se não houver ninguém além do SESMT
    """
    import re
    text = str(raw).strip()
    # Normalizar nome do autor
    text = re.sub(r"Eng\.?[oº]?\s*Denisson\s+M\.", "Denisson Monteiro", text)
    # Se só tiver SESMT sem ninguém de produção, adiciona supervisor
    if supervisor and "SESMT" in text and "Produção" not in text and "producao" not in text.lower():
        supervisor_clean = supervisor.strip()
        # Abreviar sobrenomes longos: "Gabriel Broetto Maffessoni" → "Gabriel B. Maffessoni"
        parts = supervisor_clean.split()
        if len(parts) >= 3:
            supervisor_clean = f"{parts[0]} {parts[1][0]}. {parts[-1]}"
        text = text.rstrip() + f"\n{supervisor_clean} (Produção)"
    return text


def cell_signature(name: str, re_value: str) -> str:
    name_clean = str(name).strip() if name else ""
    re_clean = str(re_value).strip() if re_value else ""
    generic_names = (
        "médico do trabalho", "medico do trabalho", "representante da cipa",
        "cipeiro", "supervisor", "liderança", "sesmt", "sesmt - grupo açotubo",
        "-", "não aplicável", "nao aplicavel"
    )
    if not name_clean or name_clean.casefold() in generic_names:
        return "Nome:\nRE:"
    if not re_clean or re_clean.casefold() in ("crm/sc", "crm/sp", "cipa", "-", ""):
        return f"{name_clean}\nRE:"
    return f"{name_clean}\nRE: {re_clean}"


def fill_common(doc: Document, data: dict[str, Any], case_folder: Path) -> None:
    victim = data["victim"]
    incident = data["incident"]
    investigation = data["investigation"]
    sdts = doc._element.xpath(".//w:sdt")
    _unit = format_unit(victim["unit"])
    _re = format_re(victim["re"])
    _team = format_team(investigation["team"], victim.get("supervisor", ""))
    sdt_values = {
        0: incident["rat_number"],
        1: _unit,
        2: incident["datetime"],
        3: victim["name"],
        4: _re,
        5: incident["narrative"],
        6: incident["type"],
        7: incident["rat_number"],
        8: incident["location"],
        9: "☒" if int(incident["category"]) == 1 else "☐",
        10: "☒" if int(incident["category"]) == 2 else "☐",
        11: "☒" if int(incident["category"]) == 3 else "☐",
        12: incident["datetime"],
        13: _team,
        14: investigation["root_cause"],
        15: victim["name"],
        16: incident["location"],
        17: incident["date"],
        18: incident["datetime"],
        19: victim["name"],
        20: _re,
        21: incident["location"],
        22: incident["narrative"],
        23: incident["type"],
        24: investigation["start"],
        25: investigation["end"],
        26: _team,
        27: investigation["root_cause"],
        28: data["actions"][0]["status"],
        29: data["actions"][1]["status"],
        30: data["actions"][2]["status"],
        31: victim["name"],
        32: _re,
    }
    if len(sdts) < 33:
        raise RuntimeError(f"Template inesperado: apenas {len(sdts)} controles")
    for index, value in sdt_values.items():
        is_rat = index in (0, 7)
        is_chk = index in (9, 10, 11)
        set_sdt_text(
            sdts[index],
            value,
            size=7.5,
            bold=is_rat,
            italic=not is_rat and not is_chk,
        )

    set_cell_text(get_cell(doc, 0, 1, 3), victim["role"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 1, 7), _unit, size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 1, 9), victim["absence"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 1, 11), victim["contact"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 5, 3), incident["status"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 6, 3), incident["release"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 8, 1), incident["immediate_actions"], size=7.5, italic=True)

    # No campo da lesão, a fotografia vem primeiro e a descrição fica abaixo.
    injury_cell = get_cell(doc, 0, 3, 6)
    add_picture(
        injury_cell,
        data["images"]["injury"],
        case_folder,
        max_width=1.12,
        max_height=1.0,
        clear=True,
    )
    add_caption(injury_cell, "Lesão:\n" + incident["injury"], size=6.1)

    dynamics_cell = get_cell(doc, 0, 4, 6)
    add_picture(
        dynamics_cell,
        data["images"]["dynamics"],
        case_folder,
        max_width=3.55,
        max_height=3.75,
        clear=True,
    )

    for row, item in zip(range(11, 17), investigation["ishikawa"]):
        value = item["analysis"] if isinstance(item, dict) else str(item)
        set_cell_text(get_cell(doc, 0, row, 2), value, size=7.2, italic=True)
    if data["classification"].casefold() == "trabalho":
        add_picture(
            get_cell(doc, 0, 11, 3),
            data["images"]["details"],
            case_folder,
            max_width=2.86,
            max_height=2.45,
            clear=True,
        )
    else:
        set_cell_text(get_cell(doc, 0, 11, 3), investigation["details"], size=7.0, italic=True)
    for physical, why in enumerate(investigation["whys"], start=1):
        set_cell_text(get_cell(doc, 0, 18, physical), why, size=7.0, italic=True)

    set_cell_text(get_cell(doc, 0, 19, 3), investigation["summary"], size=7.2, italic=True)

    for row_index, action in zip(range(2, 5), data["actions"]):
        set_cell_text(get_cell(doc, 1, row_index, 1), action["who"], size=7.5, italic=True)
        set_cell_text(get_cell(doc, 1, row_index, 2), action["what"], size=7.5, italic=True)
        set_cell_text(get_cell(doc, 1, row_index, 3), action["how"], size=7.2, italic=True)
        set_cell_text(get_cell(doc, 1, row_index, 4), action["when"], size=7.5, italic=True)

    # O template mantém STATUS em células envolvidas por controles de conteúdo.
    center_cell(get_cell(doc, 1, 1, 1))
    center_cell(get_cell(doc, 1, 1, 2))
    for row_index in range(2, 5):
        center_cell(get_cell(doc, 1, row_index, 1))
    for index in (28, 29, 30):
        center_sdt_cell(sdts[index], doc.tables[1])

    # O rótulo e o número da RAT ocupam campos separados no template.
    set_cell_text(
        get_cell(doc, 0, 3, 3),
        "*RAT",
        size=7.5,
        bold=True,
        italic=False,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )
    set_cell_text(
        get_cell(doc, 0, 3, 4),
        rat_number_only(incident["rat_number"]),
        size=7.5,
        bold=True,
        italic=False,
        align=WD_ALIGN_PARAGRAPH.CENTER,
    )

    signatures = data["signatures"]
    set_cell_text(
        get_cell(doc, 2, 2, 0),
        cell_signature(signatures.get("author", ""), signatures.get("author_re", "")),
        size=7.5,
        italic=True,
    )
    set_cell_text(
        get_cell(doc, 2, 2, 1),
        cell_signature(victim.get("name", ""), victim.get("re", "")),
        size=7.5,
        italic=True,
    )
    set_cell_text(
        get_cell(doc, 2, 2, 2),
        cell_signature(signatures.get("doctor", ""), signatures.get("doctor_re", "")),
        size=7.5,
        italic=True,
    )
    set_cell_text(
        get_cell(doc, 2, 2, 3),
        cell_signature(signatures.get("cipeiro", ""), signatures.get("cipeiro_re", "")),
        size=7.5,
        italic=True,
    )
    set_cell_text(
        get_cell(doc, 2, 2, 4),
        cell_signature(signatures.get("supervisor", ""), signatures.get("supervisor_re", "")),
        size=7.5,
        italic=True,
    )
    witness_val = signatures.get("witnesses", "") or victim.get("witnesses", "")
    if not witness_val or witness_val.casefold() in ("-", "não se aplica", "nenhuma", "sem testemunhas"):
        witness_val = "Não Aplicável"
    set_cell_text(get_cell(doc, 2, 1, 5), witness_val, size=7.5, italic=True)


def fill_workplace(doc: Document, data: dict[str, Any]) -> None:
    victim = data["victim"]
    investigation = data["investigation"]
    witness_val = victim.get("witnesses", "")
    if not witness_val or witness_val.casefold() in ("-", "não se aplica", "nenhuma", "sem testemunhas"):
        witness_val = "Não Aplicável"
    set_cell_text(get_cell(doc, 0, 2, 2), witness_val, size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 2, 4), victim["supervisor"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 2, 6), victim["experience"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 2, 8), victim["recurrence"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 20, 3), investigation["unsafe_act"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 21, 3), investigation["unsafe_condition"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 22, 2), investigation["containment_24h"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 23, 2), investigation["potential"], size=7.5, italic=True)


def fill_trajectory(doc: Document, data: dict[str, Any]) -> None:
    victim = data["victim"]
    route = data["route"]
    investigation = data["investigation"]
    set_cell_text(get_cell(doc, 0, 2, 2), route["origin"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 2, 4), route["destination"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 2, 6), victim["experience"], size=7.5, italic=True)
    set_cell_text(get_cell(doc, 0, 2, 8), route["deviation"], size=7.5, italic=True)
    details = (
        f"Tipo de trajeto: {route['direction']}\n"
        f"Meio de transporte: {route['transport']}\n"
        f"Envolvimento de terceiros: {route['third_parties']}\n"
        f"BO: {route['police_report']}\n\n"
        f"{route['clarification']}\n\n{investigation['details']}"
    )
    set_cell_text(get_cell(doc, 0, 11, 3), details, size=6.8, italic=True)
    set_cell_text(get_cell(doc, 0, 20, 3), investigation["behavioral_factor"], size=7.2, italic=True)
    set_cell_text(get_cell(doc, 0, 21, 3), investigation["technical_factor"], size=7.2, italic=True)
    set_cell_text(get_cell(doc, 0, 22, 3), investigation["climatic_factor"], size=7.2, italic=True)
    set_cell_text(get_cell(doc, 0, 23, 2), investigation["containment_24h"], size=7.2, italic=True)
    set_cell_text(get_cell(doc, 0, 24, 2), investigation["potential"], size=7.2, italic=True)


def fix_page_break_spacing(doc: Document) -> None:
    """Ensure paragraph containing page break between Folha 1 and Folha 2 has zero height so it fits on Page 1."""
    for p in doc.paragraphs:
        if p._p.xpath(".//w:br[@w:type='page']"):
            pPr = p._p.find(qn("w:pPr"))
            if pPr is None:
                pPr = OxmlElement("w:pPr")
                p._p.insert(0, pPr)
            for child in list(pPr):
                if child.tag.split("}")[-1] in ("spacing", "rPr"):
                    pPr.remove(child)
            spacing = OxmlElement("w:spacing")
            spacing.set(qn("w:before"), "0")
            spacing.set(qn("w:after"), "0")
            spacing.set(qn("w:line"), "20")
            spacing.set(qn("w:lineRule"), "exact")
            pPr.append(spacing)
            rPr = OxmlElement("w:rPr")
            sz = OxmlElement("w:sz")
            sz.set(qn("w:val"), "2")
            rPr.append(sz)
            pPr.append(rPr)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_json", type=Path)
    parser.add_argument("output_docx", type=Path)
    parser.add_argument("--case-folder", type=Path)
    parser.add_argument("--draft", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.case_json.read_text(encoding="utf-8"))
    errors = validate(data, require_approvals=not args.draft)
    if errors:
        raise SystemExit("BLOQUEADO:\n- " + "\n- ".join(errors))

    classification = data["classification"].casefold()
    template = TEMPLATES[classification]
    case_folder = (args.case_folder or args.case_json.parent).resolve()
    temp_docx = args.output_docx.with_suffix(".building.docx")
    clone_and_sanitize(template, temp_docx)
    doc = Document(temp_docx)
    fill_common(doc, data, case_folder)
    if classification == "trabalho":
        fill_workplace(doc, data)
    else:
        fill_trajectory(doc, data)
    strip_data_bindings(doc)
    fix_page_break_spacing(doc)
    args.output_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(args.output_docx)
    temp_docx.unlink(missing_ok=True)
    print(args.output_docx)


if __name__ == "__main__":
    main()
