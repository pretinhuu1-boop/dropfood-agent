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

## Fases

- **F0** (validação): `--set-phone` → `--login` (OTP no WhatsApp do dono) →
  `--coletar` (código via stdin): puxa pedidos recentes (descobre os
  merchant_ids sem buscar), items de N concorrentes, grava JSON. Leitura
  pura. Roda local; o JSON é dado da loja (privado).
- **F1**: radar 7h via SDK (GETs) com fallback de scraping; aviso ao dono
  quando precisar re-OTP.
- **F2**: SDK como MCP server no Hermes (tools nativas pros bots) + geo
  tático no B1.
- **F3** (gate): 1 pedido de benchmark/mês do principal concorrente
  (cart + checkout Pix + delivery_code), recibo documentado.

## Config

```yaml
radar:
  vitrine:
    sdk: false                # true = usa ifood-sdk
    concorrentes: []          # merchant_ids opcionais
```

Telefone e lat/lng ficam no perfil privado da loja (`~/.hermes/loja/`),
nunca no repo. Ver `scripts/sdk/f0_paridade.py`.