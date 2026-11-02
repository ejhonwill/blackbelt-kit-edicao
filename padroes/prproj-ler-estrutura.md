---
name: prproj-ler-estrutura
description: Como ler a estrutura real de uma sequência do Premiere pelo .prproj (gzip+XML) — a cadeia de referências que não é óbvia
metadata:
  type: reference
---

Quando o MCP só lê a sequência **ativa** e é preciso saber o que tem dentro de sequências
aninhadas (BLOCO 1..N dentro de uma PARTE), dá pra ler o `.prproj` sem tocar no Premiere e sem
trocar a sequência ativa — que é o caminho seguro quando a tarefa proíbe alterar o projeto.

```sh
cp projeto.prproj /tmp/p.prproj
python3 -c "import gzip;open('/tmp/p.xml','w').write(gzip.open('/tmp/p.prproj').read().decode())"
```

## A cadeia de travessia (me custou 3 parsers errados em 11/09/2026)

Duas famílias de referência convivem: `ObjectID`↔`ObjectRef` **e** `ObjectUID`↔`ObjectURef`.
Um deref que só trata a primeira devolve `None` no meio do caminho e a lista sai **vazia sem erro**.

```
Sequence[ObjectUID]
  └─ TrackGroups
       └─ TrackGroup            ← NÃO é o grupo; é um par
            ├─ First            (GUID do tipo de mídia)
            └─ Second[ObjectRef] → VideoTrackGroup | AudioTrackGroup
                 └─ TrackGroup
                      └─ Tracks
                           └─ Track[ObjectURef] → VideoClipTrack | AudioClipTrack
                                └─ ClipTrack
                                     └─ ClipItems          ← a pegadinha
                                          └─ TrackItems
                                               └─ TrackItem[ObjectRef]
                                                    └─ Video/AudioClipTrackItem
                                                         ├─ ClipTrackItem/TrackItem/{Start,End}  (ticks)
                                                         └─ SubClip[ObjectRef] → o conteúdo
```

Os dois erros que fazem o parser devolver zero itens calado:
- pendurar em `TrackGroup` direto em vez de seguir o **`Second`**;
- procurar `TrackItems` sob `ClipTrack` — ele está sob **`ClipTrack/ClipItems/TrackItems`**.

Ticks → segundos: dividir por **254016000000** (mesma constante de
[[premiere-script-ticks-e-corte-do-movimento]]).

Para o nome do clipe, descer pelo `SubClip` testando em ordem `Sequence` (sequência aninhada,
resolve pelo `Name`), depois `ActualMediaFilePath`, depois `Name`, e só então recursão nos
filhos. Sem o teste de `Sequence` primeiro, sequência aninhada volta como "?".

⚠ **O que esse arquivo NÃO responde:** o estado de **mudo** das trilhas. Não há `<Muted>` nem
propriedade equivalente legível. Se a pergunta for "essa A2 está muda?", o `.prproj` não serve —
ou se pergunta ao usuário, ou se marca como verificação pendente. Não afirmar que está aberta.

Marcador também não aparece aqui como tag `<Marker>`: procurar **`<DVAMarker>`**
(ver [[toolspro-chaves-de-retorno]]). Zero ocorrências = projeto sem marcador nenhum,
em qualquer sequência — é a forma barata de provar que não há nada manual a preservar.

## Por que isso vale a pena

Comparar a duração da sequência aninhada com a duração do arquivo-fonte revela **buraco de
montagem** que nenhuma leitura da timeline mostra: na PARTE 1 da VSL CardioFlush, o BLOCO 7
durava 90,24 s com locução de só 60,44 s — 30 s de timeline parada logo depois do ponto alto do
mecanismo, porque as reações encadeadas esticaram o bloco. Só apareceu no `ffprobe` dos fontes
contra o `End` lido aqui.

Ver [[toolspro-chaves-de-retorno]], [[premiere-qe-transicoes-efeitos]].
