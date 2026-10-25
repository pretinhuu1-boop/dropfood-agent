#!/usr/bin/env python3
"""DROPFOOD — espelho.py: espelha o catálogo da loja com o fornecedor.

Mecânica do PRODUTO (MIT): lê o catálogo da instância e a disponibilidade do
fornecedor e produz DECISÕES de sincronização — o que sai do ar (faltou no
atacado), o que volta (reposição chegou) e o que fica. O script NÃO toca o
portal: gera o plano (espelho.json) para o agente aplicar com a sessão do
dono e com aprovação (regra de ouro).

Perfil: fornecedor.nome. Entradas em ~/.hermes/loja/<id>/:
  catalogo.json        itens da loja: [{nome, preco, ativo, ...}]
  fornecedor.json      disponibilidade do fornecedor:
                       [{nome, disponivel: bool|float(estoque), preco?}]
Saída: espelho.json — [{nome, decisao: TIRA_DO_AR|VOLTA_AO_AR|MANTEM, motivo}]

Uso: python3 espelho.py
"""
import json
import os
import sys
import time

try:
    import yaml
except ImportError:
    sys.exit("PyYAML ausente — rode com o python do runtime Hermes (pip install pyyaml)")

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
LOJA_DIR = os.path.join(HERMES_HOME, "loja")


def slug(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())[:24] or "loja"


def load_yaml(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def key(nome):
    return "".join(c for c in (nome or "").lower() if c.isalnum())


def main():
    cfg = load_yaml(os.path.join(LOJA_DIR, "config.yaml"))
    loja = cfg.get("loja", {}) or {}
    dados = os.path.join(LOJA_DIR, slug(loja.get("nome")))

    catalogo = load_json(os.path.join(dados, "catalogo.json"))
    if not catalogo:
        sys.exit(f"catálogo não encontrado em {dados}/catalogo.json")
    forne = load_json(os.path.join(dados, "fornecedor.json"))
    if not forne:
        sys.exit(f"fornecedor.json não encontrado em {dados}/ — roda a coleta "
                 "do fornecedor antes (ou pede no chat: 'roda a coleta')")

    disp = {}
    for f in forne:
        nome = f.get("nome") or ""
        if not nome:
            continue
        est = f.get("disponivel", f.get("estoque", 1))
        if isinstance(est, (int, float)):
            disp[key(nome)] = est > 0
        else:
            disp[key(nome)] = bool(est)

    decisoes = []
    for it in catalogo:
        nome = it.get("nome") or ""
        if not nome:
            continue
        ativo = bool(it.get("ativo", True))
        em = key(nome) in disp and not disp[key(nome)]
        if em and ativo:
            decisoes.append({"nome": nome, "decisao": "TIRA_DO_AR",
                             "motivo": "faltou no fornecedor"})
        elif not em and not ativo:
            decisoes.append({"nome": nome, "decisao": "VOLTA_AO_AR",
                             "motivo": "reposição chegou no fornecedor"})
        elif em and not ativo:
            decisoes.append({"nome": nome, "decisao": "MANTEM",
                             "motivo": "já fora do ar"})
        else:
            decisoes.append({"nome": nome, "decisao": "MANTEM", "motivo": ""})

    espelho = {"gerado_em": time.strftime("%Y-%m-%d %H:%M"),
               "loja": loja.get("nome"), "decisoes": decisoes}
    with open(os.path.join(dados, "espelho.json"), "w", encoding="utf-8") as f:
        json.dump(espelho, f, ensure_ascii=False, indent=1)

    n = {"TIRA_DO_AR": 0, "VOLTA_AO_AR": 0, "MANTEM": 0}
    for d in decisoes:
        n[d["decisao"]] += 1
    print(f"OK -> {dados}/espelho.json | {dict(n)} | "
          "aplicar no portal = pedido explícito do dono (regra de ouro)")


if __name__ == "__main__":
    main()
