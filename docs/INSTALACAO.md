# Instalação

## Requisitos

- macOS 13+ ou Linux (x86_64/ARM64)
- O fork **já traz o Hermes** (`core/` pinado). Hoje (progresso da F4) o
  `install.sh` aplica a camada do produto sobre uma instalação Hermes local
  de desenvolvimento; na distribuição final o produto instala sozinho
  (standalone, wizard) — o dono de loja nunca instala o Hermes separado.
- [Ollama](https://ollama.com) + modelos locais (para os bots 100% offline):
  `ollama pull lfm2.5:8b qwen3.5:2b qwen3.5:4b`

## Passos

```bash
git clone https://github.com/pretinhuu1-boop/dropfood-agent.git
cd dropfood-agent
./install.sh
```

O install copia em `~/.hermes/`:
- `skins/dropfood.yaml` (+ ativa `display.skin=dropfood` e `display.language=pt`)
- `skills/dropfood-ops/` (skill de operação)
- `loja/config.yaml` (perfil da loja — a partir do exemplo)
- `dropfood/scripts/` (utilitários)

## Configuração da loja

Edite `~/.hermes/loja/config.yaml`:

```yaml
loja:
  nome: "Adega do Seu João"
  modelo: reseller           # ou: dono
fornecedor:
  nome: "Atacadão X"
  markup: 0.49
```

A persona dos bots, o radar e os alertas leem esse arquivo.

## Primeira subida

1. Reinicie o Hermes desktop → interface em PT-BR com a skin DROPFOOD.
2. Abra o portal do iFood **uma vez, manualmente, você** (regra de ouro) —
   o DROPFOOD usa a sessão já logada, nunca pede senha.
3. Rode o radar (precisa de catálogo gerado antes): `python3 ~/.hermes/dropfood/scripts/radar_precos.py`
   (ou peça no chat: "roda o radar").
4. O briefing diário chega no canal configurado (terminal por padrão).

## Atualização

```bash
cd dropfood-agent && git pull && ./install.sh
```

O upstream do Hermes **não** se atualiza por cima (é fork): `core/UPSTREAM.txt`
pina o commit; atualizar = re-snapshot + diff listável, nunca reimplementar o core.