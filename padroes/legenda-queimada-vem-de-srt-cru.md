---
name: legenda-queimada-vem-de-srt-cru
description: Legenda queimada nos ADs sai de um SRT de transcrição automática não revisado — conferir palavra a palavra contra a copy
metadata:
  type: feedback
---

Nos criativos da H&W a legenda na tela é gerada a partir de um `.srt` que fica em
`MEDIA/<AD>/CAPTIONS/` e é **saída crua de transcrição automática**, não a copy digitada.
O editor corrige alguns erros na hora de queimar e deixa outros passar.

Achado no VigorBoost 32_JV (21/08/2026): o AD05 foi ao ar com a palavra **"Byakuya"** na tela
onde a copy diz **"Viagra"** — nas três versões de hook. O `AD05 Copy.srt` trazia o mesmo erro
na entrada 46, junto com "pendant on Viagra", "Oh, may preparation", "is incompatible",
"For 1850 men", "our looking at you" e "what $1 billion industry". Essas seis foram corrigidas
na queima; só a "Byakuya" escapou.

**Como aplicar:** ao conferir legenda de AD, não confie em amostragem — puxe o `.srt` da pasta
CAPTIONS, compare linha a linha com a copy e depois confirme na tela os pontos onde o SRT
divergia. Nomes próprios, números e negativas ("isn't" → "is") são onde a transcrição erra e
onde o erro mais custa.

Vale também o inverso: **áudio e legenda podem divergir**. No AD04 a legenda dizia "buddy"
(certo) e a locução falava "body". Só se pega transcrevendo o áudio e comparando com o que
está queimado.

Ver [[whisper-passada-longa-inventa]] e [[padrao-resumo-criativo-ad]].
