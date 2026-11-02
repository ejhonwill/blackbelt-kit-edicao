---
name: nunca-importar-do-scratchpad
description: Mídia gerada tem que ser gravada na pasta do projeto ANTES de importar no Premiere/AE — o scratchpad é apagado e a mídia fica offline
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8aa29fe2-71a0-4f7f-bf69-ae18745214aa
  modified: 2026-10-06T20:34:51.846Z
---

Gerei 14 MP3 de locução no scratchpad da sessão e importei no After a partir de lá. O
scratchpad foi limpo entre uma mensagem e outra e **os 14 itens ficaram offline** no projeto
salvo — o usuário viu "os áudios sumiram". Os 70 itens restantes sobreviveram porque eu tinha
copiado para dentro da pasta da demanda.

**Why:** o scratchpad (`/private/tmp/claude-501/<sessão>/scratchpad`) é temporário e some sem
aviso, inclusive no meio da sessão. Um projeto do AE/Premiere é persistente e guarda o caminho
absoluto — importar do temporário é plantar mídia offline num arquivo que o usuário vai abrir
amanhã.

**How to apply:** qualquer artefato que vá **entrar** num projeto (áudio de TTS, imagem gerada,
logo baixada, render intermediário) é gravado **direto na pasta da demanda** antes de importar.
Scratchpad só para o que é descartável: frames de conferência, mosaicos, scripts .jsx, logs.

**Regra do Jhon (06/10/2026), válida para tudo:** todo arquivo baixado ou gerado (Higgsfield,
HeyGen, ElevenLabs, renders, downloads) fica na **pasta do projeto**, organizado por tipo — nunca em
temporário, Downloads ou pasta da conversa. Virou regra embutida no Editor Automático 0.22.1
(contexto da Conversa + skill boas-praticas-black-belt + destino do download das prévias).

Regerar TTS **não é idempotente**: as mesmas 7 linhas com os mesmos `voice_settings` voltaram com
durações diferentes (−0,371 s a +0,186 s). Se a legenda foi cortada em cima do alinhamento antigo,
ela dessincroniza — tem que regravar o `*_timing.json` **junto do áudio, na pasta do projeto**, e
recalcular legenda e ticker a partir dele. Ver [[elevenlabs-conta-limites]].

Para achar o estrago: varrer `FootageItem` + `mainSource instanceof FileSource` e testar
`new File(...).exists`; religar com `footageItem.replace(File)`. Ver [[toolspro-ae-mcp-porta-errada]].
