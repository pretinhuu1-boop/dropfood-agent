# Segurança — DROPFOOD Agent

## O que este produto faz (e o que não faz)

O DROPFOOD opera a **sua própria loja** no iFood Mercado usando a **sua**
sessão do portal. Não é ferramenta de scraping em massa, não toca contas de
terceiros e não automatiza login.

## Reportando uma vulnerabilidade

**Não abra issue pública para problemas de segurança.** Escreva para o
mantenedor via issue "security" privada ou contato do repo — resposta sem
prazo garantido (projeto comunitário), mas toda reporte legítimo é tratado.

Inclua: versão/commit afetado, passo a passo para reproduzir, impacto, e
sugestão de correção se tiver.

## Principais riscos e mitigação

| Risco | Mitigação |
|---|---|
| Vazamento de dado real de loja no repo | CI `sanitize.yml` (hard gate em push/PR) + regra de contribuição |
| Senha do portal iFood capturada | **Regra de ouro**: login manual do dono, 1x; o produto nunca pede/guarda senha; só observa a sessão (`portal_monitor.py`) |
| Conta consumidora iFood (ifood-sdk) | OTP manual do dono; sem write automatizado (F3 tem gate do dono); cadência de GETs moderada; sinais de bloqueio = parar |
| Segredos/tokens no repo | Gitignore local da pasta `loja/`; CI varre `api_key/secret/password/token` com 16+ chars |
| Execução de scripts maliciosos (addons) | Adaptadores de fonte são código aberto revisado no repo; instalar só o que você leu |

## Escopo de responsabilidade

- O código é MIT e "como está". Operar o portal com automação tem risco de
  bloqueio pela plataforma — o produto é desenhado para mitigar (cadência,
  login manual, health check), mas **quem opera é o dono da conta**, com a
  própria responsabilidade.
- Se o iFood mudar o fluxo (OTP, PerimeterX), integrações quebram — sem
  garantia de correção imediata.
