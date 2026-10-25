---
version: alpha
name: DROPFOOD
description: Neobrutalismo de mercado brasileiro — café quente, amarelo de preço bom, verde de entrega. UI do produto DROPFOOD Agent sobre o Hermes desktop.
colors:
  primary: "#F0B429"
  secondary: "#34D399"
  tertiary: "#F87171"
  warn: "#FB923C"
  neutral: "#EDE5D8"
  neutralDim: "#9C9185"
  background: "#171310"
  ink: "#000000"
  border: "#3A332B"
  brand: "#16a34a"
  brandDeep: "#14532d"
  paper: "#fafaf9"
  label: "#D8CCBB"
  thinking: "#B4A896"
typography:
  display:
    fontFamily: system-ui, -apple-system, sans-serif
    fontSize: 3rem
    fontWeight: 900
    lineHeight: 1.0
    letterSpacing: "-0.03em"
  heading:
    fontFamily: system-ui, -apple-system, sans-serif
    fontSize: 1.5rem
    fontWeight: 800
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body:
    fontFamily: system-ui, -apple-system, sans-serif
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: system-ui, -apple-system, sans-serif
    fontSize: 0.75rem
    fontWeight: 700
    letterSpacing: "0.15em"
rounded:
  sm: 2px
  md: 4px
  lg: 8px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.brandDeep}"
    textColor: "{colors.paper}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-secondary:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 12px
  card:
    backgroundColor: "{colors.background}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.md}"
  badge-ok:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  badge-warn:
    backgroundColor: "{colors.warn}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
  badge-error:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
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
    textColor: "{colors.label}"
    rounded: "{rounded.sm}"
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
**neobrutalismo quente**: blocos sólidos, bordas marcadas, contraste chapado —
mas com a paleta de um mercadinho de bairro à noite (café, amarelo de "preço
bom", verde de entrega) em vez do cinza frio dos temas de desenvolvedor. Tudo
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

system-ui em tudo (sem fontes custom na v1). **Display** = uppercase,
weight 900, tracking -0.03em (o "DROPFOOD" do logo e do gancho).
**Heading** = weight 800, tracking -0.01em. **Body** = regular 1rem/1.5.
**Label** = uppercase, weight 700, tracking 0.15em (chips, badge, "AGENT").

## Layout

Espaçamento em escala 4/8/16/24/40. Layout em blocos: cards com borda
marcada (1-2px em Primary ou Ink), cantos de 2-4px (neubrutal: quase nada de
raio), sombras duras (offset 4px, sem blur) — não existe sombra suave.

## Elevation

Neobrutal: elevação = deslocamento duro (0 4px 0 Ink), não blur. Um card
"flutuante" tem o bloco de sombra em Ink deslocado 4px pra baixo.

## Shapes

Cantos: 2px (sm), 4px (md), 8px (lg — só em superfícies grandes como o
composer). Sem raio acima de 8px. O logo é círculo (exceção explícita).

## Components

- **button-primary:** bloco amarelo, texto ink, borda ink, sombra dura.
  Hover → verde-escuro BrandDeep com texto paper (a "entrega" da ação).
- **button-secondary:** bloco café com contorno amarelo.
- **card:** superfície café, borda marcada, conteúdo creme.
- **badge-ok/warn/error:** status do radar (MANTEM/SOBE/DESCE/ALERTA).
- **tool-marker:** o ● de tool-call do Hermes em Primary (sem tocar headings).

## Do's and Don'ts

- **Faça:** borda marcada em Primary; blocos sólidos; contraste chapado;
  superfícies escuras com texto creme; brand verde só no logo/hover.
- **Não faça:** sombras suaves/neblur; raios grandes; gradientes; texto de
  baixo contraste sobre Primary; verde Brand como accent geral (o accent é
  o amarelo — o verde é sucesso/marca).

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