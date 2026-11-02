---
name: pipeline-leitura-concorrente
description: "Quem LÊ um estado de execução não pode 'consertar' etapa em andamento — o SSE sabotava a própria pipeline que exibia"
metadata:
  type: feedback
---

Num executor com estado em arquivo (`pipeline.json` do adrun-creative-studio), a
função de leitura tinha uma regra que parecia defensiva: *"etapa em `running` na
leitura = o servidor caiu no meio, marca como falha"*. Serve para o restart. Só
que **ela roda em toda leitura**, e o SSE de progresso lê a cada 0,7 s — então a
etapa que estava rodando naquele instante era marcada como falha e **gravada
assim no disco**, brigando com a thread que executava.

O sintoma engana: a tela mostrava `failed` no meio de uma execução saudável, que
terminava bem mesmo assim (o executor regravava por cima). Parecia bug de
interface; era corrupção de estado.

**Why:** "etapa rodando" e "servidor morreu" só se distinguem por QUEM é o dono
do processo. Sem essa informação, todo leitor vira escritor.

**How to apply:** marcar posse. Um token por processo (`DONO = uuid4().hex` no
import), gravado na execução quando ela começa a rodar; a leitura só conserta
etapas órfãs quando `run["dono"] != DONO`. O caso "mesmo processo, thread
morta" resolve no `iniciar()`, que já segura a trava e pode afirmar que ninguém
está executando.

Vale para qualquer par ler/executar sobre arquivo compartilhado: **a leitura não
escreve; quem escreve é quem tem a posse.**

Relacionado: [[adrun-creative-studio]], [[hw-studio-nao-escrever-projeto-json]]
