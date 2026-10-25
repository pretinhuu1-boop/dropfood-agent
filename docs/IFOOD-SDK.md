# Radar de vitrine via ifood-sdk (opcional)

O DROPFOOD pode comparar o preço da vitrine (o que o consumidor vê) sem
scraping de DOM, usando o cliente **ifood-sdk** (MIT, não oficial, login OTP
da própria conta do dono — regra de ouro: nunca senha, OTP é manual).

## O que o SDK expõe (auditoria 25/10 — 26 endpoints medidos)

| Recurso | Uso no DROPFOOD |
|---|---|
| `merchants.items(id, lat, lng)` | Preço de vitrine por concorrente (fora do PerimeterX; o catálogo agrupado é bloqueado) |
| `merchants.get(id)` | Ficha do concorrente (marketplace host, sem auth) |
| `orders.recent/get/events/reorder` | Benchmark de experiência: timeline aceite→entrega (1 pedido de teste/mês, com gate) |
| `carts.build/set_payment/checkout` | Checkout Pix controlado (F3, com gate — writes exigem sessão fresca ~40 min) |
| `vouchers.list` | Cupons ativos da conta (insumo de pesquisa) |
| `locations.search/reverse` | Geocodificação/geo tático (densidade de concorrentes por bairro) |
| MCP server nativo | Plugável como tool MCP em qualquer Hermes |

Limites medidos pelo autor: GETs aguentam sessão de minutos a ~40 min como
escrita; renovação = re-OTP manual do dono; busca de cardápio e catálogo
agrupado ficam atrás de PerimeterX/`EdgeBlocked` (não usar).

> ⚠️ **Estado real (auditoria de integração, verificado):** F0 **consertado e
> funcionando** (era esqueleto quebrado — dependência não instalada, argparse
> com subcomandos inválidos, path apontando pro H1). F1/F2/F3 **pendentes** —
> ver "Fases" abaixo.

## Dependência (1x, opcional)

```bash
./install.sh --com-sdk    # cria ~/.hermes/dropfood/venv com pyyaml + ifood-sdk
                          # (exige Python 3.14+; sem ele, radar de vitrine desligado)
```

> Python é o runtime do Hermes (3.14+). O install.sh procura `python3.14`,
> `python3.13`, `python3.12` ou `python3` com `>=3.14` — na dúvida: `./install.sh --com-sdk`
> e veja a mensagem.

## Fases

- **F0 ✅ (verificado)**: `f0_paridade.py` — fluxo completo de leitura:
  1. `f0_paridade.py --set-phone '+5511...'` — salva telefone no perfil privado
     (`~/.hermes/loja/<id>/ifood_sdk_cfg.json`); `localizacao.lat/lng` no
     `config.yaml` da loja;
  2. `f0_paridade.py --login` — dispara OTP no WhatsApp do dono;
  3. `f0_paridade.py --coletar < out.txt` — verifica, descobre os
     merchant_ids pelos pedidos recentes (ou `--ids id1,id2` explícito), puxa
     `merchants.items` de N concorrentes e grava
     `~/.hermes/loja/<id>/vitrine.json` — formato que o `radar_precos.py`
     já consome (`"vitrine": [{nome, preco, loja}, ...]`).
  Só leituras. Roda local; o JSON é dado da loja (privado).
- **F1 ⏳ (pendente)**: radar 7h via SDK (GETs) com fallback de scraping;
  aviso ao dono quando precisar re-OTP. Hoje o dono roda o radar no chat
  ("roda o radar") ou agenda o cron; quando `vitrine.json` existir, o
  `radar_precos.py` já usa na comparação com `radar.vitrine.sdk: true`.
- **F2 ⏳ (parcial)**: SDK como MCP server no Hermes — config de exemplo no
  `config.yaml.example`; falta ativar no perfil real (OTP 1x do dono) + geo
  tático no B1.
- **F3 ⏳ (pendente, gate do dono)**: 1 pedido de benchmark/mês do principal
  concorrente (cart + checkout Pix + delivery_code), recibo documentado.

## Config

```yaml
localizacao:
  lat: -23.5505              # usada pelo radar de vitrine (ifood-sdk)
  lng: -46.6333
radar:
  vitrine:
    sdk: false                # true = radar compara com vitrine.json (ifood-sdk)
    concorrentes: []          # merchant_ids opcionais
```

Telefone e sessão ficam no perfil privado da loja (`~/.hermes/loja/<id>/`),
nunca no repo. Ver `scripts/sdk/f0_paridade.py`.
