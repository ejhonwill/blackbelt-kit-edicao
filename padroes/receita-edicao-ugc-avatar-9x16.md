---
name: receita-edicao-ugc-avatar-9x16
description: "A receita de edição de criativo UGC 9:16 virou a skill editor-automatico-de-broll — usar ela, não reinventar"
metadata: 
  node_type: memory
  type: project
  originSessionId: 49cf0b57-d35b-46d3-b8f4-72ff899a2b8d
  modified: 2026-07-26T03:21:24.436Z
---

O pipeline de edição de criativo UGC 9:16 a partir de body de avatar (B-roll + inserts + punch-in + legenda) está implementado como skill:

**`~/.claude/skills/editor-automatico-de-broll/`**

Inclui `SKILL.md` com o fluxo, `references/armadilhas.md` (falhas silenciosas de Premiere/ffmpeg/Whisper/Higgsfield), `references/prompts-broll.md`, `references/estilo-ugc.md`, `references/config.md`, e três scripts testados: `legendas.py`, `conferir_legenda.py`, `montar.py`.

**Why:** construída e validada no AD01 da LeafTide em 25/07/2026 — ver [[leaftide-ad01-validado]]. O usuário pediu para salvar como skill justamente para não redecidir a cada job.

**How to apply:** quando chegar um bruto de criativo, invocar a skill em vez de refazer o raciocínio. Se descobrir uma armadilha nova durante um job, escrever em `references/armadilhas.md` da skill — não numa memória nova. Ver também [[premiere-ptbr-nomes-de-efeito]] e [[whisper-passada-longa-inventa]].
