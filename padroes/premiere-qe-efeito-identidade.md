---
name: premiere-qe-efeito-identidade
description: "Duas referências ao mesmo clipe não são iguais por identidade no ExtendScript — casar por (trilha, ticks de início)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: a9d79f93-3728-4614-82d8-b8f92f628dd4
  modified: 2026-08-31T10:15:15.911Z
---

**Não comparar objetos de clipe com `!==` / `===` no ExtendScript.** Duas
referências ao MESMO clipe (ex.: `seq.getSelection()[0]` e
`tr.clips[c]`) **não são idênticas**. Uma varredura do tipo

```js
for (...) { if (tr.clips[c] !== clip) continue; /* nunca entra */ }
```

devolve sempre "não achei", e o erro sai apontando para o lugar errado — no
pr-zoom saiu como *"não consegui pôr o efeito Transformar"*, quando o
`addVideoEffect` funcionava perfeitamente.

**O que identifica um clipe sem ambiguidade:** o par
`(índice da trilha, clip.start.ticks)`, com o nome como desempate.

Complementos medidos no mesmo dia (Premiere 26.3.2):
- `qi.addVideoEffect(ef)` devolve `true` e **o mesmo objeto `clip` já enxerga**
  o novo componente em `clip.components` — não precisa reobter o clipe.
- `qe.project.getVideoEffectByName('Transformar')` devolve objeto com `.name`
  preenchido; `'Transform'` (inglês) devolve `.name` vazio nesta instalação
  PT-BR. O `.matchName` do objeto QE vem indefinido — quem tem matchName é o
  componente já aplicado (`AE.ADBE Geometry`).

Ver [[premiere-qe-transicoes-efeitos]] para o resto da API (pin de efeito por
clipe, remoção, export de frame) e [[premiere-movimento-depois-do-efeito]] para
a ordem efeito → Movimento.
