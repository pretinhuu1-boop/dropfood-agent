# Mapa completo de UI da janela DROPFOOD (v1 — substrato verificado)

> Pedido do dono 25/10: mapear TUDO de uma vez para não refazer. Direção aprovada
> (D1-D5): faixas inline por bot, modal por clique + badge, cor fixa por bot,
> tokens de motion, faixas antes do modal. Base: core/apps/desktop do produto
> (snapshot Hermes d0509566) lido arquivo a arquivo. Regra-mãe: adaptar a UI que
> já existe, nunca reescrever. Documentos relacionados: fluxograma-janela.html
> (design/), UX-ATIVIDADE-BOTS.md (detalhe das faixas/modal).

## Descoberta central

O desenho aprovado (navegador no meio + agente na lateral operando via
computer-use + bots nativos) **já existe como infraestrutura no Hermes**:

- Preview pane nativo com barra de URL: `app/chat/right-rail/preview-pane.tsx`,
  `preview-browser-bar.tsx`, `preview-browser-frame.ts` (webview no desktop
  Electron / iframe sandboxed no browser-hosted)
- Agente JÁ dirige esse pane: `preview-act.ts` + `preview-drive.ts` +
  `preview-reader.ts` (clickAt, pressKey, clearCharsBack, selectAll, glideTo,
  engine in-page, inventory pós-ação) — é o computer-use nativo do Hermes
  apontado pro pane
- A skill computer-use (Camoufox) vira o MESMO padrão em janela própria

Logo, "navegador central operado pelo agente" não é componente novo: é
**reposicionar o pane existente + skin + definir a superfície de comando**
(ver D6).

## 0. Legenda de status

- ✅ NAT = existe no core Hermes (arquivo citado), não tocar
- ✅ DF = já existe na biblioteca dropfood_components
- ❌ NOV = componente novo a criar na camada do produto (shadcn-compatível)
- 🟡 AJU = ajuste de posição/cor/comportamento na camada, base nativa

## 1. Zona A — Navegador central (portal iFood)

| Peça | Status | Onde/Base | Componente dropfood |
|---|---|---|---|
| Pane com barra de URL | ✅ NAT | `right-rail/preview-pane.tsx`, `preview-browser-bar.tsx` | — (skin) |
| Frame webview/iframe | ✅ NAT | `preview-browser-frame.ts` | — |
| Agente dirige o pane | ✅ NAT | `preview-act.ts`, `preview-drive.ts`, `preview-reader.ts` | 🟡 `drive-preview` (wrapper p/ o operador) |
| Sessão real do dono (portal) | 🟡 AJU | login manual 1x (regra de ouro); pane navega pra URL do portal | `browser-session` badge de estado |
| Anotação no preview | ✅ NAT | `preview-annotate-card.tsx`, `preview-annotate-host.ts` | — |
| Tour do preview | ✅ NAT | `preview-tour.ts` | — |
| Controle de popout | ✅ NAT | `preview-popout-bridge.ts` | — |

**Falta (Zona A):** nada estrutural. 🟡 reposicionar o pane pro centro quando
a skin/layout F1 ativar; `browser-session` (chip de estado da sessão do portal
na barra do navegador: ativa/OTP pendente/quebrada).

## 2. Zona B — Chat central: atividade do agente POR BOT

