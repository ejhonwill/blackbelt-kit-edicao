---
name: premiere-modo-mesclagem-valores
description: "Valores numéricos do 'Modo de mesclagem' no Premiere 26.3 (Screen=22, Add=14) e como identificá-los por medida"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 3ebbf125-7ecd-48e7-9f89-88b9b84c3c6e
  modified: 2026-08-21T15:10:05.993Z
---

Medido ao vivo em 21/08/2026, Premiere 26.3.2, montando as transições por asset
do Tools PRO.

O modo de mesclagem de um clipe vive na propriedade **"Modo de mesclagem"** do
componente **`AE.ADBE Opacity`**. É um número, e **não é o índice da lista da
interface**: o padrão "Normal" já vem como **18**.

## Tabela (confirmada por quadro renderizado, não por suposição)
| valor | modo |
|---|---|
| 18 (padrão), 12, 7, 6 | Normal |
| 3  | Escurecer (Darken) |
| 17 | Multiplicar (Multiply) |
| 2, 26 | Superexposição de cor (Color Dodge) |
| **11** | Clarear (Lighten) |
| **14** | Subexposição linear / **Add** (Linear Dodge) |
| **22** | **Tela (Screen)** ← o certo para overlay de luz com fundo preto |

Valores de 19 pra cima em geral voltam como identidade (o quadro sai igual à
base), então **não** servem: parecem "funcionar" e não fazem nada.

## Como identificar sem adivinhar
Comparar aparência não resolve — vários modos parecem iguais num flash branco
sobre preto. O que separa é um **cinza 50% sólido sobre uma cor conhecida**,
porque aí cada fórmula dá um número diferente e previsível:
- base (236,41,58) com overlay (128,128,128):
  Screen→(246,148,157) · Add→(255,169,186) · Lighten→(236,128,128) ·
  Multiply→(118,21,29) · ColorDodge→(255,82,116) · Normal→(128,128,128)
Gerar o cinza com `ffmpeg -f lavfi -i color=c=0x808080`, pôr numa trilha acima,
varrer os valores e exportar o quadro com `qeSeq.exportFramePNG` (ver
[[premiere-qe-transicoes-efeitos]]). **Amostrar o CENTRO do quadro**: clipe
vertical em sequência horizontal tem tarja preta que envenena a média.

## Onde isso importa
Overlay de luz (flash, light leak, film burn) do Baú dos Black Belt é H.264 com
**fundo preto e sem alpha** — sem Screen (22) o clipe de baixo some. Ver
[[bau-dos-black-belt-acervo]].

## Volume de clipe de áudio (mesma sessão, mesma máquina)
A propriedade **"Nível"** do componente **Volume** (`Internal Volume Mono`) não é dB
nem porcentagem. Medido escrevendo e lendo de volta:

    v  = 10^((dB - 15) / 20)        dB = 20 * log10(v) + 15

- clipe intocado = **0,177827939** (= 10^-0,75) → exatamente **0 dB**
- 0,0891 → −6 dB · 0,0316 → −15 dB · 0,5 → +9 dB
- **teto 1.0 = +15 dB**; escrever 2.0 é grampeado para 1.0 **em silêncio**

Cuidado com a fórmula errada `10^(dB/20)/15.8489` (teto +24 dB): ela põe tudo
**9 dB abaixo** do pedido e a escrita "funciona", então o erro não aparece em teste
de leitura — só no ouvido.
