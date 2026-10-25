# Contribuindo para o DROPFOOD Agent

Obrigado por querer ajudar. Este produto é MIT e feito para donos de mercado
brasileiro — mantenha esse espírito.

## Regras que valem para tudo

1. **Nunca inclua dado real de loja no repo.** Este repositório é 100%
   sanitizado. CNPJ, CPF, telefone, endereço real, nome de cliente, sessão de
   portal: nada entra. O CI (`sanitize.yml`) bloqueia push/PR — rode o mesmo
   grep antes de commitar:
   ```bash
   grep -rIniE "NOME|ENDERECO|BAIRRO" . --exclude-dir=.git --exclude-dir=core
   ```
   (substitua pelos padrões reais que o CI usa — ver `sanitize.yml`.)
2. **Exemplos usam loja fictícia** ("Adega do Seu João"), nunca a real.
3. **PT-BR** no código, docs e mensagens (o produto fala português).
4. **Dinheiro com vírgula** em texto (R$ 14,90).
5. **Login do portal iFood é manual, 1x, pelo dono** — o produto nunca pede,
   guarda ou digita senha. Automação de login = risco de ban = rejeitado em
   review.
6. **Mecânica no produto, dado no perfil**: o código lê a loja do
   `config.yaml`/instância (`~/.hermes/loja/<id>/`), nunca hard-coded.
7. **core/ é upstream pinado** (NousResearch/hermes-agent, `UPSTREAM.txt`) —
   não se edita. Mudança de produto vive na camada fora de `core/`.

## Fluxo

1. Fork + branch `feat/<nome>`.
2. Testes: `python3 tests/test_motor.py` (loja demo fictícia).
3. Sanitize local (regra 1) antes do push.
4. PR contra `main` — o CI roda sanitize + testes. Título em PT-BR curto.

## Onde mexer

| Área | Pasta |
|---|---|
| Operação (skill/scripts do dono de loja) | `skills/dropfood-ops/`, `scripts/` |
| Radar de vitrine (ifood-sdk) | `scripts/sdk/`, `docs/IFOOD-SDK.md` |
| Design system / skin | `design/`, `skins/` |
| Bots (SOULs neutros) | `bots/templates/` |
| Instalação/wizard | `install.sh`, `scripts/wizard.py` |

Dúvida? Abra uma issue — comunidade não tem SLA, responde quem puder.
