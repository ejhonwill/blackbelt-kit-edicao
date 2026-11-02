---
name: gif-camera-travada-peso
description: "GIF de 5s com push-in de tela cheia estoura o peso — travar a câmera no prompt corta 3x e ainda ganha resolução"
metadata:
  type: reference
---

Levantado em 19/08/2026 nos GIFs do advertorial MemoFlow (Seedance 2.0 → ffmpeg).

Num GIF, o que pesa não é o movimento: é **quantos pixels mudam por quadro**. Um push-in
digital de 3-5% faz *todo* pixel mudar sempre, o `paletteuse=diff_mode=rectangle` não tem o
que reaproveitar e o arquivo explode.

Números reais da mesma cena (plano cenital de mesa, 5s):

| versão | config | peso |
|---|---|---|
| com push-in | 600px · 10fps · 96 cores | **5,09 MB** |
| câmera travada | 800px · 12fps · 192 cores | **1,80 MB** |

Ou seja: travando a câmera o GIF ficou **3x menor com resolução maior**. Mexer em dither,
paleta ou fps não resolve — testei `bayer_scale` 3/4/5, `dither=none` e `sierra2_4a` e todos
ficaram em 10-11 MB a 720p. O único lever real é pixel parado.

**Como aplicar:** no prompt do vídeo, escrever a trava explícita —
*"THE CAMERA NEVER MOVES: no push-in, no zoom, no dolly, no drift, no rotation, no reframing —
the framing is identical in the first and the last frame"* — e deixar a animação só no
conteúdo (uma pessoa que se mexe, uma gota que cai, uma luz que muda). Depois `hqdn3d` antes
do `palettegen` para o grão não virar ruído dithered.

Cascata que funcionou (para no primeiro que couber em ~2,5 MB):
800/12/192 → 720/12/160 → 640/12/128 → 640/10/128 → 600/10/96.

Ver [[nano-banana-deriva-fotorreal]] e [[higgsfield-cli-vs-mcp]].
