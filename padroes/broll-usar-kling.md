---
name: broll-usar-kling
description: "Jhon pediu: B-roll de criativo deve ser animado no Kling (kling3_0_turbo), não no Seedance"
metadata:
  type: feedback
---

Em 25/09/2026, no job LeafTide 01_JH, o Jhon disse: "da próxima usa o kling para esses broll" (o lote tinha sido animado no Seedance 2.0).

**Why:** preferência dele de qualidade/estilo para B-roll de UGC. Além disso, o modo `fast` do Seedance sumiu da conta (dá "Not found") e o `--start-image` com caminho local também falha — o Seedance exigiu upload antes.

**How to apply:** nos próximos jobs, animar B-roll com `higgsfield generate create kling3_0_turbo --start-image <upload_id> --aspect_ratio 9:16 --resolution 720p|1080p --duration 5`. O script `MEDIA/COPY/broll_gerar.py` do job 01_JH usa seedance — trocar o modelo antes de reaproveitar. Ver [[leaftide-01jh-brutos-heygen]].
