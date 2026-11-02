---
name: premiere-movimento-depois-do-efeito
description: No Premiere o Movimento é aplicado DEPOIS dos efeitos da pilha — por isso mexer em escala/posição não reenquadra o que um Track Matte Key recorta
metadata: 
  node_type: memory
  type: reference
  originSessionId: a9d79f93-3728-4614-82d8-b8f92f628dd4
  modified: 2026-08-30T00:57:28.159Z
---

O **Movimento (Motion) é intrínseco** e o Premiere o aplica **depois** de todos os
efeitos da pilha. Como o Track Matte Key é efeito de pilha, a ordem real é:

    imagem crua -> Track Matte Key (corta no buraco) -> Movimento

**Consequência que custa caro:** mexer em escala/posição do clipe recortado NÃO
reenquadra o que aparece dentro da janela. Move e encolhe o **recorte já feito**,
que sai de baixo da moldura e deixa o buraco vazio.

Medido no [[skill-motion-omni-vsl]] não — medido no PiP do Tools PRO, com quadro
exportado da timeline, os dois modos lado a lado: conteúdo mandado para o centro
da janela (escala 46, pos 0.72/0.90) → círculo VAZIO; conteúdo parado (escala do
clipe, 0.5/0.5) → círculo cheio.

Para reenquadrar ANTES do corte é preciso pôr um efeito **Transformar** no
próprio clipe, ordenado antes do Track Matte Key. Aí a conta de "preencher"
passa a valer.

**Como isso me pegou:** o `geo.js` do PiP tinha um comentário dizendo que mandar
o conteúdo para o centro da janela "já foi tentado e estava errado". Passei por
cima achando que o defeito era não escalar para cobrir. O comentário estava
certo e a razão era esta. Ver [[toolspro-chaves-de-retorno]] e
[[premiere-script-ticks-e-corte-do-movimento]].

⚠ Corolário de diagnóstico: `property.getValue()` numa propriedade com keyframes
devolve valor que **não** corresponde ao playhead — usar `getValueAtTime(t)`.
E `displayName` se repete dentro do mesmo efeito (dois "Modo de mesclagem",
dois "Dimensionar largura"), então varrer por nome lê a propriedade errada.
Quadro exportado é a única prova.
