---
name: qc-sync-correlacao-mente
description: "Medir lip sync por correlação entre abertura de boca e envelope do áudio dá falso reprovado em massa; a prova é o quadro do silêncio contra o quadro do pico"
metadata:
  type: feedback
---

Em 17/09/2026 montei um QC automático de lip sync que correlaciona um sinal de "abertura de boca" (pixels escuros
no ROI da boca, via landmarks do YuNet) com o envelope RMS do áudio, varrendo atrasos. Ele reprovou **42 de 68**
clipes por "sincronia fraca" ou "lag".

**Era o instrumento, não os clipes.** O sinal de boca é dominado por sombra, barba e movimento de cabeça; o pico da
correlação caía quase sempre **no limite da janela de busca** (±12, depois ±20 quadros) — assinatura clássica de
ruído. Tentei uma v2 com sinal melhor (altura da faixa escura central) e ficou **pior**: correlação ~0 em tudo.

**A prova que vale, e é barata:** para cada clipe, extrair o quadro do **silêncio inicial** (0,5 s de lead que já
existe no wav) e os 3–4 quadros de **pico de RMS**, bem espaçados, e montar uma grade recortada na boca. Se no
silêncio a boca está fechada e nos picos está aberta com formas de vogal distintas, a sincronia está boa — e isso se
enxerga numa imagem só, para 6 clipes de uma vez. Foi o que reabilitou os 42 "reprovados".

**Regra que fica:** métrica de correlação em sinal visual improvisado serve para **ordenar suspeitos**, nunca para
reprovar. Quando o pico bate na borda da janela de busca, descartar a medida.

Ver [[lipsync-rotulo-reescrito-recolagem]], [[conferir-broll]], [[opencv5-sem-haarcascade]].
