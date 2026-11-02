---
name: meat-hook-frames-gpt-vs-nano
description: "Start frames de Meat Hook — GPT Image 2.5 com referência troca o prop (coração→tubo, tornozelo→braço); Nano Banana Pro acerta; demonstração pede 3 frames"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2be87d91-a03a-417a-8c78-6d071a81fd97
  modified: 2026-09-23T13:01:38.038Z
---

Levantado em 23/09/2026 nos 10 hooks do CardioFlush 128_PG (pressão alta, "ritual do mel").

**GPT Image 2.5 com `--image-references` de uma âncora copia o PROP da âncora.** Referenciando o frame do
cilindro entupido, o "heart model" saiu como o mesmo tubo (2/2) e o "swollen ankle" saiu como antebraço (2/2),
sem erro nenhum — só a conferência visual pega. Também errou dígito no monitor de pressão (172/93 em vez de 98).
**Nano Banana Pro** (`nano_banana_pro`, 9:16, 2k, sem `--quality`) acertou os 5 de primeira: coração anatômico,
perna com meia e tornozelo inchado, e o monitor com o número exato ao escrever "EXACTLY 172 on the top line and 98
on the bottom line".

Filtro NSFW do GPT Image barrou: coração com "cement-like lining… crusted", pai com camisa aberta recebendo o
ritual no peito, pé descalço. Coração passou ao virar "classroom heart model… smeared with wax"; peito passou com
**camisa abotoada e o próprio pai derramando**. O usuário mandou: barrou → Grok Image ou Nano Banana Pro.

**Hook de demonstração = 3 frames em sequência lógica** (pedido do usuário, com referência do Pedro):
A prop com a gordura na lente → B o ritual sendo derramado → C a gordura derretida caindo (na calça/no cepo).
Isso casa com `minimax_h3_max` (`--start-image` + `--end-image`, 768p, até 15s): A→B e B→C.

**Deriva de rosto no frame C:** usando só o frame B como referência, o rosto mudou. Passar **B + âncora** como
duas `--image-references` com "IDENTITY IS CRITICAL: the SAME man as in BOTH reference images" resolveu.

Script reaproveitável: rodadas por nome (`frames.py wave1|wave2 <nomes>`), move reprovado para `_REPROVADOS/`,
estado de job em JSON. Aprovação vai numa sequência clonada da 9x16 (`HOOKS - APROVACAO FRAMES`), 3 s por frame,
1 s entre hooks, marcador por frame; escala = 1080/largura (GPT sai 1520×2688, Nano 1536×2752).

Ver [[gpt-image-25-personas-com-produto]], [[anti-cara-de-ia-em-imagem]], [[premiere-modal-trava-ponte]].

**Mapear comentário de copy → hook pelo HORÁRIO erra.** O leitor do Drive devolve os comentários sem dizer em
qual hook estão; distribuí por ordem de criação e troquei H06/H07 (o "joga no peito e esfrega" era do médico no
H06, o "gordura dissolve devagar" era do padre no H07). E o avatar de cada hook está na IMAGEM de referência do
doc (H04 médico, H06 médico + idoso na cama, H07 padre com artéria), que o export não entrega ("File too large").
**Antes de gerar, pedir print das referências por hook** — o usuário vê o doc; eu não.

**Animação no `minimax_h3_max` (23/09/2026, 21 clipes):** gera a fala com áudio junto (não tem parâmetro de
áudio; `audio_references` não combina com start_image). Sai 768×1344, 24 fps, 2,5 créditos/s. Com a trava de
fala única + janela, 17/20 bateram palavra a palavra de primeira (Whisper small). Falhou com **fala embaralhada**
quando (1) o personagem derrama o ritual no próprio pescoço enquanto fala — falhou 2×, só passou dividindo em dois
clipes sem end_image — e (2) a fala era pedida para começar só depois de 3 s de ação muda (padre); começar a fala
em ~1 s e deixar a ação correr junto resolveu. Com end_image, a primeira frase às vezes some ("Now watch…") —
mandar "starts speaking right away with the words '…'". Números: escrever por extenso no prompt; o Whisper
devolve em dígito, então match ~0,85 com número é aprovação, não falha.

