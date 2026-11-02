---
name: padrao-resumo-criativo-ad
description: Padrão de entrega do resumo/detalhamento de criativo (card AD-por-AD) usado no QA de ADs
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ceef947f-ef8c-4e8e-acd0-1eb5ec97027a
  modified: 2026-07-21T18:22:11.567Z
---

Padrão de entrega aprovado para o **detalhamento de criativo AD por AD** (relatório de conferência/QA). Cada AD é um **card** com layout de duas colunas:

- **Header:** badge com o rótulo do AD (ex.: `AD1`, `AD10 H1`) + **uma linha** de descrição visual (criador, cenário, b-roll principal, cards/overlays). Ex.: "Criadora ruiva, filmada no quarto/cama; b-roll de frascos de melatonina, gráficos de cérebro e card roxo 'Yu Sleep'."
- **Coluna esquerda:** o **mosaico de frames** amostrados com timestamp (arco completo do AD).
- **Coluna direita**, nesta ordem:
  1. **Duração · Resolução** (linha de metadados)
  2. **RESUMO DA EDIÇÃO** — prosa curta descrevendo o ângulo/hook, como alterna talking-head × inserts × b-roll, e como fecha (prova social + CTA).
  3. **TRANSCRIÇÃO DE ÁUDIO (palavra por palavra)** — transcrição limpa completa, em caixa destacada. Transcrever no **idioma real do áudio** (ex.: áudio EN → transcrever em inglês, não forçar PT).
  4. **PONTOS DE ATENÇÃO** — bullets com bolinha de severidade: 🔴 crítico · 🟠 compliance/claim/IP · 🟡 execução/continuidade. Incluir "gêmeo do ADx" quando for mesma criadora/roteiro.

**Why:** é o formato que o usuário considera o resumo de criativo "certo" — combina referência visual, o que foi editado, a fala verbatim e os riscos, tudo escaneável sem assistir o vídeo.

**How to apply:** ao conferir ADs (skill [[conferir-ads-por-frame]]), gerar o detalhamento nesse card. Tema escuro combina com o dashboard. Para análise estratégica de conversão, somar a grade do método PONTE por cima (ver [[metodo-ponte-criativos]]).
