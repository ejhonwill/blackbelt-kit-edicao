---
name: motion-insert-armadilhas
description: "Armadilhas de animar insert com ffmpeg — alpha descartado, apresentação aplicada duas vezes, prévia sem repintar"
metadata: 
  node_type: memory
  type: project
  originSessionId: 04f0496b-9465-4207-8b49-1e1eda40d954
  modified: 2026-08-17T12:13:28.092Z
---

Motor de animação de insert do adrun-creative-studio (`nucleo/motion.py`, criado em 17/08/2026). Três armadilhas que só aparecem no vídeo pronto:

**1. Alpha morre no encode.** Estilo de máscara/revelação feito com `geq` no canal `a` sai sem efeito nenhum: o encode final é `yuv420p` e descarta alfa, então o clipe renderiza inteiro visível desde o primeiro quadro. O teste "renderizou sem erro" passa. Máscara tem que ser **composta** sobre um `color=c=black` com `overlay` dentro do mesmo filtergraph.

**2. Apresentação aplicada duas vezes.** Se o estilo de motion já desenha o recorte/janela do template (`recorte_animado`, `colagem`), o compositor aplica a apresentação de novo por cima — dá recorte dentro de recorte, que na tela aparece como cartão branco quase vazio. Resolvido com `motion.EMBUTE_APRESENTACAO` + flag `sem_apresentacao` no shot, respeitada em `render.py` E no compositor do editor.

**3. Prévia não repinta quando a mídia fica pronta.** `<video>`/`<img>` de B-roll levam alguns quadros para decodificar; se nada escuta `onloadeddata`/`oncanplay`/`onseeked`/`onload`, parar o playhead sobre um insert mostra preto até o usuário mexer de novo. Parece bug de composição e não é.

Bônus: `zoompan` precisa de upscale antes (senão o zoom vira mosaico) e a expressão deve usar `on` (índice do quadro de saída), não `zoom+incremento` — acumular impede easing.

Relacionado: [[nano-banana-deriva-fotorreal]], [[chrome-debug-zumbi]]

**Tela desenhada sobre celular em vídeo (HyperFrames, 349_BM 30/10):** se o vídeo e a tela por cima recebem push-in em elementos separados, a tela treme (Jhon reprovou: "recortes no celular trêmulos"). Medir o retângulo branco quadro a quadro (OpenCV, limiar >215), encaixar a tela sem rotação com 2 px de sobra e travar a câmera nessas cenas.
