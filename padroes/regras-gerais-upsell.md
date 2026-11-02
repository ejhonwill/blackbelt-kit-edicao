---
name: regras-gerais-upsell
description: "Regras do Jhon para todo upsell (frasco, b-roll, cards, legenda, preço, gifts, fluxo de aprovação) consolidadas das revisões do Upsell #1 EreVanton em 30/10/2026"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1d3630f8-da34-4dbd-ba25-a12d6f7c1db9
  modified: 2026-11-01T19:55:47.848Z
---

Regras que o Jhon consolidou em 30/10/2026 depois das revisões do Upsell #1 EreVanton. Valem para TODO upsell.

**Fluxo:** formato 9:16 1080×1920, salvo pedido diferente (o EreVanton foi 4:3 porque o briefing do copy pediu). A aprovação é pela prévia aberta no HyperFrames, nunca pelo Frame.io, e o render só vem depois. Antes de gerar, reaproveitar b-roll de jobs anteriores do produto. O IA Creator (Agência Samurai) audita cada lote e a prévia.

**Frasco:**
- Rótulo oficial dos mockups. Frasco branco, genérico ou de outra marca reprova, inclusive em fábrica.
- Sempre em pé, com o rótulo de frente. Deitado reprova.
- ~10 cm, cabe na palma. Tamanho único em todas as telas.
- Rótulo fosco que pega a luz do ambiente, com sombra dos dedos. Conferir letra por letra, incluindo o número de cápsulas.
- **Cena da entrega = caminhão UPS** (Jhon, 01/11, vale para TODO upsell): no trecho que mostra o pedido saindo/chegando, o caminhão é o da UPS — carroceria marrom-escura com o escudo dourado "ups" na lateral, entregador de uniforme marrom; as caixas continuam com a logo do produto. Referência: `~/.claude/skills/upsell-premium-916/references/ref_entrega_ups/ups_caminhao_logo_ref.png` (antes, sem logo: `cinnashield_entrega_sem_logo_antes.png`). Gerar a imagem já com o escudo (GPT Image/Nano Banana com a ref) e conferir a grafia "ups"; não colar logo por cima. Obs.: é marca registrada de terceiro — decisão do Jhon ciente do risco; se a copy/compliance de algum produto pedir sem logo, perguntar.
- Não inventar embalagem fora dos mockups. Caixa de envio leva a logo do produto no padrão premium (logo impressa de verdade, caixa limpa e bem acabada) — o Jhon confirmou em 31/10, mesmo com copy pedindo caixa lisa.
- A quantidade falada aparece na tela, sincronizada com a palavra.

**B-roll:**
- **Nada de b-roll estilo Pixar 3D/cartoon** (Jhon, 31/10). Só real ou IA fotorrealista; 3D anatômico médico realista ok.
- **Orgânico primeiro, IA por último** (Jhon, 31/10): para cada plano, buscar antes footage real (acervo do produto/DTC, jobs anteriores, banco de vídeo/stock, TikTok/IG) e só gerar por IA o que não existir — IA erra rótulo e tem cara de IA.
- O insert demonstra a fala. Dor concreta, do dia a dia.
- 3D explica (progressão, antes e depois, mês 1→2→3). Para ereção, 3D anatômico translúcido e médico.
- Mesmo rosto em todos os planos. Figurino muda a cada momento/dia da história e só se repete dentro do mesmo momento contínuo (regra nova do Jhon, 01/11; planejar roupa por cena no storyboard e no prompt; ver `upsell-premium-916/references/REGRAS_JHON_3010.md`).
- Bloco ANTI-STOCK nos prompts.

**Cards e legenda:**
- Proibido texto solto sobre avatar borrado. Todo destaque precisa de imagem ou 3D que diga a mesma coisa.
- Interface de pedido é mão real segurando celular, nunca celular desenhado.
- Legenda nunca para (pula só as palavras da headline). Headline em cima, legenda embaixo, nenhuma cobre rosto.
- **Número na legenda sempre em algarismo** (Jhon, 01/11): a locução pode falar por extenso ("nineteen a bottle… one twenty-nine total"), mas a legenda mostra "$19 a bottle… $129 total". Vale para preço, total, quantidade de frascos, dias, porcentagem e idade. O TTS recebe o texto falado; o `_alin.json` e a legenda usam o texto com algarismos (alinhar pelo tempo das palavras).
- Lettering atrás do avatar opaco e nunca cortado pela cabeça.
- Transições de luz e light leak. Ritmo bbkatana.

**Preço (padrão ArtiBrex 335_DA):** bancada real com luz natural, frascos em pé e mão pegando um. Card branco ou translúcido arredondado, com "$X/bottle" grande e o total embaixo. Legenda em faixa escura translúcida. Cor do card na identidade do produto. Não copiar caixa de kit que o produto não tem.

**Kit premium (aprovado 30/10, EreVanton):** caixa de kit aberta com frascos em nichos mais frascos soltos em pé na frente, bancada de mármore, sol lateral e cozinha clara desfocada. Referência em `~/Documents/01_Producao/_SAMURAI/erevanton-up1/referencias/kit_padrao_premium_jhon.png`. O total visível bate com a versão, e o "N BOTTLES" na caixa só aparece se bater.

**Gifts:** cada um ganha imagem ou vídeo próprio. Video lesson é personagem assistindo no tablet ou celular. E-book é mockup com o nome na capa. Texto de capa ou tela entra em HTML, nunca gerado pela IA. "GIFT #N" e o valor riscado virando FREE são lettering integrado. Tom sugestivo, nada explícito.

**CTA:** botão no padrão do upsell validado.

