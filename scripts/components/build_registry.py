#!/usr/bin/env python3
"""Gera components/registry.json (registro shadcn-compatível) a partir dos
arquivos da pasta components/dropfood/. Formato: spec raspada em
/Volumes/Arquivo_iMac/dropfood-pesquisa/componentes/docs_html/shadcn-registry-spec.html
Uso: python3 scripts/components/build_registry.py
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "components" / "dropfood"
OUT = ROOT / "components" / "registry.json"

def item(name: str) -> dict:
    files = []
    for path in sorted(SRC.glob(f"{name}.*")):
        files.append({
            "name": path.stem,
            "type": "registry:file",
            "path": f"components/dropfood/{path.name}",
            "content": path.read_text(encoding="utf-8"),
        })
    return {
        "name": name,
        "type": "registry:ui",
        "registry": files,
    }

if not SRC.is_dir():
    sys.exit(f"ERRO: {SRC} não existe")

registry = {
    "name": "dropfood",
    "type": "registry:style",
    "description": "DROPFOOD — componentes neobrutal sobre tokens do DESIGN-DROPFOOD",
    "dependencies": ["react"],
    "registry": [item(p.stem) for p in sorted(SRC.glob("*.tsx"))],
}

OUT.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
n = sum(len(i["registry"]) for i in registry["registry"])
print(f"registry.json OK: {len(registry['registry'])} componentes, {n} arquivos -> {OUT}")
