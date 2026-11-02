---
name: metodo-ponte-criativos
description: Método PONTE do usuário para produzir/auditar criativos de tráfego pago
metadata: 
  node_type: memory
  type: project
  originSessionId: ceef947f-ef8c-4e8e-acd0-1eb5ec97027a
  modified: 2026-08-02T22:32:00.225Z
---

**PONTE** — método do usuário para **produzir criativos de tráfego pago** (ADs/VSLs Meta/TikTok) com origem em dado, não no chute. As 5 letras vivem em 3 altitudes: conteúdo (O, P, T), formato (N), processo (E).

- **P — Persuasão** (esqueleto): estrutura dor → promessa → mecanismo → prova → CTA.
- **O — Orgânico decupado** (combustível): minerar o que já performa no orgânico e decupar em 3 ativos → gancho, frase-objeção, momento de retenção. Letra mais original do método.
- **N — Native creator** (embalagem): parecer criador nativo, não anúncio (UGC; pode ser avatar sintético).
- **T — Traduzir mecanismo** (diferencial): o "por que ISSO funciona quando o resto falhou" — mata a objeção "já tentei de tudo". Fronteira com P: P é o formato do argumento, T é o argumento único.
- **E — Experimentação** (motor): não testa nada novo — testa as outras 4 letras (hook/ângulo/creator/CTA/duração). Ordem de execução real: O→P→T→N→E (o acrônimo é só mnemônico).

**Aplicação:** dar nota 1-5 por letra + veredito + matriz de teste. Piloto validado no AD10 H1 Sonnus (nota global 3,4/5) em 21/07/2026. Entregar a análise junto com o [[padrao-resumo-criativo-ad]] e o QA técnico.

**Skill empacotada:** `analise-criativos-ponte` — reúne QA técnico + detalhamento AD-por-AD + análise PONTE num relatório HTML único, pra qualquer criativo. Pacote distribuível (README de instalação + `instalar-macos.command` / `instalar-windows.bat` + `skill/`) em `~/Documents/Skills Claude/analise-criativos-ponte/`; instalada em `~/.claude/skills/analise-criativos-ponte/`. Deps: ffmpeg + pillow (obrigatórias), tesseract+`por` (OCR), faster-whisper (transcrição) — detalhes em `skill/references/setup.md`. **Publicado pros alunos** (02/08/2026) em **github.com/jhonatangtw/skills-ponte** (PÚBLICO, sem trava de licença — decisão do usuário: é um SKILL.md em texto, trava seria removível). O repo entrega o funil INTEIRO: `bifi-funil-completo` + `dissecador-de-ads-atlas` + `dissecador-de-vsl-atlas` + `analise-criativos-ponte`, em `skills/`, com um instalador que copia as 4 e instala `python-docx` (os geradores de .docx importam `docx` — faltava, quebrava na Fase 3). Distribuição por "Code → Download ZIP" + duplo-clique no instalador (não usa Releases como o [[toolspro-distribuicao]]); o bit de execução do `.command` sobrevive ao ZIP do GitHub. Pré-requisito que gera suporte: aluno precisa do Claude Code com assinatura ativa, e o 1º uso baixa ~500MB de modelo Whisper. Usuário decidiu MANTER os exemplos reais (Sonnus/Goli) no repo público — mais didático, ciente de que expõe cliente e winner modelado. Fluxo: `conferir.py` (QA) → Claude lê mosaico → `analise.json` → `montar_relatorio.py`.
