---
name: convencoes-producao-criativo
description: "Regras fixas da operação de criativo — voz sempre em inglês americano, e o usuário cria/abre o projeto do Premiere antes de eu executar"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 49cf0b57-d35b-46d3-b8f4-72ff899a2b8d
  modified: 2026-07-27T17:22:03.158Z
---

Duas convenções definidas pelo usuário em 27/07/2026. São regras fixas, não preferências de job — não perguntar de novo a cada criativo.

**1. Voz sempre em padrão de fala AMERICANO.**
Toda geração de TTS e todo clone de voz seguem inglês americano. Vale para `text2speech_v2`, `seed_audio`, ElevenLabs e MiniMax. Ao escolher voz de catálogo, filtrar por `(en)` americano; ao clonar, a amostra tem que ser de falante americano.

**Why:** os criativos são para o mercado americano — o body da LeafTide estava em inglês mesmo com a copy PT-BR no documento. Sotaque britânico ou neutro-internacional destoa e denuncia produção estrangeira num formato que vive de parecer feito por uma pessoa comum dos EUA.

**2. O usuário cria a pasta e o projeto do Premiere, e abre. Eu executo dentro do que estiver aberto.**

**Why:** o MCP não tem tool para criar projeto. No AD01 da LeafTide isso me obrigou a montar dentro do `VSL - Upsell BIFI.prproj` (projeto de outro job) e a não salvar, pra não sujar o arquivo alheio — a timeline ficou só em memória o tempo todo.

**How to apply:** no começo de cada job, conferir com `pr_get_project_info` se o projeto aberto é o do job. Se for, **salvar normalmente** com `pr_save_project` ao longo do trabalho — é o projeto dele, salvar é o esperado. Se estiver aberto um projeto de outro job, avisar e não salvar. Ver [[receita-edicao-ugc-avatar-9x16]] e [[premiere-ptbr-nomes-de-efeito]].

- **"H&W" se fala em inglês** ("eitch and dâbliu") em qualquer locução, mesmo em PT-BR (Jhon, 20/10/2026, vídeo institucional do H&W Chat). No TTS, escrever a pronúncia em vez do símbolo e conferir ouvindo.
