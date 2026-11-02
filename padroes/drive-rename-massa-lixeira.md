---
name: drive-rename-massa-lixeira
description: Renomeio em massa no Google Drive montado joga pastas inteiras na lixeira — sempre reconferir a contagem depois e gravar o undo fora do scratchpad
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ec9b4848-3eb5-47cf-868e-7d355cd4e067
  modified: 2026-08-09T00:11:48.233Z
---

Ao renomear/mover milhares de arquivos dentro de um Drive compartilhado montado
(Google Drive for Desktop), o cliente pode **jogar pastas inteiras na lixeira**
ao reconciliar o lote — mesmo com o script local reportando 0 erros.

Aconteceu em 08/08/2026 na reorganização de `Assets/Footages` (5.804 operações):
`Chaves` (32), `IA` (3) e `Podcasts` (14) sumiram **depois** da verificação
pós-execução, que tinha dado 2.987/2.987 certo. Os arquivos estavam em
`~/Library/CloudStorage/GoogleDrive-<conta>/.Trash/<Pasta>/`, **já com o nome
novo**. Restaurar é só mover de volta pra pasta viva.

Pista do diagnóstico: o `.webp` de preview continuava na pasta e só o vídeo
sumia. E a contagem ficou **estável** em três medições — ou seja, não era sync
em voo, era remoção mesmo.

**How to apply:**

1. **Reconferir a contagem algumas horas depois**, não só logo após rodar. A
   verificação imediata passa e o estrago aparece depois.
2. **Gravar o undo e o plano de-para FORA do scratchpad da sessão** — o
   scratchpad é limpo e leva o `undo.json` junto. Perdi o undo de 5.804 pares
   assim, depois de ter dito ao usuário que era 100% reversível. Usar
   `~/Documents/Backups-Painel/` ou similar.
3. Ao contar arquivos num Drive montado, lembrar que **o `ls` local mente**: a
   raiz do drive mostrava 4 itens e a nuvem tinha 15 (o cliente não materializa
   tudo). Para saber o que existe de verdade, usar a API do Drive
   (`search_files` com `parentId`), não o filesystem.
4. O índice de busca do Drive **atrasa** depois de mexida em massa — pasta
   recém-criada não aparece em `search_files` por um bom tempo. Não concluir
   "não existe" por causa disso.

Ver [[convencoes-producao-criativo]].
