# Arquitetura — DROPFOOD Agent

## Princípio: FORK com modificação mínima (decisão do dono 25/10)

O DROPFOOD é um **fork do Hermes** (`core/` = snapshot de
NousResearch/hermes-agent, MIT, commit d0509566 — ver core/UPSTREAM.txt).
O núcleo upstream fica intacto; o produto modifica o MÍNIMO (identidade +
operação) e reaproveita tudo nativo. Atualizações = re-snapshot com diff
listável; nunca reimplementar o core. Login = conectar a loja do iFood
(manual do dono 1x); API/provider = nativo (OpenRouter ou providers
suportados).

```
┌─────────────────────────────────────────────────┐
│ D6 Pessoal Cloud: GitHub privado DO DONO        │
│    sync da loja (backup_loja.sh) — retomada     │
├─────────────────────────────────────────────────┤
│ D5 Distribuição: repo + install.sh + wizard     │
├─────────────────────────────────────────────────┤
│ D4 UI do produto: Desktop Plugin SDK            │
│    panes OPS (Dia, Catálogo, Preços, Radar,     │
│    Alertas, Config) + ⌘K + dashboard tab        │
├─────────────────────────────────────────────────┤
│ D3 Bots: Bot Mode, SOULs templates (neutros)    │
│    persona por loja via ~/.hermes/loja/config   │
├─────────────────────────────────────────────────┤
│ D2 Skill dropfood-ops + scripts (radar, portal, │
│    catálogo, monitor, backup_loja)              │
├─────────────────────────────────────────────────┤
│ D1 Skin dropfood.yaml + PT-BR (language pack)   │
├─────────────────────────────────────────────────┤
│ D0 core/ = fork do Hermes (upstream MIT,        │
│    modificação mínima: identidade/operação)     │
└─────────────────────────────────────────────────┘
```

## Camadas

- **D0 — Hermes core**: nada do DROPFOOD altera o core. Atualizações upstream
  não quebram o produto (caem os mesmos riscos de fork drift).
- **D1 — Skin + idioma**: `skins/dropfood.yaml` instala em
  `~/.hermes/skins/`; tokens 1:1 com `design/DESIGN.md` (spec Google,
  validado com `npx @google/design.md lint`, WCAG AA). PT-BR via
  `display.language=pt` (language pack bundled do Hermes).
- **D2 — Skill + scripts**: skill `dropfood-ops` (neutra, sem dados de
  loja — loja vem do perfil). Scripts: radar de preços, espelho de
  catálogo, monitor do portal, notas→dataset de treino.
- **D3 — Bots**: templates de SOUL em `bots/templates/` — ofícios neutros
  (estratégia, radar, roteiro, direção, produção, revisão, controle,
  treinador). A persona de cada bot lê o perfil da loja em
  `~/.hermes/loja/config.yaml`. Runtime local: lfm2.5:8b (motor) +
  qwen3.5:2b/4b (leve/qualidade) — única família com tool-call nativo
  no Ollama (radar de modelos, 25/10/2026).
- **D4 — UI do produto**: Desktop Plugin SDK do Hermes (sem build): panes
  OPS, entrada ⌘K, sidebar, status bar e tab no dashboard. Alcance do SDK
  validado por spike antes de qualquer promessa (fallback: fork de UI
  apenas, core intacto).
- **D5 — Distribuição**: repo público + `install.sh` (one-click) + wizard
  para quem não tem Hermes + docs.
- **D6 — Pessoal Cloud (GitHub privado)**: cada dono conecta o GitHub DELE;
  `~/.hermes/loja/<id>/` sincroniza pra um repo privado do próprio dono
  (`dropfood-loja-<id>`) — retomada de qualquer máquina. Design completo em
  `docs/BACKUP-GITHUB.md`; usa o que já existe (gh CLI, device flow) e não
  reinventa backup do Hermes (nativo: `hermes backup`/`import`/`sync`).

## Regras de higiene (obrigatórias)

1. **Nada de dados reais no repo**: `~/.hermes/loja/<id>/` vive fora do
   git. O CI (`sanitize.yml`) bloqueia push/PR com dados de loja real,
   segredos ou arquivos proibidos.
2. **Login manual, 1x, pelo dono**: o DROPFOOD nunca pede nem guarda
   senha do portal iFood (regra de ouro — protege a conta contra ban).
3. **Conteúdo público revisado**: qualquer doc/asset que cite loja real
   particular é neutralizado antes de entrar.
4. **Se o upstream mudar**: revalidar skin/keys e SDK contra a versão
   instalada (catálogo de capacidades + testes).
5. **Dados de loja sobem SOMENTE pro repo privado do dono** (D6 —
   `scripts/backup_loja.sh`). Nunca pro repo público do produto; tokens,
   cookies de sessão do portal e senhas nunca versionam (gitignore local
   da pasta loja).