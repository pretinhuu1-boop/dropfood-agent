# Instalação

## Requisitos

- macOS 13+ ou Linux (x86_64/ARM64)
- [Hermes Agent](https://hermes-agent.nousresearch.com/docs) instalado e rodando
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
3. Rode o radar: `hermes dropfood radar` (ou peça no chat: "roda o radar").
4. O briefing diário chega no canal configurado (terminal por padrão).

## Atualização

```bash
cd dropfood-agent && git pull && ./install.sh
```

O Hermes core atualiza separado: `hermes update`.