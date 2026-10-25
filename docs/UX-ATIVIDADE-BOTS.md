# UX de atividade dos bots — mapeamento (pedido do dono 25/10)

> ⚠️ **SUPERSEDIDO pelo mapa completo** — ver `UX-MAPA-COMPLETO.md` (inventário
> por zona da janela, nativos do core, 13 componentes dropfood, D1-D5
> resolvidos, D6-D9 em aberto). Este doc mantém o detalhe do comportamento das
> faixas e do modal.

> Estado: MAPEAMENTO (sem código). Fonte: core/ do produto (snapshot do
> Hermes pinado d0509566) + biblioteca dropfood_components. Regra: o Hermes
> desktop que já existe é a base; nada se perde — a camada DROPFOOD se
> adapta à UI existente (skin + componentes + plugin SDK), nunca substitui.

## 1. O que o Hermes já renderiza (✅ nativo — reaproveitar, não reescrever)

| Capacidade | Onde (core/apps/desktop/src/components) | O que faz |
|---|---|---|
| Tool run em linha única | `assistant-ui/tool/run-ticker.tsx` (`tool-ticker`) | reel de 1 linha: cada nova chamada "ticks" a anterior pra cima — a "faixa do agente trabalhando" já existe |
| Resumo do run | `assistant-ui/tool/run-summary.ts` | título/estado consolidado de uma sequência de tools |
| Card de delegação | `assistant-ui/tool/delegate.tsx` | usa o MESMO ticker p/ o stream de cada subagente |
| Título de skill carregando | `assistant-ui/tool/skill-activity.ts` | skill_view/skills_list → linha de atividade ("carregando skill…") |
| Feed de tools (chrome) | `assistant-ui/tool/tool-feed-chrome.tsx`, `tool-group.tsx` | agrupamento visual dos tool calls no thread |
| Conversa entre bots NO THREAD | `assistant-ui/thread/inter-agent-collapse.tsx` + `agent-delivery.tsx` | mensagem "Message from 🤖 bX" e resposta colapsada ("Replied to bX", expansível); pipeline `hermes -p <bot> chat -q "Message from…"` — entrega inter-bot já é nativa (#85855) |
| Indicador de atividade duplicada | `assistant-ui/thread/duplicate-activity-indicator.tsx` | dedup de linhas de tool repetidas |
| Spinner/glyph | `ui/glyph-spinner.tsx`, `ui/loader.tsx` | loading neobrutal já existe no design system do próprio Hermes |
| Avatar de agente | `ui/avatar-chip.tsx`, `thread/agent-avatar-cache.ts` | avatar resolvido por agente (`🤖 bX`) |
| Status dot | `status-dot.tsx`, `chat/activity-timer.ts` | ponto de estado + timer de atividade |
| Notificação de processo | `assistant-ui/thread/process-notification.tsx`, `background-resume.tsx` | processo em background voltando |
| **Pet/mascote** | `pet/` (floating-pet, pet-bubble, pet-egg-hatch, pet-star-shower, pet-sprite) | mascote do Hermes JÁ EXISTE — tematizar, não criar do zero |
| Modal/dialog | padrão: `ui/confirm-dialog`, `prompt-overlays.tsx`, `catalog-advanced-dialog.tsx`, `model-visibility-dialog.tsx` | dialogs são padrão nativo (base pro modal de conversa) |
| Bot mode / multi-perfil | rail de perfis + `session-picker.tsx` | chats por perfil, como hoje |

**Conclusão: a "faixa/card do agente trabalhando" por tool JÁ existe (ticker,
run-summary, skill-activity) e a conversa entre bots JÁ existe no thread
(colapse). O que falta é: (a) camada de IDENTIDADE DROPFOOD por bot
(cor/nome/verbo), (b) o MODAL dedicado de conversa entre bots, (c) os
componentes dropfood equivalentes pro produto.**

## 2. Detalhes pedidos (o que construir na camada do produto)

### 2.1 Faixas/cards do agente trabalhando POR BOT (no chat do operador)

Hoje o thread mostra tools de forma genérica (ticker). O dono quer cada bot
identificado enquanto trabalha. Na camada do produto:

| Peça | Comportamento | Componente dropfood novo |
|---|---|---|
| **Faixa de atividade por bot** | no chat principal, quando bX roda: linha com avatar+cor do bot + verbo vivo ("b2 está escaneando concorrentes…") + contagem de passos | `activity-strip` |
| **Card de trabalho** | versão expandida da faixa: bot, missão, steps (1..n), resultado sumário, duração | `working-card` |
| **Animação de presença** | o ponto de estado do bot pulsa enquanto trabalha; neobrutal: "desloca" 2px no loop (mesma linguagem do hover do botão) | `activity-dot` (estilos de animação) |
| **Progresso de passos** | mini-steps neobrutais (quadradinhos ink/pink, preenchimento por passo) | `step-progress` |
| **Avatar de bot com cor canônica** | cada bot ganha cor da paleta (b1 pink, b2 mint, b6 lilac, b7 canary…) p/ leitura instantânea de quem trabalha | extensão do `avatar-chip` (tema dropfood) |

### 2.2 Modal de conversa entre bots

Gatilho: quando uma mensagem inter-bot entra no thread ("Message from 🤖 bX" /
delivery via `hermes -p bX chat -q "Message from…"`), o operador pode abrir o
MODAL — chat dedicado com os bots conversando entre si, tipo "janela de
bastidor".

| Peça | Comportamento | Componente dropfood novo |
|---|---|---|
| **Modal de conversa inter-bot** | modal nativo (padrão Hermes) com: header "Conversa entre bots · b1 ⇄ b2", corredor de mensagens em 2 colunas (cada bot com cor/avatar), espelho expandido do que no thread aparece colapsado | `bot-chat-modal` |
| **Botão de abertura** | chip na mensagem inter-bot (junto do collapse) + entrada no rail de perfis | `bot-chat-open` (chip com ação) |
| **Auto-abertura?** | decisão do dono D2: abrir sozinho quando bots começam a conversar ou só por clique | — |
| **Timeline de handoff** | dentro do modal: linha do tempo dos gates (b1 → b2 recebeu → respondeu…) | `handoff-timeline` |

### 2.3 Animações (linguagem única)

- Todos os estados de "trabalhando" usam o MESMO vocabulário de motion:
  translate 2px (deslocamento neobrutal, igual hover do `df-btn`), durações
  80-150ms, steps em vez de lerp onde der (neobrutal é quadrado).
- O reel/ticker nativo continua (não reescrever) — só skin de cor pelo bot.
- Pet nativo: tematizar com canary/mint; nenhum pet novo.

## 3. Componentes que faltam na biblioteca dropfood_components

Hoje: `alert, badge, button, chip, input, tokens` (registry shadcn-compatível,
MCP `dropfood_components`). Faltam (todos `components/dropfood/<nome>.{css,tsx}`
+ registro no `registry.json`):

| # | Componente | Tipo | Base | Status |
|---|---|---|---|---|
| 1 | `activity-strip` | registry:ui | ticker nativo (wrap com identidade do bot) | ❌ falta |
| 2 | `working-card` | registry:ui | run-summary + delegate-card | ❌ falta |
| 3 | `activity-dot` | registry:ui | status-dot + animação pulse/deslocar | ❌ falta |
| 4 | `step-progress` | registry:ui | novo (steps neobrutais) | ❌ falta |
| 5 | `bot-avatar` | registry:ui | avatar-chip + cor por bot (paleta canônica) | ❌ falta |
| 6 | `bot-chat-modal` | registry:ui | dialog nativo do Hermes + corredor 2 colunas | ❌ falta |
| 7 | `handoff-timeline` | registry:ui | entregas/gates entre bots | ❌ falta |
| 8 | `tokens` (extensão motion) | registry:style | `--df-motion-*` (dur/easing paso) — SÓ motion, cor segue a canônica | ⚠️ decisão D4 |

Regra da casa mantida: identificar `tone` por bot = cores da paleta canônica
(cream/ink/pink/mint/canary/lilac/coral) — nenhum token de COR novo.

## 4. Onde isso vive (adaptação, não reescrita)

- **Skin**: cores/estados já cobrem (skin-keys inventário); nada de key nova.
- **Componentes**: biblioteca dropfood_components (produto) — shadcn-compatível,
  MCP local; o desktop do fork consome via plugin SDK D4 (não patchar `core/`).
- **Thread/ticker/collapse nativos**: INTOCADOS — a camada DROPFOOD embeleza
  por cima (plugin stylesheet + componentes dropfood).
- **Entrega inter-bot**: pipeline nativo `hermes -p bX chat -q "Message
  from…"` continua sendo o meio — o modal é uma JANELA sobre o que já acontece.

## 5. Decisões em aberto (pro dono — numerar)

- **D1** — Faixa por bot no chat: inline no thread (junto das tools, como hoje) ou
  num painel lateral fixo de atividade (activity rail)? (proposta: inline,
  menos código novo, respeita o Hermes)
- **D2** — Modal de conversa entre bots: abre SOZINHO quando detecta delivery
  inter-bot, ou só por clique (é menos enxerido e não rouba o fluxo)?
  (proposta: só por clique + badge discreto "2 bots conversando")
- **D3** — Cor por bot fixa na paleta (b1 pink, b2 mint, b6 lilac, b7 canary)
  ou o dono define o mapa? (proposta: mapa fixo documentado, trocável no config)
- **D4** — Tokens de motion (`--df-motion-*`) entram no tokens.css como
  categoria nova (não é cor, não fura a canônica) ou ficam hard-coded nos
  componentes? (proposta: tokens — centraliza a linguagem de animação)
- **D5** — Ordem de entrega: primeiro `activity-strip+working-card` (visão
  imediata no chat) e o modal depois; ou modal primeiro? (proposta:
  faixas primeiro, modal em seguida)

## 6. Próximo passo

Aprovar decisões → atualizar `registry.json` + escrever os componentes
(shadcn-compatível, lint DESIGN.md) → aplicar no fork via plugin SDK D4.
