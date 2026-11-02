---
name: demo-sem-produto-real
description: vídeo/tela de demonstração nunca mostra nome de produto real da H&W — usar nome fictício desde a semente
metadata:
  type: feedback
---
Dados de demo (ofertas, briefings, criativos) que vão aparecer em vídeo institucional ou material de venda **não podem usar produto real da H&W** (LinfaFlow, CardioFlush, NeuroFlow…). O Jhon barrou o institucional do AdRun v01 (25/10/2026) porque "LinfaFlow" aparecia nas telas da Copy, no Supercomputer e na legenda queimada do criativo.

**Why:** é produto da casa; vídeo do AdRun vai para venda/redes.
**How to apply:** semear a demo já com nome inventado. Se a captura já existe, trocar na hora da foto (TreeWalker no DOM, regex que pegue o nome truncado com "…", ex. /linfa\s*fl(ow)?/gi) e depois varrer o MP4 inteiro com tesseract a 4 qps. Legenda queimada em criativo gerado não se troca: escolher trecho sem o nome. Feito no institucional v02 com "VitaDrena" (telas/capturar_estudio.py). Ver [[hwstudio-app]].
