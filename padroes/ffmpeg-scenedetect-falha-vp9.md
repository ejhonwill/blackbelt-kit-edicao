---
name: ffmpeg-scenedetect-falha-vp9
description: "O filtro scene do ffmpeg da ZERO corte em VP9 baixado do Instagram; medir diferenca quadro a quadro na mao"
metadata:
  node_type: memory
  type: reference
---

Em vídeo VP9 baixado do Instagram pelo yt-dlp, o
`select='gt(scene,X)',showinfo` do ffmpeg **não acha corte nenhum** — nem com
limiar 0.08. Testado em 15/09/2026 num reel de 33 s que tinha 7 cortes secos.
Silencioso: não dá erro, só devolve lista vazia, o que parece "plano único".

**Substituto que funciona** — diferença média absoluta de luminância entre
quadros consecutivos, em miniatura:

```
ffmpeg -i in.mp4 -vf "fps=30,scale=96:-1" f/a_%04d.jpg
# em Python: np.abs(frame - anterior).mean()
# corte onde diff > media + 5*desvio  (e > ~8 absoluto)
```

No caso real: média 4,12 / desvio 4,08 / limiar 24,5 → achou os 7 cortes, o mais
forte com diff 67. **Sempre conferir visualmente** o quadro anterior e o
posterior de cada candidato antes de tratar como corte — a montagem
antes/depois em tira resolve em uma olhada.

Mesma armadilha do `drawtext`: esse ffmpeg do brew **não tem o filtro drawtext**,
então timecode queimado no mosaico tem que ser desenhado com PIL.

Relacionado: [[analise-criativo-ficha]], [[corte-viral]].
