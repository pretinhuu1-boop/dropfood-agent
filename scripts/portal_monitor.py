#!/usr/bin/env python3
"""DROPFOOD — portal_monitor.py: health check da sessão do portal iFood.

Checa o daemon do Camoufox e, se o portal estiver na aba, grava se está
logado. Grava portal_status.json na pasta da instância (o painel/agente só
lê — nunca bate no portal). Conta transições deslogado->logado do dia.

Regra de ouro: login é SEMPRE manual do dono (1x). Este script apenas
OBSERVA a sessão — nunca loga, nunca digita senha.

Uso: python3 portal_monitor.py   (cron 30min)
"""
import json
import os
import subprocess
import sys
import time

try:
    import yaml
except ImportError:
    sys.exit("PyYAML ausente — rode com o python do runtime Hermes (pip install pyyaml)")

HERMES_HOME = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
LOJA_DIR = os.path.join(HERMES_HOME, "loja")
CB = os.path.expanduser("~/.local/bin/camoufox-browser")


def slug(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())[:24] or "loja"


def ident_loja():
    cfg = os.path.join(LOJA_DIR, "config.yaml")
    if os.path.exists(cfg):
        with open(cfg, encoding="utf-8") as f:
            return slug(yaml.safe_load(f).get("loja", {}).get("nome"))
    return "loja"


def load(dados, p, default):
    try:
        with open(os.path.join(dados, p), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save(dados, p, obj):
    os.makedirs(dados, exist_ok=True)
    with open(os.path.join(dados, p), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def main():
    dados = os.path.join(LOJA_DIR, ident_loja())
    hoje = time.strftime("%Y-%m-%d")
    prev = load(dados, "portal_state.json", {"logado_prev": None, "logins_hoje": 0, "dia": hoje})
    if prev.get("dia") != hoje:
        prev = {"logado_prev": None, "logins_hoje": 0, "dia": hoje}

    if not os.path.exists(CB):
        save(dados, "portal_status.json", {"ok": False, "daemon": False,
             "portal_na_aba": False, "logado": None, "url": None, "ts": time.time(),
             "logins_hoje": prev["logins_hoje"], "dia": hoje,
             "msg": "camoufox-browser não encontrado"})
        return

    status = subprocess.run([CB, "status"], capture_output=True, text=True, timeout=20)
    if "Daemon is running" not in status.stdout:
        save(dados, "portal_status.json", {"ok": False, "daemon": False,
             "portal_na_aba": False, "logado": None, "url": None, "ts": time.time(),
             "logins_hoje": prev["logins_hoje"], "dia": hoje,
             "msg": "daemon do browser fora"})
        return

    try:
        ev = subprocess.run([CB, "eval",
                             "JSON.stringify({u:location.href,l:!location.href.includes('/login')})"],
                            capture_output=True, text=True, timeout=30)
        payload = (ev.stdout or "").strip()
        if not payload or "Error" in (ev.stderr or ""):
            raise RuntimeError(f"eval vazio ({ev.stderr or ''})".strip()[:120])
        while payload and not payload.startswith("{"):
            payload = payload.split("\n", 1)[-1].strip()
        info = json.loads(payload) if payload.startswith("{") else {}
    except Exception as e:
        save(dados, "portal_status.json", {"ok": False, "daemon": True,
             "portal_na_aba": False, "logado": None, "url": None, "ts": time.time(),
             "logins_hoje": prev["logins_hoje"], "dia": hoje, "msg": f"eval falhou: {e}"})
        return

    url = info.get("u") or ""
    portal_na_aba = "portal.ifood.com.br" in url
    logado = portal_na_aba and bool(info.get("l"))

    logins = prev["logins_hoje"]
    if portal_na_aba and prev.get("logado_prev") is False and logado:
        logins += 1
    prev["logado_prev"] = logado if portal_na_aba else prev.get("logado_prev")
    prev["logins_hoje"] = logins
    prev["dia"] = hoje

    estado = {
        "ok": (not portal_na_aba) or bool(logado),
        "daemon": True,
        "portal_na_aba": portal_na_aba,
        "logado": logado,
        "url": url[:80],
        "ts": time.time(),
        "logins_hoje": logins,
        "dia": hoje,
        "msg": ("sessao ok" if logado else
                "portal deslogado (login so manual)" if portal_na_aba else
                "portal nao esta na aba do daemon"),
    }
    save(dados, "portal_status.json", estado)
    save(dados, "portal_state.json", prev)
    print(estado["msg"])


if __name__ == "__main__":
    main()
