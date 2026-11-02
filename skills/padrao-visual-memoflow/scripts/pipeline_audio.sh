#!/bin/bash
export PATH="$HOME/.npm-global/bin:$PATH"
S=/private/tmp/claude-501/-Users-jhonwill/aa133884-6487-45b8-a7a6-b0899fb49075/scratchpad; cd $S
until grep -q "QC done" /private/tmp/claude-501/-Users-jhonwill/aa133884-6487-45b8-a7a6-b0899fb49075/tasks/bk32b9rye.output 2>/dev/null; do sleep 15; done
echo "== aprovar t1"; python3 aprovar_audio.py qc_t1_all.json > aprov1.log 2>&1; tail -1 aprov1.log
faltam=$(python3 -c "import json;print(','.join(b.replace('_BLOCO_',':').lstrip('0') if False else b for b in json.load(open('$AP/aprovacao.json'))['sem_aprovacao']))" 2>/dev/null)
for T in t2 t3; do
  faltam=$(python3 - <<'PY'
import json,os
AP="/Users/jhonwill/Library/CloudStorage/GoogleDrive-jhonatan.araujo@hw-publishing.com/Drives compartilhados/H&W - Edição de Vídeo -Q3/Arquivo de Edição /08. Memory/MemoFlow/OT/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_LIPSYNC/04_AUDIOS_APROVADOS/aprovacao.json"
f=json.load(open(AP))["sem_aprovacao"]
print(",".join(b.split("_BLOCO_")[0]+":"+str(int(b.split("_BLOCO_")[1])) for b in f))
PY
)
  if [ -z "$faltam" ]; then echo "== nada a regenerar antes de $T"; break; fi
  echo "== $T para: $faltam"; python3 tts.py "$faltam" $T > tts_$T.log 2>&1; python3 qc_audio.py $T "$faltam" 2>&1 | grep -v -i "warn\|fp16" > qc_$T.log
  qcf=$(ls "$AUDSRC"/qc_${T}_*.json | head -1); prev=$(ls "$AUDSRC"/qc_t*.json | xargs -n1 basename | tr '\n' ' ')
  python3 aprovar_audio.py $prev > aprov_$T.log 2>&1; tail -1 aprov_$T.log
done
echo "== submit lipsync"; python3 lipsync.py submit v1 all > lipsync_submit.log 2>&1; grep -c " -> " lipsync_submit.log; grep -c "SEM AUDIO" lipsync_submit.log
echo "== collect lipsync"; python3 lipsync.py collect v1 > lipsync_collect.log 2>&1; tail -1 lipsync_collect.log
echo "PIPELINE DONE"