| Peça | Status | Onde/Base | Componente dropfood |
|---|---|---|---|
| Faixa 1-linha (ticker) | ✅ NAT | `tool/run-ticker.tsx` | 🟡 `activity-strip` (identidade do bot em volta) |
| Resumo do run | ✅ NAT | `tool/run-summary.ts` | 🟡 `working-card` (versão expandida) |
| Skill carregando | ✅ NAT | `tool/skill-activity.ts` | — (vira linha do strip) |
| Card de delegação | ✅ NAT | `tool/delegate.tsx` (mesmo ticker) | 🟡 `working-card` (modo delegação) |
| Feed de tools | ✅ NAT | `tool/tool-feed-chrome.tsx`, `tool-group.tsx` | — |
| Aprovação inline | ✅ NAT | `tool/approval.tsx` | — |
| Faixa no composer | ✅ NAT | `composer/status-stack/` (coding-row, drawer, preview-row) | 🟡 skin por bot |
| Mensagem inter-bot no thread | ✅ NAT | `thread/user-message.tsx` (AGENT_MESSAGE_RE), `inter-agent-collapse.tsx`, `agent-delivery.tsx` | 🟡 `bot-chat-open` (chip de abrir modal) |
| Indicador actividad duplicada | ✅ NAT | `thread/duplicate-activity-indicator.tsx` | — |
| Processo em background | ✅ NAT | `thread/process-notification.tsx`, `background-resume.tsx` | 🟡 avatar do bot |
| Spinner/loader | ✅ NAT | `ui/glyph-spinner.tsx`, `ui/loader.tsx`, `ui/status-pulse.tsx` | 🟡 `activity-dot` |
| Avatar de agente | ✅ NAT | `ui/avatar-chip.tsx`, `thread/agent-avatar-cache.ts` (LRU de avatares por profíle) | 🟡 `bot-avatar` (cor canônica por bot) |

**Componentes novos Zona B (D1-D5 aprovados):** `activity-strip`, `working-card`,
`activity-dot`, `step-progress`, `bot-avatar`.

## 3. Zona C — Modal de conversa entre bots

| Peça | Status | Onde/Base | Componente dropfood |
|---|---|---|---|
| Dialog base | ✅ NAT | `ui/dialog.tsx`, `ui/sheet.tsx`, `prompt-overlays.tsx` | 🟡 `bot-chat-modal` (shell) |
| Corredor 2 colunas bX ⇄ bY | ❌ NOV | nenhum (thread é 1 coluna) | `bot-chat-modal` (body) |
| Timeline de handoff/gates | ❌ NOV | nenhum | `handoff-timeline` |
| Chip de abertura | ❌ NOV | (chip nativo existe: `ui/chip.tsx`) | `bot-chat-open` |
| Badge "2 bots conversando" | ❌ NOV | (badge nativo: `ui/badge.tsx`) | `bot-chat-badge` |
| Dados (fonte) | ✅ NAT | gateway `profiles.list` + mensagens inter-bot do thread | ler do mesmo canal |
| Auto-abertura | 🟡 AJU | D2 RESOLVIDO: por clique + badge | — |

## 4. Zona D — Sidebar esquerda (HERMES intocado)

| Peça | Status | Onde | Componente dropfood |
|---|---|---|---|
| Sessões, filtros, profile switcher | ✅ NAT | `app/chat/sidebar/` (profile-switcher, filter-menu) | — NADA |
| Bots/rail de perfis | ✅ NAT | profiles nativo (mesma UX do Hermes — pedido do dono) | — NADA |
| Kanban/tasks/cron | ✅ NAT | app/ (nativo) | — |

## 5. Zona E — Tela de entrada / onboarding (F1)

| Peça | Status | Onde/Base | Componente dropfood |
|---|---|---|---|
| Fluxo de onboarding | ✅ NAT | `components/onboarding/` (flow.tsx, first-run, skip-setup, onboarding-end) | 🟡 `df-onboarding` (re-skin + logo DROPFOOD) |
| Tela de entrada/boot | 🟡 AJU | boot-failure-overlay, gateway-connecting-overlay | skin da marca |
| Ícone .icns/.ico | ❌ NOV | só `assets/logo-dropfood.svg` existe | gerar a partir do SVG |
| Mascote/pet | ✅ NAT | `pet/` (floating-pet, pet-egg-hatch, pet-star-shower) | 🟡 skin canary/mint |
| Marca/branding | ✅ NAT | `components/brand-mark.tsx`, skin keys `branding.*` | 🟡 logo dropfood |

## 6. Zona F — Statusbar + chrome

