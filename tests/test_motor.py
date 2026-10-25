"""DROPFOOD — testes do motor com loja demo (100% fictícia).

Valida radar_precos.py + espelho.py + wizard.py com dados falsos em
HERMES_HOME isolado (Adega do Seu João). Sem rede, sem portal.

Uso: tests/test_motor.py   (Python 3.10+; yaml no ambiente)
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPTS = RAIZ / "scripts"
PY = sys.executable


def roda(home, *args, stdin=None):
    env = dict(os.environ, HERMES_HOME=str(home))
    return subprocess.run([PY, *map(str, args)], capture_output=True, text=True,
                          env=env, input=stdin)


def cria_loja_demo(home: Path):
    loja = home / "loja"
    loja.mkdir(parents=True, exist_ok=True)
    dados = loja / "adegadoseujoao"
    dados.mkdir(parents=True, exist_ok=True)
    (loja / "config.yaml").write_text(
        "loja:\n  nome: \"Adega do Seu Joao\"\n  modelo: reseller\n"
        "localizacao: {lat: -23.5505, lng: -46.6333}\n"
        "fornecedor: {nome: \"Atacadão X\", markup: 0.49}\n"
        "radar:\n  frequencia_horas: 7\n"
        "  faixas:\n    bebidas: {bom: 0.40, ok: 0.25}\n"
        "  vitrine: {sdk: true}\n", encoding="utf-8")
    (dados / "catalogo.json").write_text(json.dumps([
        {"nome": "Cerveja Lata 350ml", "secao": "bebidas", "compra": 2.10, "venda_atual": 3.99},
        {"nome": "Refrigerante 2L", "secao": "bebidas", "compra": 4.50, "venda_atual": 6.99},
        {"nome": "Salgadinho 100g", "secao": "snacks", "compra": 3.20, "venda_atual": 3.50},
    ], ensure_ascii=False), encoding="utf-8")
    (dados / "fornecedor.json").write_text(json.dumps([
        {"nome": "Cerveja Lata 350ml", "disponivel": True},
        {"nome": "Refrigerante 2L", "disponivel": 0},
        {"nome": "Salgadinho 100g", "disponivel": True},
    ], ensure_ascii=False), encoding="utf-8")
    (dados / "vitrine.json").write_text(json.dumps({
        "gerado_em": "2026-10-25T10:00:00", "fonte": "ifood-sdk F0 (teste)",
        "lojas": [], "vitrine": [{"nome": "Cerveja Lata 350ml", "preco": 3.49,
                                  "loja": "Concorrente X"}]},
        ensure_ascii=False), encoding="utf-8")
    return dados


def main():
    with tempfile.TemporaryDirectory(prefix="dropfood-test-") as tmp:
        home = Path(tmp)
        dados = cria_loja_demo(home)

        r = roda(home, SCRIPTS / "radar_precos.py")
        assert r.returncode == 0, f"radar falhou: {r.stderr}"
        radar = json.loads((dados / "radar.json").read_text())
        v = {i["nome"]: i["veredito"] for i in radar["itens"]}
        assert v["Cerveja Lata 350ml"] == "DESCE", f"cerveja com vitrine menor devia DESCE: {v}"
        assert v["Refrigerante 2L"] == "MANTEM", f"refri: {v}"
        print("✓ radar_precos (vereditos + vitrine)")

        r = roda(home, SCRIPTS / "espelho.py")
        assert r.returncode == 0, f"espelho falhou: {r.stderr}"
        esp = json.loads((dados / "espelho.json").read_text())
        dec = {d["nome"]: d["decisao"] for d in esp["decisoes"]}
        assert dec["Refrigerante 2L"] == "TIRA_DO_AR", f"refri zerado devia sair do ar: {dec}"
        print("✓ espelho (catálogo vs fornecedor)")

        r = roda(home, SCRIPTS / "wizard.py")
        assert r.returncode != 0  # config existe → recusa
        r = roda(home, SCRIPTS / "wizard.py", "--force", stdin="Adega do Seu Joao\nCuiaba\nCentro\nreseller\nAtacadao X\n0.49\n-15.6\n-56.1\n")
        assert r.returncode == 0, f"wizard falhou: {r.stderr}"
        cfg_atual = (home / "loja" / "config.yaml").read_text(encoding="utf-8")
        assert "Cuiaba" in cfg_atual and "-15.6" in cfg_atual
        print("✓ wizard (recusa + --force com entrada)")

        r = roda(home, SCRIPTS / "portal_monitor.py")
        assert r.returncode == 0, f"portal_monitor falhou: {r.stderr}"
        print("✓ portal_monitor (sem browser → estado gracefu)l")

    print("\nTODOS OS TESTES PASSARAM")


if __name__ == "__main__":
    main()
