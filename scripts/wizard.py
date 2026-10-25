#!/usr/bin/env python3
"""DROPFOOD — wizard.py: cria ~/.hermes/loja/config.yaml guiado (F2).

Mecânica do PRODUTO (MIT): só pergunta e grava — não conhece loja nenhuma.
Não sobrescreve config existente (avisa onde editar). Nada de dado real de
loja aqui.

Uso: python3 wizard.py [--force]
"""
import os
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML ausente — rode ./install.sh --com-sdk (venv do produto)")

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
DEST = os.path.join(HERMES_HOME, "loja", "config.yaml")
EXAMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.yaml.example")


def ask(rotulo, default=""):
    try:
        v = input(f"{rotulo} [{default}]: ").strip() or default
    except EOFError:
        v = default
    return v


def main():
    if os.path.exists(DEST) and "--force" not in sys.argv:
        sys.exit(f"já existe {DEST} — edite direto (ou passe --force)")

    nome = ask("Nome da loja", "Minha Loja")
    cidade = ask("Cidade", "")
    regiao = ask("Bairro/zona", "")
    modelo = ask("Modelo (reseller|dono)", "reseller")
    fornecedor = ask("Fornecedor (atacadista)", "")
    markup = ask("Markup (0.49 = 49%)", "0.49")
    lat = ask("Latitude (radar de vitrine)", "0.0")
    lng = ask("Longitude (radar de vitrine)", "0.0")

    cfg = {
        "loja": {"nome": nome, "cidade": cidade, "regiao": regiao, "modelo": modelo},
        "localizacao": {"lat": float(lat), "lng": float(lng)},
        "fornecedor": {"nome": fornecedor, "markup": float(markup),
                       "pedido_minimo": 0, "prazo_entrega_h": 6},
        "radar": {"frequencia_horas": 7, "concorrentes": [], "faixas": [],
                  "vitrine": {"sdk": False, "concorrentes": []}},
        "portal": {"login": "manual", "email": ""},
        "runtime": {"ollama_url": "http://localhost:11434/v1",
                    "motor": "lfm2.5:8b", "leve": "qwen3.5:2b", "qualidade": "qwen3.5:4b"},
        "alertas": {"canal": "terminal", "horario": "08:00"},
        "backup": {"github": False, "repo": "", "frequencia": "diario"},
        "display": {"skin": "skins/dropfood.yaml", "interface": "auto"},
    }
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    with open(DEST, "w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, allow_unicode=True, sort_keys=False)

    print(f"\nOK -> {DEST}")
    print("Próximos passos:")
    print("  1. login manual no portal iFood (regra de ouro, 1x)")
    print("  2. gere o catálogo e rode: radar_precos.py")
    print("  3. radar de vitrine (opcional): ./install.sh --com-sdk e f0_paridade.py")


if __name__ == "__main__":
    main()
