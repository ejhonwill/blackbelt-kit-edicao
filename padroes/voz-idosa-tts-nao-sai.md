---
name: voz-idosa-tts-nao-sai
description: "Catálogo de TTS não entrega voz de idoso convincente; medir F0 e jitter não prevê idade percebida — o Jhon reprovou duas rodadas"
metadata:
  type: feedback
---

Em 17/09/2026, nas personas do MemoFlow Upsell #1 (depoentes de 64 a 82 anos), **duas rodadas de escolha
de voz foram reprovadas de ouvido** pelo Jhon: a primeira na ElevenLabs ("muito usadas"), a segunda na
HeyGen ("a voz tá muito infantil", sobre a senhora de 68 anos). Ele decidiu gerar no **MiniMax** e entregar
os arquivos prontos.

**O que eu media e por que não bastou:** F0 mediana e jitter. Escolhi a voz feminina de F0 mais baixo do
lote (172 Hz) e ainda soou infantil. Na segunda tentativa acrescentei **shimmer** (variação de amplitude)
e **HNR** (relação harmônico/ruído, que cai com a idade), montei um índice e reordenei — continuou ruim.

**A lição:** idade percebida em voz não se resolve por medida de sinal no nível que eu consigo extrair.
Timbre, colocação e padrão de fraseado pesam mais. **Não gastar rodada atrás de rodada tentando adivinhar
por número** — em job com faixa etária alta, gerar 1 amostra por candidata, montar na timeline junto da
imagem e **pedir o ouvido do Jhon logo na primeira rodada**, antes de gerar o lote.

**O que funcionou como processo** (vale repetir): sequência `AMOSTRAS DE VOZ` no Premiere com a imagem
aprovada de cada persona na V1 e a amostra da voz na A1, na ordem de idade. Ele ouve as 8 em 67 s e
responde. Custo: 8 créditos.

**Buscas que não ajudam:** `heygen voice create --prompt "elderly grandmother voice"` (desenho de voz por
descrição) devolve **lista vazia** nesta conta. O catálogo tem 1.904 vozes em inglês mas **não expõe idade
nem sotaque** (`accent` e `labels` vêm nulos em todas). Filtrar por nome sugestivo ("Warm Elder Narrator",
"Grandpa Joe", "Mabel Forsythe") acha candidatas, mas o nome não garante o resultado.

**O que passou de primeira (08/10/2026, Criativo ASTRON, hook de senhora negra de 75 anos):** HeyGen Avatar IV
pelo Fal (`fal-ai/heygen/avatar4/image-to-video`, texto→fala) com a voz **`Helen`** do enum — aprovada pelo
Jhon contra a `Grace Elder`. Mesmo processo: 2 candidatas no mesmo still, lado a lado na timeline, ele escolhe.
No Fal o campo `expression` só aceita `"happy"`; para tom sério, deixar sem e travar a expressão no still.

Ver [[convencoes-producao-criativo]], [[elevenlabs-conta-limites]], [[heygen-cli-e-creditos]].
