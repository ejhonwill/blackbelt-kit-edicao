---
name: ae-camera-3d-armadilhas
description: "As 6 armadilhas de montar cena com câmera 3D real no AE por ExtendScript — ordenação por Z, rig acumulativo, lettering que viaja, glow que vira magenta, contador borrado e faixa com corte reto"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b64e22fc-7714-4cbf-bcec-82769710861e
  modified: 2026-09-12T18:39:17.114Z
---

Quando a comp tem câmera 3D de verdade (não simulação por escala), estas seis coisas quebram e
custam uma rodada de render cada:

1. **Camada 3D é ordenada por Z, não pela pilha.** Um plano de B-roll atrás do apresentador (z maior)
   não aparece, mesmo estando acima na timeline. Camada 2D no meio quebra o grupo 3D e muda tudo —
   por isso um plano aparece e o outro não, sem padrão aparente. Solução confiável: **apagar o
   apresentador por opacidade** na janela do B-roll, não confiar em ordem nem em Z.
2. **Movimento de câmera tem que ser absoluto.** Somar delta a cada trecho (`valor + dz`) acumula:
   em 18 trechos o rig chegou a +1240 e o enquadramento virou um close no microfone. Escrever
   posição-alvo por trecho, com um keyframe HOLD um quadro antes para o corte ser seco.
3. **Lettering 3D viaja com a câmera e sai do quadro.** Prender o texto ao `NULL_CAMERA_RIG`: ele
   continua 3D (ganha profundidade e DOF) mas fica estável na tela, que é o que a referência faz.
   A posição do filho passa a ser relativa ao rig — descontar `[W/2, H/2]`.
4. **Glow em texto vermelho puxa pro magenta.** `#F62542` com glow saiu `#F12681`; sem glow saiu
   `#EB233E`. Guardar o glow para o amarelo fluorescente e deixar o vermelho limpo.
5. **Contador + motion blur = dígito fantasma.** O AE amostra sub-quadros e o número muda em cada um,
   então empilha algarismos diferentes. Desligar motion blur na camada do contador.
6. **Desfoque com "repetir pixels da borda" em máscara de shape cria corte reto.** A faixa escura do
   rodapé ficou com uma linha horizontal nítida. Desligar `repeat edge pixels` no Gaussian Blur da
   matte.

Duas a mais, de API: **"Saturação mestre" do Matiz/Saturação não aceita keyframe** nesta versão
(usar Tint / Quantidade a matizar); e **adicionar um segundo efeito invalida a referência do
primeiro** — pegar as propriedades pelo Effect Parade depois de montar todos os efeitos.

**Why:** na VSL CardioFlush (12/09/2026), BLOCO 01, cada uma dessas apareceu só no quadro exportado,
nunca no retorno da API — o script dizia "OK" com o B-roll invisível e a câmera fugindo.

Relacionado: [[skill-motion-viral-jhon1]], [[vsl-cardioflush-premium-v02]], [[ae-mcp-armadilhas]]
