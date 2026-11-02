---
name: whisper-passada-longa-inventa
description: Whisper small numa passada longa duplica/desloca segmentos — reverificar todo achado com trecho curto + medium
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1c2c4d82-ef6f-4e54-a0f4-a0360b6c9134
  modified: 2026-08-17T16:35:08.737Z
---

Nunca afirmar ao Jhon que existe falso começo / take repetido / linha duplicada com base **só** numa transcrição Whisper `small` do arquivo inteiro. Reverificar cada achado extraindo o trecho (`ffmpeg -ss X -t Y`) e rodando `--model medium --word_timestamps True`.

**Why:** na VSL de upsell do Bifi (8 min), a passada `small` do arquivo completo inventou um take de fechamento que não existia (contei 3, eram 2) e reportou a frase "duas coisas que eu preciso te falar com clareza" duas vezes quando ela aparece uma só. Os dois erros foram repassados ao usuário antes de eu conferir — e cada um mudava a decisão de edição dele. A passada `small` longa também arredonda timestamps pra segundo inteiro, inútil pra definir ponto de corte.

**How to apply:** fluxo em duas etapas — `small` no arquivo inteiro só pra **localizar** regiões suspeitas, depois `medium` + `--word_timestamps True` em janelas de ~20s pra **confirmar e cronometrar**. Cortar usando o `end` da última palavra boa e o `start` da primeira palavra do take escolhido, com as margens da receita (0,34s depois / 0,42s antes).

Pegadinha de formatação que também me fez reportar timecode errado: `f"{t/60:.0f}"` **arredonda** o minuto (7:34 saiu como "8:34"). Usar `int(t//60)`.

**ATUALIZAÇÃO 17/08/2026 (aula do Roque, 56 min, `large-v3-turbo` no mlx):** o problema não é o tamanho do modelo, é a **passada longa em cima de silêncio** — e o árbitro é o **nível do áudio, não outro modelo**.

- A passada longa **inventa palavras dentro do silêncio**, com duração fixa suspeita ("E" com exatamente 1,4 s, "aí" com 4,7 s, "Obrigado."). Isso reprova falsamente o QC de "não cortou palavra": 57 palavras apareciam dentro dos cortes, e medindo o áudio naquelas janelas o pico ia de **−33 a −90 dBFS** (RMS até −99) — silêncio puro. Nenhum corte havia pegado fala.
- **Como provar de verdade:** para cada palavra que cair dentro de um corte, medir pico/RMS do trecho no WAV. Fala real fica acima de −26 dBFS de pico; abaixo disso é alucinação, e aí não precisa reabrir o corte.
- Numa janela de 24 s quase toda silenciosa, o `large-v3-turbo` entrou em **loop**: repetiu "Beleza tudo." ~30 vezes. `condition_on_previous_text=False` não impede.
- Corolário útil pra editar aula: **buraco na narração com áudio ALTO não é pausa** — é playback do material gerado rodando na tela (vídeo/voz em outro idioma, que o Whisper não transcreve). Classificar buraco por nível antes de chamar de pausa: quieto = pausa a apertar, alto = conteúdo que não se corta.
- Detector automático de gaguejo/repetição rende quase só falso positivo em aula falada: de 11 "gaguejos", os que conferi eram fim de frase ("...pra ele. Ele vai..."), "blá blá blá" dito de propósito e fragmento de fala em inglês do playback. Conferir um por um em janela curta antes de reportar; de 9 "repetições", 5 eram reforço pedagógico intencional.


**ATUALIZAÇÃO 11/09/2026 (VSL CardioFlush, `faster-whisper` medium):** o `medium` também
**OMITE** — não só inventa. Num bloco de 37 s ele colapsou "cardiologist increases the dose of
your medications" numa única palavra `your` com **2,66 s de duração**, e a frase sumiu da
transcrição. Eu ia reportar ao Jhon um trecho da copy ausente na gravação. O `large-v3` no mesmo
recorte devolveu a frase inteira: estava lá o tempo todo.

**How to apply:** palavra com duração absurda (>1,5 s numa fala corrida) é **bandeira de trecho
engolido**, não de pausa. Antes de afirmar que a copy não foi gravada, recortar a janela com
`ffmpeg -ss/-to` e repassar com `large-v3`. Afirmar ausência de fala é caro: manda regravar
locução que existe.

Relacionado: [[corte-lossless-master-all-i]], [[aula-roque-obs-empilhado-16x9]]
