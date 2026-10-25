#!/usr/bin/env python3
"""DROPFOOD — radar_precos.py: ciclo de comparação e classificação de preços.

Mecânica do PRODUTO (MIT): lê o perfil da loja (config.yaml) e o catálogo da
instância (~/.hermes/loja/<id>/catalogo.json) — NUNCA dados hard-coded.
Vereditos MANTEM/SOBE/DESCE/ALERTA por faixa de margem e categoria.

Perfil lido:
  fornecedor.markup           margem sobre o custo de compra (0.49 = 49%)
  radar.faixas                bom/ok/caro por categoria (opcional)
  radar.vitrine.sdk           se true, compara com vitrine.json quando existe
                              (alimentado pelo ifood-sdk — OTP manual do dono)

Saída: ~/.hermes/loja/<id>/radar.json

Uso: python3 radar_precos.py [--dry-run]
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


def veredito(margem, faixas, categoria):
    """MANTEM se dentro da faixa; SOBE se margem folgada; DESCE se apertada;
    ALERTA se margem negativa (venda abaixo do custo)."""
    if margem < 0:
        return "ALERTA"
    f = (faixas or {}).get(categoria) if faixas else None
    if f:
        ok = float(f.get("ok", 0) or 0)
        bom = float(f.get("bom", 0) or 0)
        if margem >= bom:
            return "SOBE"
        if margem < ok:
            return "DESCE"
        return "MANTEM"
    if margem >= 0.40:
        return "SOBE"
    if margem < 0.20:
        return "DESCE"
    return "MANTEM"


def main():
    cfg = load_yaml(os.path.join(LOJA_DIR, "config.yaml"))
    loja = cfg.get("loja", {}) or {}
    forne = cfg.get("fornecedor", {}) or {}
    radar_cfg = cfg.get("radar", {}) or {}
    markup = float(forne.get("markup", 0.49) or 0.49)
    faixas = radar_cfg.get("faixas") or {}
    vitrine_on = bool((radar_cfg.get("vitrine") or {}).get("sdk"))

    ident = slug(loja.get("nome"))
    dados = os.path.join(LOJA_DIR, ident)
    catalogo = load_json(os.path.join(dados, "catalogo.json")) or \
        load_json(os.path.join(LOJA_DIR, "catalogo.json"))
    if not catalogo:
        sys.exit(f"catálogo não encontrado em {dados}/catalogo.json — "
                 "gere o catálogo antes (export do portal ou planilha)")

    vitrine = load_json(os.path.join(dados, "vitrine.json")) if vitrine_on else None
    vmap = {(v.get("nome") or "").lower(): v.get("preco") for v in (vitrine or [])} if vitrine else {}

    itens, alertas = [], []
    for it in catalogo:
        nome = it.get("nome") or ""
        custo = float(it.get("compra") or it.get("custo") or 0)
        if custo <= 0:
            continue
        venda = float(it.get("venda_atual") or it.get("venda") or 0)
        if venda <= 0:
            venda = custo * (1 + markup)
        margem = (venda - custo) / venda if venda else 0
        cat = (it.get("secao") or it.get("categoria") or "").strip()
        vq = vmap.get(nome.lower())
        vrd = veredito(margem, faixas, cat)
        if vq and vq > 0 and venda > vq * 1.05:
            vrd = "DESCE"
        if margem < 0:
            alertas.append(f"{nome}: venda R${venda:.2f} abaixo do custo R${custo:.2f}")
        itens.append({"nome": nome, "categoria": cat, "custo": round(custo, 2),
                      "venda": round(venda, 2), "margem_pct": round(margem * 100, 1),
                      "vitrine": vq, "veredito": vrd})

    radar = {"gerado_em": time.strftime("%Y-%m-%d %H:%M"), "loja": loja.get("nome"),
             "markup": markup, "itens": itens, "alertas": alertas}
    os.makedirs(dados, exist_ok=True)
    path = os.path.join(dados, "radar.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(radar, f, ensure_ascii=False, indent=1)
    n = {"ALERTA": 0, "DESCE": 0, "MANTEM": 0, "SOBE": 0}
    for i in itens:
        n[i["veredito"]] += 1
    print(f"OK -> {path} | {len(itens)} itens | {dict(n)} | {len(alertas)} alertas")


if __name__ == "__main__":
    main()
