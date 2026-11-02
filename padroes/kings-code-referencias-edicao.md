---
name: kings-code-referencias-edicao
description: "The King's Code (7 bodies, doc \"Bodys Kings Code\") — padrão de edição medido nas 3 refs do copywriter e as trocas por compliance"
metadata:
  node_type: memory
  type: project
  originSessionId: 3ac7ca15-899b-4c14-a10c-97ead60b1da9
  modified: 2026-10-09T13:21:42.754Z
---

Job The King's Code (manifestação/identidade, "escritos de Michael Jackson"), 7 bodies em EN no Doc
`1V4uczgZoBhVh2T7fztG1z23ve-GOarb9qxYsBOMDHdc`. Hooks vazios no doc em 09/10/2026. Body 5 (e 3) = avatar feminino.

Refs de edição (Drive, dono jimmysleepybr; baixam por curl direto, sem cookie):
ref1 `1Z_sRMF87vNGI8_fSVEo0E4wefZJwDK-u` (187 s, mulher na cama), ref2 `1vIqgj0UVi1TGwI4vsW69pFvG6HpxfGdN`
(106 s, mulher no carro), ref3 `1pkzuQk0ugv6zsjkxxPrQyIi6vKSDQVbL` (110 s, homem de moletom).
**ref2 e ref3 são o MESMO roteiro e o MESMO pacote de b-roll, só troca o avatar** (ref3 ganha 3 s de hook
"stitch" de TikTok na frente) — é um winner replicado.

Medido: 160–180 wpm, plano médio 2,3–2,5 s (ref1: 4,2 s), avatar ≈50% da tela alternando 1:1 com b-roll
literal da palavra falada, rajada de 6–10 cortes em ~4 s perto da metade, trilha a ~-22 dB sob voz a -17 LUFS,
legenda 2–4 palavras CAIXA ALTA no meio-baixo com palavra ativa em caixa colorida (azul na ref1, roxo nas 2/3).
Recorrentes: triângulo de alerta com glitch "SYSTEM ERROR" no "scrub this footage", olho macro, cérebro
brilhando, carta manuscrita em close com pan, PiP de "neurocientista" de podcast.

**Why:** as refs usam rosto do MJ, Bill Gates e Kardashian e a carta real de 1979 — nós não podemos
(direito de imagem + bloqueio da Meta por celebrity bait). Trocar por silhueta/palco/arquivo anônimo e
caderno manuscrito genérico.

**How to apply:** um pacote de b-roll único para os 7 bodies (as frases se repetem), como fizeram as refs 2/3.
Ver [[broll-usar-kling]] e [[rostos-famosos-borrar]].

**Execução (09/10/2026):** demanda 215_MV montada no Premiere — 7 sequências `Bxx - BODY [Kings Code]` 25 fps,
V1 avatar HeyGen Avatar IV, V2 b-roll/punch-in, V3 lettering/transição/CTA, A2 voz ElevenLabs `eleven_v4` decupada
(v02, por silêncio real — a v01 por alinhamento mordia fim de palavra), A3 trilha pré-mixada, A4 SFX. Bodies 2/4/6/7
viraram personas fictícias (originais eram Tom Brady, Michael Phelps e duas criadoras reais do TikTok). Vozes:
B01 Savvy, B02 Chris, B03 Sarah, B04 Dan, B05 Laura, B06 Jessica, B07 Matilda. Pacote b-roll BR01–BR46 em
MEDIA/HIGGSFIELD/broll_broll.json. Jhon liberou vídeo público do TikTok nos trechos de assunto público.

**Lettering premium (09/10/2026, pedido do Jhon):** palavra-chave em AMARELO com deep glow (5 camadas de text-shadow
#FFD60A→laranja + camada borrada com bloom na entrada), resto em branco com contorno, halo escuro atrás. Feito no
HyperFrames (`HYPERFRAMES/_gerador/build.py`, overlay ProRes 4444 v02 na V3). NÃO animar letterSpacing (lint
`gsap_non_transform_motion`: pula pixel no render); camadas de glow precisam de `data-layout-allow-overlap` em cada span.

**Figuras reais + zoom (09/10/2026):** footage público do YouTube (yt-dlp `ytsearch6:`; TikTok não busca por palavra)
em `MEDIA/BANCO/FIGURAS PUBLICAS` com FONTES.txt (MJ 1979/80/88, Ali BBC, Phelps Pequim, Carrey/Oprah). Toda menção
a figura ganha footage real (troca o b-roll gerado ou insere). Zoom do avatar = keyframes de escala na própria V1
(100→107 / 107→100 alternando por janela ≥2 s, virada sempre num corte). Buracos <0,6 s na V2 fazem o avatar
"piscar" — fechar lendo a V2 de volta e esticando o clipe anterior em ticks (`fechar.jsx`).
Recortes a evitar: logo BBC, marca d'água "MUHAMMADALI_GOAT" (cortar acima), tarja preta do comercial Under Armour.
