---
name: corte-video-hdr-hlg-iphone
description: "Cortar/acelerar vídeo de iPhone em HDR HLG sem lavar a cor — e por que a receita libx264 da aula não serve"
metadata:
  type: feedback
---

Bruto de iPhone (IMG_xxxx.MOV) costuma vir **HEVC Main 10, HLG** (`color_trc=arib-std-b67`, `bt2020nc`) e com **`rotation=-90`** na matriz de display. Se o corte de silêncio usar o render `libx264 -pix_fmt yuv420p` de [[edit-aulas-avatar-ultrarealista]], o HDR morre: a cor lava e fica cinza-esverdeada.

**Why:** o libx264 em yuv420p 8 bits descarta o 10 bits e não carrega as tags de cor — o player passa a ler HLG como SDR.

**How to apply:**
- Reencodar com `hevc_videotoolbox -pix_fmt p010le -tag:v hvc1` e **re-declarar as tags à mão**: `-color_primaries bt2020 -color_trc arib-std-b67 -colorspace bt2020nc -color_range tv`. `-b:v 55–60M` segura 4K60.
- `-c copy` não é opção quando há mudança de velocidade (`setpts`/`atempo`).
- A rotação: o autorotate do ffmpeg **é aplicado também em `-filter_complex`**, então a saída já sai vertical (2160x3840). Conferir com ffprobe no fim — não presumir.
- Acelerar 1.1x mantendo 60 fps gera `drop=~10%` no log do ffmpeg. Isso é **correto**, não erro: 1706 frames de entrada → 1553 de saída.
- Não existe `zscale` nem `libplacebo` neste ffmpeg (8.1.2), então não dá pra tonemapar frame HLG→SDR direito. Pra still de referência, `eq=gamma=0.80:saturation=1.55:contrast=1.12` chega perto o bastante.

QC que peguei nesse job: silencedetect a −36 e −40 dB deu praticamente o mesmo mapa → prova de que as pausas eram silêncio de verdade e a margem podia ser apertada (0.22/0.28 em vez de 0.34/0.42 da aula). Ainda assim vale reverificar transcrevendo **o render final** e comparando com o original — foi o que confirmou que nenhuma palavra foi comida.

**23/10/2026 — HLG→SDR de verdade sem zscale:** gerar LUT 3D em Python (HLG inverso → OOTF 1000 nits → 2020→709 → joelho suave nas altas → gamma 2.4) e aplicar com `scale=in_color_matrix=bt2020,format=gbrpf32le,lut3d=...,scale=out_color_matrix=bt709`. Script: `~/Documents/01_Producao/Demanda Outubro/Criativo Lucas/cor/gerar_lut.py` (joelho 0.42, exposição 0.7 resolveu sol forte "estourado"). Depois do libx264, o container herda a tag HLG: remux com `-c copy -color_primaries bt709 -color_trc bt709 -colorspace bt709` e conferir no ffprobe.
