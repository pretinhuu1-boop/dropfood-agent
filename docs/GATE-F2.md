# Gate F2 — ciclo demo ponta a ponta (Adega do Seu João)

> F2 do plano: os bots de operação viram um ciclo completo em uma loja demo
> (100% fictícia). Nenhum dado real; login de portal não participa deste
> gate (o portal real é gate do dono, regra de ouro).

## O que o gate prova

1. `wizard.py` cria o perfil da loja a partir de perguntas (ou `config.yaml`
   pronto).
2. `radar_precos.py` lê catálogo + fornecedor (+ `vitrine.json` quando
   `radar.vitrine.sdk: true`), produz vereditos dentro das faixas.
3. `espelho.py` compara catálogo vs fornecedor e decide TIRA_DO_AR /
   VOLTA_AO_AR / MANTEM.
4. `portal_monitor.py` reporta estado sem login (graceful).
5. os bot templates (b1/b2/b6/b7/operador) existem e referenciam as
   ferramentas certas.

## Como rodar

```bash
HERMES_HOME=$PWD/examples/loja-demo \
  ~/.hermes/dropfood/venv/bin/python scripts/radar_precos.py
HERMES_HOME=$PWD/examples/loja-demo \
  ~/.hermes/dropfood/venv/bin/python scripts/espelho.py
HERMES_HOME=$PWD/examples/loja-demo \
  ~/.hermes/dropfood/venv/bin/python scripts/portal_monitor.py
python3 tests/test_motor.py   # mesmo fluxo, isolado, sem rede (CI)
```

## Resultado registrado (25/10, H2 fe68e196)

- radar: Cerveja Lata 350ml -> DESCE (vitrine 3,49) · Refrigerante 2L ->
  MANTEM · Salgadinho 100g -> DESCE (vitrine 2,99) — margens nas faixas.
- espelho: Refrigerante 2L -> TIRA_DO_AR (indisponível no fornecedor) ·
  demais MANTEM. "aplicar no portal = pedido explícito do dono".
- portal_monitor: `ok:false` sem sessão, sem quebrar (estado graceful).
- testes: 4/4 verdes no CI (job `test` do sanitize.yml).

## Pendências de F2 (gates do dono)

- Gate real de login/edição no portal (dono, 1x) — F5 beta.
- Decisão: operador como bot real de produção (b6 a decidir no produto).
