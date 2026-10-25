# Backup & retomada — GitHub pessoal de cada dono (design, 25/10/2026)

Pedido do dono: cada usuário conecta o **GitHub dele** (conta pessoal) e os
dados da loja ficam salvos num **repo privado do próprio dono** — a operação
retoma de qualquer lugar.

## 1. Por que

- **Retomada total**: máquina nova (ou formatada) → restore da loja e o Hermes
  volta operando igual (config, notas, radar, estado).
- **Histórico**: cada sync deixa registro versionado do estado da operação
  (quem/quando/o quê mudou).
- **Confiança**: o dado fica na conta do próprio dono (privado, 2FA do GitHub),
  não numa nuvem de terceiros.

## 2. O que JÁ EXISTE (mapeamento — regra: nunca reinventar)

| Existe em | Ferramenta | Cobre |
|---|---|---|
| Hermes core | `hermes backup` / `hermes backup --quick` | zip de config, skills, sessões, dados (exclui codebase); quick = só estado crítico (config, state.db, .env, auth, cron) |
| Hermes core | `hermes import` | restaura um backup zip |
| Hermes core | `hermes sync` (Skill Sync) | skills do usuário entre devices (pull/push/device) |
| Hermes core | `hermes sessions export` | histórico de sessões (texto) |
| Produto (dropfood-agent) | `~/.hermes/loja/<id>/` | dados de operação da loja: config.yaml, notas, radar, catálogo — **fora de qualquer git hoje** |
| Produto (dropfood-agent) | regra de higiene #1 | nada de dado real no repo público do produto |
| GitHub | `gh` CLI + repos privados | destino do sync; auth por device flow (token nunca aparece) |

**Lacuna que o produto fecha**: um destino versionado e privado para
`~/.hermes/loja/<id>/` + o comando de sync/restore + a regra. O backup do
Hermes (zip) já cobre o resto do ambiente; o sync de skills é nativo.

## 3. Desenho: camada D6 — Pessoal Cloud

```
┌──────────────────────────────────────────────┐
│ D6 Sync GitHub pessoal (scripts/backup_loja) │
│  ┌────────────────────────────────────────┐ │
│  │ github.com/<EU>/dropfood-loja-<id>     │ │  ← repo PRIVADO do dono
│  │  config.yaml · radar/*.json · notas/   │ │     (não é o repo do produto)
│  │  catalogo/*.json · estado/*.json       │ │
│  └────────────────────────────────────────┘ │
│  fluxo: connect → sync (push) → restore     │
└──────────────────────────────────────────────┘
```

### Fluxo connect (primeira vez)
1. `gh auth status` — se não logado: `gh auth login` (device flow; o token
   vive no keyring do usuário — nunca é impresso nem versionado).
2. `scripts/backup_loja.sh` cria `dropfood-loja-<slug-da-loja>` **privado**
   (ou usa `backup.repo` do config.yaml) e faz o primeiro push.

### Fluxo sync (recorrente)
- No fim de cada ciclo de operação (B7/CONTROLE garante) e/ou via cron do
  usuário: `scripts/backup_loja.sh` → commit + push do estado da loja.
- Mensagem de commit padrão: `sync <data> — <resumo do ciclo>` (1 linha).

### Fluxo restore (máquina nova)
1. Instala Hermes + DROPFOOD (install.sh).
2. `gh auth login` (a conta do dono).
3. `git clone <repo-privado> ~/.hermes/loja/<id>` (o install.sh pergunta).
4. `hermes backup --quick`/`import` para o ambiente (opcional).

### O que sobe / o que nunca sobe

| Sobe (texto, pequeno) | Nunca sobe (gitignore local da pasta loja) |
|---|---|
| config.yaml (perfil da loja) | `.env`, tokens, senhas |
| radar/*.json (estado dos preços) | sessões do portal (cookies) — risco de ban/replay |
| notas/*.md (decisões da operação) | `.venv`, cache, zip de backup pesado |
| catalogo/*.json (espelho do fornecedor) | dados do repo público do produto |

Sessões de conversa (`hermes sessions export`) ficam **off por padrão** —
podem conter dados sensíveis em texto; ligar é decisão do dono (seção 7).

## 4. Segurança

- Repo **privado** sempre (checado no create); nunca público.
- Auth exclusivamente via `gh` (device flow) — token no keyring do SO.
- Gitignore local bloqueia `.env`, sessões e credenciais (defesa em profundidade).
- Criptografia dos arquivos (age/sops) = evolução futura, não bloqueia v1
  (repo privado já é o controle de acesso).
- O repo privado da loja NUNCA se mistura com o repo público do produto
  (sanitize.yml continua valendo do lado público).

## 5. Regra nova (normativa — ARQUITETURA.md §higiene)

> **#5 — Dados de loja sobem SOMENTE para o repo privado do dono, via
> `dropfood sync` (backup_loja.sh).** Nunca para o repo público do produto;
> tokens, cookies de sessão e senhas nunca versionam (gitignore local).

## 6. Implementação v1

- `scripts/backup_loja.sh`: connect / sync / restore-guide / --dry-run / --cron
  (instala crontab diário do usuário, só com flag explícita).
- `config.yaml` ganha `backup:` (github, repo, frequencia).
- SOUL do B7/CONTROLE: garantir sync no fim do ciclo e reportar estado.
- Skill dropfood-ops: seção "Backup e retomada".

## 7. Decisões em aberto (dono)

- D1: testar ponta-a-ponta criando um repo privado demo na conta do dono?
- D2: incluir `hermes sessions export` no sync (off por padrão)?
- D3: versionar também um `hermes backup --quick` por sync (zip pequeno,
  ~KB) — dá restore do ambiente inteiro a partir do mesmo repo?