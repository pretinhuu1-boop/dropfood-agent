#!/usr/bin/env python3
"""MCP server da biblioteca de componentes DROPFOOD (stdio).

Ferramentas:
- list_components   → catálogo (nomes + arquivos de cada componente)
- get_component     → conteúdo de um componente (instalação/referência)
- search_components → busca no catálogo por nome
- install_component → grava os arquivos de um componente em destino permitido

Padrão: registry.json shadcn-compatível (components/registry.json do produto)
gerado por scripts/components/build_registry.py.

Registro no Hermes (config.yaml → mcp_servers):
  mcp_servers:
    dropfood_components:
      command: "<python do runtime Hermes (mcp SDK 2.x)>"
      args: ["<caminho>/mcp_components.py"]
Requer restart do Hermes após registrar (conexão é criada no startup).
"""
from __future__ import annotations

import asyncio
import json
import pathlib
from typing import Any

from mcp.server.mcpserver import MCPServer

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent  # raiz do repo
REGISTRY = ROOT / "components" / "registry.json"
ALLOWED_OUT = [pathlib.Path.home() / "dev"]  # alvos de install permitidos


def _registry() -> dict[str, Any]:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _list() -> list[dict[str, Any]]:
    return [
        {
            "name": item["name"],
            "type": item["type"],
            "files": [f["path"] for f in item.get("registry", [])],
        }
        for item in _registry().get("registry", [])
    ]


def _get(name: str) -> dict[str, Any]:
    for item in _registry().get("registry", []):
        if item["name"] == name:
            return {"name": name, "registry": item.get("registry", [])}
    return {"error": f"componente '{name}' não encontrado"}


def _install(name: str, out_dir: str) -> dict[str, Any]:
    data = _get(name)
    if "error" in data:
        return data
    dest = pathlib.Path(out_dir).expanduser().resolve()
    if not any(str(dest).startswith(str(p.resolve())) for p in ALLOWED_OUT):
        return {"error": f"destino fora dos permitidos: {ALLOWED_OUT}"}
    dest.mkdir(parents=True, exist_ok=True)
    written = []
    for f in data["registry"]:
        target = dest / pathlib.Path(f["path"]).name
        target.write_text(f["content"], encoding="utf-8")
        written.append(str(target))
    return {"ok": True, "component": name, "written": written}


def list_components() -> dict[str, Any]:
    """Lista os componentes da biblioteca DROPFOOD (nome + arquivos)."""
    return {"count": len(_list()), "components": _list()}


def get_component(name: str) -> dict[str, Any]:
    """Retorna o componente informado com o conteúdo de todos os arquivos."""
    return _get(name)


def search_components(query: str) -> list[dict[str, Any]]:
    """Busca componentes por nome (ex.: button, chip, input, alert, badge)."""
    q = query.lower()
    return [
        {"name": i["name"], "files": i["files"]} for i in _list() if q in i["name"].lower()
    ]


def install_component(name: str, out_dir: str) -> dict[str, Any]:
    """Instala o componente informado gravando os arquivos em out_dir (somente sob ~/dev)."""
    return _install(name, out_dir)


def main() -> None:
    server = MCPServer(
        name="dropfood-components",
        title="DROPFOOD Components",
        description="Biblioteca de componentes neobrutal do DROPFOOD (registry shadcn-compatível).",
        version="0.1.0",
    )
    server.add_tool(list_components)
    server.add_tool(get_component)
    server.add_tool(search_components)
    server.add_tool(install_component)
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
