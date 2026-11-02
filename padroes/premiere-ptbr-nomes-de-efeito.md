---
name: premiere-ptbr-nomes-de-efeito
description: "Premiere do usuário está em PT-BR — pr_set_clip_transform falha em silêncio; usar pr_set_effect_property com \"Movimento\"/\"Escala\""
metadata: 
  node_type: memory
  type: project
  originSessionId: 49cf0b57-d35b-46d3-b8f4-72ff899a2b8d
  modified: 2026-07-26T02:32:34.853Z
---

O Premiere Pro do usuário roda com interface em **português**. Isso quebra `pr_set_clip_transform` do MCP Higgsfield: a tool procura o efeito pelo nome em inglês (`Motion`) e, quando não acha, **retorna `{"updated": false, "changes": {}}` sem erro** — falha silenciosa clássica.

**Why:** descoberto em 25/07/2026 montando o AD01 da LeafTide. Quatro chamadas de punch-in "tiveram sucesso" e não mudaram nada na timeline. O sintoma só aparece se você ler o `updated: false` — um `pr_get_active_sequence` não mostra escala, então dá pra passar a edição inteira achando que aplicou.

**How to apply:** para qualquer transform (escala, posição, rotação, opacidade), usar `pr_set_effect_property` com os nomes em PT-BR e conferir o `actual` no retorno:
- efeito `Movimento` (matchName `AE.ADBE Motion`) → propriedades `Posição`, `Escala`, `Rotação`, `Ponto de ancoragem`, `Dimensionar largura`
- tracks aparecem como `Vídeo 1` / `Áudio 1`

Quando um nome de efeito falhar, chamar `pr_get_effect_properties` para descobrir o nome exato antes de repetir. Ver [[ae-mcp-armadilhas]] — mesmo padrão de falha silenciosa no After Effects.

## A tradução é MISTA — nem todo efeito virou português (27/08/2026)

Medido ao vivo no Premiere 26.x do Mac (`qe.project.getVideoEffectByName`, um nome por vez),
montando a aba PiP do Tools PRO:

- **em português**: `Movimento`, `Transformar`, `Opacidade`, `Cortar`, `Máscara`,
  `Ajustar alfa`, `Espelho`
- **em inglês, mesmo com a interface em PT-BR**: `Track Matte Key`

`Chave de fosco de faixa`, `Fosco de faixa`, `Recortar` e `Crop` **não existem** — todos
devolvem nulo. Ou seja: supor "interface em PT ⇒ todo efeito em PT" é tão errado quanto
supor tudo em inglês.

**Why:** eu ia hardcodar "Chave de fosco de faixa" para o Track Matte Key. Teria dado
`getVideoEffectByName` nulo → efeito não aplicado → PiP sem recorte nenhum, e nada disso
levanta exceção: é a mesma falha silenciosa de sempre, só que uma camada acima.

**How to apply:** nunca hardcodar UM nome de efeito. Procurar por uma **lista de candidatos**
(PT e EN), guardar qual funcionou e **devolver esse nome no relatório** — foi assim que
`ppNomesEfeito()` do pr-pip ficou. Vale o mesmo para displayName de propriedade: procurar
por lista e, quando não achar, listar as propriedades que existem na mensagem de erro em vez
de falhar mudo. Ver [[toolspro-chaves-de-retorno]].