| Peça | Status | Onde/Base | Componente dropfood |
|---|---|---|---|
| Statusbar | ✅ NAT | `app/shell/statusbar-*.tsx`, system-resources-statusbar | — (skin cobre: status_bar_*) |
| Titlebar | ✅ NAT | `app/shell/titlebar*.tsx` | — (skin) |
| Butterbar/avisos | ✅ NAT | `app/shell/butterbar.tsx` | — |
| Modais do sistema | ✅ NAT | `ui/confirm-dialog`, overlays | — |

## 7. Biblioteca dropfood_components — inventário final

**Existe (6):** `tokens.css`, `alert`, `badge`, `button`, `chip`, `input`.

**Faltam (total 13):**

| # | Componente | Zona | Base nativa | Obs |
|---|---|---|---|---|
| 1 | `activity-strip` | B | run-ticker | faixa 1-linha com identidade do bot |
| 2 | `working-card` | B | run-summary + delegate | missão, steps, duração, resultado |
| 3 | `activity-dot` | B | status-pulse/glyph-spinner | pulsa/desloca 2px neobrutal |
| 4 | `step-progress` | B | novo | quadrinhos ink/pink por passo |
| 5 | `bot-avatar` | B | avatar-chip | cor canônica por bot (D3) |
| 6 | `bot-chat-open` | C | chip | abre o modal (D2: por clique) |
| 7 | `bot-chat-badge` | C | badge | "2 bots conversando" |
| 8 | `bot-chat-modal` | C | dialog/sheet | corredor 2 colunas |
| 9 | `handoff-timeline` | C | novo | gates b1→b2→… |
| 10 | `drive-preview` | A | preview-act/drive | wrapper operador → pane |
| 11 | `browser-session` | A | novo | chip de estado da sessão portal |
| 12 | `df-onboarding` | E | onboarding/flow | login = conectar a loja (F1) |
| 13 | `tokens` motion | global | tokens.css | só `--df-motion-*` (D4) |

## 8. Decisões RESOLVIDAS (dono, 25/10)

- **D1** — faixas inline no thread (não painel lateral fixo)
- **D2** — modal abre por clique + badge discreto (não automático)
- **D3** — cor fixa por bot: b1 pink, b2 mint, b6 lilac, b7 canary, bt treinador canary, operador coral (mapa documentado)
- **D4** — tokens de motion `--df-motion-*` no tokens.css (categoria nova; cor segue a canônica)
- **D5** — ordem: faixas (1-5) primeiro, modal (6-9) em seguida

## 9. Decisões NOVAS em aberto

- **D6** — Superfície de comando do navegador central: (a) preview-act/drive
  nativo apontado ao pane (recomendado: já existe, é o "computer-use do
  Hermes") ou (b) skill computer-use/Camoufox em janela própria espelhada no
  pane (garante anti-bot com perfil real, mas é browser duplicado)?
- **D7** — O logo `assets/logo-dropfood.svg` ainda é VERDE mercado (#16a34a) —
  alinhar à canônica (pink/ink, Archivo Black) junto da F1? (recomendado: sim,
  marca única)
- **D8** — Tela de entrada F1 reaproveita o onboarding nativo re-skinado
  (recomendado) ou fluxo próprio? 
- **D9** — `browser-session` da Zona A como chip na barra do navegador ou na
  statusbar? (recomendado: barra do navegador)

## 10. Ordem de execução (após aprovação)

1. Fase 1 (F1 identidade + Zona A): skins/branding, df-onboarding, ícone,
   drive-preview + browser-session, reposicionar pane
2. Fase 2 (Zona B — D5): tokens motion → activity-dot/strip/working-card/
   step-progress/bot-avatar
3. Fase 3 (Zona C): bot-chat-open/badge/modal/handoff-timeline
4. Gate: DESIGN.md lint (npx @google/design.md) + registry.json + MCP
   dropfood_components + skill dropfood-ops
