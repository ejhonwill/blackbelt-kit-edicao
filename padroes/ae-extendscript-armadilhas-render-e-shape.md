---
name: ae-extendscript-armadilhas-render-e-shape
description: "saveFrameToPng é assíncrono, `in` como chave mata o script, e a ordem de grupos no shape layer é invertida — 3 armadilhas da transição bandeira 116M"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 12050bbf-a0d4-47f9-b6e6-10f34b35c992
  modified: 2026-10-02T18:10:09.202Z
---

Medido em 02/10/2026 montando a transição da bandeira 3D na VSL CardioFlush (`TRANS_FLAG_116`, pasta "TRANSICAO BANDEIRA 116M" no `Jhon parte 1 -2.aep`):

1. **`comp.saveFrameToPng` é assíncrono.** O script volta "ok" antes de os PNGs existirem; disparar 10 quadros e já ler a pasta pega 6. Esperar a contagem de arquivos (laço com `ls | wc -l`) antes de montar contato ou vídeo. Disparar 80 quadros de uma vez funciona, e é o jeito de fazer uma prévia com áudio sem aerender (depois o ffmpeg junta com a locução).
2. **`{in: ...}` como chave de objeto é erro de sintaxe no ES3 do AE.** O `ae_extendscript` devolve só "host devolveu vazio", sem linha. Usar `ip`/`op`. Concatenar array direto numa string também pode voltar lixo pelo serializador (`[3296,4120,0]`), então extrair `v[0]`, `v[1]`.
3. **Shape layer: o primeiro grupo adicionado fica POR CIMA.** Um "dark" de fundo criado antes das faixas claras cobriu tudo, e o sombreamento das dobras virou escurecimento chapado. `grupo.moveTo(2)` resolve. Ler a ordem de volta.

Receita da bandeira que ficou boa: arte em shape (3000×1580 + folga transparente de 160 px, senão o Wave Warp corta a borda), dobras com faixas cinza 0,62/0,18 repetidas no comprimento da onda, desfocadas e em Overlay andando na velocidade do Wave Warp (altura 70, largura 700, vel 1,1), mais um Turbulent Displace leve.

4. **`camada.property("ADBE Rotate Y")` devolve null** — só os grupos de topo resolvem direto. Usar `camada.property("ADBE Transform Group").property("ADBE Rotate Y")` (o atalho `.position` funciona, as rotações não). Visto de novo em 08/10/2026.

Receita 2 (08/10/2026, comp de teste `T AE`): pré-comp própria `TRANS_BANDEIRA_EUA` com câmera + luzes dentro (a câmera não vaza pras camadas 3D da comp principal); câmera atravessando o plano (z −2250 → +600) com **saída lenta na chave de partida (85) e chegada rápida (8)** — com a influência invertida ela fura a bandeira cedo e freia depois.

**Why:** cada uma custou uma rodada de render e de diagnóstico.

Ver [[ae-camera-3d-armadilhas]], [[toolspro-extendscript-mcp]], [[toolspro-ae-mcp-porta-errada]].
