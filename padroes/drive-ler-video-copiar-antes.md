---
name: drive-ler-video-copiar-antes
description: Ler MP4 direto do Google Drive com ffmpeg trava; copiar pro local primeiro é ~100x mais rápido
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 96802f85-be87-4d64-8142-e098ca3f4c38
  modified: 2026-08-14T13:32:24.366Z
---

Ao conferir renders que moram no Drive (CloudStorage), **nunca aponte o ffmpeg direto pro caminho
do Drive**. Copie para o scratchpad primeiro e processe a cópia local.

Medido em 14/08/2026 no CardioFlush (renders de ~100 MB):

- `ffmpeg -i "<caminho do Drive>"` → ~14 frames em 17 min. O processo fica preso em I/O
  (13 s de CPU em 19 min de relógio). Dois passes no mesmo arquivo (hook + body) piora,
  porque o DriveFS parece re-buscar.
- `cp` do mesmo arquivo → 107 MB em ~8-100 s. Depois disso, extrair 55 frames leva segundos.

Como detectar antes de perder tempo: `du -h` no arquivo. Se devolver **4.0M** num MP4 de 100 MB,
é stub — o conteúdo não está materializado. Arquivo materializado devolve o tamanho real.

O conector do Drive **não** resolve: `download_file_content` corta em **10 MB** para binário
(o texto/docx vai muito além disso, mas vídeo não passa).

Ver [[drive-copia-perde-comentarios]] e [[nomenclatura-entregaveis-hw]].

## Copiar em paralelo, e conferir o tamanho depois (21/08/2026, VigorBoost 32_JV)

`cp` sequencial de 15 arquivos (4 GB) rodou a ~11 MB/min — 6 h estimadas. **Disparar os 15 `cp`
em paralelo** (loop com `&` + `wait`) baixou tudo em ~25 min: o DriveFS materializa vários
arquivos ao mesmo tempo sem penalidade, o gargalo é a latência por arquivo, não a banda
(medi 23 MB/s no en0 durante as cópias).

Armadilhas na volta:

- `xargs -P` no macOS **não** serve aqui: não tem `-d`, e com `-I{}` os caminhos longos da
  demanda estouram ("command line cannot be assembled, too long"). Use `while read` + `&`.
- **Um `cp` pode morrer calado** e deixar o arquivo truncado. Aconteceu: um MP4 de 45 MB ficou
  com 12 MB exatos e o `ffprobe` devolveu bitrate de 649 kb/s — quase reportei "queda de
  qualidade na exportação" que não existia. Sempre compare `stat -f %z` local × remoto antes
  de analisar, e só processe quem bater.
- `for K in $VAR` não faz word split no zsh (o shell padrão daqui). Scripts de loop têm que
  rodar via `bash arquivo.sh`, não inline.

Ver [[whisper-passada-longa-inventa]].
