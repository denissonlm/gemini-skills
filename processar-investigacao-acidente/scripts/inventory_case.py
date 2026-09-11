#!/usr/bin/env python3
"""Create a read-only manifest of all files in an accident case folder."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from pathlib import Path


DERIVED_MARKERS = (
    "investigacao_acidente",
    "investigação_acidente",
    "comunicado.html",
    "entendimento do acidente",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case_folder", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.case_folder.resolve()
    if not root.is_dir():
        raise SystemExit(f"Pasta inexistente: {root}")

    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = str(path.relative_to(root))
        lower = relative.casefold()
        rows.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "mime": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "role_hint": (
                    "derived_requires_validation"
                    if any(marker in lower for marker in DERIVED_MARKERS)
                    else "source_candidate"
                ),
            }
        )
    payload = {"case_folder": str(root), "files": rows}
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()

