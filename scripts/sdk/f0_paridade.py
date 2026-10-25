#!/usr/bin/env python3
"""DROPFOOD — F0: validação do ifood-sdk (paridade de preço de vitrine).

Mecânica do PRODUTO (MIT): qualquer dono roda com a conta dele. Dados e
config da loja ficam no perfil privado (~/.hermes/loja/), nunca aqui.

Fluxo (dono no meio — OTP é manual, regra de ouro: nunca senha):
  1. f0_paridade.py --set-phone            # 1x: salva no config do perfil da loja
  2. f0_paridade.py --login                # dispara o código (WhatsApp do dono)
  3. f0_paridade.py --coletar < out.txt    # verify + pedidos recentes (acham os
                                           # merchant_ids sem buscar — busca é
                                           # PerimeterX) + items com preço de
                                           # vitrine de N concorrentes → JSON

Opções: --lat/--lng (padrão: config da loja), --n (concorrentes, padrão 3),
--out (destino do JSON, padrão ./data/sdk/f0_paridade.json). Só leituras.
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SDK = os.path.expanduser("~/dev/tools/ifood-sdk")
if SDK not in sys.path:
    sys.path.insert(0, SDK)

LOJA_CFG = Path(os.path.expanduser("~/.hermes/loja/ifood_sdk_cfg.json"))


def load_cfg():
    if not LOJA_CFG.exists():
        return {}
    return json.loads(LOJA_CFG.read_text())


def save_cfg(cfg: dict) -> None:
    LOJA_CFG.parent.mkdir(parents=True, exist_ok=True)
    LOJA_CFG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))


def set_phone(args) -> None:
    cfg = load_cfg()
    cfg["phone"] = args.phone
    save_cfg(cfg)
    print(f"Telefone salvo em {LOJA_CFG} (perfil privado da loja).")


def login(args) -> None:
    import ifood
    cfg = load_cfg()
    if not cfg.get("phone"):
        sys.exit("Sem telefone. Rode: f0_paridade.py --set-phone --phone '+55...'")
    ifood.Client(phone=cfg["phone"]).login()
    print("OTP ENVIADO ao WhatsApp do dono. Próximo: --coletar (código via stdin)")


def coletar(args) -> None:
    import ifood
    cfg = load_cfg()
    code = sys.stdin.readline().strip()
    if not code:
        sys.exit("Código OTP ausente no stdin")
    lat = args.lat or cfg.get("lat")
    lng = args.lng or cfg.get("lng")
    if lat is None or lng is None:
        sys.exit("Sem localização. Passe --lat/--lng ou salve no config da loja.")

    client = ifood.Client(phone=cfg["phone"])
    client.verify(code)
    print("Sessão OK.")

    pedidos = client.orders.recent(10)
    lojas: list[tuple[str, str]] = []
    for p in pedidos:
        m = getattr(p, "merchant", None)
        if m and getattr(m, "id", None) and (m.id, getattr(m, "name", "") or "") not in lojas:
            lojas.append((m.id, getattr(m, "name", "") or ""))
    lojas = lojas[: args.n]
    if not lojas:
        sys.exit("Nenhum pedido/loja encontrado — use --ids para passar merchant ids.")

    resultado = {"lojas": [], "gerado_em": datetime.now().isoformat(), "fonte": "ifood-sdk F0"}
    for mid, nome in lojas:
        try:
            itens = client.merchants.items(mid, latitude=lat, longitude=lng)
            resultado["lojas"].append({
                "merchant_id": mid,
                "nome": nome,
                "total_itens": len(itens),
                "amostras": [
                    {"nome": i.get("name"), "preco": i.get("price"), "unidade": i.get("unit")}
                    for i in itens[: args.amostras]
                ],
            })
            print(f"OK {nome}: {len(itens)} itens")
        except Exception as e:  # noqa: BLE001
            print(f"FALHA {nome}: {e}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(resultado, ensure_ascii=False, indent=2))
    print(f"Salvo: {out}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("--set-phone", add_help=False)
    s1.add_argument("--phone", required=True)
    s1.set_defaults(fn=set_phone)
    s2 = sub.add_parser("--login", add_help=False)
    s2.set_defaults(fn=login)
    s3 = sub.add_parser("--coletar", add_help=False)
    s3.add_argument("--lat", type=float, default=None)
    s3.add_argument("--lng", type=float, default=None)
    s3.add_argument("--n", type=int, default=3)
    s3.add_argument("--amostras", type=int, default=5)
    s3.add_argument("--out", default="./data/sdk/f0_paridade.json")
    s3.set_defaults(fn=coletar)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()