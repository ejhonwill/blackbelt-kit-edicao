---
name: lipsync-rotulo-reescrito-recolagem
description: "O wan3_0 reescreve o texto do rótulo no lip sync (25 de 27 clipes); a recolagem do frasco do still por rastreamento resolve de graça"
metadata:
  type: feedback
---

Medido em 17/09/2026 nos 69 lip syncs do MemoFlow Upsell #1.

**O problema:** `wan3_0` com `image_references` + `audio_references` preserva rosto, roupa, mãos e cenário, mas
**re-renderiza o texto miúdo do rótulo do produto**. Dos 27 clipes com frasco na mão, só **2** mantiveram
"MemoFlow" legível; os outros saíram "MemoAtes", "MameoFlore", "Memo O'Cline", "MeusoFlonr". Não adianta pedir no
prompt ("the label must never change") — a corrupção é da regeneração de pixel, não de intenção.

`wan3_0_prime` (45 créditos/clipe contra 28) **segura a marca** nos mesmos clipes que falharam, mas ainda borra as
linhas finas ("Cognitive Support Formula"). Melhora, não resolve, e custa ~1.200 créditos num job de 27 clipes.

**A solução que funciona, de graça: recolar o frasco do still aprovado por cima do vídeo.**
A câmera é travada e a mão quase não se mexe, então:
1. Recorta do still aprovado (redimensionado ao tamanho do vídeo) uma caixa generosa com frasco + mão.
2. Por quadro, `cv2.matchTemplate(TM_CCOEFF_NORMED)` do miolo dessa caixa contra uma janela de ±90 px ao redor da
   posição original. **A FORMA azul sobrevive mesmo quando o TEXTO se corrompe**, então o casamento é confiável:
   medi 0,94–0,96 de correlação em todos os 27, com deslocamento máximo de ~32 px.
3. Cola o recorte limpo no deslocamento medido, com máscara de borda suavizada (gaussiana, ~10 % do lado).
4. Reencoda em h264 CRF 16 (o `mp4v` do OpenCV degrada).
Resultado: rótulo pixel a pixel igual ao aprovado, sem emenda visível, custo zero. Script `recolar_frasco.py`.

**Corolário para o futuro:** em qualquer talking head com produto na mão, planejar a recolagem desde o começo e
**não gastar crédito regerando por causa de rótulo**. Só regerar por rosto, boca ou pose.

Ver [[wan3-lipsync-avatar]], [[memoflow-produto-mockups]], [[gif-camera-travada-peso]].
