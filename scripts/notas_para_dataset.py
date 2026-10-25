#!/usr/bin/env python3
"""notas_para_dataset.py — converte notas de treinamento (marketing/training/)
em dataset JSONL formato chat (system/user/assistant) para finetune SFT.

Uso: python3 notas_para_dataset.py [--out datasets/treino.jsonl]
Idempotente: re-rodar regenera o dataset completo a partir das notas atuais.
Cada nota vira 1 exemplo: system = identidade do bot + REGRA da nota;
user = tarefa (entrada); assistant = resposta esperada (saída).
"""
import re, sys, json, pathlib

REPO = pathlib.Path(__file__).resolve().parents[2]  # raiz do repo
NOTAS = REPO / "marketing" / "training"
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else NOTAS / "datasets" / "treino.jsonl")

def parse_nota(texto: str):
    """Extrai bot, severidade, regra e exemplo de uma nota."""
    m = re.search(r"^#\s*(B\d\w*|T\d\w*)\s+(\d+)\s*[—–-]\s*(.+)$", texto, re.M)
    if not m:
        return None
    bot, numero, titulo = m.group(1), m.group(2), m.group(3).strip()
    sev = re.search(r"^-\s*severidade:\s*(.+)$", texto, re.M)
    regra_m = re.search(r"^##\s*REGRA.*?\n(.*?)(?=\n##\s|\Z)", texto, re.S | re.M)
    regra = re.sub(r"\n+", " ", regra_m.group(1)).strip() if regra_m else ""
    ex_m = re.search(r"^##\s*Exemplo.*?\n(.*?)(?=\n##\s|\Z)", texto, re.S | re.M)
    exemplo = ex_m.group(1) if ex_m else ""
    ent = re.search(r"(?:-\s*)?entrada:?\s*(.+?)(?:\s*[—\-/]\s*sa[ií]da:?\s*|\s*→\s*)", exemplo)
    sai = re.search(r"sa[ií]da:?\s*(.+)$", exemplo, re.M)
    if not ent or not sai:
        return None
    return {
        "bot": bot, "numero": numero, "titulo": titulo,
        "severidade": sev.group(1).strip() if sev else "?",
        "regra": regra,
        "entrada": ent.group(1).strip(),
        "saida": sai.group(1).strip(),
    }

def main():
    linhas = []
    erros = []
    for f in sorted(NOTAS.glob("*.md")):
        if f.name == "README.md":
            continue
        nota = parse_nota(f.read_text(encoding="utf-8"))
        if not nota:
            erros.append(f.name)
            continue
        identidade = {
            "B1": "Você é o ESTRATEGISTA, líder do time do DROPFOOD Agent.",
            "B2": "Você é o RADAR, pesquisador do time do DROPFOOD Agent.",
            "B3": "Você é o ROTEIRISTA do time do DROPFOOD Agent.",
            "B4": "Você é a DIREÇÃO VISUAL do time do DROPFOOD Agent.",
            "B5": "Você é o PRODUTOR/MONTADOR do time do DROPFOOD Agent.",
            "B6": "Você é o REVISOR/QA do time do DROPFOOD Agent.",
            "B7": "Você é o CONTROLE/COMUNICAÇÃO do time do DROPFOOD Agent.",
            "BT": "Você é o TREINADOR, o MLOps do time do DROPFOOD Agent.",
        }.get(nota["bot"], "Você é um bot do time do DROPFOOD Agent.")
        system = f'{identidade}\nREGRA: {nota["regra"]}'
        linhas.append({
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": nota["entrada"]},
                {"role": "assistant", "content": nota["saida"]},
            ],
            "meta": {"bot": nota["bot"], "nota": f"{nota['bot']}-{nota['numero']}",
                     "severidade": nota["severidade"], "titulo": nota["titulo"]},
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as fh:
        for linha in linhas:
            fh.write(json.dumps(linha, ensure_ascii=False) + "\n")
    print(f"OK: {len(linhas)} exemplos -> {OUT}")
    print(f"por bot: { {k: len([l for l in linhas if l['meta']['bot']==k]) for k in sorted(set(l['meta']['bot'] for l in linhas))} }")
    if erros:
        print(f"ERROS (sem exemplo parseável): {erros}")

if __name__ == "__main__":
    main()