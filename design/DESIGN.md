---
version: alpha
name: DROPFOOD
description: Neobrutalismo de mercado brasileiro — cream quente, rosa de ação, hortelã de sucesso, amarelo de preço bom. UI do produto DROPFOOD Agent sobre o Hermes desktop.
colors:
  primary: "#FF3D81"
  secondary: "#3DDC97"
  tertiary: "#FF6B5E"
  warn: "#FFD23F"
  neutral: "#FDF9F0"
  neutralDim: "rgba(17,17,17,0.62)"
  background: "#FDF9F0"
  ink: "#111111"
  border: "#111111"
  brand: "#0E9F6E"
  paper: "#FFFDF7"
  thinking: "#6B655C"
  lilac: "#C8A2FF"
typography:
  display:
    fontFamily: "Archivo Black, Space Grotesk, sans-serif"
    fontSize: 3rem
    fontWeight: 900
    lineHeight: 1.0
    letterSpacing: "-0.03em"
  heading:
    fontFamily: "Archivo Black, Space Grotesk, sans-serif"
    fontSize: 1.5rem
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Space Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: 1rem
    fontWeight: 500
    lineHeight: 1.5
  label:
    fontFamily: "Space Mono, ui-monospace, monospace"
    fontSize: 0.75rem
    fontWeight: 700
    letterSpacing: "0.15em"
rounded:
  sm: 2px
  md: 4px
  lg: 8px
  xl: 18px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
elevation:
  sm: "4px 4px 0 #111111"
  md: "6px 6px 0 #111111"
  lg: "9px 9px 0 #111111"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: 12px
  button-secondary:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: 12px
  card:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
  badge-ok:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
  badge-warn:
    backgroundColor: "{colors.warn}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
  badge-error:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
  tool-marker:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  muted-text:
    backgroundColor: "{colors.background}"
    textColor: "{colors.neutralDim}"
  divider:
    backgroundColor: "{colors.border}"
    textColor: "{colors.neutral}"
  label-chip:
    backgroundColor: "{colors.background}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
  accent-lilac:
    backgroundColor: "{colors.lilac}"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
  thinking-text:
    backgroundColor: "{colors.background}"
    textColor: "{colors.thinking}"
  brand-surface:
    backgroundColor: "{colors.brand}"
    textColor: "{colors.ink}"
---

# DROPFOOD — Design System do produto

## Overview

O DROPFOOD é o agente open source do dono de mercado brasileiro. A identidade é
**neobrutalismo de mercado**: blocos sólidos, bordas marcadas, contraste chapado —
cream quente de caderno de padaria, pink de ação, mint de sucesso, amarelo de
"preço bom". Tudo
corre sobre o Hermes desktop; este spec é a fonte única dos tokens, e o
apêndice mapeia cada token para as keys reais do skin engine do Hermes.

## Colors

Paleta canônica = **design system do dashboard da loja** (`dashboard/assets/neubrutal.css`,
localhost:8501 — decisão do dono 25/10): cream + ink + pink + mint + canary +
lilac + coral, sombras diagonais 4/6/9px, raios 18/8/9999, display Archivo
Black. O produto DROPFOOD herda EXATAMENTE essas cores/componentes, sem
mudar a estrutura.

