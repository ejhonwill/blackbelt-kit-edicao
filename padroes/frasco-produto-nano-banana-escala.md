---
name: frasco-produto-nano-banana-escala
description: "Frasco de produto em b-roll de IA — gerar no Nano Banana Pro com o mockup; GPT Image 2.5 afina/agiganta e colar PNG fica fake (Jhon reprovou 3 rodadas no Upsell ArtiBrex, 22/10/2026)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: d08c29df-57bf-4c55-81a8-b7563925c3f6
  modified: 2026-10-23T12:13:09.178Z
---

No Upsell #1 ArtiBrex (335_DA, 22/10/2026) o Jhon reprovou três vezes as cenas com frasco: "bugado ou gigante", "uns gordinhos e outros magros", e a colagem do mockup PNG por cima de fundo "bem fake".

**Why:** o GPT Image 2.5 Flare gera o frasco fora de escala (maior que a caneca/mão) e AFINA o frasco mesmo com a proporção escrita no prompt (2,0–2,4 contra 1,79 do mockup). Colar o PNG oficial sobre fundo, mesmo com sombra e escala medida, não convence. O Nano Banana Pro (`or:google/gemini-3-pro-image`, ~US$ 0,14) com o mockup como 1ª referência manteve a proporção de primeira (1,78–1,82).

**How to apply:** cena com produto → Nano Banana Pro + mockup oficial (+ still da cena como 2ª ref), escala real no prompt (frasco 30 cáps ≈ 11 cm; caneca 9,5; mão 18,5), MEDIR altura/largura do frasco no still antes de animar (aceitar ±8% do mockup), animar no Kling com câmera travada e usar só os primeiros 2–3 s (rótulo derrete/gira depois). Kling com 9 frascos muda a contagem → kit fica still com push. Seedance recusa referência com rosto realista. Avatar IV ignora gesto pedido (aceno) — não prometer gesto. Ver [[gpt-image-25-personas-com-produto]], [[lipsync-rotulo-reescrito-recolagem]], [[upsell-artibrex-335da]].
