---
name: mover-projeto-adobe-com-seguranca
description: Premiere e AE guardam caminho relativo além do absoluto — a regra para mover pasta de projeto sem quebrar mídia
metadata: 
  node_type: memory
  type: reference
  originSessionId: b4752e04-acfe-4ffd-9c9e-db01782c9c8c
  modified: 2026-09-10T20:08:37.145Z
---

Premiere e After Effects **não** dependem só do caminho absoluto. Os dois guardam também a posição
relativa da mídia, e relinkam sozinhos quando o absoluto falha.

- **Premiere (`.prproj`, gzip + XML):** cada mídia tem `<ActualMediaFilePath>` (absoluto) e
  `<RelativePath>` (ex. `../weeks/WEEK 4.mp4`).
- **After Effects (`.aep`, binário):** o registro é um JSON embutido:
  `{"ascendcount_base":2,"ascendcount_target":3,"fullpath":"/…","platform":2,…}`.
  `ascendcount_base` = quantos níveis subir a partir do arquivo `.aep`.
  `ascendcount_target` = quantos componentes finais do `fullpath` formam a cauda relativa.
  Não existe string `../` nenhuma no arquivo — o relativo é só esses dois números.

**Regra que sai disso:** mover a pasta do projeto é seguro *se a posição relativa entre projeto e
mídia não mudar*. Na prática:

1. Mova a **unidade inteira** (projeto + mídias irmãs), nunca só o `.prproj`/`.aep`.
2. Se duas pastas de projeto se referenciam (o projeto de um mês puxando mídia de outro), **as duas
   têm de descer o mesmo número de níveis, para o mesmo pai novo**. Aí a distância relativa se
   preserva e o relink funciona.
3. **Não renomeie** pasta que contém ou é apontada por projeto Adobe. Renomear muda a posição
   relativa e aí não tem o que salvar.
4. Referência para fora da árvore movida (Google Drive, Downloads, `~/Library`) continua valendo
   pelo caminho absoluto, porque o alvo não se mexeu.

**Como provar em vez de confiar:** leia os projetos e teste cada referência. Para o Premiere,
`gzip.open()` + regex nas duas tags. Para o AE, regex
`\{"ascendcount_base":(\d+),"ascendcount_target":(\d+),"fullpath":"((?:[^"\\]|\\.)*)"` no binário
cru, e monte o candidato com `ascend(caminho_do_aep, base) + fullpath.split("/")[-target:]`.
Script pronto em `~/Documents/_Organizacao/` — ver [[documents-estrutura-organizada]].

Duas armadilhas ao escrever esse verificador:
- `find -name "*.aep"` pega `Logs de AD04.aep`, que é **pasta**, não arquivo. Use `-type f`.
- casar `ActualMediaFilePath` com `RelativePath` por índice não funciona: a contagem das duas tags
  difere. Compare pelo nome-base, ou melhor, teste se a mídia existe no caminho novo equivalente.

Reescrever o caminho absoluto **dentro** do `.aep` não é opção: é RIFX com chunk de tamanho fixo, e
o caminho novo quase nunca tem o mesmo comprimento.
