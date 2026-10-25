# FAQ — DROPFOOD Agent

## O que é o DROPFOOD?

Um agente de operação para donos de loja no iFood Mercado. Ele é um **fork do
Hermes Agent** (NousResearch, MIT) modificado o mínimo para a operação: radar
de preços, catálogo espelhado com o fornecedor, time de bots em PT-BR e a UI
em português — mas reaproveitando 100% do que o Hermes já entrega (bot mode,
kanban, cron, MCP, skins, backup).

## Preciso saber programar?

Não. O install.sh aplica a camada do produto e o `wizard.py` cria o perfil da
sua loja com perguntas (nome, cidade, modelo, fornecedor, markup). O operador
(bot) conversa em português e roda o radar/espelho por comando de texto.

## O DROPFOOD pede a senha do meu portal iFood?

**Nunca.** O login no portal é manual, uma única vez, pelo dono (regra de
ouro do produto). O DROPFOOD observa a sessão com um health check
(`portal_monitor.py`) e avisa quando ela cai — quem reloga é você. Isso
protege sua conta de automação agressiva (risco de bloqueio).

## O radar de vitrine (ifood-sdk) é obrigatório?

Não, é opcional. Sem ele o radar usa o que está no catálogo/fornecedor. Com
`./install.sh --com-sdk` (Python 3.14+) o produto compara também o preço de
vitrine dos concorrentes via ifood-sdk — o OTP é manual do dono (1x), e só
leituras são automáticas.

## Meus dados vão para o repositório?

Não. Este repositório é 100% sanitizado (CI bloqueia push com dados reais).
Seus dados de operação ficam no seu computador em `~/.hermes/loja/<id>/`, e o
backup (camada D6) vai para um repositório GitHub **privado** seu.

## E se o iFood mudar o portal e quebrar algo?

O produto é desenhado para mitigar (cadência, login manual, health check),
mas sem garantia — o iFood muda o fluxo quando quiser (OTP, PerimeterX). O
código é MIT: a comunidade ajusta.

## Quanto custa?

O DROPFOOD é open source (MIT) — o código é grátis. Serviços opcionais
(atendimento, treinamento, marketplace de adaptadores) são separados e não
travam quem não paga.

## Dá pra usar com loja de outro marketplace?

Hoje o alvo é iFood Mercado. O design de adaptadores (fontes de dados) foi
feito para crescer — veja o roadmap no repo (docs/ARQUITETURA.md).

## Onde reporto bug / peço ajuda?

Issues no repositório (veja CONTRIBUTING.md para regras e SECURITY.md para
vulnerabilidades). Projeto comunitário — sem SLA, mas todo reporte legítimo
é tratado.
