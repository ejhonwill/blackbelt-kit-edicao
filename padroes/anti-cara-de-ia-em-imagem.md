---
name: anti-cara-de-ia-em-imagem
description: "O que tira a cara de IA/stock de uma imagem gerada — e o conflito entre o bloco de realismo e a trava de rótulo"
metadata:
  type: feedback
---

Em 12/09/2026 o Jhon reprovou um lote de idosos segurando frasco: *"ficou muito fake, parece muito
IA"*. As specs de câmera da [[specs-camera-photorealismo]] sozinhas **não bastam** — elas dizem
"isto é uma foto", mas não impedem o modelo de entregar **stock photography**: pele lisa, dente
branco, luz perfeita, cenário arrumado, sorriso posado.

**O que virou a chave** (bloco anti-stock, além das specs):

- **Assumir a falha.** "not a stock image, not a commercial shoot, not an AI render", cômodo
  vivido com bagunça pequena, tinta descascada, objeto torto, poeira; roupa amassada, com bolinha
  de pilling e gola sem forma.
- **Luz errada de propósito.** Uma janela **realmente estourada**, queda de sombra real, dominante
  de cor de uma parede próxima, duas temperaturas brigando no rosto.
- **Rosto assimétrico e item a item.** Um olho menor e mais baixo, sobrancelha desigual com fio
  solto, capilar rompido na bochecha e na asa do nariz, tom de pele manchado, mancha senil,
  acrocórdon, dente **marfim** e não branco com borda desigual, lábio seco com linha vertical.
- **Mãos.** Veia saltada, tendão, pele frouxa no nó do dedo, articulação engrossada, unha estriada.
- **Emulsão.** Grão 35 mm fino, vinheta leve, aberração cromática na borda, e **filme nomeado**
  (Portra 400/160, Gold 200, Pro 400H, Superia 400) em vez de "cinematic".
- **Negar o acabamento.** "no beauty filter, no HDR glow, no digital sharpening halo, no glossy
  plastic sheen, no teal-and-orange grade".

**A armadilha que custou uma rodada:** esse bloco é longo e **afoga a trava de rótulo** se vier
depois dela — o modelo devolveu rótulo verde com marca em caixa mista. A ordem que funciona é
**cena → bloco anti-stock → trava de produto ("THIS OVERRIDES EVERYTHING ABOVE") → frase
obrigatória de pele**. Trava de produto sempre por último, antes da frase final.

Dois efeitos colaterais do bloco: (1) "film grain" às vezes desenha uma **moldura preta de filme**
com borda irregular — detectar linha/coluna escura e recortar com margem de 25%; (2) pedido de
expressão candid faz a pessoa **olhar para fora e baixar o produto** — se for anúncio, exigir
"looking straight into the lens" e "bottle held upright at chest height, well clear of the body,
fully inside the frame".

Ver [[glucojaro-produto-rotulo]].

**09/10/2026 (LungTyde 239_MN, hooks):** de novo "tá muito fake" — eu tinha gerado os start frames *editando* as referências (que já eram IA). Refeito do zero com a gramática da photorealism + bloco anti-stock, referência só como guia de composição: aprovado. Regra: nunca editar referência de IA como start frame; sempre reescrever como foto.
