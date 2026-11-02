---
name: premiere-export-direto-trava-com-drive
description: "exportAsMediaDirect num sequência com mídia no Drive travado derruba o Premiere; pra timing de slide, pedir áudio local"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3ff7eff6-9396-46cc-89c8-7cda3846263b
  modified: 2026-09-30T21:00:06.757Z
---

Em 30/09/2026 (slides do webinar AI Loophole) precisei do áudio da sequência pra achar o segundo
de cada fala. A fonte (`Parte 1 - Webinar.mp4`, 259 MB) estava no Drive compartilhado e travada em
4 MB (cp/dd parados). Tentei `seq.exportAsMediaDirect(...)` com o preset
`WAV_Mono_16bit_16kHz.epr` pela ponte do Tools PRO: o curl estourou em 120 s e **o Premiere caiu** —
o Jhon teve que reabrir.

**Why:** o export direto é síncrono e lê a mídia fonte; se o Drive não entrega os bytes, o
Premiere trava junto. O cache do Premiere (.ims/.pek) não serve — AAC não gera .cfa.

**How to apply:** antes de qualquer export pelo script, testar leitura da fonte
(`dd` com timeout de 15 s). Se travar, não exportar — pedir ao Jhon um áudio local ou "Disponível
offline". O que funcionou: ele montou um projeto leve só com o áudio tratado local
(`Demanda Setembro/Audio Webnario/`), aí mlx_whisper large-v3-turbo com word timestamps → tempo de
cada slide → `pr_timeline_colocar` em V1 → fechar lacunas de 1–2 quadros com `clip.end = next.start`.
Relacionado: [[drive-subarvore-travada-curl]], [[premiere-modal-trava-ponte]], [[slides-webinar-lettering-curto]].
