---
name: hyperframes-tranco-e-lapso
description: Por que lettering "pula" e o vídeo dá "lapso" em composição HyperFrames/GSAP — e como medir antes de mostrar
metadata:
  type: feedback
---

Jhon reprovou a 1ª VSL 3D do SynapseDeck (04/10/2026): "os lettering fica pulando e dá uns lapso". Causas reais:

1. **`fromTo(..., {immediateRender:false})` em elemento que já está visível** → ele aparece PRONTO, some e entra animado (tranco). Todo filho que anima depois precisa de `tl.set(..., {opacity:0})` em t=0 (ou estar dentro de um pai escondido ATÉ o próprio tween começar).
2. **Empurrar elementos em `z` (perspectiva) a cada batida** → eles se deslocam na tela (pulam pro centro). Para empilhar palavras, só escurecer.
3. **Câmera com `sine.inOut` por cena** → zera a velocidade no fim de cada cena = sensação de travada antes do corte. Usar `ease:'none'` e cruzar a troca (nova entra por cima, velha sai depois — sem esmaecimento duplo).
4. `tl.to` relativo/sem from em timeline que o render busca fora de ordem → trocar tudo por `fromTo` explícito.

**Why:** o render paraleliza/busca quadros; o que parece ok no preview quebra no MP4.
**How to apply:** antes de mostrar qualquer render, rodar `ffmpeg -vf freezedetect=n=0.0005:d=0.25` (trechos parados ≥0,25 s fora de respiro intencional = "lapso") e olhar uma sequência de 6 quadros (0,1–0,2 s) na entrada de um rótulo. Cena só de texto precisa de mais deriva de câmera (escala ~1.10) pra não parecer congelada. Relacionado: [[synapsedeck-expansao-biblioteca]].
