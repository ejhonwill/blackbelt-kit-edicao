---
name: corte-lossless-master-all-i
description: "Em master 4K ALL-I, cortar silêncio sem reencodar — e as duas armadilhas de sincronia do ffmpeg"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1c2c4d82-ef6f-4e54-a0f4-a0360b6c9134
  modified: 2026-07-25T14:03:36.758Z
---

Quando o material do corte de silêncio é um **master de câmera 4K ALL-I** (todo frame é keyframe), NÃO usar o render `libx264 crf 19` da receita de [[edit-aulas-avatar-ultrarealista]] — cortar em **cópia pura** (`-c copy`), que é frame-exato e sem perda.

Como saber se é ALL-I: `ffprobe -select_streams v:0 -read_intervals "%+20" -show_entries frame=pict_type` → se nº de I-frames == nº de frames, é ALL-I.

**Why:** a receita `crf 19` foi calibrada pra screen recording de aula (.mov), onde reencodar é irrelevante. Num master de câmera, ela joga 237 Mbps → 36 Mbps e gasta ~18 min de render — perda geracional grave num arquivo que ainda vai receber motion no AE. O corte lossless faz o mesmo trabalho em ~1 min.

**How to apply:** duas armadilhas do ffmpeg que reprovaram QC no caminho e precisam ser evitadas:
1. **Concat demuxer com `inpoint`/`outpoint` perde amostras de áudio** em cada emenda (11 emendas → áudio 1,45s mais curto que o vídeo = dessincronia progressiva). Solução: cortar o áudio por **filtro** `atrim`+`concat` (PCM→PCM é bit-exato) e o vídeo por cópia, depois muxar.
2. **`-ss S -t D` inclui frame extra** em alguns segmentos (deu 11303 em vez de 11300 = ~125 ms de deriva). Solução: calcular `n = round((e-s)*fps)` e usar **`-frames:v n`**, derivando o fim do áudio de `s + n/fps`. Assim os dois streams têm duração matematicamente idêntica.

QC obrigatório no fim: `format.duration`, `stream(v).duration` e `stream(a).duration` têm que ser **os três iguais**, e `nb_read_packets` do vídeo == nº de frames esperado.

Outra lição: **silencedetect não pega tempo morto com ruído.** Um intervalo de 11,2s sem nenhuma fala passou ilesa por `-32dB:0.6` porque tinha movimento/respiração acima do limiar. Corte de silêncio não substitui conferir a transcrição.
