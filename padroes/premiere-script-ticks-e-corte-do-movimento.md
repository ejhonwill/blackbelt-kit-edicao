---
name: premiere-script-ticks-e-corte-do-movimento
description: "Timebase real da sequência, o recorte escondido dentro do Movimento, e o que não existe na API do Premiere 26.3"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 4ab5b01e-3d7b-4dcf-80f4-ed33cbd94204
  modified: 2026-08-17T16:34:43.931Z
---

Levantado em 17/08/2026 montando a aula do Roque (Premiere 26.3.2, PT-BR, via porta
de debug CEP).

**1. O tick-por-frame da sequência não é 254016000000/fps.** Numa sequência de "30
fps" vinda de gravação de OBS, `sequence.timebase` = **8467191533**, não
8467200000 (fps real 30.00003). Se você verificar a timeline dividindo por
8467200000, TODO clipe aparece 1 frame curto e fora do grid — a montagem está
certa e a conta está errada. **Sempre ler `sequence.timebase` e usar esse valor.**
Passando ticks por `new Time()`, o Premiere encaixa no frame dele; o valor que
volta é múltiplo exato do timebase.

**2. O efeito Movimento já tem recorte embutido, e ele funciona.** O componente
`AE.ADBE Motion` expõe, além de Posição/Escala/Rotação, quatro propriedades que a
UI não mostra: **`Corte à esquerda` / `Corte superior` / `Corte à direita` /
`Corte inferior`** (em porcentagem, 0–100, relativas ao quadro inteiro do clipe).
Elas renderizam de verdade — conferido no Monitor de Programa. Isso dispensa
adicionar o efeito Recortar, que é justamente o que falha:
`qe.project.getVideoEffectByName("Recortar")` devolve objeto válido mas
`qclip.addVideoEffect(...)` **não adiciona nada e não levanta erro** — o clipe
continua com 2 componentes. Falha silenciosa clássica.
O recorte é aplicado ANTES da Escala/Posição, e a âncora continua sendo o centro
do quadro original (não do trecho visível) — é isso que faz a conta de Posição.

**3. `sequence.exportFramePNG` não existe** nesta versão (`is not a function`), e a
QE DOM também não expõe export de frame. Para provar visualmente o que está no
quadro: `sequence.setPlayerPosition(ticks)`, trazer o Premiere pra frente com
osascript e `screencapture -x`, depois recortar a região do Monitor de Programa.
Funciona e é a única prova real de que um efeito pegou.

**4. Remover clipes:** `pr_timeline_remover` do Tools PRO estoura o timeout de 120s
com 167 clipes numa trilha (mas a escrita acontece — reler antes de repetir). Pela
QE DOM sai rápido, iterando **de trás pra frente** e pulando item cujo
`type === "Empty"`: `for (i = track.numItems-1; i>=0; i--) it.remove(false,false)`.
`numItems` da QE conta os vazios; `clips.numItems` da API pública não.

Ver [[toolspro-chaves-de-retorno]], [[premiere-mac-via-cep-debug]] e
[[premiere-ptbr-nomes-de-efeito]].

**6. `overwriteClip` só posiciona certo com objeto `Time`.** `track.overwriteClip(item, "36.56")`
com o tempo em **string de segundos** é aceito sem erro e coloca o clipe no **0.00**, empilhando
os seguintes em sequência a partir dali — dá uma timeline inteira errada que parece certa no log.
O que funciona: `var t=new Time(); t.seconds=36.56; track.overwriteClip(item, t);`. Descoberto em
13/09/2026 colocando 56 motions na VSL do CardioFlush; os 9 primeiros foram parar todos no zero.
E **nunca `insertClip`** quando não se pode mexer na duração: ele faz ripple e empurra tudo.
Sempre ler de volta `start`/`end` do clipe posto e comparar `sequence.end` antes e depois.

**7. Marcador que termina no fim do bloco estica a sequência em 1 quadro.** Se a janela do marcador
fecha exatamente onde o conteúdo acaba, o clipe do AE (que o `aerender` arredonda para cima em 1
quadro) passa do fim e o Premiere cresce a sequência. Aparar o render **e** travar `clip.end` com um
`Time` explícito depois de posicionar. O Premiere também arredonda o ponto de entrada para cima, então
aparar o arquivo em 1 quadro pode não bastar — conferir lendo de volta, não calculando.

**8. Mídia sobrescrita no mesmo caminho fica em cache.** Regravar o `.mp4` no mesmo path deixa o
Premiere mostrando a duração ANTIGA do item. Para forçar mídia nova, importar com outro nome de
arquivo. `projectItem.remove()` em item de footage não é confiável; `bin.deleteBin()` apaga o bin
inteiro e resolve.

**9. `qe.removeTracks` apaga ÁUDIO junto — o 3º argumento não é uma flag.** Chamei
`removeTracks(1, idx, 1, 0, 0, 0)` achando que o terceiro parâmetro ligava a remoção de vídeo; ele é a
**contagem de trilhas de áudio a remover**. Resultado: apagou a trilha de vídeo vazia *e* uma trilha de
áudio em cada uma das 25 sequências onde rodou, levando a voz principal de blocos inteiros. Não levanta
erro. O sintoma só aparece onde o áudio passa do vídeo: `sequence.end` encurta (num bloco, 46,2 s → 25,08 s);
onde áudio e vídeo terminam juntos, **nada denuncia**. Conferir SEMPRE contagem de clipes de áudio e
`end` de cada trilha de áudio antes/depois, nunca só a lista de trilhas de vídeo. Testar em cópia antes.
Aconteceu em 13/09/2026 na VSL do CardioFlush; recuperado de versão salva 45 min antes.

**10. Script que troca de projeto salvando antes de fechar anula qualquer trava de "não salvar".** Meu
validador recusou `p.save()` em 2 projetos por ter divergido — mas o passo seguinte do laço abria o próximo
projeto com `app.project.save()` + `closeDocument`, e gravou o estado ruim assim mesmo. Para inspeção e
para qualquer operação arriscada, fechar com `closeDocument(0,0)` (não salva, não pergunta).

## overwriteClip SOMA o in-point da fonte ao tempo pedido (08/10/2026, Criativo ASTRON)
Com `projectItem.setInPoint(0.96,1)` antes, `track.overwriteClip(item, 17.60)` colocou o clipe em **18,52** (= 17,60 + 0,92).
Com in-point 0 cai certo — por isso passa batido. Sempre ler `clip.start` de volta e, se vier deslocado, remover e
recolocar em `tempo - delta`. Na mesma rodada um SFX já posicionado andou 0,16 s sem ser tocado: reler TODAS as
trilhas depois de colocar, não só a que mexi. Tela dividida nativa: efeito "Cortar" (`AE.ADBE AECrop`, props
Esquerda/Superior/Direita/Inferior em %) + Posição do Movimento normalizada [0.5,y]; cópia do avatar numa trilha
acima, as duas metades cobrem o quadro e a V1 original fica por baixo sem cortar.
