---
name: premiere-qe-transicoes-efeitos
description: "API real de transição, efeito e keyframe no Premiere 26.3 via QE DOM — o que funciona, o pin por clipe e o export de frame"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3ebbf125-7ecd-48e7-9f89-88b9b84c3c6e
  modified: 2026-08-21T14:00:33.708Z
---

Medido ao vivo em 21/08/2026, Premiere 26.3.2 PT-BR, pela porta de debug CEP
(painel Tools PRO, porta 8899), num projeto de teste dedicado.

## O que FUNCIONA (tudo verificado com leitura de volta)
- **Aplicar transição**: `qeItem.addTransition(trObj, addToStart, '00:00:00:15', '00:00:00:00', 0.5, false, false)`
  → devolve `true` e a transição aparece. `addToStart=false` põe no FIM do clipe.
  A assinatura curta (`addTransition(tr)` ou só com duração) **não** aplica.
- **Ler transição**: preferir a API pública `track.transitions` — devolve `name`,
  `start`, `end` limpos. A QE `numTransitions` **conta slots vazios**: filtrar por
  `type === 'Transition'` (numa trilha com 1 transição, `numTransitions` = 3).
- **Remover transição**: `qeTransition.remove()` → `true`.
- **Adicionar efeito**: `qeItem.addVideoEffect(efObj)` → `true`.
- **Remover efeito**: `qeItem.getComponentAt(i).remove()` → `true`. **Não existe**
  remoção pela API pública: `component.remove` é `undefined` em `clip.components[i]`.
- **Undo por script**: `qe.project.undo()` **existe** (função). `app.executeCommand`
  e `app.project.undo` não existem.
- **Trilha travada**: `track.isLocked()` / `track.setLocked()` na API pública.
- **Exportar frame renderizado**: `qeSeq.exportFramePNG(timecode, caminho)` — o
  timecode sai de `qeSeq.CTI.timecode` depois de `seq.setPlayerPosition(ticks)`.
  **Ele acrescenta `.png` ao caminho** (passar `x.png` gera `x.png.png`).
  `seq.exportFramePNG` (pública) não existe. É a prova visual barata — usar sempre,
  porque [[pr-captions-mogrt]] já ensinou que gravar e ler certo não prova que renderiza.

## ⚠ REVISTO 04/10/2026 (Premiere 26.5): o "pin" era leitura errada
`addVideoEffect` põe o efeito novo no TOPO da pilha (logo depois do Movimento), não no fim.
Quem lê `components[numItems-1]` acha o efeito ANTIGO e conclui que o Premiere "repetiu o
primeiro". Medido: Tint e depois Espelho no mesmo clipe → Opacity, Motion, **Mirror, Tint**.
Achar o componente novo pela DIFERENÇA das listas de matchName antes/depois (pr-copiar 1.7.4).
Código antigo que remove `numComponents-1` (txCompGeo do pr-transicoes, no caso de efeito de
terceiro) pode tirar o efeito errado. O texto abaixo fica como histórico.

## A ARMADILHA: o pin de efeito é POR CLIPE
`qe.project.getVideoEffectByName(nome)` lê o nome certo (`.name` volta preenchido),
mas **depois do primeiro `addVideoEffect` num clipe, todo add seguinte NAQUELE clipe
re-adiciona o primeiro efeito**, ignorando o objeto passado. Persiste entre chamadas
separadas de `evalScript`. Não adianta `app.enableQE()`, reobter `qe.project`,
reobter a sequência, nem chamar `getVideoEffectList()`.
- Adicionar em **outro clipe** funciona normal.
- Um `qeComponent.remove()` naquele clipe **limpa o pin**.
Consequência de projeto: **um efeito por clipe**. Por isso as transições próprias do
Tools PRO são construídas em cima de UM efeito só.

