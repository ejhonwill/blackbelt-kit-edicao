---
name: heygen-avatar-iv-vs-v
description: "Avatar V x Avatar IV na HeyGen: o que cada um aceita, por que o Jhon reprovou o V nos depoimentos, e a armadilha de fps da sequência"
metadata:
  type: feedback
---

MemoFlow Upsell #1, 17/09/2026. Dez seções geradas primeiro em **Avatar V**; o Jhon reprovou os
depoimentos ("ficaram bugado") e pediu **Avatar IV**. As três seções do médico ficaram no V.

**O que cada engine aceita** (medido tentando, o erro da API diz o motivo):

| | Avatar V | Avatar IV |
|---|---|---|
| imagem solta (`type:"image"`) | não, exige `avatar_id` | sim |
| `expressiveness` | **recusa**: "not supported with engine 'avatar_v'" | aceita |
| `motion_prompt` | só com `reference_look_id` de um **digital_twin do mesmo grupo** — impossível para pessoa gerada por IA, que não tem filmagem real | aceita direto |

Ou seja: no Avatar V o personagem sintético fica sem direção de movimento nenhuma. No IV dá para
passar expressividade + prompt de arco emocional, e o resultado tem microexpressão e piscada bem
mais naturais. **Para persona gerada por IA, usar Avatar IV.**

**Criar o avatar de foto é instantâneo e grátis:**
`heygen avatar create -d '{"type":"photo","name":"...","file":{"type":"asset_id","asset_id":"<id>"}}'`
devolve `avatar_item.id` (= o `avatar_id` do vídeo) e `supported_api_engines`. O `status` volta
`processing` mas já dá para gerar.

**O rótulo do produto degrada nos DOIS engines** — menos que no wan3_0, mas degrada. A recolagem do
frasco ([[lipsync-rotulo-reescrito-recolagem]]) resolve nos dois; com Avatar IV a mão se mexe mais
(deslocamento de até 120 px contra ~30 px no V), e o rastreio por gabarito ainda assim segura
(casamento 0,89–0,98). Conferir visualmente os de casamento mínimo abaixo de 0,7.

**Armadilha de fps:** a HeyGen entrega **25 fps**. A sequência clonada do template da casa está em
**23,976**, e a conversão faz o Premiere derrubar quadro — justo no que mais importa, o movimento da
boca. Casar a sequência com a fonte: `st=s.getSettings(); var t=new Time(); t.ticks="10160640000";
st.videoFrameRate=t; s.setSettings(st);`.
⚠️ `t.ticks = String(254016000000/25)` com a **divisão dentro do String()** quebra o timebase
(vira 9223372036854775807, o máximo do int64, e a sequência fica com 2,7e-8 fps). Passar a string
literal já calculada, ou usar `t.seconds = 1/25`.

Ver [[heygen-cli-e-creditos]], [[voz-idosa-tts-nao-sai]].
