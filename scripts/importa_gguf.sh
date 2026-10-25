#!/bin/bash
# importa_gguf.sh — baixa os GGUFs dos candidatos que não estão no catálogo do
# Ollama (SmolLM3-3B, Spark-X2.6-4B, Spark-X2.5-1.7B, Bonsai-2-4B) e registra
# no Ollama local via `ollama create`. Store: /Volumes/Arquivo_iMac/ollama-models.
set -euo pipefail

OLLAMA_BIN="/Applications/Ollama.app/Contents/Resources/ollama"
export OLLAMA_MODELS="/Volumes/Arquivo_iMac/ollama-models"
GGUF_DIR="$OLLAMA_MODELS/gguf"
mkdir -p "$GGUF_DIR"

# nome_local|repo/path|arquivo
BAIXAR=(
  "smollm3-3b|https://huggingface.co/ggml-org/SmolLM3-3B-GGUF/resolve/main/SmolLM3-Q4_K_M.gguf"
  "spark-x2.6-4b|https://huggingface.co/XHToken/Spark-X2.6-4B-GGUF/resolve/main/Spark-X2.6-4B-Q4_K_M.gguf"
  "spark-x2.5-1.7b|https://huggingface.co/XHToken/Spark-X2.5-1.7B-GGUF/resolve/main/Spark-X2.5-1.7B-Q4_K_M.gguf"
  "bonsai2-4b|https://huggingface.co/prism-ml/Ternary-Bonsai-2-4B-gguf/resolve/main/Ternary-Bonsai-2-4B-Q2_0.gguf"
)

for item in "${BAIXAR[@]}"; do
  nome="${item%%|*}"
  url="${item#*|}"
  arq="$GGUF_DIR/$nome.gguf"
  echo "=== $nome"
  if [[ ! -s "$arq" ]]; then
    echo "  download: $url"
    curl -L --fail --progress-bar -o "$arq" "$url"
  else
    echo "  já baixado ($(du -h "$arq" | cut -f1))"
  fi
  if ! "$OLLAMA_BIN" list | grep -q "^$nome"; then
    printf 'FROM %s\nTEMPLATE """{{ .Prompt }}"""\n' "$arq" > "$GGUF_DIR/$nome.Modelfile"
    "$OLLAMA_BIN" create "$nome" -f "$GGUF_DIR/$nome.Modelfile"
  fi
  echo "  -> registrado: $nome"
done
echo "FIM: $(date +%H:%M:%S)"
"$OLLAMA_BIN" list