## O efeito que resolve sozinho: `AE.ADBE Geometry` ("Transformar")
Propriedades, todas com keyframe: Ponto de ancoragem, Posição, Dimensionar
altura/largura, Inclinação, Eixo de inclinação, Rotação, Opacidade,
**Utilizar ângulo do obturador da composição**, **Ângulo do obturador**, Amostragem.
O ângulo do obturador dá **motion blur de verdade** (desligar "Utilizar ângulo da
composição" antes). Com esse único efeito saem whip, slide, push, zoom, spin e
motion blur — tudo nativo Adobe, sem depender de plugin de terceiro.

## Nome de efeito mente — resolver por matchName
`getVideoEffectByName` devolve **objeto válido para qualquer nome**, inclusive
inventado; o discriminador é `.name` vir preenchido. Pior: nesta máquina há
**Film Impact** e outro pacote instalados, e eles **tomam o nome curto**:
- "Desfoque direcional" → `AE.Impact_Directional_Blur_FX` (terceiro, comercial)
- "Desfoque direcional (herdado)" → `AE.ADBE Motion Blur` (nativo Adobe)
- "Divisão de RGB" → `AE.Impact_RGB_Split_FX` · "Giro" → `AE.Impact_Spin_FX`
- "Transformar" → `AE.ADBE Geometry` · "Deslocamento" → `AE.ADBE Offset`
- "Distorção de lente" → `PR.ADBE Lens Distortion`
**Sempre conferir `matchName` depois de aplicar** e exigir prefixo `AE.ADBE`/`PR.ADBE`,
senão o plugin fica dependendo de software comercial que o aluno não tem.
`qe.project.getVideoEffectList()` devolve os **192 nomes** disponíveis (só strings,
sem matchName) — serve para saber o que existe naquela instalação.

## Nomes reais de transição nesta instalação (PT-BR)
Válidos: `Dissolução cruzada`, `Dissolução de filme`, `Dissolução aditiva`,
`Dissolução não aditiva`, `Zoom cruzado`, `Deslizar`, `Empurrar`,
`Transição para preto` (= Dip to Black), `Persiana`.
⚠ CORRIGIDO em 16/09/2026: **Morph Cut existe e chama `Recorte de metamorfose`**
nesta instalação — o nome que eu tinha testado ("Corte morphing") é que estava
errado. `getVideoTransitionList()` devolve 110 nomes e é a forma de descobrir o
nome real em vez de adivinhar (boa parte dos 110 é de plugin de terceiro —
Film Impact e afins — então continuar exigindo prefixo Adobe).

Inválidos (testados): "Esmaecer para preto", "Imersão em preto", "Corte morphing",
"Íris…", "Cortina", "Virar página". Como o nome é localizado e frágil, o catálogo
deve ser **descoberto em runtime** pelo critério do `.name`, não escrito fixo.

## Keyframe
Vale a receita já provada do `pr-zoom`: os tempos de keyframe são em **SOURCE time**
(`clip.inPoint.seconds` … `clip.outPoint.seconds`), não em tempo de timeline.
`prop.setTimeVarying(true)` → `addKey(t)` → `setValueAtKey(t, valor, 1)`.
Propriedade de 2 valores (Posição) aceita array `[x,y]`, normalizado (0.5,0.5 = centro).

Ver [[premiere-script-ticks-e-corte-do-movimento]] (timebase real, recorte do
Movimento), [[premiere-legendas-api]] (`captionTracks` continua ausente) e
[[toolspro-chaves-de-retorno]].

## Mais três armadilhas (medidas em 21/08/2026 construindo o módulo)
- **`track.setLocked` exige INTEIRO, não booleano.** `setLocked(true)` levanta
  "Illegal Parameter type"; `setLocked(1)` / `setLocked(0)` funcionam.
  `isLocked()` devolve booleano normal. Se o `true` for engolido num try/catch,
  a trava de trilha vira proteção que nunca liga.
- **`seq.clone()` TROCA a sequência ativa para a cópia.** Fazer snapshot antes de
  uma operação e sair aplicando manda tudo para a cópia — a sequência do usuário
  fica intacta, o oposto do que ele pediu, e sem aviso nenhum. Depois de clonar,
  reatribuir `app.project.activeSequence = original` e CONFERIR pelo `sequenceID`.
- **Achar a cópia por índice não funciona.** `app.project.sequences` não vem na
  ordem de criação; `sequences[n-1]` pegou a ORIGINAL e o código renomeou a
  sequência do usuário achando que era a cópia. O jeito seguro é guardar o
  conjunto de `sequenceID` ANTES do clone e procurar o que apareceu.

## Remover keyframe: reler getKeys() a cada volta
Guardar `var ks = pr.getKeys()` e remover de trás pra frente **falha calado** —
os Time do array ficam velhos e o `removeKey` não faz nada, mas a função devolve
"removi". O laço que funciona é o mesmo do `pr-zoom`:
`while (pr.getKeys().length > 0) pr.removeKey(pr.getKeys()[0]);`

## Índice de clipe: o da API pública NÃO serve para a QE
A QE DOM conta os **buracos** da trilha como itens (`type === 'Empty'`). Numa trilha
de legendas (cheia de intervalos), os índices públicos 0,1,2 correspondem aos da QE
**1,3,5** — e `getItemAt(0)` devolve um vazio. `addVideoEffect` num item vazio **não
faz nada e não levanta erro**: a animação simplesmente não aparece.
Numa trilha de vídeo com clipes encostados os índices batem por acaso, então o
problema só surge quando há buraco. **Casar sempre por TEMPO DE INÍCIO:**
```js
var qt = qe.project.getActiveSequence().getVideoTrackAt(v);
for (var i=0;i<qt.numItems;i++){ var it=qt.getItemAt(i);
  if (String(it.type)!=='Clip') continue;
  if (Math.abs(Number(it.start.secs) - inicioDoClipePublico) < 0.05) return it; }
```

## MOGRT: inPoint/outPoint mentem sobre a duração
Num clipe de Motion Graphics, `clip.inPoint`/`clip.outPoint` devolvem a duração
**INTEIRA do template** (10s), não o trecho aparado. Um bloco de legenda de 1,9s na
timeline lê `in=0.000 out=9.977`. Como keyframe de clipe usa SOURCE time, confiar
nisso joga a animação de SAÍDA para ~9,8s — fora do que o clipe mostra. Ela nunca
renderiza, e nada acusa erro.
Usar a duração da TIMELINE como teto:
`if ((out-in) > (end-start)) fim = in + (end-start);`

## Reentrância: polling de painel PENDURA o Premiere
Confirmado de novo em 21/08/2026, e desta vez eu causei. Há **uma** thread de
ExtendScript. Durante uma operação longa (`importMGT`, que acorda o After Effects
headless), todo `evalScript` novo entra na fila. Um painel com `setInterval` de 4s
empilha centenas de chamadas e o Premiere trava de vez — 30 min sem responder, AE e
PR a ~80% de CPU, sem diálogo e sem crash. Só sai com `kill -9` (e apagar o
`.prlock` órfão antes de reabrir).
Uma flag `ocupado` **não basta**: ela só conhece as operações do próprio painel.
A guarda tem que ser sobre a CHAMADA — contador de requisições em voo, e o polling
só dispara com o contador zerado.
**Para carimbar MOGRT sem risco**: importar o `.mogrt` UMA vez e usar
`track.overwriteClip(projectItem, ticks)` nos demais — isso é instantâneo e não
acorda o After Effects. Só o `importMGT` acorda.
