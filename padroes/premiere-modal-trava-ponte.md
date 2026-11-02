---
name: premiere-modal-trava-ponte
description: createNewSequence abre diálogo modal e congela a ponte de script do Premiere; como diagnosticar por captura de tela e fechar sem perder nada
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3ed5c894-05b8-4d50-ae45-1d19e0b5d8e0
  modified: 2026-10-08T21:21:40.097Z
---

Em 17/09/2026, montando a timeline de lip sync do MemoFlow, uma chamada de
`app.project.createNewSequence("UPSELL #1 - LIPSYNC", id)` **abriu o diálogo "Nova sequência"** em vez de criar
direto. O diálogo é modal: prende a thread principal do Premiere e, por tabela, **a ponte CEP inteira**. Toda
chamada seguinte — até `pr_sequencias_listar`, que é leitura leve — estourou timeout por mais de 15 minutos.

**Diagnóstico que funciona** (o da [[premiere-deadlock-import-lote]] não bastou, porque a RAM estava BAIXA, 116 MB,
não alta):
- `tools/list` do Tools PRO responde em ~1 ms → **não é a ponte que caiu**, é o script dentro do Premiere.
- CPU do processo em ~5 % → thread bloqueada, não processamento.
- `osascript ... count of windows` devolve **0** e `window 1` dá "Índice inválido" — a AX não enxerga a UI do
  Premiere, então ausência de janela na AX **não prova** ausência de diálogo.
- **`screencapture -x` e OLHAR a imagem é o diagnóstico definitivo.** Foi o que mostrou o diálogo.

**Como fechar:** `osascript -e 'tell application "System Events" to click at {x, y}'` funciona mesmo sem a AX
enxergar a árvore — ele devolveu `button 2 of UI element Nova sequência` e fechou. Clicar em **Cancelar** não cria
nada e devolve a ponte na hora. `activate` e `key code 53` (Esc) **não funcionam**: o AppleEvent também expira
(-1712) porque a thread está presa. Achar o botão: recortar a região do `screencapture` e ler as coordenadas na
imagem (a captura veio 1920×1080, 1:1 com as coordenadas de tela nesta máquina).

**Como criar sequência SEM diálogo:** clonar uma que já tenha o formato certo.
`src.clone()` cria a cópia chamada `Cópia de <nome>` — **NÃO necessariamente no fim da lista** (08/10/2026: pegar
`sequences[numSequences-1]` pegou a `16x9` original, e eu renomeei/limpei/mudei o fps dela). Achar o clone pelo
nome `Cópia de …` ou pelo `sequenceID` que não existia antes; depois `novo.name = "..."` e apagar os clipes herdados
(`for(c=tr.clips.numItems-1;c>=0;c--) tr.clips[c].remove(false,false)`). Preserva tamanho, timebase e taxa de áudio
sem tocar em preset nenhum.

**Renomear trilha:** `track.setName()` da API pública **não existe** no Premiere 26.5 (`is not a function`).
Pela QE DOM funciona: `qe.project.getActiveSequence().getVideoTrackAt(i).setName("...")` e
`getAudioTrackAt(j).setName(...)`, e o nome volta a ser lido pela API pública normalmente.

**Import em lote:** um arquivo por chamada de `importFiles`, 6 arquivos por execução de script — 138 arquivos
passaram sem travar. Ver [[premiere-deadlock-import-lote]].

Ver [[premiere-script-ticks-e-corte-do-movimento]], [[toolspro-extendscript-mcp]].
