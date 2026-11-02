# Padrão premium DR (medido nas referências do Kings Code)

## O que as referências tinham (3 vídeos do copywriter)

| Medida | Ref 1 | Ref 2 | Ref 3 |
|---|---|---|---|
| fala | 160 ppm | 180 ppm | 180 ppm |
| plano médio | 4,2 s | 2,5 s | 2,3 s |
| avatar na tela | ≈ 50% | ≈ 50% | ≈ 50% |

- Ref 2 e Ref 3 eram **o mesmo AD com outro avatar** → um pacote de b-roll serve a todos os bodies.
- B-roll **literal à palavra falada** ("vision board" mostra quadro dos sonhos), 1–3 s, alternando 1:1 com avatar.
- Rajada de 6–10 cortes em ~4 s perto da metade (momento da revelação).
- Recorrentes: alerta "SYSTEM ERROR" com glitch, olho macro, cérebro brilhando, carta manuscrita com pan, PiP de "neurocientista".
- Legenda 2–4 palavras, CAIXA ALTA, meio-baixo, palavra ativa em caixa colorida (roxo/azul).
- Trilha por baixo ≈ 6 dB abaixo da voz (voz em −17 LUFS).

Como medir uma referência nova: `select='gt(scene,0.25)',showinfo` (cortes), mosaico `fps=1/2,tile=8x4`,
`mlx_whisper` por palavra (ppm, pausas), `volumedetect` nas pausas (trilha).

## Nosso padrão de saída

**Trilhas**: V1 AVATAR · V2 BROLL (b-roll + punch-in) · V3 LETTERING (overlay HyperFrames) ·
A1 AVATAR (MUDO) · A2 VOZ DECUPADA · A3 TRILHA · A4 SFX. Sequência 1080×1920, **25 fps** (= HeyGen).

**Marcadores** (nome + conteúdo no comentário): BROLL_nn vermelho(1) · LETTERING_nn azul(6) · KEYWORD_nn
amarelo(4) · CORTE_RITMO_nn ciano(7) · TRANSICAO_nn laranja(3) · CENA_01_HOOK / CENA_99_CTA branco(5).

**Ritmo**
- Hook: avatar cheio nos 3 primeiros s com push-in 100→110% (exceto se a copy cita uma figura no hook — aí
  figura real logo no nome).
- B-roll 2–3,2 s, entrada com whoosh, Ken Burns 101→108%. Cobertura 30–40% + punch-ins.
- Punch-in seco 112% nas frases longas de avatar (cópia do avatar na V2 com `inPoint == start`).
- Zoom in/out no próprio V1: janelas de avatar ≥ 2 s alternam 100→107 e 107→100; virada sempre num corte.
- Nenhum buraco < 0,6 s na V2 (o avatar "pisca").
- Nenhum footage repetido na mesma timeline.

**Overlay HyperFrames (V3, MOV ProRes 4444)**
- Legenda: Montserrat ExtraBold 76 px, branca com contorno, 2–4 palavras, top 71%, palavra ativa em caixa
  roxa `#6C2BD9`. Legenda escondida quando o lettering grande mostra a mesma palavra.
- Lettering: top 47–50% (peito), palavra-chave em amarelo `#FFD60A` com deep glow (5 camadas de
  text-shadow amarelo→laranja + camada borrada com bloom na entrada), resto branco com contorno, halo escuro
  atrás. 4 fases em sequência, cada uma até a próxima entrar. Entrada: escala 0,6→1,06→1 + desfoque 18→0.
- Viradas da copy, saída do hook e CTA: flash branco 0,35 s. A cada 3 b-rolls: varredura de luz quente.
- CTA: botão branco "LEARN MORE ↓" vermelho pulsando, top 84%, até o fim.

**Áudio**: voz −16 LUFS (decupada), trilha pré-mixada −34 LUFS com fade 1 s / 2,5 s, SFX normalizados −22 LUFS
(whoosh, pop, boom, ding, glitch, riser). Final ≈ −16 LUFS.

**Entrega**: `[DDMMYY][OT] NNN_XX ADnn [Produto] [Squad].mp4` em `EXPORT/` (body nn = ADnn).
