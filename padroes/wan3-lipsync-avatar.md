---
name: wan3-lipsync-avatar
description: "Receita de talking head com lip sync no Higgsfield: wan3_0 com image_references + audio_references (start_image NAO combina)"
metadata:
  node_type: memory
  type: project
---

Levantado em 15/09/2026 recriando um criativo UGC do Instagram com avatar feminino.

**Nao existe modelo de talking head/lipsync dedicado** no catalogo do Higgsfield
(`higgsfield model list` nao tem speak/lip/talk/avatar). Quem faz lip sync a partir
de audio proprio: **`wan3_0`** e **`seedance_2_0`** — sao os dois que aceitam
`audio_references`.

## A receita que funciona (wan3_0)

```
higgsfield generate create wan3_0 --aspect-ratio 9:16 --resolution 1080p \
  --duration <inteiro 2..30> \
  --image  <still_da_cena.png> \
  --audio  <voz_da_cena.wav> \
  --generate-audio false \
  --prompt "<pessoa da imagem fala pra camera, lip-synced ao audio...>"
```

**Armadilha central:** `start_image`/`end_image` **nao combinam com midia de
referencia**. Usar `--image` (`image_references`), nunca `--start-image`. A
constraint aparece em `model get wan3_0` mas e facil passar batido.

`duration` e **inteiro**, 2 a 30 (ou -1 pra "smart"). Pedir o inteiro acima da
duracao da cena e aparar na timeline.

Com `--generate-audio false` o mp4 volta **sem faixa de audio** — o que e bom:
aplica-se a locucao original na montagem e a sincronia fica garantida, sem
depender do audio que o modelo devolveria.

## Consistencia de personagem sem Soul ID

Gerar 3 ancoras no `nano_banana_pro` (9:16, 2k), escolher uma, e usa-la como
`--image` em TODAS as cenas junto do prompt de acao. Prendeu face, cabelo, roupa,
brinco, cozinha e luz nas 8 cenas. Quando um adereco derivou (caneca de vidro
virou ceramica), resolveu passar **duas** imagens de referencia: a ancora + o
still da cena anterior, com a continuidade escrita em CAIXA no prompt.

## Filtro NSFW

Prompt de "abdomen com camada de gordura" (a metafora do criativo original) foi
**recusado 2x** como `nsfw` — com pele realista E com torso em argila. O status
volta literalmente `nsfw` no `generate get`, nao `failed`. Passou quando tirei o
corpo inteiro da cena: domo ceramico com gel ambar sendo dissolvido por po branco
entrega a mesma leitura visual.

## Escolher voz por medicao

As vozes preset nao expoem genero nem sotaque (`voices list --json` so tem
name/category/voice_type/status). Gerar a locucao inteira com 2-3 candidatas e
medir: **F0 mediana** por autocorrelacao (mulher ~165-255 Hz) e **palavras/min**.
Ritmo se acerta depois com `atempo` (1.14x passou despercebido). Sotaque continua
precisando de ouvido humano — avisar.

Ver [[higgsfield-cli-vs-mcp]], [[higgsfield-cli-saida-json]], [[nano-banana-deriva-fotorreal]].

## Áudio de referência acima de 15 s → "failed" mudo (10/10/2026, Divine Prayer)
De 10 hooks, só passou o de 14,0 s; todos de 15,9 a 27,5 s voltaram `status: failed` **sem motivo** (e sem cobrar), mesmo com `duration` folgado. Partir a locução **decupada** em fim de frase, com cada parte ≤ 14,5 s → passou. Montagem: p1 + p2 com punch-in de 1,10 no corte, mais a voz inteira por cima. A 1ª rodada também teve vários "no response received" com 10 jobs simultâneos: limitar a 3 por vez. Nos planos com duas pessoas, o prompt "the pope on the LEFT speaks… the bishop on the RIGHT stays completely SILENT with his mouth closed" funcionou (só o da esquerda mexeu a boca).
