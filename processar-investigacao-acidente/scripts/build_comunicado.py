#!/usr/bin/env python3
"""Fill the approved SESMT communication HTML without inventing fields."""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
from pathlib import Path
from typing import Any

from validate_case import validate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "comunicado-template.html"


def get(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(dotted)
        value = value[part]
    if value is None or str(value).strip() in {"", "-", "?"}:
        raise ValueError(f"Campo ausente: {dotted}")
    return value


def picture_tag(path_value: str, case_folder: Path) -> str:
    path = Path(path_value)
    if not path.is_absolute():
        path = case_folder / path
    if not path.is_file():
        raise FileNotFoundError(path)
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f'<img src="data:{mime};base64,{encoded}" alt="Registro da lesão do caso">'


def format_unit(raw: str) -> str:
    """Simplifica o nome da unidade (mesmo mapa de build_investigation.py)."""
    _UNIT_MAP = [
        ("tubos e acos", "TA Prod"), ("tubos e aços", "TA Prod"),
        ("inox producao", "Inox Prod"), ("inox produção", "Inox Prod"),
        ("incotep", "Incotep"), ("solucoes", "Soluções"), ("soluções", "Soluções"),
        ("joinville", "Joinville"), ("canoas", "Canoas"),
        ("caxias", "Caxias do Sul"), ("curitiba", "Curitiba"),
        ("sertaozinho", "Sertãozinho"), ("sertãozinho", "Sertãozinho"),
        ("minas gerais", "MG"), ("belo horizonte", "BH"), ("rio de janeiro", "RJ"),
        ("goiania", "Goiânia"), ("goiânia", "Goiânia"),
        ("brasilia", "Brasília"), ("brasília", "Brasília"),
        ("guarulhos", "Guarulhos"),
    ]
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_json", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument("--case-folder", type=Path)
    parser.add_argument("--draft", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.case_json.read_text(encoding="utf-8"))
    errors = validate(data, require_approvals=not args.draft)
    if errors:
        raise SystemExit("BLOQUEADO:\n- " + "\n- ".join(errors))
    case_folder = (args.case_folder or args.case_json.parent).resolve()
    communication = data.get("communication")
    if not isinstance(communication, dict):
        raise SystemExit("Campo communication ausente no JSON")

    severity = str(get(data, "communication.severity")).casefold()
    if severity not in {"leve", "moderado", "grave"}:
        raise SystemExit("communication.severity deve ser leve, moderado ou grave")

    replacements = {
        "DATA_EXPEDICAO": get(data, "document.publication_date"),
        "NUMERO_RAT": get(data, "incident.rat_number"),
        "NOME_VITIMA": get(data, "victim.name"),
        "RE_VITIMA": format_re(get(data, "victim.re")),
        "CARGO_VITIMA": get(data, "victim.role"),
        "UNIDADE_ACIDENTE": format_unit(get(data, "victim.unit")),
        "DATA_HORA_ACIDENTE": get(data, "incident.datetime"),
        "LIDER_IMEDIATO": get(data, "victim.supervisor"),
        "REINCIDENCIA_SN": get(data, "victim.recurrence"),
        "TIPO_ACIDENTE": get(data, "incident.type"),
        "TESTEMUNHAS": get(data, "victim.witnesses"),
        "LOCAL_ACIDENTE": get(data, "incident.location"),
        "AFASTAMENTO_SN_MOTIVO": get(data, "victim.absence"),
        "TEMPO_EXPERIENCIA_ADMISSAO": get(data, "victim.experience"),
        "DESCRICAO_O_QUE_HOUVE": get(data, "incident.narrative"),
        "DESCRICAO_ACOES_IMEDIATAS": get(data, "incident.immediate_actions"),
        "DESCRICAO_LESAO": get(data, "incident.injury"),
        "DESCRICAO_CONDICAO_VITIMA": get(data, "incident.status"),
        "SEVERIDADE_LEVE_CLASS": "marked" if severity == "leve" else "",
        "SEVERIDADE_MODERADA_CLASS": "marked" if severity == "moderado" else "",
        "SEVERIDADE_GRAVE_CLASS": "marked" if severity == "grave" else "",
        "VIDEO_METADADOS": communication.get("video_metadata", ""),
        "LINK_VIDEO_SHAREPOINT": communication.get("video_link", ""),
    }

    image_value = get(data, "images.injury")
    replacements["IMAGEM_LESAO_TAG"] = picture_tag(str(image_value), case_folder)

    source = TEMPLATE.read_text(encoding="utf-8")
    raw_keys = {"IMAGEM_LESAO_TAG"}
    for key, value in replacements.items():
        rendered = str(value) if key in raw_keys else html.escape(str(value), quote=True)
        source = source.replace("{{" + key + "}}", rendered)

    video_confirmed = communication.get("video_confirmed") is True
    if not video_confirmed:
        source = re.sub(
            r"<!-- ▌VIDEO -->.*?(?=<!-- ▌FOOTER -->)",
            "",
            source,
            flags=re.DOTALL,
        )
    elif not replacements["VIDEO_METADADOS"] or not replacements["LINK_VIDEO_SHAREPOINT"]:
        raise SystemExit("Vídeo confirmado exige video_metadata e video_link confirmados")

    leftovers = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", source)))
    if leftovers:
        raise SystemExit("Placeholders não preenchidos: " + ", ".join(leftovers))
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(source, encoding="utf-8")
    print(args.output_html)


if __name__ == "__main__":
    main()
