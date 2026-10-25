# PLANO-PONTA-A-PONTA — DROPFOOD Agent

> Fonte única do plano de fases do produto (este repositório). A divisão de
> papéis com o repositório de desenvolvimento (`ifood-mercado-operador`) está
> em docs/ARQUITETURA.md. O core é o fork do Hermes pinado (core/UPSTREAM.txt).

## Modelo

O produto **é** um Hermes forkado e modificado a mínimo para a operação do
iFood Mercado — nada de "Hermes constrói o produto". A camada do produto
(skins, scripts, componentes, plugins) vive neste repo; o core segue pinado
e atualiza por re-snapshot + diff.

## Fases (estado 25/10)

| Fase | Nome | Estado | Entrega |
|---|---|---|---|
| F0 | Fork base | ✅ | core/ pinado d0509566, CI sanitize (scan+test), skin dropfood |
| F1 | Identidade | ✅ base | ícone .icns/.ico, df-onboarding, tokens canônicos, DESIGN.md lint 0/0, logo v1 (dono troca D7) |
| F2 | Operação (bots/ciclo) | ⏳ parcial | wizard ✓, templates ✓ (operador ✓), scripts ✓, GATE-F2 ✓; gate portal real = dono |
| F3 | Conhecimento embutido | ✅ v1 | docs/ESTADO-DA-ARTE.md, skill dropfood-ops, ifood-sdk F0 (`install.sh --com-sdk`) |
| F4 | Distribuição | ⏳ parcial | CONTRIBUTING/SECURITY/FAQ/tests/examples ✓, install standalone (core próprio) ✓, desktop-plugin dropfood v1 ✓; build do desktop e marketplace adptadores pendentes |
| F5 | Beta 3-5 donos | ⏳ gate | depende do dono (convites) + itests do desktop com o plugin |
| F6 | Open source / vídeo | ⏳ gate | MIT ✓ (dono), vídeo + vitrine web pendentes |

## Decisões canônicas (25/10)

- Login do portal: **manual do dono (1x), nunca no código** (SECURITY.md).
- Aplicar preço/TIRA_DO_AR no portal: **pedido explícito do dono**.
- Radar de vitrine (ifood-sdk): opcional, `--com-sdk`, OTP manual, leituras
  espaçadas (cadência ≥5s; ciclo radar 7h).
- Zero dado de loja real no repo; exemplos usam a Adega do Seu João.
- UI: componentes shadcn-compatíveis (registry), tokens `--df-*` no
  tokens.css, mapa UX à frente do código (docs/UX-MAPA-COMPLETO.md).

## Próximo bloco

1. Itests do desktop com o plugin dropfood (chip + settings) — precisa da
   build do desktop do fork (node instalado).
2. Build standalone: empacotar o repo como app de desktop do produto.
3. F5: convidar 3-5 donos (beta) e F6: vídeo + vitrine web.