**Voz muda entre clipes do mesmo personagem** (o usuário ouviu no H09): cada geração do MiniMax inventa a voz.
Correção que funcionou: ElevenLabs IVC da voz do 1º clipe → speech-to-speech em todos os clipes daquele
personagem → troca só o áudio no mp4 (`-c:v copy`), original guardado em `_REPROVADOS/*_voz_original.mp4`. A conta
tem 9/10 vagas ocupadas por vozes de outros jobs: clonar UMA por vez e apagar só o clone temporário (`TMP_128PG_*`).
Fala manteve o mesmo match depois da troca. Fazer isso por padrão sempre que um hook tiver mais de um clipe.

**Premiere: sobrescrever arquivo em uso no Drive deixa o item OFFLINE** (não atualiza). `refreshMedia()` não
basta; `item.changeMediaPath(mesmoCaminho, true)` religa. Conferir com `isOffline()` e exportar um quadro.
**Armadilha do clone de sequência:** `src.clone()` + `p.sequences[último]` NÃO pega o clone quando já existe outra
sequência criada por script — renomeei e esvaziei a sequência de aprovação. Achar o clone pelo `sequenceID` que
não existia antes.

**Montagem hook + body (23/09/2026):** os ADs validados vieram em **AV1** (Drive de terceiro; baixou por
`drive.usercontent.google.com/download?id=…&confirm=t` sem cookie). O Premiere 26 importa AV1 **só com áudio**, sem
erro. Converter para H.264 e — armadilha — **salvar com NOME NOVO** (`_h264`): no mesmo caminho o cache do Premiere
continua achando que é só áudio. `detect de cena` do ffmpeg não acha corte em AV1; medir diff quadro a quadro.
Cortar body pelo quadro, não pela palavra: o AD02 tem Fox → quadro preto → fade; o in-point do Premiere arredonda
para a grade 23,976 da sequência e deixou 1 quadro da Fox — conferir exportando o quadro da emenda.
Decupagem de hook: silencedetect -40 dB/0,3 s + tempos do Whisper para descartar ruído solto; transcrever o hook
decupado e comparar com o copy (pegou o "Please" perdido — Whisper marca palavra curta inicial fora do lugar).
Loudness: bodies ~-14,3 LUFS, hooks -15 a -20 → loudnorm dois passos no hook.

**Media Encoder por script (`app.encoder.encodeSequence`) não grava no Drive da H&W:** o caminho chega deformado
("H&W - Edição de Vídeo" vira "H__E__W - Edic'ao de Video") e todos os jobs falham com "destino de saída não foi
encontrado" (log em `~/Documents/Adobe/Adobe Media Encoder/26.0/AMEEncodingErrorLog.txt`, UTF-16). Renderizar em
pasta local ASCII (`~/Movies/<job>_EXPORT/ADxx/`) e copiar para EXPORT depois. Preset H.264 padrão:
`…/MediaIO/systempresets/4E49434B_48323634/01 - Match Source - High bitrate.epr` (o "Adaptive" do Frame.io veio
com metadado HLG/PQ).
Replicar edição do usuário numa sequência para outras: clonar a sequência-modelo, trocar V1/A1, `clip.move(delta)`
nos elementos da emenda — mas a **transição de áudio NÃO acompanha** `clip.end`; remover pela QE e recriar com
`addTransition(tr,false,"00:00:06:05","00:00:00:00",1.0,false,false)` (alinhamento 1.0 = termina no fim do clipe).

**Rodada 2 do 128_PG (pedido do usuário): hook de demonstração COMEÇA NA AÇÃO.** HK4/6/7/8 passaram a abrir no frame B
(já derramando o mel), com a fala 1 por cima da ação — não mais "fala com o prop → depois derrama". Padrão para os
próximos. Continuidade entre dois clipes: o 2º começa no **último quadro do 1º** (`LAST:<clip>` no anim.py, extrai com
`ffmpeg -sseof -0.1`) e termina no frame C. Insert de dado (aparelho 192/118) = frame próprio + clipe mudo de 5 s,
sobreposto no hook decupado nas palavras do número (Whisper), dissolve de 0,12 s.
Armadilha da decupagem: com a cauda protegida (`KEEP_TAIL`), o som do mel caindo virava "trecho sem fala" e era
descartado — a cena da perna sumiu. Correção: último trecho do clipe protegido vai sempre até o fim.
Voz: guardar a voz original do 1º clipe de cada personagem como `<PERSONAGEM>_voz_referencia.mp4` antes de regerar,
senão a nova versão vira referência e a voz do hook muda de novo.
