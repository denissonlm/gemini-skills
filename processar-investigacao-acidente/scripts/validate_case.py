#!/usr/bin/env python3
"""Reject incomplete or unconfirmed accident case data before authoring."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PLACEHOLDERS = {
    "",
    "-",
    "?",
    "a definir",
    "não encontrado",
    "nao encontrado",
    "desconhecido",
    "pendente de confirmação",
    "pendente de confirmacao",
    "todo",
    "preencher",
}

# Campos administrativos que podem permanecer vazios somente quando o usuário
# autorizar expressamente o preenchimento manual posterior. Conteúdo técnico,
# causas e plano de ação nunca entram nesta exceção.
CONFIRMED_BLANK_ALLOWED = {
    "victim.contact",
    "signatures.author_re",
    "signatures.doctor",
    "signatures.doctor_re",
    "signatures.cipeiro",
    "signatures.cipeiro_re",
    "signatures.supervisor",
    "signatures.supervisor_re",
    "signatures.witnesses",
}

COMMON = [
    "classification",
    "document.publication_datetime",
    "document.publication_date",
    "victim.name",
    "victim.role",
    "victim.re",
    "victim.unit",
    "victim.absence",
    "victim.contact",
    "victim.witnesses",
    "victim.supervisor",
    "victim.experience",
    "victim.recurrence",
    "incident.datetime",
    "incident.date",
    "incident.location",
    "incident.type",
    "incident.rat_number",
    "incident.injury",
    "incident.status",
    "incident.release",
    "incident.category",
    "incident.narrative",
    "incident.immediate_actions",
    "investigation.team",
    "investigation.start",
    "investigation.end",
    "investigation.ishikawa",
    "investigation.details",
    "investigation.whys",
    "investigation.root_cause",
    "investigation.unsafe_act",
    "investigation.unsafe_condition",
    "investigation.containment_24h",
    "investigation.potential",
    "investigation.summary",
    "actions",
    "signatures.author",
    "signatures.author_re",
    "signatures.doctor",
    "signatures.doctor_re",
    "signatures.cipeiro",
    "signatures.cipeiro_re",
    "signatures.supervisor",
    "signatures.supervisor_re",
    "signatures.witnesses",
    "images.injury",
    "images.dynamics",
    "images.dynamics_kind",
    "communication.severity",
    "communication.injury_caption",
    "communication.video_confirmed",
]

WORKPLACE = [
    "images.details",
    "images.details_kind",
]

TRAJECTORY = [
    "route.origin",
    "route.destination",
    "route.deviation",
    "route.direction",
    "route.transport",
    "route.third_parties",
    "route.police_report",
    "route.clarification",
    "investigation.behavioral_factor",
    "investigation.technical_factor",
    "investigation.climatic_factor",
]


def get_path(data: dict[str, Any], dotted: str) -> Any:
    value: Any = data
    for part in dotted.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip().casefold() in PLACEHOLDERS
    if isinstance(value, (list, dict)):
        return len(value) == 0
    return False


def validate(data: dict[str, Any], require_approvals: bool = True) -> list[str]:
    errors: list[str] = []
    classification = str(data.get("classification", "")).casefold()
    if classification not in {"trabalho", "trajeto"}:
        errors.append("classification deve ser 'trabalho' ou 'trajeto'")
    required = list(COMMON)
    if classification == "trabalho":
        required.extend(WORKPLACE)
    elif classification == "trajeto":
        required.extend(TRAJECTORY)

    ledger = data.get("evidence_ledger", {})
    for path in required:
        value = get_path(data, path)
        record = ledger.get(path) if isinstance(ledger, dict) else None
        if path == "victim.contact" and isinstance(value, str) and value.strip() == "-":
            # '-' é a convenção padrão para ausência de número de contato
            pass
        elif missing(value):
            if (
                path in CONFIRMED_BLANK_ALLOWED
                and isinstance(record, dict)
                and record.get("status") == "confirmed_blank"
                and not missing(record.get("source"))
            ):
                continue
            errors.append(f"campo ausente/não confirmado: {path}")
            continue
        if not isinstance(record, dict):
            errors.append(f"proveniência ausente: {path}")
            continue
        if record.get("status") != "confirmed":
            errors.append(f"proveniência não confirmada: {path}")
        if missing(record.get("source")):
            errors.append(f"fonte ausente na proveniência: {path}")

    ishikawa = get_path(data, "investigation.ishikawa")
    if isinstance(ishikawa, list) and len(ishikawa) != 6:
        errors.append("investigation.ishikawa deve conter exatamente 6 itens")
    whys = get_path(data, "investigation.whys")
    if isinstance(whys, list) and len(whys) != 5:
        errors.append("investigation.whys deve conter exatamente 5 itens")
    root_cause = str(get_path(data, "investigation.root_cause") or "").casefold()
    inconclusive_markers = (
        "inconclus",
        "não determinada",
        "nao determinada",
        "não determinado",
        "nao determinado",
        "a apurar",
        "não foi possível concluir",
        "nao foi possivel concluir",
    )
    if any(marker in root_cause for marker in inconclusive_markers):
        approvals = data.get("approvals", {})
        if approvals.get("root_cause_inconclusive") is not True:
            errors.append(
                "causa raiz inconclusiva sem afirmação expressa do usuário: "
                "approvals.root_cause_inconclusive deve ser true"
            )
    if get_path(data, "images.dynamics_kind") != "generated_reconstruction":
        errors.append(
            "images.dynamics_kind deve ser 'generated_reconstruction'; "
            "não use CFTV no campo de dinâmica"
        )
    if classification == "trabalho" and get_path(data, "images.details_kind") != "generated_detail":
        errors.append(
            "images.details_kind deve ser 'generated_detail' para RAT de acidente do trabalho"
        )
    actions = data.get("actions")
    if isinstance(actions, list):
        if len(actions) != 3:
            errors.append("actions deve conter exatamente 3 ações para o template atual")
        for idx, action in enumerate(actions, start=1):
            for field in ("who", "status", "what", "how", "when"):
                if missing(action.get(field) if isinstance(action, dict) else None):
                    errors.append(f"ação {idx} sem {field}")

    communication = data.get("communication", {})
    if communication.get("video_confirmed") is True:
        for field in ("communication.video_metadata", "communication.video_link"):
            if missing(get_path(data, field)):
                errors.append(f"vídeo confirmado sem campo: {field}")
            elif not isinstance(ledger.get(field), dict) or ledger[field].get("status") != "confirmed":
                errors.append(f"proveniência não confirmada: {field}")

    if require_approvals:
        approvals = data.get("approvals", {})
        for key in ("classification", "technical_analysis", "action_plan"):
            if approvals.get(key) is not True:
                errors.append(f"aprovação obrigatória ausente: approvals.{key}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_json", type=Path)
    parser.add_argument("--draft", action="store_true", help="não exige aprovações, mas ainda exige fatos completos")
    args = parser.parse_args()
    data = json.loads(args.case_json.read_text(encoding="utf-8"))
    errors = validate(data, require_approvals=not args.draft)
    if errors:
        print("BLOQUEADO: o documento não pode ser gerado.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(2)
    print("VALIDADO: fatos, proveniência e aprovações suficientes.")


if __name__ == "__main__":
    main()
