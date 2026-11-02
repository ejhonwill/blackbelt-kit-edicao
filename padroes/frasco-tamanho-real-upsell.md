---
name: frasco-tamanho-real-upsell
description: "Medida real do frasco de suplemento (300 ml, 13 × 6,9 cm) — régua de escala que o Jhon cobra em todo b-roll de produto"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a10737e1-e26a-4f1e-a64f-e613d536fdc5
  modified: 2026-10-31T19:13:44.475Z
---

Frasco de cápsulas padrão dos upsells (ex.: NightRenew): **300 ml, 13 cm de altura com tampa × 6,9 cm de diâmetro** (Jhon mandou a ficha em 30/10/2026). Conta-gotas 1 fl oz (CogniClear) = 0,9× o frasco.

**Why:** reprovou escala 4 vezes no 349_BM (estoque gigante, kit cortado, frasco maior que a mão, colagem pequena). Eu tinha chutado 9,5 cm e errei — a medida dele é a régua.

**How to apply:** em todo b-roll com produto, medir contra a referência da cena antes de animar: frasco ÷ mão (18–19 cm) ≈ 0,7; ÷ caneca (~9,5 cm) ≈ 1,3; ÷ caixa de depósito (30–40 cm) ≈ 0,33–0,43; ±10 %, e ±3 % entre frascos da mesma cena. No prompt do GPT Image escrever as medidas reais (ele amplia o produto da referência).

**31/10 (aprovado: "ficou perfeito"):** o padrão é o frasco de cápsula do ArtiBrex 335_DA. Produto sempre gerado na cena, nunca colado. O GPT afina e alonga o pote, então o prompt leva LABEL LOCK + SHAPE LOCK, com `ia/mockups/nr_forma_ouro.png` (altura/largura ≈ 1,9) como referência de forma. Para corrigir, editar a imagem pronta ("redraw only the bottles"). Frasco de gotas segue o padrão de gotas. Antes de renderizar, montar uma folha ArtiBrex × atual × novo. Ver [[gpt-image-25-personas-com-produto]] e [[upsell-aprovar-no-hyperframes]].
