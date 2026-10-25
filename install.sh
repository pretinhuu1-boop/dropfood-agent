#!/usr/bin/env bash
# DROPFOOD Agent — install.sh (camada do produto; o core é o fork em core/)
# Uso: ./install.sh [--com-sdk]
#   --com-sdk    instala também o venv do produto (pyyaml + ifood-sdk p/ radar
#                de vitrine — exige Python 3.14+; sem ele, o radar de vitrine
#                fica desligado, o resto funciona normal).
set -euo pipefail

HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COM_SDK=0
for a in "$@"; do
  [ "$a" = "--com-sdk" ] && COM_SDK=1
done

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

# D4 — desktop plugin do produto (runtime, zero patch no core)
if [ -d "$REPO_DIR/desktop-plugins/dropfood" ]; then
  mkdir -p "$HERMES_HOME/desktop-plugins"
  rm -rf "$HERMES_HOME/desktop-plugins/dropfood"
  cp -R "$REPO_DIR/desktop-plugins/dropfood" "$HERMES_HOME/desktop-plugins/"
  echo "  ✓ desktop plugin dropfood (\$HERMES_HOME/desktop-plugins/dropfood/plugin.js)"
fi

# F4 — core standalone: se a CLI hermes global não existe, monta o core do fork
# (o produto NÃO depende do Hermes instalado; o desktop do repo é o app).
if ! command -v hermes >/dev/null 2>&1; then
  echo "  · CLI 'hermes' global ausente — usando o core do fork (core/hermes)"
  PY=""
  for c in python3.14 python3.13 python3.12 python3; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
      PY="$(command -v "$c")"
      break
    fi
  done
  if [ -n "$PY" ] && [ -d "$REPO_DIR/core" ]; then
    "$PY" "$REPO_DIR/core/hermes" pm repair >/dev/null 2>&1 \
      && echo "  ✓ core montado (pm repair)" \
      || echo "  ! pm repair do core falhou — rode à mão: python3 core/hermes pm repair"
  else
    echo "  ! Python 3.10+ não encontrado para o core standalone"
  fi
fi

# D1 + PT-BR — ativa via CLI do Hermes (global ou core do fork)
if command -v hermes >/dev/null 2>&1; then
  hermes config set display.skin dropfood >/dev/null 2>&1 && echo "  ✓ skin ativada (display.skin=dropfood)"
  hermes config set display.language pt >/dev/null 2>&1 && echo "  ✓ idioma PT-BR (display.language=pt)"
elif [ -x "$REPO_DIR/core/hermes" ]; then
  "$REPO_DIR/core/hermes" config set display.skin dropfood >/dev/null 2>&1 && echo "  ✓ skin ativada via core (display.skin=dropfood)"
  "$REPO_DIR/core/hermes" config set display.language pt >/dev/null 2>&1 && echo "  ✓ idioma PT-BR via core (display.language=pt)"
else
  echo "  ! CLI 'hermes' não achada — ative depois: hermes config set display.skin dropfood"
fi

# Scripts utilitários
mkdir -p "$HERMES_HOME/dropfood/scripts"
for s in "$REPO_DIR"/scripts/*.py "$REPO_DIR"/scripts/*.sh; do
  [ -f "$s" ] && cp "$s" "$HERMES_HOME/dropfood/scripts/" && chmod +x "$HERMES_HOME/dropfood/scripts/$(basename "$s")" && echo "  ✓ script $(basename "$s")"
done
# SDK de vitrine (subpasta)
mkdir -p "$HERMES_HOME/dropfood/scripts/sdk"
for s in "$REPO_DIR"/scripts/sdk/*.py; do
  [ -f "$s" ] && cp "$s" "$HERMES_HOME/dropfood/scripts/sdk/" && chmod +x "$HERMES_HOME/dropfood/scripts/sdk/$(basename "$s")" && echo "  ✓ script sdk/$(basename "$s")"
done

# Venv do produto + ifood-sdk (opcional — radar de vitrine)
if [ "$COM_SDK" = "1" ]; then
  PY=""
  for c in python3.14 python3.13 python3.12 python3; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 14) else 1)' 2>/dev/null; then
      PY="$(command -v "$c")"
      break
    fi
  done
  if [ -z "$PY" ]; then
    echo "  ! Python 3.14+ não encontrado — radar de vitrine desligado. Instale o"
    echo "    python 3.14 e rode: ./install.sh --com-sdk"
  else
    VENV="$HERMES_HOME/dropfood/venv"
    if [ ! -x "$VENV/bin/python" ]; then
      "$PY" -m venv "$VENV"
    fi
    "$VENV/bin/python" -m pip install -q --upgrade pip >/dev/null 2>&1 || true
    "$VENV/bin/python" -m pip install -q "pyyaml" "ifood-sdk @ git+https://github.com/felipeadeildo/ifood-sdk" 2>/dev/null \
      && echo "  ✓ venv + ifood-sdk ($("$VENV/bin/python" -c 'import ifood; print("import OK")' 2>/dev/null || echo "pendente"))" \
      || echo "  ! falha ao instalar ifood-sdk (rede?) — radar de vitrine desligado; tente: pip install ifood-sdk"
  fi
else
  echo "  · radar de vitrine (ifood-sdk) NÃO instalado — para ativar: ./install.sh --com-sdk"
fi

echo ""
echo "Pronto! Próximo passo:"
echo "  edite ~/.hermes/loja/config.yaml (nome da loja, fornecedor, markup)"
echo "  e reinicie o Hermes desktop para ver a skin DROPFOOD em PT-BR."
