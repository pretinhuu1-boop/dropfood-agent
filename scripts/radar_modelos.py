#!/usr/bin/env python3
"""radar_modelos.py — varre o HuggingFace (trending text-generation) e
filtra candidatos p/ o time DROPFOOD (pequenos, permissivos, úteis p/ bot).

Uso: python3 radar_modelos.py [--limit 40]
Saída: top candidatos no stdout + data/radar-modelos-<data>.json (bruto).
Sem chave: usa a API pública (rate-limite). Reproduzível e idempotente.
"""
import json, sys, datetime, pathlib, urllib.request

REPO = pathlib.Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "marketing" / "training" / "radar-modelos" / "data"
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 40

# licenças que NÃO contaminam o pacote open source do DROPFOOD (MIT)
LICENCAS_BLOQUEADAS = ("llama3.1", "llama3.2", "llama3.3", "llama4", "gemma",
                       "llama", "proprietary", "bigscience-openrail-m", "cc-by-nc")

def hf(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "dropfood-radar/0.1"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def main():
    url = (f"https://huggingface.co/api/models?sort=trendingScore&direction=-1"
           f"&limit={LIMIT}&pipeline_tag=text-generation")
    modelos = hf(url)
    candidatos = []
    for m in modelos:
        lic = (m.get("library_name") or "",)
        lic_cards = {f.get("rfilename", "") for f in m.get("siblings", [])}
        tags = set(m.get("tags", []))
        lic_link = next((f.get("rfilename") for f in m.get("siblings", []) if "license" in f.get("rfilename", "").lower()), "")
        novo = {
            "id": m.get("id"), "likes": m.get("likes", 0),
            "downloads": m.get("downloads", 0), "tags_lic": [t for t in tags if "license" in t.lower()],
            "tags": sorted(t for t in tags if t.startswith(("tiny", "1b", "2b", "3b", "4b", "7b", "8b", "9b"))),
            "modified": m.get("lastModified", "")[:10],
        }
        candidatos.append(novo)
    # filtro por licença (heurística: tags/nome)
    ok = []
    for c in candidatos:
        nome = (c["id"] or "").lower()
        if any(b in nome for b in ("-nc-", "non-commercial")):
            continue
        if any(b in " ".join(c["tags_lic"]).lower() for b in ("cc-by-nc", "noncommercial")):
            continue
        ok.append(c)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dia = datetime.date.today().isoformat()
    bruto = {"data": dia, "fonte": url, "modelos": candidatos}
    with (OUT_DIR / f"radar-modelos-{dia}.json").open("w", encoding="utf-8") as fh:
        json.dump(bruto, fh, ensure_ascii=False, indent=1)
    print(f"RADAR {dia} — {len(candidatos)} trending text-generation; {len(ok)} sem restricao comercial óbvia")
    for c in ok[:12]:
        print(f"  {c['likes']:>5} ♥ {c['id']}  lic={c['tags_lic'] or '?'}  tam_tags={c['tags']}  mod={c['modified']}")
    print(f"bruto: {OUT_DIR / ('radar-modelos-' + dia + '.json')}")

if __name__ == "__main__":
    main()