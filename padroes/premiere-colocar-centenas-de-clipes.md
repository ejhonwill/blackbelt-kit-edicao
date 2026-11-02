---
name: premiere-colocar-centenas-de-clipes
description: "pr_timeline_colocar pendura com projeto grande; colocar 800 stills por ExtendScript próprio em lotes de 50, e ler de volta paginado"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 3ff7eff6-9396-46cc-89c8-7cda3846263b
  modified: 2026-09-30T22:16:56.617Z
---

Em 30/09/2026 (827 slides do webinar AI Loophole em V1 da sequência "part 4"):
`pr_timeline_colocar` com 100 clipes num projeto de ~830 itens estourou 120 s até no `simular`,
e o motor de script do painel ficou pendurado (0 % CPU, nem `return 1` respondia) — só reabrir
o Premiere resolveu (pedir Cmd+S antes).

**Why:** a ferramenta resolve cada nome varrendo o projeto; com centenas de itens vira O(n²).

**How to apply:** montar o mapa nome→item UMA vez no ExtendScript, `overwriteClip(item, Time)`
(nunca string de segundos), achar o clipe recém-posto e setar `end` com `Time` — lotes de 50 com
pausa de 3 s: 827 clipes em < 1 min. O retorno do `pr_extendscript` é truncado quando grande
(lista de 827 veio com 501): ler de volta em páginas de 200 e conferir contagem, sobreposição,
lacunas < 0,2 s e desvio de tempo. Pipeline e scripts: `~/Documents/01_Producao/Webinar AI Loophole - Slides/pipeline/`.
Relacionado: [[premiere-script-ticks-e-corte-do-movimento]], [[toolspro-painel-via-cdp]], [[premiere-export-direto-trava-com-drive]].
