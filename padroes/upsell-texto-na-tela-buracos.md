---
name: upsell-texto-na-tela-buracos
description: "Regra \"ou lettering ou legenda\" gerou ~75 s sem texto no upsell 349_BM; chips com palavra após o fim do b-roll nunca apareciam"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a10737e1-e26a-4f1e-a64f-e613d536fdc5
  modified: 2026-10-31T13:59:24.239Z
---

Jhon reprovou o r12 do 349_BM (31/10/2026): "muita parte não tem headline nem legenda". Também reprovou o card de estudo que ficou pendurado em "ability to" e entrou vazio.

**Why:** o build bloqueava a legenda pela cena INTEIRA (F/M/T/A, b-roll com chip, tarja, pílula, área da CTA), mesmo antes do texto da cena entrar. Resultado: 21 buracos, ~75 s de fala sem nada. Além disso, 6 chips tinham a palavra-gatilho depois do fim do b-roll (teto do asset), por isso nunca apareciam.

**How to apply:**
- A legenda só sai da tela enquanto o texto da cena está visível, da entrada até o fim da cena. Ela é aparada, não descartada.
- Ao procurar a entrada do texto, ignorar o fundo da cena (`#cNNNi`).
- Chip/lettering cuja palavra caia depois de b−1,2 s entra em b−1,2 s.
- Card com várias linhas: cada linha entra na sua palavra, e o card nunca entra vazio.
- Antes de renderizar, rodar um mapa de cobertura: fala sem legenda nem lettering por ≥1,5 s = buraco.

Ver [[upsell-aprovar-no-hyperframes]].