- **Cream (#FDF9F0):** fundo base (paper) — a app troca para base clara.
- **Ink (#111111):** texto, bordas de moldura (2px) e todas as sombras duras.
- **Primary — Pink (#FF3D81):** ação, destaque, tab ativa, botões. O accent
  de tudo que é clicável (contraste AA sobre Cream).
- **Secondary — Mint (#3DDC97):** sucesso, disponível, entregue, ok.
- **Tertiary — Coral (#FF6B5E):** erro, bloqueio, falta (pulso de alerta).
- **Warn — Canary (#FFD23F):** atenção, preço bom, destaque de valor.
- **Lilac (#C8A2FF):** destaque secundário alternado (barras, ícones).
- **Fontes:** `Archivo Black` (display/kpi) · `Space Grotesk` (corpo) ·
  `Space Mono` (números/mono) — as mesmas do dashboard.
- **Sombras:** `4px 4px 0` (sm) / `6px 6px 0` (md) / `9px 9px 0` (lg) sempre
  com Ink; hover desloca (-1,-1) e active afunda (+1,+1).
- **Raios:** 18px (cards/chat) · 8px (botões/inputs) · 9999 (pills/tabs).
- **Grid:** fundo com grid 24px (rgba ink 5%) — textura do dashboard.
- **Brand — Mint profundo (#0E9F6E):** derivado do Mint p/ links sobre
  Cream (AA); o verde-mercado anterior é substituído pela paleta do
  dashboard (decisão do dono).

Regra: nunca texto de baixo contraste sobre Primary (texto = Ink). Verde
Brand só em superfícies claras, em BrandDeep ou como hover — nunca como
accent geral.

## Typography

**Display** = Archivo Black, uppercase
weight 900, tracking -0.03em (o "DROPFOOD" do logo e do gancho).
**Heading** = Archivo Black, weight 800, tracking -0.01em. **Body** = Space
Grotesk 500, 1rem/1.5. **Label** = Space Mono, uppercase, weight 700,
tracking 0.15em (chips, badge, "AGENT").

## Layout

Espaçamento em escala 4/8/16/24/40. Layout em blocos: cards com borda
marcada (1-2px em Primary ou Ink), cantos de 2-4px (neubrutal: quase nada de
raio), sombras duras (offset 4px, sem blur) — não existe sombra suave.

## Elevation

Neobrutal: elevação = deslocamento duro (0 4px 0 Ink), não blur. Um card
"flutuante" tem o bloco de sombra em Ink deslocado 4px pra baixo.

## Motion

Linguagem única de animação (decisão do dono 25/10 — D4; só em
`tokens.css`, fora do schema do lint): deslocamento 2px em vez de fade,
durações curtas (80ms fast · 150ms base · 260ms slow), `steps` em vez de
lerp onde der. Tokens: `--df-motion-fast/base/slow/step/ease/ease-step/pulse`.

## Shapes

Cantos: 2px (sm), 4px (md), 8px (lg — só em superfícies grandes como o
composer). Sem raio acima de 8px. O logo é círculo (exceção explícita).

## Components

- **button-primary:** bloco pink, texto ink, borda ink, sombra dura, hover
  desloca (-1,-1). Pink é a ação de tudo que é clicável (contraste AA sobre
  cream, texto ink).
- **button-secondary:** bloco cream com borda ink (ação neutra).
- **card:** superfície paper, borda ink 2px, sombra dura 4px, raio 18px.
- **badge-ok/warn/error:** status do radar (MANTEM/SOBE/DESCE/ALERTA).
- **tool-marker:** o ● de tool-call do Hermes em Primary (sem tocar headings).

## Do's and Don'ts

- **Faça:** borda marcada em ink; blocos sólidos de cor chapa; contraste
  chapado; texto ink sobre pink/mint/canary/lilac/coral (AA); sombras duras
  4/6/9px; deslocamento 2px no hover/active.
- **Não faça:** sombras suaves/neblur; gradientes; raios acima de 18px;
  texto de baixo contraste sobre Primary; verde-brand como accent geral (o
  accent é o pink — o brand verde é sucesso/links AA sobre cream; motion usa
  steps e durações curtas (--df-motion-*), nunca lerp longo.

---

## Appendix — Mapa DESIGN.md → Hermes skin engine (source: hermes_cli/skin_engine.py)

Toda key abaixo existe no engine/built-ins (conferido no código, 25/10/2026).
A skin do produto vive em `<HERMES_HOME>/skins/dropfood.yaml` e repinta
CLI+TUI+Desktop via gateway (watcher ~1s).

| Token DESIGN.md | Skin key | Superfície |
|---|---|---|
| `colors.background` | `background` | fundo da app (GUI deriva a paleta dele) |
| `colors.primary` | `ui_accent`, `banner_accent`, `input_rule`, `response_border`, `prompt`, `session_label`, `ui_tool` | accent: headings, links, ● de tool-call, prompt, regras |
| `colors.secondary` | `ui_ok`, `status_bar_good` | sucesso |
| `colors.warn` | `ui_warn`, `status_bar_warn` | aviso |
| `colors.tertiary` | `ui_error`, `status_bar_critical` | erro |
| `colors.neutral` | `banner_title`, `banner_text`, `ui_text`, `status_bar_text`, `prompt` fallback | texto primário |
| `colors.label` | `ui_label` | rótulos |
| `colors.neutralDim` | `banner_dim`, `status_bar_dim` | secundário, conectores |
| `colors.ink` | `status_bar_bg` | chão sólido |
| `colors.border` | `ui_border`, `banner_border`, `session_border` (ou Primary p/ moldura neubrutal) | bordas |
| `colors.thinking` | `ui_thinking` | texto de raciocínio |
| — | `status_bar_strong`, `status_bar_bad`, `completion_menu_bg`, `completion_menu_current_bg`, `selection_bg`, `shell_dollar`, `voice_status_bg`, `diff_added`, `diff_removed`, `diff_added_word`, `diff_removed_word`, `syntax_*` | chrome restante (preenchidas na skin com valores derivados da paleta) |
| branding | `branding.agent_name/prompt_symbol/welcome/goodbye/help_header`, `tool_prefix` | identidade textual do produto |