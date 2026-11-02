---
name: premiere-legendas-api
description: "Limite do ExtendScript do Premiere pra legenda/caption e os contornos (ferramenta CopySync do app)"
metadata:
  node_type: memory
  type: reference
  originSessionId: d9dec341-b3d7-4400-80b2-a37369f7b88a
  modified: 2026-07-26T22:59:39.461Z
---

O ExtendScript do Premiere **não lê nem escreve o texto de legenda nativa (Transcrição/Captions) de forma estável** — `seq.captionTracks` + `clip.getCaptionText()` é best-effort e na maioria das versões cai em `api_unsupported`. **Confirmado ao vivo na versão do usuário (26/07/2026): `seq.captionTracks` = `api_unsupported`** (não existe). Log de diagnóstico do CopySync sai em `~/Desktop/BB_copysync.log`. Como a leitura direta não funciona, o CopySync oferece (em ordem de preferência): **Carregar transcrição (.txt)** — o principal p/ o usuário: no Premiere *Texto → Transcrição → menu (…) → Exportar → Exportar para arquivo de texto*; o painel (`ccPickTXT`) lê o .txt, extrai os timecodes (`HH:MM:SS:FF`, converte FF→ms com o fps da sequência via `ccInfo`) e monta blocos SRT — sem render, sem preset. Também: **Carregar arquivo SRT…** (`ccPickSRT`), colar SRT manual, ou render `.epr`. Obs.: o export de transcrição do Premiere dá `.txt`/CSV (não SRT); SRT só sai de *Arquivo → Exportar → Mídia → aba Legendas → sidecar SubRip*. Não existe "escrever no item de legenda nativa". O MCP Higgsfield confirma: só tem `pr_create_caption_track` (criar faixa a partir de um .srt importado); **não** há tool de ler/gravar texto de legenda.

Contornos usados:
- **Ler a faixa**: exportar sidecar `.srt` via `seq.exportAsMediaDirect(out, preset.epr, 0)` com um preset `.epr` que tenha *aba Legendas → Criar arquivo sidecar (SubRip .srt)* ligado. Render de áudio, rápido e bloqueante; lê o `.srt` do temp e limpa. (A faixa de legenda precisa estar ativa/olhinho ligado.)
- **Escrever de volta**: `app.project.importFiles([srt])` + `seq.createCaptionTrack(item, 0)` — recria a faixa corrigida (a antiga fica; desativar/apagar). Assinatura do `createCaptionTrack` varia por versão: tentar `(item,0)`, `(item,0,3)`, `(item)` em ordem.
- **ARMADILHA CR/LF (Mac)**: ao gravar o SRT via `File.write` no ExtendScript do Mac, o `\n` é convertido pro padrão antigo **CR (Macintosh)** — arquivo fica com quebras só-CR e o importador de SRT do Premiere recusa com "**O importador informou um erro genérico**". Correção: `f.lineFeed = 'Unix'` + gravar com `\n` (validado ao vivo 26/07/2026 — a mesma SRT com LF importou via `pr_import_media` sem erro). Escrever **ao lado do projeto** (não em `Folder.temp`, que no Mac vai pra `T/TemporaryItems`) e garantir nenhum bloco de texto vazio.
- **Legenda como MOGRT/título** (clip de texto): aí SIM dá pra corrigir NO LUGAR com `pr_set_mogrt_text` (MCP) — verdadeira edição in-place, sem round-trip de SRT.
- **Legenda queimada em .mov** (ex.: `AD01_LETTERING.mov` das VSLs do usuário): não editável no Premiere; só regerando na origem (AE/gerador).

Ferramenta no app: **Editor Black Belt Tools PRO → Premiere → Legendas → CopySync** (`tools/pr-copysync`). Motor de alinhamento (Needleman-Wunsch com banda + termos protegidos) portado do plugin **HW CopySync** (`com.hwpublishing.copysync`, de terceiro) — reaproveitados `align.js`/`srt.js` verbatim; a ponte com o Premiere foi adaptada pro nosso app (funções `cc*`, retorna `BB_COPYSYNC_OK`). Fluxo: cola a copy → Ler legendas da sequência → alinha e mostra diff/confiança/edição → Aplicar (recria a faixa). O usuário usa **legenda nativa** (confirmado 26/07/2026). Motor validado ponta a ponta em cenário de VSL; o clique real de ler/aplicar depende de uma sequência com faixa de legenda nativa. Relacionado: [[ae-mcp-armadilhas]].

## UXP APAGA e RETEMPORIZA legenda (medido ao vivo 19/10/2026, Premiere 26.5.2)
Plugin de teste UXP (`BB Teste Legenda`, fonte em scratchpad da sessão; instalado com UPIA `--install x.ccx` — manifest com `host` como OBJETO, array dá -267; reinstalar exige reiniciar o Premiere):
- `seq.getCaptionTrack(0).getTrackItems(ppro.Constants.TrackItemType.CLIP,false)` devolve os blocos (`TrackItem`, nome "SyntheticCaption") com início/fim/duração certos.
- **Apagar**: `TrackItemSelection.createEmptySelection(sel => { sel.addItem(it,true); project.lockedAccess(()=> project.executeTransaction(ca=> ca.addAction(SequenceEditor.getEditor(seq).createRemoveItemsAction(sel,false,Constants.MediaType.DATA,false)))) })` — tudo DENTRO do callback (fora dele: "script object is no longer valid"). 4→3, todos→0, persiste ao salvar/reabrir, Cmd+Z desfaz num passo.
- **Tempo**: `createSetEndAction`/`createSetStartAction`/`createMoveAction(TickTime.createWithSeconds(x))` funcionam; a ação tem que ser CRIADA dentro do `lockedAccess` ("Requires locked access").
- **Texto continua inacessível**: `getComponentChain()` vem com 0 componentes; nenhum getter de texto. Trocar texto = recriar faixa por .srt (`pr_legenda_nativa_criar`).
