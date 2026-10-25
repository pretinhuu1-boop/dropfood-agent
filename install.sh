#!/usr/bin/env bash
# DROPFOOD Agent — install.sh (camada do produto; o core é o fork em core/)
# Uso: ./install.sh
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "→ Instalando DROPFOOD em $HERMES_HOME"

# D1 — skin do produto
mkdir -p "$HERMES_HOME/skins"
cp "$REPO_DIR/skins/dropfood.yaml" "$HERMES_HOME/skins/dropfood.yaml"
echo "  ✓ skin dropfood.yaml"

# D2 — skill de operação (neutra)
mkdir -p "$HERMES_HOME/skills"
rm -rf "$HERMES_HOME/skills/dropfood-ops"
cp -R "$REPO_DIR/skills/dropfood-ops" "$HERMES_HOME/skills/"
echo "  ✓ skill dropfood-ops"

# D3 — templates de bots
mkdir -p "$HERMES_HOME/loja"
[ -f "$HERMES_HOME/loja/config.yaml" ] || cp "$REPO_DIR/config.yaml.example" "$HERMES_HOME/loja/config.yaml"
echo "  ✓ perfil de loja (config.yaml)"

# D1 + PT-BR — ativa via CLI do Hermes, se disponível
if command -v hermes >/dev/null 2>&1; then
  hermes config set display.skin dropfood >/dev/null 2>&1 && echo "  ✓ skin ativada (display.skin=dropfood)"
  hermes config set display.language pt >/dev/null 2>&1 && echo "  ✓ idioma PT-BR (display.language=pt)"
else
  echo "  ! CLI 'hermes' não achada — ative depois: hermes config set display.skin dropfood"
fi

# Scripts utilitários
mkdir -p "$HERMES_HOME/dropfood/scripts"
for s in "$REPO_DIR"/scripts/*.py "$REPO_DIR"/scripts/*.sh; do
  [ -f "$s" ] && cp "$s" "$HERMES_HOME/dropfood/scripts/" && echo "  ✓ script $(basename "$s")"
done

echo ""
echo "Pronto! Próximo passo:"
echo "  edite ~/.hermes/loja/config.yaml (nome da loja, fornecedor, markup)"
echo "  e reinicie o Hermes desktop para ver a skin DROPFOOD em PT-BR."