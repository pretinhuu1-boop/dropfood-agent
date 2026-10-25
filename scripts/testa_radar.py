#!/usr/bin/env python3
"""testa_radar.py — benchmark dos candidatos do radar DROPFOOD (passo 2 do
CONTINUAR-AQUI). Roda contra o Ollama local (localhost:11434, API nativa).

Uso:
  python3 testa_radar.py <modelo> <papel>            # geração: prompt de ofício PT-BR
  python3 testa_radar.py <modelo> <papel> --tool     # + teste de tool-call
  python3 testa_radar.py --lista                     # papéis disponíveis

modelo: nome como registrado no Ollama (ex: qwen3.5:4b, smollm3-3b)
papel:  b1..b7 | edge | treinador

Mede: TTFT (primeiro token), tokens/s (eval_count/eval_duration do Ollama),
latência total; valida tool-call (tool_calls correta vs. texto chutado).
Grava/append em marketing/training/radar-modelos/data/testes-<data>.json e
imprime report markdown pronto pra colar na nota do radar.
"""
import argparse, datetime, json, pathlib, sys, time, urllib.request
from typing import Optional

REPO = pathlib.Path(__file__).resolve().parents[2]
OUT_DIR = REPO / "marketing" / "training" / "radar-modelos" / "data"
API = "http://localhost:11434/api/chat"

# --------------------------------------------------------------------------
# Prompts de ofício por bot (derivados de docs/SYSTEM-PROMPTS-BOTS.md §4)
# --------------------------------------------------------------------------
PAPEIS = {
    "b1": {
        "nome": "B1 ESTRATEGISTA",
        "prompt": (
            "Você é o ESTRATEGISTA, o líder do time DROPFOOD Agent — quem dá a "
            "tese e a coerência. Contexto: o dono da loja {{loja.nome}} (modelo "
            "{{loja.modelo}}) está construindo um agente de IA open source (MIT) "
            "para donos de mercado; o time é de 7 bots especializados. "
            "Entregue em PT-BR, direto, sem enchimento: a tese de posicionamento "
            "do DROPFOOD em 1 parágrafo (pra quem é, qual a dor resolvida, por "
            "que agora) + a mensagem-chave de 1 linha."
        ),
    },
    "b2": {
        "nome": "B2 RADAR",
        "prompt": (
            "Você é o RADAR, o pesquisador do time DROPFOOD — fatos com fonte, "
            "nunca chute. Tarefa: liste 3 fatos verificáveis sobre o uso de IA "
            "generativa por pequenos varejistas no Brasil em 2026. Para cada "
            "fato: a afirmação, a fonte (instituição/publicação), e o ano. "
            "Se não tiver certeza da fonte, diga explicitamente que não sabe. "
            "Responda em PT-BR, formato de lista curto."
        ),
    },
    "b3": {
        "nome": "B3 ROTEIRISTA",
        "prompt": (
            "Você é o ROTEIRISTA do time DROPFOOD — transforma a tese em vídeo "
            "de 4-5 min. Tese: 'IA que roda na máquina do próprio dono de "
            "mercado, sem mensalidade, com time de agentes especializados — "
            "open source, MIT.' Entregue o ROTEIRO estruturado: gancho (0-20s), "
            "problema (20-90s), solução (90-210s), prova/demo (210-270s), CTA "
            "(270-300s) — com o timing exato de cada bloco, em PT-BR."
        ),
    },
    "b4": {
        "nome": "B4 DIREÇÃO",
        "prompt": (
            "Você é a DIREÇÃO do time DROPFOOD — quem dá a cara do projeto, "
            "design novo, nada de telas reais. Tema do vídeo: agente de IA para "
            "donos de mercado. Entregue um STORYBOARD de 6 cenas em tabela: "
            "cena | descrição visual (sem texto na tela) | transição | duração. "
            "Estilo: cores quentes de mercado brasileiro, tipografia forte, "
            "motion graphics limpo. Em PT-BR."
        ),
    },
    "b5": {
        "nome": "B5 PRODUTOR",
        "prompt": (
            "Você é o PRODUTOR do time DROPFOOD — monta o MP4 final com os "
            "recursos medidos da máquina (ffmpeg, iMac Apple Silicon). "
            "Entregue o plano de render de um vídeo 1080p30, 60s: cadeia de "
            "comandos ffmpeg (concat de takes, áudio, fade in/out), codecs e "
            "bitrates, e o passo a passo de validação do arquivo final. "
            "Direto, em PT-BR, formato de lista numerada."
        ),
    },
    "b6": {
        "nome": "B6 REVISOR",
        "prompt": (
            "Você é o REVISOR do time DROPFOOD — nada passa sem teu QA. "
            "Texto a auditar: 'Com o DropFood, o dono de mercado economiza até "
            "10 horas por semana e aumenta as vendas em 25% garantido.' "
            "Audite com 3 critérios: (1) números contestáveis, (2) tom "
            "apropriado para material público, (3) clareza. Para cada critério: "
            "veredito (PASSA/FALHA) + correção sugerida. PT-BR, curto."
        ),
    },
    "b7": {
        "nome": "B7 CONTROLE",
        "prompt": (
            "Você é o CONTROLE do time DROPFOOD — mantém o dono e a equipe "
            "alinhados. Entregue a pauta da reunião semanal do time (7 bots + "
            "dono): 5 itens, cada um com dono (B1-B7), objetivo e tempo máx. "
            "Inclua um item de risco/blocker. PT-BR, tabela enxuta."
        ),
    },
    "edge": {
        "nome": "EDGE (loja)",
        "prompt": (
            "Você é o assistente da loja {{loja.nome}}, mercado de bairro. "
            "Cliente mandou: 'oi, cês tão aberto domingo? e quanto "
            "custa a coca 2L?' Responda em PT-BR, tom simpático de bairro, "
            "curto, e informe que hoje (domingo) fechamos 19h."
        ),
    },
    "treinador": {
        "nome": "TREINADOR (teacher/judge)",
        "prompt": (
            "Você é o TREINADOR do time DROPFOOD — teacher/judge do pipeline de "
            "treinamento. Avalie a resposta abaixo de um bot com nota 1-5 e "
            "justificativa em 2 linhas. Resposta do bot: 'O DROPFOOD é um "
            "agente de IA open source para donos de mercado, com 7 bots "
            "especializados rodando localmente.'"
        ),
    },
}

