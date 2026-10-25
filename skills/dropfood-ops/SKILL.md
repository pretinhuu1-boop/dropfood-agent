---
name: dropfood-ops
description: Operação diária de loja no iFood Mercado — radar de preços, catálogo espelhado do fornecedor, alertas de falta, briefing. Use para operar a loja do perfil (NUNCA para automatizar login).
version: 0.1.0
metadata:
  hermes:
    category: ifood-mercado-operador
    tags: [ifood, mercado, reseller, radar, catálogo, portal]
---

# dropfood-ops — operação da loja no iFood Mercado

Identidade da loja: **`~/.hermes/loja/config.yaml`** (nome, modelo, fornecedor,
markup, radar). Nunca hard-code dados de loja neste skill ou nos scripts.

## REGRA DE OURO (contrato, não negocia)

**Login no portal iFood é manual, UMA vez, pelo dono.** O agente nunca pede,
guarda ou digita senha (nem ao dono, nem à comunidade). Automação de login =
risco real de ban da loja. O agente usa a sessão já aberta no navegador.

## Backup e retomada (regra D6 — GitHub pessoal do dono)

- Os dados da operação (`config.yaml`, radar, notas, catálogo) vivem em
  `~/.hermes/loja/<id>/` e sincronizam para o **repo privado do próprio dono**
  (`scripts/backup_loja.sh` — camada D6, docs/BACKUP-GITHUB.md).
- **Sobe**: config, radar/*.json, notas/*.md, catálogo. **NUNCA sobe**: `.env`,
  cookies/sessões do portal, senhas, zips (gitignore local cuida).
- No fim de cada ciclo de operação, o B7/CONTROLE garante o sync e reporta o
  estado. Máquina nova: `gh auth login` + clone do repo privado em
  `~/.hermes/loja/<id>` + `hermes import` (backup do ambiente é nativo do core).

## Operação

1. **Radar de preços** (ciclo `radar.frequencia_horas`, padrão 7h):
   - comparar preço do fornecedor vs. concorrentes (`radar.concorrentes`);
   - classificar por faixa (`radar.faixas`): MANTEM / SOBE / DESCE / ALERTA;
   - preço novo = reaplicar `fornecedor.markup` (padrão 0.49);
   - ALERTA (produto sumiu do fornecedor) → tirar do ar no catálogo e avisar.
2. **Catálogo espelhado**: o catálogo segue o fornecedor. O que faltou no
   atacado sai do ar (evita cancelamento e nota baixa). Reposição voltou? Volta
   ao ar no preço atualizado.
3. **Briefing diário** no canal configurado (`alertas.canal`, `alertas.horario`):
   resumo do ciclo: o que sobou/desceu/trocou, faltas, pedido de reposição
   sugerido, ticket médio e meta do dia.
4. **SLA de despacho**: `fornecedor.prazo_entrega_h` define o compromisso com o
   cliente; pedido que estoura o SLA vira alerta.

## Ferramentas do produto (scripts em ~/.hermes/dropfood/scripts/)

- `wizard.py` — cria o perfil da loja guiado (config.yaml a partir do template)
- `radar_precos.py` — ciclo completo de comparação e classificação (config da loja);
  com `radar.vitrine.sdk: true` compara também com `vitrine.json` (ifood-sdk)
- `espelho.py` — sincroniza catálogo com o fornecedor (tira/volta do ar)
- `portal_monitor.py` — saúde da sessão do portal (estado em `~/.hermes/loja/<id>/`)
- `notas_para_dataset.py` — notas de operação → JSONL de treino (para o treinador)
- `sdk/f0_paridade.py` — radar de vitrine via ifood-sdk (OTP manual do dono;
  requer `install.sh --com-sdk`; ver `docs/IFOOD-SDK.md`)

## Regras de escrita

- PT-BR sempre; dinheiro com vírgula (R$ 14,90); decisão com número e fonte.
- Proibido em docs/saídas: nome real de loja de terceiros como exemplo (use
  "Adega do Seu João"); CNPJ real; e-mail real.