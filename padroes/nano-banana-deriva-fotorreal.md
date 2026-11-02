---
name: nano-banana-deriva-fotorreal
description: "Em história 3D, o nano_banana_pro abandona o estilo e volta pra fotorrealismo/vintage quando o plano é de ambiente"
metadata:
  type: feedback
---

Achado em 11/08/2026 na história 3D Pixar do AD06 (SlimSoda).

Nos planos **centrados no personagem** o estilo 3D segura. Nos planos onde o **ambiente
domina** (rua à noite, academia, churrasco de família, carro), o modelo larga o Pixar e
entrega **foto real** — e pior, escorrega para **noir anos 40, preto e branco e carro
antigo**, e ainda queima letreiro na fachada ("PALACE GYM", "OPEN 24 HRS").

**Why:** descrição de cenário puxa o modelo para o prior fotográfico; sem uma âncora visual
o bloco de estilo no fim do prompt não segura.

**How to apply:**
1. **Toda cena precisa de `--image-references` com um personagem 3D**, mesmo figurante.
   Criar âncora dedicada (ex.: DAWN, a espectadora) em vez de escrever "uma outra mulher".
2. Abrir o prompt com a trava dura, não só fechar com ela: *"A FRAME FROM A PIXAR 3D
   ANIMATED MOVIE. EVERYTHING in the frame — people, clothes, cars, buildings — is rendered
   in the SAME stylized 3D style. THIS IS NOT A PHOTOGRAPH."*
3. Somar época e texto: *"Present day, not vintage, not noir, not black and white. NO signs,
   NO banners, NO neon lettering."*
4. Espelho vira gêmea: exigir *"the mirror's frame must be visible"* ou saem duas pessoas.

Detector de colagem (`qc_colagem.py`) dá muito falso positivo — conferir na folha de
contato antes de regerar. De 36 suspeitos, só 4 eram colagem de verdade.

Ver [[broll-narrativo-armadilhas]] e [[historia-3d-pixar]].
