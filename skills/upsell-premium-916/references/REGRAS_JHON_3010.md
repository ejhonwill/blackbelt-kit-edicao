# Regras gerais do Jhon para upsell (revisões do EreVanton 362_BM, 30/10/2026)

Aplicar em todo upsell, junto com PADRAO.md e REPROVADO.md.

## Fluxo
- 9:16 1080×1920, salvo pedido.
- Prévia aberta no HyperFrames para o Jhon aprovar antes de qualquer render. Não subir no Frame.io. Render/master só depois da aprovação.
- Reaproveitar b-rolls de jobs anteriores do mesmo produto, se passarem nos critérios.
- IA Creator (Agência Samurai) supervisiona cada lote e a prévia antes de liberar.

## Produto e frasco
- Rótulo oficial (mockups) em todo frasco; branco/genérico/outra marca reprovado, inclusive fábrica e esteira.
- Sempre em pé, rótulo de frente.
- Escala real (~10 cm, cabe na palma); tamanho único; kits repetem o mesmo frasco.
- Sem cara de IA: luz do ambiente, rótulo fosco, dedos fazem sombra. Conferir rótulo letra por letra (inclusive nº de cápsulas).
- **Cena da entrega = caminhão UPS** (Jhon, 01/11, vale para TODO upsell): no trecho que mostra o pedido saindo/chegando, o caminhão é o da UPS — carroceria marrom-escura com o escudo dourado "ups" na lateral, entregador de uniforme marrom; as caixas continuam com a logo do produto. Referência: `references/ref_entrega_ups/ups_caminhao_logo_ref.png` (antes, sem logo: `cinnashield_entrega_sem_logo_antes.png`). Gerar a imagem já com o escudo (GPT Image/Nano Banana com a ref) e conferir a grafia "ups"; não colar logo por cima. Obs.: é marca registrada de terceiro — decisão do Jhon ciente do risco; se a copy/compliance de algum produto pedir sem logo, perguntar.
- Não inventar embalagem do produto. **Caixa de envio leva a logo do produto, padrão premium** (Jhon, 31/10): na bancada, nas prateleiras do fundo e no caminhão — logo impressa de verdade, caixa limpa, grafia conferida. Referência visual aprovada: `references/ref_caixas_envio_logo/` (EreVanton 57/65/66). Vale para todo produto.
- Quantidade falada = quantidade na tela, sincronizada com a palavra.

