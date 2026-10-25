# DROPFOOD Agent

O agente de operação para donos de loja no **iFood Mercado** — open source (MIT), em português, roda em cima do [Hermes Agent](https://hermes-agent.nousresearch.com) no seu próprio computador.

## O que ele faz

- **Radar de preços** — acompanha fornecedor vs. concorrência e avisa quando algo sobe, desce, ou some da faixa.
- **Catálogo espelhado** — seu catálogo acompanha o fornecedor; o que faltou no atacado sai do ar na hora (menos cancelamento, nota de loja preservada).
- **Alerta de falta** — falta no fornecedor vira tarefa: repor, substituir ou tirar do ar.
- **Time de bots em PT-BR** — ofícios de estratégia, radar, operação e revisão, cada um com sua função (persona por loja via perfil).
- **Interface em português** — o Hermes desktop inteiro traduzido, com a skin DROPFOOD (neobrutalismo de mercado: café, amarelo de preço bom, verde de entrega).

## Para quem é

- **Modelo loja-reseller**: você abre uma loja no iFood Mercado sem estoque — compra do fornecedor local sob demanda, entrega e recebe o repasse em ~7 dias. O DROPFOOD é o cérebro da operação.
- **Dono de mercado com estoque**: mesma ferramenta, operação clássica.

## Instalação (1 min)

Requisitos: macOS/Linux, [Hermes Agent](https://hermes-agent.nousresearch.com/docs) instalado, [Ollama](https://ollama.com) (opcional — para os bots 100% locais).

```bash
git clone https://github.com/pretinhuu1-boop/dropfood-agent.git
cd dropfood-agent
./install.sh
```

Depois: copie `config.yaml.example` para `~/.hermes/loja/config.yaml` e preencha com os dados da sua loja.

> **Regra de ouro**: o login no portal do iFood é **manual, uma única vez, pelo dono** — o DROPFOOD nunca pede senha. Isso protege sua conta de automação agressiva.

## Arquitetura

Overlay sobre o Hermes core (sem fork):

| Camada | O que é |
|---|---|
| D0 | Hermes core (upstream, atualiza via `hermes update`) |
| D1 | Skin do produto (`skins/dropfood.yaml` — paleta em `design/DESIGN.md`) |
| D2 | Skill `dropfood-ops` + scripts (radar, catálogo, monitor) |
| D3 | Bots (SOULs templates em `bots/templates/` — persona por loja) |
| D4 | UI do produto (Desktop Plugin SDK — panes OPS, ⌘K, dashboard tab) |
| D5 | Distribuição (este repo + install.sh + wizard) |

Detalhes em `docs/ARQUITETURA.md`.

## Repositório sanitizado

Este repositório é **100% sanitizado**: nenhum dado real de loja entra aqui. Dados de operação vivem fora do repo, em `~/.hermes/loja/<id>/`. O CI bloqueia qualquer push/PR que contenha dados sensíveis (grep de padrões + segredos).

## Licença

MIT — veja `LICENSE`. Feito para o dono de mercado brasileiro; use, mude e distribua.