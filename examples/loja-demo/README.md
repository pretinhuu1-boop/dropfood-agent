# Loja demo — "Adega do Seu João" (100% fictícia)

Exemplo de instância do DROPFOOD para testes e desenvolvimento. Nenhum
dado real — a loja, o fornecedor e a concorrência são inventados.

## Uso

```bash
HERMES_HOME=examples/loja-demo
python3 ~/.hermes/dropfood/scripts/wizard.py --force   # se quiser regenerar o config
HERMES_HOME=examples/loja-demo python3 scripts/radar_precos.py   # do repo
HERMES_HOME=examples/loja-demo python3 scripts/espelho.py
```

A estrutura espelha o que o install.sh cria em `~/.hermes/`:

```
loja/
  config.yaml          perfil da loja (modelo reseller, markup 49%)
  adegadoseujoao/
    catalogo.json      3 itens: Cerveja, Refrigerante, Salgadinho
    fornecedor.json    disponibilidade do atacadista
    vitrine.json       preços de vitrine via ifood-sdk (F0)
    radar.json         saída do radar_precos.py (gerada)
    espelho.json       saída do espelho.py (gerada)
```

## O que os dados validam

- Cerveja Lata 350ml: vitrine do concorrente R$ 3,49 < venda R$ 3,99 → radar
  sugere **DESCE** para R$ 3,29 (margem 47%)
- Refrigerante 2L: **indisponível no fornecedor** → espelho **TIRA_DO_AR**
- Salgadinho 100g: margem 8,6% → **DESCE** (faixa ok)

## Testes

O mesmo material é usado por `tests/test_motor.py` (asserts automatizados).
