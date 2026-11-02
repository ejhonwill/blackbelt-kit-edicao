---
name: footage-sem-repeticao-na-timeline
description: Jhon não aceita o mesmo footage/b-roll duas vezes na mesma timeline — planejar alternativas por tema antes de montar
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3ac7ca15-899b-4c14-a10c-97ead60b1da9
  modified: 2026-10-09T14:47:36.185Z
---

Em 09/10/2026 (Kings Code 215_MV), com o B01 montado repetindo BR13, BR01, BR08, BR16 e BR07, o Jhon disse:
"Não quero ver footage repetido na mesma timeline".

**Why:** repetição denuncia banco pequeno e derruba a percepção de edição premium no DR.

**How to apply:** o plano de b-roll leva uma lista de ALTERNATIVAS por palavra-chave (mesmo tema) e um conjunto
`usados` por sequência; ao esgotar, gerar clipe novo específico (GPT Image 2.5 → Kling Turbo) em vez de repetir ou
deixar buraco. Entre timelines diferentes pode repetir. Conferir com contagem antes de dar por pronto.

Armadilhas da mesma montagem (Premiere via pr_extendscript):
- Kling Turbo e as transições do Baú vêm COM áudio — `overwriteClip` na V2/V3 joga o som na A2/A3 e apaga a voz/trilha.
  Gerar cópia `-map 0:v -c copy` (`_mute`) antes de importar.
- Punch-in com o avatar duplicado na V2 precisa de tempo travado no quadro (25 fps); mesmo assim o Premiere arredondou
  um inPoint para 1 quadro antes — corrigir com `Time.ticks` = quadro × 10160640000 e conferir `inPoint == start`.
- `pr_legendas_mogrt_aplicar` (BB Snap) DERRUBOU o Premiere ao acordar o After Effects; o reinício desligou o Modo
  avançado. Lettering feito como PNG (Pillow + Montserrat) com pop por keyframe de escala é o caminho seguro.
- Lettering a 30% da altura cobre o rosto em selfie 9:16; 62% (peito) fica acima da legenda e longe dos olhos.

Ver [[kings-code-referencias-edicao]], [[premiere-script-ticks-e-corte-do-movimento]], [[pr-captions-mogrt]].
