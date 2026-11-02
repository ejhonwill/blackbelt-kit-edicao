---
name: formatos-de-trabalho-hw
description: "Os 5 formatos de trabalho da operação (VSL, Criativos, Microleads, Lead, Troca de potes) e o que já foi automatizado de cada um"
metadata: 
  node_type: memory
  type: project
  originSessionId: 49cf0b57-d35b-46d3-b8f4-72ff899a2b8d
  modified: 2026-07-28T20:05:16.654Z
---

A operação de edição da H&W trabalha com **cinco formatos**, e o usuário quer automação para todos:

| Formato | Estado da automação (28/07/2026) |
|---|---|
| **Criativos** | **Feito.** Skill `editor-automatico-de-broll`, validada em AD01 e AD05 do LeafTide |
| **VSL** | Não automatizado. Existem as skills de análise (`dissecador-de-vsl-atlas`, `bifi-funil-completo`), mas nenhuma de edição |
| **Microleads** | Não automatizado. Aparece como seção própria no doc de copy, com ângulos e avatares |
| **Lead** | Não automatizado |
| **Troca de potes** | Não automatizado. **Nunca vi um job desses** — só o nome do arquivo `UPSELL - TESTE DE TROCA DE POTES.prproj`, na pasta do Cardio Flush |

**Why:** o usuário listou os cinco em 28/07/2026 ao perguntar se eu já sabia troca de potes. Respondi honestamente que não.

**How to apply:**
- **Cada formato vira uma skill separada**, não uma skill gigante. O repo `jhonatangtw/creative-automation` já está estruturado para isso — basta adicionar em `skills/` e listar no `marketplace.json`.
- Para aprender um formato novo, **pedir um job JÁ FEITO** (material de entrada + saída final + o `.prproj` se existir) e deduzir o processo, em vez de pedir explicação. Foi assim que a skill de criativo pegou o padrão de legenda, ritmo de insert e estilo de corte — olhando o `EXEMPLO DE AVATAR.mp4`.
- Hipótese sobre troca de potes, **não confirmada**: substituir o pote do produto num criativo já validado para vender outra oferta. Se for isso, é o mais automatizável dos cinco por ser substituição mecânica — melhor retorno por hora investida que VSL.

Ver [[leaftide-ad01-validado]] e [[receita-edicao-ugc-avatar-9x16]].
