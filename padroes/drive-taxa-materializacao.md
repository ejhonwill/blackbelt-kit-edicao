---
name: drive-taxa-materializacao
description: Teto de ~6 arquivos/min ao copiar do Google Drive e as 3 armadilhas que custam horas
metadata: 
  node_type: memory
  type: project
  originSessionId: 6a7d36b6-5c43-4e8f-a98a-d4d3a572c8e3
  modified: 2026-08-21T13:19:06.521Z
---

Copiar em massa de um Drive compartilhado para outro (Drive for Desktop, macOS 26) tem teto de **~6 arquivos/min**. O limite é a taxa de materialização do daemon do Drive — não é banda (a rede fica em ~2,85 MB/s ociosa) nem CPU. Mais paralelismo não sobe o número.

**Why:** medido em 21/08/2026 no job do Footage Black Belt; perdi horas otimizando algo que não tinha folga.

**How to apply:**
- **Nunca escrever no Drive com muitas threads.** Com 40, o daemon vai a 104% de CPU, os arquivos ficam em 0 byte e a taxa cai para 1/min. Use 5–12 threads. Escrever é write-back (instantâneo); o gargalo é sempre a leitura.
- **Ler só o começo do arquivo não materializa nada.** A flag `dataless` (via `stat -f %Sf`, ou `st_flags & 0x40000000`) só cai quando o download termina. Prefetch tem que ler o arquivo **inteiro**; ler 1 MB para "aquecer" faz o lote inteiro parecer frio.
- **O Python 3.9 do CommandLineTools dá segfault** com `subprocess` em muitas threads. Use `/opt/homebrew/bin/python3.14`.
- Erros `OSError(89, 'Operation canceled')` e timeouts são **transitórios** do Drive — marque para retry, não como falha definitiva.
- Não existe eviction oficial: `fileproviderctl` do macOS 26 não tem mais o subcomando `evict`. O Drive evicta sozinho sob pressão de disco (vi subir de 50 → 184 GB livres). Ver [[destino-producao-arquivo-de-edicao]].

Alavanca real não testada: `rclone` fala com a API do Google direto, sem o daemon, e provavelmente faria cópia server-side.
