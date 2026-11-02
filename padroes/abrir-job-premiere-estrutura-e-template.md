---
name: abrir-job-premiere-estrutura-e-template
description: "Como abrir um job novo no Premiere do Jhon — estrutura de pastas da demanda, onde está o \"Projeto Padrão.prproj\" da casa, e a armadilha do espaço no nome da pasta raiz"
metadata:
  node_type: memory
  type: project
  originSessionId: d62fce68-8131-4cac-bbd5-460c0bd0226d
  modified: 2026-10-07T18:31:02.203Z
---

Feito em 17/09/2026 no `[160926][OT] Upsell #1 [MemoFlow] [Squad]`.

**Estrutura de pastas de uma demanda** (copiada dos jobs vizinhos do MemoFlow):
`EXPORT/`, `FOOTAGE/`, `PROJECT/`, `MEDIA/{AUDIO, IMG, SRT, LEGENDA, AEF, BANCO, IA LIPSYNC}`.
Alguns jobs antigos usam `PROJETO/` e subpastas por AD (`FOOTAGE/AD01…`, `PROJETO/AD01…`) quando a demanda é multi-AD.

**Template do Premiere:** não existe em `~/Documents`. O que a casa usa é o
`Projeto Padrão.prproj` (72 KB, jun/2026) que fica dentro de
`…/08. Memory/MemoFlow/OT/[100926][OT] Microlead [MemoFlow] [Squad B]/PROJECT/`.
Sequências: `16x9`, `9x16`, `4x5`, `Coringa LETTERING`; bins `01. Sequences`, `02. Brutos`,
`03.Medias`, `04. IA`. **Não tem 1:1** — upsell em 1:1 precisa criar a sequência. As 4 mídias
que ele referencia apontam pra máquina do Ericles (offline), é esperado.

**Cópia-mestre (achada em 07/10/2026 com `mdfind -name "Projeto Padrão.prproj"`):**
`…/Drives compartilhados/H&W - Backup Q1 e Q2/RO Edição de Video/Assets/PROJETO PADRÃO/PROJECT/Projeto Padrão.prproj`.
A sequência `9x16` dele é **23,976 fps** (provado pelos ticks: 235 quadros exatos num clipe de 9,8 s), e a HeyGen
entrega 25 fps. Trocar o fps exige `pr_extendscript` com o Modo avançado ligado pelo Jhon.

**Receita:** `cp` do template para `PROJECT/<nome do job>.prproj` + `open -a "Adobe Premiere Pro 2026" <prproj>`.
Em ~1 min o painel Tools PRO sobe na 7842 e `pr_extendscript` devolve `app.project.name/path` pra provar
que abriu o certo. O `osascript` de System Events NÃO devolve o título da janela do Premiere — não usar como prova.

**Armadilhas de caminho:** a pasta raiz local é `Arquivo de Edição ` **com espaço no fim**
(`…/Drives compartilhados/H&W - Edição de Vídeo -Q3/Arquivo de Edição /…`). E `find` na árvore
inteira do Drive não termina em 2 min — descer direto até o produto.

Ver [[destino-producao-arquivo-de-edicao]], [[convencoes-producao-criativo]], [[toolspro-extendscript-mcp]].
