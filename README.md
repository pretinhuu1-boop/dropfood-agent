# DROPFOOD Agent

O agente de operação para donos de loja no **iFood Mercado** — open source (MIT), em português. O DROPFOOD é um **fork do [Hermes Agent](https://hermes-agent.nousresearch.com)** (NousResearch, MIT) modificado o mínimo possível para a operação do iFood: identidade própria (ícone, login = a sua loja, skin) + camada de operação, sobre o núcleo upstream intacto.

## O que ele faz

- **Radar de preços** — acompanha fornecedor vs. concorrência e avisa quando algo sobe, desce, ou some da faixa.
- **Catálogo espelhado** — seu catálogo acompanha o fornecedor; o que faltou no atacado sai do ar na hora (menos cancelamento, nota de loja preservada).
- **Alerta de falta** — falta no fornecedor vira tarefa: repor, substituir ou tirar do ar.
- **Time de bots em PT-BR** — ofícios de estratégia, radar, operação e revisão, cada um com sua função (persona por loja via perfil).
- **Interface em português** — o desktop inteiro do fork traduzido (PT-BR de fábrica), com a skin DROPFOOD (neobrutalismo de mercado: cream, pink de ação, mint de sucesso, amarelo de preço bom).
- **Navegador central operado pelo agente** — o portal iFood no centro da janela, o operador na lateral dirigindo via computer-use nativo (preview-act/drive), com chip de sessão (login manual do dono — regra de ouro).
- **Atividade visível dos bots** — faixas e cards por bot enquanto trabalham (activity-strip, working-card, step-progress, bot-avatar) e modal de conversa entre bots (bot-chat-modal, handoff-timeline) — biblioteca de componentes em `components/`.

## Para quem é

- **Modelo loja-reseller**: você abre uma loja no iFood Mercado sem estoque — compra do fornecedor local sob demanda, entrega e recebe o repasse em ~7 dias. O DROPFOOD é o cérebro da operação.
- **Dono de mercado com estoque**: mesma ferramenta, operação clássica.

## Instalação

O DROPFOOD **é** o Hermes (fork) — não se instala "em cima" de outro. O repo traz o núcleo pinado em `core/` (commit em `core/UPSTREAM.txt`) + a camada do produto.

- **Hoje (desenvolvimento, até a F4)**: o `install.sh` aplica a camada do produto (skin, skill, perfil) sobre uma instalação local do Hermes.
- **Distribuição final (F4)**: instalador standalone com wizard — o dono de loja **não** instala o Hermes separado nunca.

```bash
git clone https://github.com/pretinhuu1-boop/dropfood-agent.git
cd dropfood-agent
./install.sh
```

Depois: copie `config.yaml.example` para `~/.hermes/loja/config.yaml` e preencha com os dados da sua loja.

> **Regra de ouro**: o login no portal do iFood é **manual, uma única vez, pelo dono** — o DROPFOOD nunca pede senha. Isso protege sua conta de automação agressiva.

## Arquitetura

**Fork do Hermes com modificação mínima** (decisão do dono 25/10):

| Camada | O que é |
|---|---|
| D0 | `core/` = fork do Hermes (NousResearch, MIT, commit pinado em `core/UPSTREAM.txt`) |
| D1 | Skin do produto (`skins/dropfood.yaml` — paleta em `design/DESIGN.md`) + PT-BR |
| D2 | Skill `dropfood-ops` + scripts (radar, catálogo, monitor) |
| D3 | Bots (SOULs templates em `bots/templates/` — persona por loja) |
| D4 | UI do produto (Desktop Plugin SDK — panes OPS, ⌘K, dashboard tab) |
| D5 | Distribuição (este repo + instalador standalone/wizard — F4) |

Detalhes em `docs/ARQUITETURA.md`.

## Repositório sanitizado

Este repositório é **100% sanitizado**: nenhum dado real de loja entra aqui. Dados de operação vivem fora do repo, em `~/.hermes/loja/<id>/`. O CI bloqueia qualquer push/PR que contenha dados sensíveis (grep de padrões + segredos).

## Licença

MIT — veja `LICENSE`. Feito para o dono de mercado brasileiro; use, mude e distribua.