## Imagem e b-roll
- Insert demonstra a fala; dor concreta e cotidiana, expressões naturais.
- 3D explica (progressão, antes/depois, mês 1→2→3); 3D só bonito é trocado.
- Mecanismo de ereção: 3D anatômico translúcido e médico, sem realismo explícito.
- **Cena de preço — padrão Diogo (01/11, vale para TODO upsell):** banner inclinado "Triple-Dose Kit" no topo; caixa premium do produto aberta com os frascos nos nichos + frascos na frente sobre bancada de mármore clara em cozinha com luz de manhã; card de preço em paralelogramo embaixo à esquerda ("$NN" enorme + "/bottle" + preço cheio riscado em vermelho) e tarja "$NNN TOTAL" logo abaixo; sem legenda na cena. Molduras, banner, card e tarja SEMPRE na cor da marca do produto (ex.: CinnaShield canela/dourado #3E2513/#C69A5B). Mesmo cenário serve de fundo para o selo de garantia. Elementos prontos em `ref_price_reveal_premium/`.
- **Depoimentos com CTA fixa — overlay validado (Jhon, 01/11):** canto superior direito, compacto: o mesmo card em paralelogramo do price reveal em versão pequena ("$X /bottle" + cheio riscado + tarja "$Y TOTAL") e logo abaixo a tag compacta ("<RESULTADO> IN" pequeno + "N WEEKS" grande em verde, caixa escura com borda). Nunca sobre rosto/boca/olhos. Ref: `ref_price_reveal_premium/padrao_cta_fixa_depoimento_validado.png`.
- Mesmo rosto em todos os planos. **Figurino alterna (Jhon, 01/11):** a protagonista não usa a mesma roupa o vídeo inteiro — troque de roupa a cada momento/dia diferente da história (manhã no banheiro, almoço de família, jantar fora, viagem…). Mesma roupa só dentro de um mesmo momento contínuo. Planeje o figurino por cena no storyboard e passe a roupa no prompt de cada plano.
- Bloco ANTI-STOCK nos prompts.

## Cards, lettering e legenda
- Proibido texto solto sobre avatar borrado: todo card/lettering de destaque tem imagem real ou 3D que diz o mesmo, com foco e sem área vazia.
- Interface de pedido = cena real (mão com celular e confirmação crível); packing com b-roll real.
- Legenda acompanha a fala sempre, pulando só o que está na headline. Headline em cima, legenda embaixo, sem sobrepor e sem cobrir rosto.
- Lettering atrás do avatar: opaco, legível, nunca cortado pela cabeça.
- Transições suaves (luz, light leak, continuidade); ritmo dinâmico com recompensas de atenção. Referência: bbkatana + upsells validados.

## Telas de preço (padrão ArtiBrex 335_DA)
- Bancada real com luz natural, frascos em pé, mão pegando um.
- Card branco/translúcido arredondado: "$X/bottle" grande, total embaixo.
- Legenda em faixa escura translúcida.
- **Número na legenda sempre em algarismo** (Jhon, 01/11): a locução pode falar por extenso ("nineteen a bottle… one twenty-nine total"), mas a legenda mostra "$19 a bottle… $129 total". Vale para preço, total, quantidade de frascos, dias, porcentagem e idade. O TTS recebe o texto falado; o `_alin.json` e a legenda usam o texto com algarismos (alinhar pelo tempo das palavras).
- Cor do card na identidade do produto; não copiar caixa de kit se o produto não tiver.

## Gifts
- Cada presente com imagem/vídeo próprio, nunca card com ícone.
- Video lesson: personagem assistindo no tablet/celular com player rodando.
- E-book: mockup com o nome na capa (tablet ou livro).
- Texto de capas/telas colado em HTML com tracking, nunca gerado pela IA.
- "GIFT #N" e valor riscado → FREE como lettering integrado à cena.
- Tom sugestivo e elegante, nada explícito.

## CTA e oferta
- Botão no padrão do upsell validado, destaque e leitura imediata.
- Conta da copy × rótulo (cápsulas por frasco × dose × dias). Se não fechar: fala segue a copy, conta fora da tela, avisar o copywriter.

## 30/10 (noite) — revisão do master r10 do 349
- **Nunca ida-e-volta (reverse).** Clipe mais curto que a cena: até 0,8×; senão divida em 2 b-rolls ou corte a cena (o expert volta). Em fundo de card, segurar o último quadro com push-in é aceitável; tocar ao contrário, nunca.
- **Ou lettering, ou legenda — nunca os dois.** Enquanto houver lettering, chip, card, tela de preço, tarja ou o card de abertura, a legenda some; volta quando o lettering sai. A área acima do botão fixo fica livre.
- **Lettering na palavra.** Toda entrada ancorada no tempo da palavra falada (diferença ≤ 0,15 s); conferir cada âncora que caiu no valor padrão.
- **Sem sigla no lettering** (público idoso EUA): "NRS" vira "POOR SLEEP" / "NON-RESTORATIVE SLEEP".
- **Escala do frasco:** NightRenew ≈ altura de uma caneca; CogniClear 0,9× o NightRenew; mesma escala em todas as cenas; kit inteiro no terço do meio, com respiro, sem corte, título acima.
- **Cena A (lettering atrás do expert):** o fundo nunca encolhe (sem borda preta); só o recorte recua; recorte com borda suave (erosão + feather), sem halo e sem pedaço de objeto da mesa; glow segue a letra (text-shadow), nunca caixa.
- **50 % b-roll orgânico** nas cenas de rotina e metáforas; produto continua IA/composição.
- **Fonte do b-roll real (Jhon, 31/10):** só (1) acervo da pasta de assets do produto e (2) orgânico do TikTok, nessa ordem. Sem Artlist, Magnific ou outro stock. IA por último, só para o que não existir nas duas.

## Régua de escala do frasco (Jhon, 30/10 — medida real, substitui qualquer régua anterior)
- Frasco de cápsulas 300 ml (ex.: NightRenew): **13 cm de altura com a tampa × 6,9 cm de diâmetro** (≈1,9 : 1).
- Conta-gotas 1 fl oz (ex.: CogniClear): 0,9× o frasco = ~11,7 cm com a tampa → CC ÷ frasco 0,81–0,99.
- Referências na mesma cena (tolerância ±10 %; entre frascos da mesma cena ±3 %):
  - mão adulta 18–19 cm → frasco ÷ mão ≈ 0,7; os dedos envolvem ~2/3 da circunferência, não fecham; o frasco é um pouco mais estreito que a palma (~8,5 cm). Medida prática: quatro dedos empilhados (~8 cm) ≈ 60 % da altura do frasco.
  - caneca padrão 9,5–10 cm → frasco ÷ caneca 1,3–1,35 (faixa 1,17–1,49). O frasco É mais alto que a caneca.
  - caixa de depósito 30–40 cm → frasco ÷ caixa 0,33–0,43.
- Método: grade de pixels sobre o quadro do meio de cada cena; medir só contra referência na MESMA profundidade (objeto atrás parece menor). Folha de contato antes/depois em `_SAMURAI/escala_frascos*.jpg`. Só passa o que cair na faixa.
- Prompt (GPT Image 2.5): escrever os tamanhos reais em cm de TODOS os objetos de escala, pôr a referência ao lado e na mesma profundidade, e dizer "use the attached photos ONLY to copy the label design, NOT the size". O GPT amplia o produto de referência; com caixas, pedir caixa grande (45 cm) para cair em ~0,36. Medir ANTES de animar.

- **Tamanho do produto:** ver `PADRAO_TAMANHO_PRODUTO.md` + `regua_tamanho_produto.png`. Ouro = cabeceira 349_BM (pote 28,5 % do quadro em plano aberto de mesa).

## Personagem da história ≠ expert (Jhon, 01/11 — regra fixa)
- Se o expert não é quem vive a história (paciente, cliente, parente), a história ganha um **personagem próprio**, com rosto diferente do expert. O rosto do personagem é o mesmo em todas as cenas, e o figurino troca a cada momento da história.
- Vale para o **b-roll**: as cenas da história (dia a dia, problema, virada) mostram o personagem, **nunca o rosto do expert**. O expert aparece só nas partes em que ele fala como especialista.
- **Orgânico primeiro:** no b-roll da história, procurar filmagem real com pessoa coerente com o personagem (idade e perfil), seguindo a ordem de fonte acima. IA só para o que faltar, e com o mesmo personagem ultrarealista.
- No plano: marcar em cada b-roll quem aparece (personagem, expert ou ninguém) e se a cena é orgânica ou gerada.

- **Price reveal premium validado (Jhon, 01/11):** elementos prontos em `references/ref_price_reveal_premium/` (banner "Triple Dose Kit", card "$X /bottle + $Y TOTAL" com o preço cheio riscado em vermelho, caixa do produto aberta, Example 1/2 = composição final). Versões azul (EreVanton) e marrom (Cinna Shield). Todo upsell segue esse padrão visual; para produto novo, refazer os elementos na cor da marca mantendo forma, tipografia, glow e composição.

- **Timeline antes do render (01/11/2026, Jhon):** antes de QUALQUER render, abrir APENAS a timeline (prévia do HyperFrames no navegador) para o Jhon aprovar o visual. Sem o OK dele na prévia, não pedir a vez nem renderizar. Motivo: evitar retrabalho de render.
- **Molds do price reveal (Jhon, 01/11):** banner e card entram só com o mold (fundo transparente em volta, sem retângulo escuro atrás; se o PNG vier com fundo preto, recortar na forma mantendo o glow). Banner "Triple-Dose Kit" e caixa de preço ficam pulsando suave enquanto na tela (escala 1,00→1,04 + glow, ciclo ~1,2 s, ease in-out, defasados entre si).

- **Legenda sempre embaixo** (Jhon, 01/11): mesmo lugar e estilo o vídeo inteiro; se cobre rótulo/rosto, reenquadra-se o plano, nunca a legenda.
- **Full-bleed sem fresta** (Jhon, 01/11): todo plano/painel cobre 100 % do quadro (object-fit: cover), sem moldura, borda ou vão entre painéis.
- **Padrão visual premium** (Jhon, 01/11): nada de objeto real desenhado em CSS nem lettering chapado sobre still; ver `REPROVADO.md` 01/11 — 351_MV e a `direcao_de_arte.md` do job 351.

## 01/11 (noite) — revisão do CinnaShield Up1 na prévia
- **Legenda nunca em 3 linhas** — máximo 2; quebrar a frase em 2 legendas consecutivas. Varredura automática antes de mostrar prévia.
- **Teste de glicemia fisicamente certo** — a fita encosta na gota; se a IA errar, preferir vídeo orgânico real de teste.
- **Lettering atrás do expert sem fantasma** — o recorte é o MESMO quadro do fundo (mesmo vídeo/tempo/escala/posição); se aparecer duplicado (atrás e na frente), tirar o efeito e pôr o lettering ao lado. Conferir por diferença de quadro.
- **Tamanho do frasco de cápsula = padrão ArtiBrex 335_DA (martelo batido)** em TODOS os b-rolls, inclusive quando o copy pedir "maior"; folha de escala contra o quadro equivalente do ArtiBrex.
- **Produto/rótulo = UMA imagem única (Jhon, 01/11 — reforço, reprovado de novo):** toda cena com produto, rótulo novo, caixa ou kit nasce como UMA imagem gerada já com o produto dentro (mockup oficial de referência) e a animação é feita EM CIMA dela. Proibido compor frasco/rótulo/caixa por cima de cena ou vídeo (PNG, recorte, máscara) — fica "dois planos". Exceção só para os gráficos do price reveal e o card final. Auditar o build antes de toda prévia.

- **Celular = UMA imagem com a tela já gerada (Jhon, 01/11 noite):** toda cena de celular/tablet/monitor com oferta, preço, site ou app é gerada já com a tela PRONTA dentro da imagem (ex.: "Special offer · 6 bottles · $99 · COMPLETE MY PROTOCOL" com os frascos oficiais no visor), na mão real, numa imagem única, e animada em cima. PROIBIDO gerar o celular com tela branca/verde e encaixar a cena ou um card por cima (dois planos: a tela desliza, borra, descola no movimento). Referência: references/ref_celular_tela_gerada/certo_direita_errado_esquerda.png (direita = certo, esquerda = errado). Conferir grafia, preço e contagem de frascos no visor letra por letra; se errar, gerar de novo.
