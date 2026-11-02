---
name: nano-banana-referencia-copia-composicao
description: Referência de estilo no nano_banana_pro copia a composição inteira — lote vira o mesmo plano repetido; travar estilo pelo texto
metadata:
  type: feedback
---

Em 26/09/2026 (B-roll 3D de artéria da VSL CardioFlush) gerei 2 âncoras só com texto e passei as duas
como `--image-references` nos outros 20 stills. Resultado: quase todos saíram **cópia do enquadramento
da âncora** (mesmo túnel frontal, mesma placa no mesmo lugar), só com variação de detalhe. Lote inútil
pra 22 planos diferentes.

**Why:** o nano_banana_pro trata a referência como composição, não só como estilo, mesmo com
"match the rendering style" no prompt.

**How to apply:** para B-roll 3D/abstrato, travar a consistência com um **bloco de estilo e material
idêntico em todos os prompts** (sem referência) + uma linha `CAMERA:` diferente por plano
(macro na parede, corte longitudinal, rasante, top-down, frontal). Referência de imagem só quando
o que precisa repetir é identidade (personagem, frasco) — ver [[nano-banana-deriva-fotorreal]].
Kling 3.0 Turbo não tem 4:5: gerar 9:16 (sai 1076x1928, 24 fps) e recortar o centro.
