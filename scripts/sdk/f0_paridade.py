#!/usr/bin/env python3
"""DROPFOOD — f0_paridade.py: radar de vitrine via ifood-sdk (validação F0).

Mecânica do PRODUTO (MIT): qualquer dono roda com a conta DELE. Dados e
config da loja ficam no perfil privado (~/.hermes/loja/), nunca aqui.

Dependência: pacote `ifood-sdk` (MIT, felipeadeildo/ifood-sdk) instalado no
venv do produto — rode `./install.sh --com-sdk` (cria ~/.hermes/dropfood/venv
e instala pyyaml + ifood-sdk). Login é OTP no WhatsApp do dono (regra de
ouro: nunca senha, OTP manual).

Fluxo (dono no meio — OTP é manual):
  1. f0_paridade.py --set-phone '+5511...'              # 1x: salva no perfil da loja
  2. f0_paridade.py --login                             # dispara o código no WhatsApp
  3. f0_paridade.py --coletar < out.txt                 # verify + pedidos recentes
                                                        # (descobre merchant_ids sem
                                                        #  buscar — busca é PerimeterX)
                                                        # + itens de vitrine → vitrine.json

Opções do --coletar: --lat/--lng (padrão: localizacao do config da loja),
--n (concorrentes, padrão 3), --ids (merchant_ids explícitos, substitui a
descoberta por pedidos), --amostras (itens por loja, padrão 5).

Saída: ~/.hermes/loja/<id>/vitrine.json — consumido pelo radar_precos.py
(campo "vitrine" = lista {nome, preco} + detalhe por loja em "lojas").
Só leituras.
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML ausente — rode ./install.sh --com-sdk (venv do produto)")

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
LOJA_DIR = Path(HERMES_HOME) / "loja"
CFG_PATH = LOJA_DIR / "config.yaml"


def slug(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())[:24] or "loja"


def ident_loja():
    if CFG_PATH.exists():
        with open(CFG_PATH, encoding="utf-8") as f:
            return slug(yaml.safe_load(f).get("loja", {}).get("nome"))
    return "loja"


def sdk_cfg_path():
    return LOJA_DIR / ident_loja() / "ifood_sdk_cfg.json"


def load_cfg():
    p = sdk_cfg_path()
    if not p.exists():
        return {}
    return json.loads(p.read_text())


def save_cfg(cfg):
    p = sdk_cfg_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))


def config_loja():
    if not CFG_PATH.exists():
        return {}
    with open(CFG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def set_phone(args):
    cfg = load_cfg()
    cfg["phone"] = args.set_phone
    save_cfg(cfg)
    print(f"Telefone salvo em {sdk_cfg_path()} (perfil privado da loja).")


def login(args):
    try:
        import ifood
    except ImportError as e:
        sys.exit(f"ifood-sdk não instalado ({e}) — rode ./install.sh --com-sdk")
    cfg = load_cfg()
    if not cfg.get("phone"):
        sys.exit("Sem telefone. Rode: f0_paridade.py --set-phone --phone '+55...'")
    ifood.Client(phone=cfg["phone"]).login()
    print("OTP ENVIADO ao WhatsApp do dono. Próximo: --coletar (código via stdin)")


def coletar(args):
    try:
        import ifood
    except ImportError as e:
        sys.exit(f"ifood-sdk não instalado ({e}) — rode ./install.sh --com-sdk")
    cfg = load_cfg()
    code = sys.stdin.readline().strip()
    if not code:
        sys.exit("Código OTP ausente no stdin")

    loja = config_loja()
    loc = (loja.get("localizacao") or {}) if loja else {}
    lat = args.lat if args.lat is not None else cfg.get("lat", loc.get("lat"))
    lng = args.lng if args.lng is not None else cfg.get("lng", loc.get("lng"))
    if lat is None or lng is None:
        sys.exit("Sem localização — passe --lat/--lng ou adicione "
                 "`localizacao: {lat, lng}` no config.yaml da loja.")

    client = ifood.Client(phone=cfg["phone"])
    client.verify(code)
    print("Sessão OK.")

    if args.ids:
        lojas = [(mid.strip(), "") for mid in args.ids.split(",") if mid.strip()]
    else:
        pedidos = client.orders.recent(10)
        lojas = []
        for p in pedidos:
            m = getattr(p, "merchant", None)
            if m and getattr(m, "id", None) and (m.id, getattr(m, "name", "") or "") not in lojas:
                lojas.append((m.id, getattr(m, "name", "") or ""))
        lojas = lojas[: args.n]
        if not lojas:
            sys.exit("Nenhum pedido/loja encontrado — use --ids para passar merchant ids.")

    resultado = {"gerado_em": datetime.now().isoformat(), "fonte": "ifood-sdk F0",
                 "lojas": [], "vitrine": []}
    for mid, nome in lojas:
        try:
            itens = client.merchants.items(mid, latitude=lat, longitude=lng)
            amostras = []
            for i in itens[: args.amostras]:
                preco = i.get("price")
                if preco is None:
                    continue
                amostras.append({"nome": i.get("name"), "preco": preco,
                                 "unidade": i.get("unit")})
                resultado["vitrine"].append({"nome": i.get("name"), "preco": preco,
                                             "loja": nome or mid})
            resultado["lojas"].append({
                "merchant_id": mid, "nome": nome or mid,
                "total_itens": len(itens), "amostras": amostras,
            })
            print(f"OK {nome or mid}: {len(itens)} itens")
        except Exception as e:  # noqa: BLE001
            print(f"FALHA {nome or mid}: {e}")

    dados = LOJA_DIR / ident_loja()
    dados.mkdir(parents=True, exist_ok=True)
    out = dados / "vitrine.json"
    out.write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    print(f"Salvo: {out} ({len(resultado['vitrine'])} itens de vitrine)")


def main():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exemplos:\n"
               "  f0_paridade.py --set-phone '+5511...'   # 1x\n"
               "  f0_paridade.py --login                   # dispara o OTP\n"
               "  f0_paridade.py --coletar < out.txt       # verifica e coleta",
    )
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--set-phone", metavar="PHONE",
                   help="salva o telefone da conta no perfil privado da loja (1x)")
    g.add_argument("--login", action="store_true",
                   help="dispara o código OTP no WhatsApp do dono")
    g.add_argument("--coletar", action="store_true",
                   help="verifica o OTP (stdin) e coleta a vitrine → vitrine.json")
    p.add_argument("--lat", type=float, default=None)
    p.add_argument("--lng", type=float, default=None)
    p.add_argument("--n", type=int, default=3,
                   help="concorrentes (descoberta por pedidos; padrão 3)")
    p.add_argument("--ids", default=None,
                   help="merchant_ids explícitos separados por vírgula "
                        "(substitui a descoberta por pedidos recentes)")
    p.add_argument("--amostras", type=int, default=5,
                   help="itens de vitrine por loja (padrão 5)")
    args = p.parse_args()
    if args.set_phone:
        set_phone(args)
    elif args.login:
        login(args)
    else:
        coletar(args)


if __name__ == "__main__":
    main()
