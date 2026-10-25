# Perfil da loja (config.yaml)

Todo o DROPFOOD lê a identidade da loja de UM arquivo:
`~/.hermes/loja/config.yaml` — nunca do repositório.

## Campos

### loja
| campo | tipo | descrição |
|---|---|---|
| `nome` | string | nome exibido nos bots/relatórios |
| `cidade` / `regiao` | string | usados pelo radar de concorrência |
| `modelo` | `reseller` \| `dono` | reseller = sem estoque, compra sob demanda; dono = estoque físico próprio |

### fornecedor (modelo reseller)
| campo | tipo | descrição |
|---|---|---|
| `nome` | string | atacadista local |
| `markup` | float | margem sobre o atacado. Referência: 0.49 (49%) cobre comissão do iFood (6–23% + 3,5%) e sobra lucro |
| `pedido_minimo` | number | R$ mínimo (0 = sem mínimo) |
| `prazo_entrega_h` | number | prazo típico em horas (define o SLA de despacho) |

### radar
| campo | tipo | descrição |
|---|---|---|
| `frequencia_horas` | number | ciclo do radar de preços (padrão 7h) |
| `concorrentes` | list | nomes/links das lojas a comparar |
| `faixas` | list | faixas bom/ok/caro por categoria — embasam MANTEM/SOBE/DESCE/ALERTA |
| `vitrine.sdk` | bool | usa ifood-sdk para preço de vitrine (OTP do dono, 1x manual) |
| `vitrine.concorrentes` | list | merchant_ids opcionais; vazio = descobre dos pedidos recentes |

### localizacao (radar de vitrine / ifood-sdk)
| campo | tipo | descrição |
|---|---|---|
| `lat` / `lng` | float | coordenadas da loja — usadas pelo ifood-sdk (`--coletar`) |

### portal
| campo | tipo | descrição |
|---|---|---|
| `login` | `manual` (fixo) | regra de ouro — nunca automatizado |
| `email` | string | referência local, nunca enviado |

### runtime
| campo | tipo | descrição |
|---|---|---|
| `ollama_url` | string | endpoint da API Ollama |
| `motor` / `leve` / `qualidade` | string | modelos por peso (base: lfm2.5:8b / qwen3.5:2b / qwen3.5:4b) |

### alertas
| campo | tipo | descrição |
|---|---|---|
| `canal` | `terminal` \| `whatsapp` | onde chegam os alertas (whatsapp: em breve) |
| `horario` | HH:MM | briefing diário |

### backup (camada D6 — GitHub privado do dono)
| campo | tipo | descrição |
|---|---|---|
| `github` | bool | liga o sync (requer `gh auth login` 1x — device flow, token no keyring) |
| `repo` | string | repo privado de destino; vazio = cria `dropfood-loja-<slug>` automático |
| `frequencia` | `diario` \| `manual` | diario instala cron 19h; manual = B7/CONTROLE sincroniza no fim do ciclo |

O que sobe: config, radar, notas, catálogo (texto pequeno). O que nunca sobe:
tokens, cookies de sessão do portal, senhas, zips (zips do ambiente vão por
GitHub Release — `--release`, rotate 3). Design completo:
`docs/BACKUP-GITHUB.md`.