**Oferta:** conferir cápsulas × dose × dias contra o rótulo. Se não fechar, a fala segue a copy, a conta fica fora da tela e o copywriter é avisado.

**Why:** reprovações reais do Jhon no EreVanton (frasco deitado, rótulo CGI, logo em caixa de envio, frasco gigante, kit fake).
**How to apply:** checklist obrigatório antes de mostrar qualquer prévia de upsell. Complementa [[upsell-cor-psicologia-vence-referencia]] e [[anti-cara-de-ia-em-imagem]].

**Frascos lado a lado (31/10, 346_PG):** no trecho "how many bottles / mês 1-2-3", o Jhon pede os frascos lado a lado na ideia do ArtiBrex: split de 3 painéis verticais com fio branco e rótulo pequeno (cena 33 de `artibrex-up1-335da/edicao/build_antes_DEF.py`, CSS `.split`). Conferir na prévia antes do render.
**Referências visuais (31/10, 346_PG):** o split chapado foi reprovado ("estilo de edição muito fraco"). Cena de produto/frascos/kit segue ArtiBrex + CogniClear 349_BM + CinnaShield Up1 (`~/Documents/01_Producao/_SAMURAI/`); lettering segue o CogniClear 349_BM; frasco de cápsula tem o TAMANHO do frasco do ArtiBrex (padrão da casa).
**Tamanho por tipo de frasco (31/10):** frasco de GOTAS (conta-gotas, ex. CardioFlush, CogniClear) segue o padrão de tamanho de gotas já validado; frasco de CÁPSULA (ex. NightRenew) segue o padrão de cápsula validado do ArtiBrex 335_DA.
**Reprovado 2× em 31/10 (346_PG):** frascos PNG em painéis/fundo azul chapado e card "100" sobre expert desfocado = "zero padrão visual". O lado a lado do ArtiBrex são 3 FOTOS REAIS (café/almoço/jantar); lettering CogniClear = título condensado branco + linha colorida sobre imagem full-bleed. Pranchas em `~/Documents/01_Producao/_SAMURAI/cardioflush-up2-346pg/referencias_padrao/`; mandar a prancha pro agente em vez de descrever.
**Frasco direto na imagem (Jhon 31/10):** cena de produto = UMA imagem gerada já com os frascos + rótulo/logo dentro (GPT Image/Nano Banana com o rótulo oficial de referência), animada no Kling se for b-roll. Não colar PNG de frasco por cima de cena vazia; se a grafia sair errada, regerar ou corrigir só a palavra.

**Personagem da história ≠ expert (01/11/2026):** quando o expert não é quem vive a história, o b-roll da história usa um personagem próprio. O rosto é diferente do expert e fica o mesmo em todas as cenas, e o figurino muda a cada momento. O foco é b-roll orgânico com pessoa coerente com esse personagem; IA só no que faltar. O rosto do expert nunca aparece na história de outra pessoa. Gravado também em REGRAS_JHON_3010.md.
**Why:** o Jhon pediu no Upsell 2 Oculume (347_PG) e mandou deixar como regra.
**How to apply:** no plano de todo upsell, VSL ou AD com história, marcar em cada b-roll quem aparece e se a cena é orgânica ou gerada.
**Tela de celular/tablet (01/11, 346_PG):** tela desenhada em HTML colada sobre mão/tablet foi reprovada como "bugado". Gerar a cena já com o conteúdo na tela (oferta, capa do guia) e animar; lettering por fora da tela.
**Cena de frasco = padrão ArtiBrex (01/11):** momento real de uso à mesa (1 frasco, mão com cápsula, prato de café/almoço/jantar, mesma mesa mudando a luz, rótulo pequeno com ícone, legenda em faixa), não fileira de catálogo com título grande. Ficha: `cardioflush-up2-346pg/referencias_padrao/ficha_frascos_artibrex_x_nosso.jpg`; ref ArtiBrex V2 Preço A 182/188/434 s.
**Tela de preço validada (01/11) — padrão Diogo, SEMPRE assim:** kit premium aberto + frascos soltos na frente (mármore, cozinha com sol de manhã), banner inclinado "Triple-Dose Kit" no topo, card "$X /bottle" em paralelogramo com cheio riscado em vermelho + tarja "$Y TOTAL", sem legenda na cena; mesmo cenário de fundo para o selo de garantia. **Molduras (banner, card, tarja) sempre na cor da marca do produto** (o azul-escuro do exemplo é do EreVanton; CinnaShield = canela/dourado). Substitui o card branco do padrão ArtiBrex acima. Claims de tratamento na caixa ("Restores Insulin Sensitivity") trocar por claim de rótulo seguro e avisar o Jhon. Exemplo: `cardioflush-up2-346pg/referencias_padrao/padrao_price_validado_erevanton.png` (o "R$33" do exemplo é erro; usar $).

- **Timeline antes do render (01/11/2026, Jhon):** antes de QUALQUER render, abrir APENAS a timeline (prévia do HyperFrames no navegador) para o Jhon aprovar o visual. Sem o OK dele na prévia, não pedir a vez nem renderizar. Motivo: evitar retrabalho de render.

- **Supervisor-Upsell obrigatório (01/11/2026, Jhon):** todo upsell passa pelo agente `supervisor-upsell` (~/.claude/agents/supervisor-upsell.md) antes da prévia, antes do render e nos mp4. Ele lê todas as regras na versão mais nova, corrige no build o que não custa dinheiro e devolve só geração paga e decisões do Jhon. Regra nova de upsell → gravar no REGRAS_JHON_3010.md, que é de onde ele lê.

