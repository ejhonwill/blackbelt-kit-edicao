# Padrão visual validado — Upsell DR 1:1 (MemoFlow, 17–18/09/2026)

Tudo abaixo foi **aprovado no render pelo Jhon** e medido de volta do projeto. Os valores são os que
estão no `.aep` `[160926][OT] Upsell #1 [MemoFlow] [Squad]`; a comp `MASTER_LETTERING_MEMOFLOW` é a
referência viva do lettering. Quadro 1080×1080, 25 fps.

## 1. Lettering (cartelas de destaque) — imagem 1 é o mestre

| item | valor |
|---|---|
| Fonte | `Montserrat-ExtraBold`, CAIXA ALTA, tracking −14, alinhamento pelo bloco (X=540) |
| Corpo | base 96 px, reduz de 5 em 5 até o bloco caber em **900 px** (mín. 56) |
| Hierarquia | linha que carrega o azul = principal; a outra a **62%** dela; entrelinha 1,06× |
| Cores | branco `[1,1,1]`; UMA expressão em azul da marca **`[0.40,0.44,1.0]`** (= #3E44AA luminoso) |
| Deep Glow 2 (`PEDG2`) | branco: raio **28** / exposição **0,40** · azul: raio **78** / exposição **1,35** (props 24 e 25) |
| Sombra (`ADBE Drop Shadow`) | opacidade 52, ângulo 135, distância 8, suavidade 14 |
| Fundo | footage do apresentador em **Z +400** (escala 100·(1500+400)/1500 = 126,7%; se o VIDEO base é 103,1 → 130,6), Box Blur **26**; sólido ESCURECER `[0.01,0.012,0.03]` em Z +300 a **78%** (cartela cheia) / **68%** (cartela sobre bloco de avatar, blur 20) / **66%** (take do produto); HALO azul `[0.26,0.32,1.0]` ADD, elipse **395×268** pena 215, Z +150, opacidade 26, blur 56 |
| Câmera | 50 mm → zoom **1500**, posição `[540,540,−1500]`, **Anchor Point = ponto de interesse = `[540,540,0]`** (zerar o anchor joga a câmera para a origem) |
| Controle | todas as palavras filhas de um nulo 3D `CTRL` em `[540,540]`, Z **+80 → −210** ao longo da comp; escala do nulo reduzida se largura·1,163 > **940** (margem) |
| Animação | animador de texto: opacidade 0, posição `[0,28,0]`, escala `[93,93,100]`; seletor **Units=index (2), Based On=words (3)**, smoothness 100, End=999; Start sobe 1 por palavra **no tempo em que ela é dita**, rampa 0,14–0,26 s, ease 18/84 |
| Luminância do fundo atrás do texto | alvo **≈ 67** (medido nas cartelas aprovadas; 59 a 74 aceitável) |

Regras: máx. 2–3 linhas; toda cartela tem exatamente uma expressão em azul; sem legenda corrida
onde há lettering (remover se ≥60% de sobreposição).

## 2. Legenda corrida

`HelveticaNeue-Bold` 54 px, tracking −8, centralizada em `[540,952]`; pílula branca (shape
retângulo arredondado, texto+56 × texto+34, cantos = altura/2) a **94%**; texto quase-preto
`[0.07,0.07,0.09]` aplicado por **efeito Fill** (o `fillColor` do TextDocument não persiste).
Largura máxima 980 px — reduz o corpo de 2 em 2 até caber (mín. 38). Grupos de até 4 palavras /
1,6 s, quebra em pontuação, fecha vão < 0,45 s. **Texto vem da copy, nunca do Whisper.**
Cada `LEG n` fica **imediatamente acima** da sua `PIL n` — reordenar **um par por vez**
(`leg.moveBefore(pil)`); mover em lote embaralha metade dos pares.

## 3. Sincronia com a fala (a lição mais cara)

1. Whisper `medium`, word timestamps. Ele **gruda a 1ª palavra em 0,00**: medir o início real da
   fala pelo envelope RMS (janela 10 ms, limiar = percentil 10 + 12 dB) e corrigir **só a 1ª
   palavra**. Nunca esticar a frase inteira — as demais já estão certas.
2. Lettering ancora no **texto inteiro da cartela** (difflib, janela ±5 s da âncora), palavra a
   palavra; janela de busca = palavras do card **+6** (a fala tem palavras que o card omite).
3. Legenda entra de 0,00 a −0,08 s **antes** da palavra — esse é o comportamento certo.
4. Provar sempre **transcrevendo o próprio render** e comparando; casador ingênuo mente com
   palavras comuns ("the", "your") — imprimir lado a lado e ler.

## 4. B-roll e cobertura

- Entrada: 44 px no ciclo direita→cima→baixo, escala 110%→base (fim em base·1,035), **Desfoque
  direcional** (`ADBE Motion Blur`) 46→0 em 0,34 s, eixo 90° lateral / 0° vertical, ease 18/85.
  Motion blur de comp ligado (180°).
- Corrente: o plano que entra **sobe por cima** do anterior (in = i−0,22, opacidade 0→100 até i);
  o anterior só corta quando o novo está cheio. Fade de 0,18 s **só** onde o apresentador volta
  (bloco de avatar). Pausas de fala < 0,9 s entre blocos de insert são emendadas.
- Cartela nunca estica além da própria comp (+0,75 s): quem encosta nela é o B-roll seguinte.
- Auditar lendo as chaves de opacidade de volta do projeto; buraco ≠ volta prevista.
- Kling reescreve rótulo: gerar still com o produto oficial em `--image-references` e a trava do
  produto **antes** do bloco de estilo; animar com câmera travada e trava explícita de rótulo.
  Frasco é cobalto (nunca âmbar/transparente).

## 5. Take do produto (menção ao MemoFlow)

Comp própria: fundo = apresentador Z +400 blur 0→26, ESCURECER 0→66, GLOW elipse 196×302 pena 165
blur 52 opacidade 0→32; frasco (pré-comp do recorte do Jhon, escala 82) vem de Z +1400/y 1185 →
overshoot Z −95/y 578 → Z −40/y 593 em **11 quadros**, Box Blur 22→0 resolvendo o foco, desfoque
direcional 44→0; lettering `CO-FOUNDER OF` (52 px) / `MEMOFLOW` (84 px azul) entra **na palavra**
e **sai quando a frase acaba**; frasco fica ~1,8 s a ~63% da altura e recua em 15 quadros.
Sem `SWEEP` (borda dura sobre o rótulo); light wrap 12%.

## 6. CTA final ("Click the button below…")

Preto + fita 3D a 28%; frasco 46% no alto (y 480→238, overshoot); bloco de 3 linhas (base 96,
MAXW 960) a partir de y 560: `CLICK THE BUTTON BELOW` / `to get your` (62%) / `TRIPLE-DOSE
TREATMENT` azul; seta chevron azul (Deep Glow 70/1,2) entra em "below", pulsa ±18 px a cada
0,42 s, **abaixo** do bloco (y = 3ª linha + base·1,55, máx. 985). Sem áudio dentro da comp.

## 7. Entrega

Master = uma comp com cada parte como comp aninhada (ordem da copy). Emendas com ~0,7 s de cauda +
~0,67 s de cabeça (≈ 12,5 s no filme): apertar para ~0,25 s quando aprovado. Loudness alvo
≈ −15 LUFS, pico ≤ −1,5 dBTP. Render `aerender` com `-OMtemplate "H.264 - Corresponder
configurações de renderização - 15 Mbps"` (nome localizado). No Premiere, entrar por
**Dynamic Link** (`importAEComps`) e colocar com `overwriteClip` — **lembrar que o item DL
carrega áudio vazio e sobrescreve a trilha de áudio**: remover o clipe de áudio dele e verificar.
