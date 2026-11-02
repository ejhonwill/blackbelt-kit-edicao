---
name: premiere-razor-qe-e-audio-embutido
description: QE razor erra o ponto em sequência que teve o fps trocado; vídeo com áudio embutido sobrescreve a trilha de voz ao ser posto na V1
metadata:
  node_type: memory
  type: feedback
  originSessionId: 266174c5-dd5c-4a4e-93cf-49baceafcda1
  modified: 2026-10-19T19:02:42.235Z
---

Montando o clone Baking Soda no Premiere (19/10/2026), sequência clonada da `9x16` do Projeto Padrão (23,976) e trocada para 30 fps por `setSettings`:

1. **`qe...getVideoTrackAt(0).razor("HH:MM:SS:FF")` cortou nos lugares errados** (10,5 s virou 8,5 s; 47,37 virou 37,97) — o timecode é lido com outra base. Não usar razor por timecode. O que funcionou: pôr o mesmo item em PEDAÇOS contíguos (`setInPoint`/`setOutPoint` + `overwriteClip` + `clip.end`), e depois alinhar `clip.inPoint = start + folga` de cada pedaço (dois vieram 1 quadro fora: 0,267 em vez de 0,300 — fonte 25 fps).
2. **O lip sync da HeyGen tem áudio.** `overwriteClip` na V1 levou o áudio junto para a A1 e apagou a `voz_clone.wav` que já estava lá — sem erro. Pôr o vídeo com áudio ANTES da voz, ou reler a A1 e recolocar a voz depois. `pr_timeline_listar` mostra (A1 com N clipes do .mp4).
3. Keyframe de Escala/Posição: `addKey(T)` usa o tempo da MÍDIA (a partir do inPoint), não o da timeline.
4. Screenshot da janela do Premiere (`screencapture -l<id>`, id via Swift `CGWindowListCopyWindowInfo`) pega o painel Tools PRO com o TOKEN visível quando "Conectar IA" está aberto — recortar só o Monitor de Programa e apagar o original.

Ver [[premiere-script-ticks-e-corte-do-movimento]], [[premiere-modal-trava-ponte]], [[premiere-legendas-api]].