TOOL = {
    "type": "function",
    "function": {
        "name": "buscar_preco",
        "description": "Busca o preço atual de um produto no catálogo da loja.",
        "parameters": {
            "type": "object",
            "properties": {
                "produto": {"type": "string", "description": "Nome do produto, ex: 'coca-cola 2l'"}
            },
            "required": ["produto"],
        },
    },
}

PROMPT_TOOL = (
    "Cliente perguntou o preço da coca-cola 2L na loja {{loja.nome}}. "
    "Use a ferramenta buscar_preco para consultar o catálogo e responda o "
    "preço encontrado. Responda em PT-BR."
)


def chat(modelo: str, messages: list, tools: Optional[list] = None, timeout: int = 300):
    """Uma chamada /api/chat com streaming; devolve métricas + conteúdo."""
    payload = {"model": modelo, "messages": messages, "stream": True}
    if tools:
        payload["tools"] = tools
    req = urllib.request.Request(
        API, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST",
    )
    t0 = time.time()
    ttft = None
    content, tool_calls = [], []
    eval_count = eval_duration = prompt_eval_count = None
    with urllib.request.urlopen(req, timeout=timeout) as r:
        for line in r:
            if not line.strip():
                continue
            chunk = json.loads(line)
            if chunk.get("done"):
                eval_count = chunk.get("eval_count")
                eval_duration = chunk.get("eval_duration")
                prompt_eval_count = chunk.get("prompt_eval_count")
                break
            if ttft is None and chunk.get("message"):
                ttft = time.time() - t0
            msg = chunk.get("message", {})
            if msg.get("content"):
                content.append(msg["content"])
            for tc in msg.get("tool_calls", []) or []:
                tool_calls.append(tc)
    total = time.time() - t0
    tok_s = (eval_count / (eval_duration / 1e9)) if eval_count and eval_duration else None
    return {
        "ttft_s": round(ttft, 3) if ttft else None,
        "total_s": round(total, 3),
        "tokens": eval_count,
        "tok_s": round(tok_s, 1) if tok_s else None,
        "prompt_tokens": prompt_eval_count,
        "content": "".join(content),
        "tool_calls": tool_calls,
    }


