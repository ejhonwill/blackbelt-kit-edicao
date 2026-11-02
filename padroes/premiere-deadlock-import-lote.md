---
name: premiere-deadlock-import-lote
description: "importFiles com lote grande pendura o motor de ExtendScript do Premiere; como diagnosticar deadlock e o que o auto-save salva"
metadata:
  node_type: memory
  type: project
---

Em 15/09/2026, `app.project.importFiles([8 mp4s], true, bin, false)` **pendurou o
motor de ExtendScript** do Premiere 26.5. Toda chamada seguinte do MCP do Tools PRO
deu timeout, inclusive `pr_midia_info`.

## Diagnostico — separar "ocupado" de "travado"

| Sinal | Ocupado | Travado |
|---|---|---|
| `curl /health` do Tools PRO | 200 | **200 tambem** (o servidor nao e o problema) |
| CPU do Premiere (`top -l 1`) | alta | **0,0 %** com RAM alta (11 GB) |
| `AXDialog` count via System Events | 0 | 0 |
| `count of windows` via System Events | >0 | **0** |
| Arquivos novos em Media Cache Files | aparecendo | nenhum |

**0 % de CPU com RAM alta e `count of windows` = 0 e deadlock**, nao processamento.
Nao adianta esperar. `tell application ... to quit` tambem pendura; so `killall -9`.

## O auto-save salva o que o save nao salvou

O `.prproj` no disco ficou na versao anterior (39 KB), mas
`08_PREMIERE/Adobe Premiere Pro Auto-Save/` tinha um arquivo **maior** (46 KB) com
os imports que tinham entrado antes do travamento. Ao reabrir, o Premiere trouxe
a midia importada. **Conferir o tamanho do auto-save antes de assumir que se
perdeu trabalho.**

## Prevencao

Importar em lotes pequenos. Um arquivo so (o B-roll) passou sem travar logo depois
do restart. Antes de matar, `cp` do `.prproj` e apagar o `.prlock` orfao depois.

## Bonus: audio so-audio nao recorta com mediaType 1

`projectItem.setInPoint(t, 1)` num `.wav` **nao faz nada** e o `overwriteClip`
coloca o arquivo inteiro — deu a mesma locucao de 33 s em todas as 8 cenas, sem
erro. Com **`mediaType 2`** recorta certo. Conferir sempre `clip.inPoint.seconds`
depois de posicionar, nao so `start`/`end`.

Ver [[premiere-script-ticks-e-corte-do-movimento]], [[toolspro-extendscript-mcp]],
[[premiere-legendas-api]].
