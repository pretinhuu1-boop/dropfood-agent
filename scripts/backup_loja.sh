#!/usr/bin/env bash
# DROPFOOD — backup_loja.sh: sync da operação da loja para o GitHub privado do dono.
# Camada D6 (docs/BACKUP-GITHUB.md). Usa gh CLI (device flow — token nunca aparece).
#
# Uso:
#   backup_loja.sh [--dry-run] [--connect] [--cron] [--repo <owner/name>]
#   backup_loja.sh --help
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
LOJA_DIR="$HERMES_HOME/loja"
CONFIG="$LOJA_DIR/config.yaml"
DRY_RUN=0
MODE="sync"
REPO=""

usage() {
  sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
}

# conecta (primeira vez): gh auth + criação do repo privado + primeiro push
connect() {
  echo "→ Conectando GitHub pessoal (device flow — nada é impresso)"
  if ! gh auth status >/dev/null 2>&1; then
    echo "  ! Rode 'gh auth login' (escolha GitHub.com → HTTPS → login via navegador)."
    exit 1
  fi
  local WHO
  WHO=$(gh api user --jq '.login')
  echo "  ✓ autenticado como $WHO"

  if [ -z "$REPO" ]; then
    local SLUG
    SLUG=$(python3 -c "
import re, sys
n = '$1'
n = re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
print(n or 'loja')
" 2>/dev/null || echo "loja")
    REPO="$WHO/dropfood-loja-$SLUG"
  fi

  if [ "$DRY_RUN" = 1 ]; then
    echo "  (dry-run) criaria repo privado: $REPO"
    return 0
  fi

  if ! gh repo view "$REPO" >/dev/null 2>&1; then
    echo "  → criando repo privado $REPO"
    gh repo create "$REPO" --private --description "DROPFOOD — dados da loja (backup privado)"
  else
    echo "  ✓ repo já existe"
  fi
}

sync() {
  [ -f "$CONFIG" ] || { echo "! $CONFIG não existe — copie config.yaml.example e preencha."; exit 1; }
  local NOME LOJA_ID
  NOME=$(grep -m1 -A2 '^loja:' "$CONFIG" | grep -m1 'nome:' | sed -E 's/.*nome:[[:space:]]*//; s/["'\'']//g' || echo "Minha Loja")
  LOJA_ID=$(basename "$LOJA_DIR")

  echo "→ Sync da loja '$NOME' ($LOJA_ID)"

  # gitignore local de defesa (nunca versiona credencial/sessão)
  local GI="$LOJA_DIR/.gitignore"
  if [ -f "$GI" ]; then
    touch "$GI"
  else
    cat > "$GI" <<'EOF'
.env
*.pem
*.key
*.p12
sessions/
cookies*
*.zip
.venv/
__pycache__/
EOF
  fi

  # garante repo/remote (connect se preciso)
  if ! git -C "$LOJA_DIR" rev-parse --git-dir >/dev/null 2>&1; then
    echo "  → git init em $LOJA_DIR"
    [ "$DRY_RUN" = 1 ] || git -C "$LOJA_DIR" init -q
  fi
  local REMOTE
  REMOTE=$(git -C "$LOJA_DIR" remote get-url origin 2>/dev/null || true)
  if [ -z "$REMOTE" ]; then
    if [ -z "$REPO" ]; then
      # deriva do nome da loja, igual ao connect
      local SLUG
      SLUG=$(python3 -c "
import re, sys
n = '$NOME'
n = re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
print(n or 'loja')
" 2>/dev/null || echo "loja")
      local WHO
      WHO=$(gh api user --jq '.login' 2>/dev/null || echo "meu-usuario")
      REPO="$WHO/dropfood-loja-$SLUG"
    fi
    echo "  → remote origin = $REPO"
    if [ "$DRY_RUN" = 0 ]; then
      connect "$NOME"
      git -C "$LOJA_DIR" remote add origin "https://github.com/$REPO.git"
    fi
  fi

  if [ "$DRY_RUN" = 1 ]; then
    echo "  (dry-run) subiria:"
    if git -C "$LOJA_DIR" rev-parse --git-dir >/dev/null 2>&1; then
      git -C "$LOJA_DIR" add -An 2>/dev/null | head -20
    else
      ( cd "$LOJA_DIR" && find . -type f \
          ! -name '.env' ! -name '*.pem' ! -name '*.key' ! -name '*.p12' \
          ! -name '*.zip' ! -path './sessions/*' ! -path './.venv/*' \
          ! -path './.git/*' 2>/dev/null | head -20 )
    fi
    echo "  (dry-run) fim — nada foi alterado."
    return 0
  fi

  git -C "$LOJA_DIR" add -A
  if git -C "$LOJA_DIR" diff --cached --quiet; then
    echo "  ✓ nada a sincronizar (estado já versionado)"
    git -C "$LOJA_DIR" push -q origin HEAD 2>/dev/null || true
    return 0
  fi
  git -C "$LOJA_DIR" -c user.name="DROPFOOD sync" -c user.email="dropfood@localhost" \
    commit -q -m "sync $(date +%Y-%m-%d) — operação da loja"
  git -C "$LOJA_DIR" push -q -u origin HEAD
  echo "  ✓ sincronizado em $(date +%H:%M:%S)"
}

[ $# -gt 0 ] || set -- --sync
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --connect) MODE="connect" ;;
    --sync)    MODE="sync" ;;
    --repo)    MODE="repo" ;;
    --cron)    MODE="cron" ;;
    --help|-h) usage ;;
    *)
      case "$MODE" in
        repo) REPO="$arg"; MODE="sync" ;;
        connect) CONNECT_NAME="$arg" ;;
        cron)
          LINE="0 19 * * * $HERMES_HOME/dropfood/scripts/backup_loja.sh --sync"
          ( crontab -l 2>/dev/null | grep -v "backup_loja.sh" ; echo "$LINE" ) | crontab -
          echo "✓ cron diário 19h instalado (remova com: crontab -e)"
          exit 0
          ;;
        *) echo "! argumento desconhecido: $arg (--help)" >&2; exit 1 ;;
      esac
      ;;
  esac
done

case "$MODE" in
  connect) connect "${CONNECT_NAME:-Minha Loja}" ;;
  sync)    sync ;;
esac