def valida_tool(tool_calls):
    """True se veio tool_calls com nome buscar_preco e args JSON válidos."""
    for tc in tool_calls:
        fn = tc.get("function", {})
        if fn.get("name") != "buscar_preco":
            continue
        args = fn.get("arguments") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except (json.JSONDecodeError, TypeError):
                args = {}
        if isinstance(args, dict) and args.get("produto"):
            return True, args
    return False, None


def main():
    ap = argparse.ArgumentParser(description="benchmark de modelo candidato do radar DROPFOOD")
    ap.add_argument("modelo", nargs="?", help="nome do modelo no Ollama local")
    ap.add_argument("papel", nargs="?", choices=PAPEIS, help="papel do bot (b1..b7|edge|treinador)")
    ap.add_argument("--tool", action="store_true", help="roda também o teste de tool-call")
    ap.add_argument("--lista", action="store_true", help="lista os papéis e sai")
    args = ap.parse_args()

    if args.lista or args.modelo is None or args.papel is None:
        print("Papéis disponíveis:")
        for k, v in PAPEIS.items():
            print(f"  {k:9s} {v['nome']}")
        sys.exit(0 if not args.modelo else 1)

    dia = datetime.date.today().isoformat()
    registro = {
        "data": dia, "modelo": args.modelo, "papel": args.papel,
        "geracao": None, "tool": None, "erro": None,
    }
    papel = PAPEIS[args.papel]
    print(f"# Teste radar — {args.modelo} ({papel['nome']}) — {dia}\n")

    # 1) geração: prompt de ofício
    try:
        g = chat(args.modelo, [{"role": "user", "content": papel["prompt"]}])
        registro["geracao"] = {k: g[k] for k in ("ttft_s", "total_s", "tokens", "tok_s", "prompt_tokens")}
        registro["geracao"]["resposta"] = g["content"][:800]
    except Exception as e:
        registro["erro"] = f"geracao: {e}"
        print(f"ERRO geracao: {e}")
        g = None
    if g:
        r = g["content"][:400].replace("\n", " ")
        print(f"generacao: TTFT {g['ttft_s']}s | total {g['total_s']}s | "
              f"{g['tokens']} tok | {g['tok_s']} tok/s")
        print(f"  saida: {r}...\n")

    # 2) tool-call
    if args.tool:
        try:
            t = chat(args.modelo, [{"role": "user", "content": PROMPT_TOOL}], tools=[TOOL])
            ok, arg = valida_tool(t["tool_calls"])
            registro["tool"] = {k: t[k] for k in ("ttft_s", "total_s", "tokens", "tok_s")}
            registro["tool"]["tool_call_valido"] = ok
            registro["tool"]["chamada"] = json.dumps(t["tool_calls"], ensure_ascii=False)[:300] if t["tool_calls"] else None
            registro["tool"]["resposta"] = t["content"][:300]
            print(f"tool-call: TTFT {t['ttft_s']}s | total {t['total_s']}s | "
                  f"{t['tokens']} tok | {t['tok_s']} tok/s | valido: {ok}")
            if t["tool_calls"]:
                print(f"  chamada: {json.dumps(t['tool_calls'], ensure_ascii=False)[:200]}")
            print(f"  resposta: {t['content'][:200]}\n")
        except Exception as e:
            registro["erro"] = f"tool: {e}"
            print(f"ERRO tool: {e}\n")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    arq = OUT_DIR / f"testes-{dia}.json"
    dados = []
    if arq.exists():
        dados = json.loads(arq.read_text(encoding="utf-8"))
    dados.append(registro)
    arq.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"registrado: {arq} ({len(dados)} testes no dia)")


if __name__ == "__main__":
    main()