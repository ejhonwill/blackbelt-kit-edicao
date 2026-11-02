---
name: medir-legenda-de-referencia
description: "Como medir legenda de vídeo-referência sem errar — resolver o corpo pela largura do texto, não detectar banda"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 04f0496b-9465-4207-8b49-1e1eda40d954
  modified: 2026-08-17T14:00:46.588Z
---

Para extrair um template de um vídeo-referência (estilo Captions), a detecção automática da banda de legenda **não funciona** e não vale insistir:

* ela trava na linha dos **olhos e da boca** de quem fala — que também formam faixa larga e baixa, e também mudam entre quadros;
* se a pessoa usa **camisa clara**, qualquer regra de cor lê a roupa como texto;
* diferença temporal a 0,5s captura o **corpo inteiro em movimento**, não a legenda;
* estimar corpo por contagem de pixels claros satura no teto e no piso do clamp (dava 130 e 34 onde o real era 62 e 84).

**O que funciona**, e é o método a usar:

1. **Cadência e rajada**: automático e confiável via `select='gt(scene,0.2)',showinfo`, agrupando timestamps a menos de ~0,22s como um único evento de rajada.
2. **Cor**: automático, com limiar de diferença alto (~110) e filtro de tom de pele.
3. **Posição e corpo**: a olho, sobre um quadro com grade em fração da altura + régua de 10px.
4. **Fechamento fino**: medir a **largura em pixels do texto** na referência e resolver por busca binária o `corpo` que reproduz aquela largura naquela fonte. Depois sobrepor o nosso render no quadro da referência e conferir — o alvo é a legenda da referência ficar completamente escondida sob a nossa.

Com isso o desvio ficou em 0–6 px na vertical e 0,97–1,01x na largura.

Ao comparar dois textos brancos na mesma imagem, **tingir um deles ou imprimir os bboxes** — a olho não dá para saber qual é qual, e eu inverti a leitura duas vezes.

Relacionado: [[skill-analise-criativo-ficha]], [[padrao-resumo-criativo-ad]]
