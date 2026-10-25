# ESTADO-DA-ARTE — operação de loja iFood Mercado (conhecimento embutido)

> F3 do plano: conhecimento genérico de operação que o produto embute, para
> os bots (b1 estratégia, b2 radar, b6 revisão, b7 controle, operador)
> decidirem melhor. Nenhum dado real de loja — tudo aqui é público e
> neutralizado ({{loja.*}}). Fontes: auditoria de campo 25/10 + docs de
> suporte do iFood (parceiros).

## 1. Modelo de negócio da loja-reseller

- O dono abre uma loja no iFood Mercado **sem estoque próprio**: o
  fornecedor local (atacadista do bairro) é quem segura a mercadoria.
- Fluxo: cliente compra na vitrine → loja compra do fornecedor (sob
  demanda) → entrega → iFood repassa o valor em ~7 dias.
- **A margem vive no markup entre o preço do fornecedor e o preço de
  venda.** Markup típico 30–50% cobre: custo do produto, taxa da
  plataforma, entrega e perda. Markup baixo demais = prejuízo disfarçado
  de movimento.

## 2. Radar de preços (regras de decisão)

- **Faixas por categoria** (bom/ok/caro) são relativas à margem da loja,
  não ao preço absoluto: um item caro na vitrine pode ser lucrativo se o
  markup aguenta.
- Decisões do radar:
  - `SOBE` — preço atual abaixo da faixa bom (margem apertando ou
    já negativa): subir até a faixa.
  - `DESCE` — preço atual acima da faixa ok e concorrência menor:
    descer para manter volume (a regra de ouro: ajuste no portal é
    SEMPRE do dono; o radar propõe).
  - `MANTEM` — dentro da faixa.
  - `ALERTA` — margem negativa ou item sumindo da vitrine do fornecedor.
- Preço de **vitrine** (o que o consumidor vê) ≠ preço de **venda** na
  plataforma em alguns fluxos de promoção — comparar sempre o mesmo campo.

## 3. Portal do parceiro (iFood)

- Login **manual do dono, 1x** (regra de ouro do produto): nunca
  automatizar credencial. A sessão do portal cai sozinha (tempo, troca de
  rede, anti-fraude) — o produto MONITORA (`portal_monitor.py`) e avisa,
  nunca re-loga.
- Cadência de leitura: ciclos espaçados (radar 7h), nada de varredura em
  loop; o portal tem proteções contra automação (PerimeterX etc.).
- Se o portal bloquear a conta: parar TODA automação, esperar o dono
  resolver manualmente (documentado no anti-bloqueio).

## 4. Fornecedor e catálogo espelhado

- O espelho (`espelho.py`) compara o catálogo da loja com a disponibilidade
  do fornecedor:
  - item sem estoque no fornecedor → `TIRA_DO_AR` (evita cancelamento +
    nota negativa na loja);
  - item voltou → `VOLTA_AO_AR` (propor ao dono).
- Aplicar mudança no portal é passo explícito do dono — nunca automático.

## 5. Entrega e experiência (o que derruba nota)

- Atraso > tempo prometido é a principal causa de nota baixa no iFood.
- Ofertar item sem estoque (não espelhado) = cancelamento = perda dupla
  (cliente + ranking da loja).
- Quando o fornecedor atrasa, a decisão correta é tirar do ar o item
  afetado ANTES do pedido, não depois.

## 6. Custo de oportunidade dos bots

- b1 (estratégia) define faixas e políticas de preço por categoria.
- b2 (radar) executa o ciclo e propõe movimentos.
- b6 (revisão) confere as propostas contra as regras antes do dono ver.
- b7 (controle) acompanha execução e saúde (portal, backup, cadência).
- O operador coordena e reporta ao dono — o dono decide, sempre.

## 7. Limites honestos (não validado)

- Evolução de nota/ranking da loja e impacto de promoções NÃO têm modelo
  validado neste estado da arte — medir por observação, não prometer.
- Tempo real de repasse (~7 dias) e taxas exatas variam por contrato —
  confirmar com o suporte do iFood antes de decisão de precificação.
