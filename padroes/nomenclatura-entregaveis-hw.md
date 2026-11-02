---
name: nomenclatura-entregaveis-hw
description: Padrão de nome dos arquivos entregues nos jobs da H&W — e o que ele implica sobre o formato do entregável
metadata: 
  node_type: memory
  type: reference
  originSessionId: fc9b8b99-03a8-4414-83dc-b443b920a6ea
  modified: 2026-07-31T22:29:58.474Z
---

Padrão definido pelo usuário em 31/07/2026, no job do VitaRenew:

```
[DDMMYY][OT] NN_JV ADxx HKn [Produto] [Squad].mp4
```

Exemplo real: `[310726][OT] 18_JV AD01 HK1 [VitaRenew] [Squad].mp4`

Os campos vêm do **nome da pasta do job** (`[310726][OT] 18_JV [VitaRenew] [Squad]`),
com `ADxx HKn` inserido antes do produto.

**O que o padrão implica (e me pegou de surpresa):** o `HKn` no nome significa que o
entregável é **um arquivo por variação de hook, com hook + body já montados** — não as
peças soltas. Eu tinha produzido body e hooks separados de propósito (pra trocar hook na
timeline sem re-renderizar o body), o que é bom pra produção, mas **não é o formato de
entrega**. As peças soltas ficam em `02_GERADO/`; `04_ENTREGA/` recebe os concatenados.

Com 10 ADs × 3 hooks, são 30 entregáveis.

**How to apply:** o concat pode ser sem reencodar (`ffmpeg -f concat -c copy`) porque
as peças saem todas da HeyGen com specs idênticos — h264 / 1080×1920 / yuv420p / 25fps /
aac 48kHz estéreo. Conferir os specs antes mesmo assim; se divergir, reencodar.

Ver [[convencoes-producao-criativo]] e [[formatos-de-trabalho-hw]].
