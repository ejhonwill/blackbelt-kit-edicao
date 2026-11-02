## Comandos usados, na ordem

Cada bloco é um pedido separado que o Jhon mandou no job 128_PG. Troque link, caminho e números de hook pelo job da vez.

### 1. Análise da copy
```
Analise essa copy <link do Google Doc>
```
```
agora analise
```
(depois de dar acesso ao doc para a conta conectada)

### 2. Abrir o projeto
```
Perfeito, crie o projeto no Adobe Premiere, o caminho é esse: Arquivo de Edição/23. Heart/CardioFlush/OT/[230926][OT] 128_PG [CardioFlush] - Hooks [Squad]
```

### 3. Comando principal — geração dos hooks
```
COMANDO — Geração de Hooks (Kling 3.0) + Timeline

Depois de criar o projeto no Premiere, siga estas etapas na ordem:

1. Ler as referências antes de tudo
Leia a skill hook-dr-saude em /Users/jhonwill/Documents/04_Skills-e-Automacao/Skills Claude/_skills/hook-dr-saude, incluindo todas as imagens e exemplos de referência que estão na pasta. É o visual que já treinei: avatar, prop anatômico na lente, cenário de autoridade, bandeira dos EUA e estética de celular.
Leia também a skill photorealism-prompts.
Me resuma em 3 a 5 linhas qual é o padrão visual que você identificou nas referências. Só siga depois que eu aprovar.

2. Mapear os hooks
Liste todos os hooks do projeto (H1, H2, H3…) com: a fala, a estrutura usada (entre as 6 da skill), o prop anatômico e o cenário.
Monte uma tabela para eu revisar antes de gerar qualquer imagem.

3. Gerar as imagens de referência (start frames)
Escreva um prompt de imagem por hook, em inglês, combinando as regras da photorealism-prompts com o padrão visual da hook-dr-saude.
Mantenha o mesmo avatar em todos os hooks (consistência de rosto, roupa e cenário), a não ser que eu peça variação.
Formato 9:16, vertical, com estética de celular.
Gere as imagens e me mostre todas juntas para aprovação. Refaça só as que eu reprovar.

4. Gerar os vídeos no Kling 3.0
Use cada start frame aprovado como imagem de entrada (image-to-video).
Escreva o prompt de animação em inglês, seguindo a skill hook-dr-saude. Duração de ~3s, com fala sincronizada.
Aplique as travas: sem legenda queimada, sem voz extra, sem loop ou repetição, sem cortar a primeira palavra e com números por extenso.
Salve cada vídeo com o nome H01_[estrutura]_[prop].mp4, H02_…, na pasta Hooks do projeto.

5. Montar na timeline
Importe todos os hooks para um bin chamado HOOKS no Premiere.
Coloque os hooks em sequência na timeline, na ordem H1 → Hn, na trilha V1/A1, com 1s de gap entre eles.
Adicione um marcador em cada hook com o nome e a estrutura.

6. Relatório final
Me mande uma lista com cada hook, o status (ok ou refazer), o prompt de imagem e o de vídeo usados e o caminho do arquivo.
Aponte qualquer hook que tenha saído com problema (boca, prop deformado, avatar inconsistente).

Pode colocar as imagens para eu aprovar antes de gerar no Premiere com a nomenclatura correta.
```

### 4. Aprovações e decisões
```
exato, o Meat Hook é o visual
```
```
H09 e H10 saíram da sugestão do copy: um é numa fazenda e o outro num açougue
```
```
pode manter, e pode fazer 2 clipes caso precise; pode usar o MiniMax H3 Max 720p, que dá para fazer até 15s
```
```
gere as imagens primeiro e coloque na timeline para aprovar antes de animar
```
```
caso forem barrados, tente criar as imagens no Grok Image ou Nano Banana Pro
```

### 5. Ajustes nos start frames
```
algumas imagens como essa, que têm uma sequência lógica para demonstrar a ação do produto na maquete, têm que ser feitas assim  [+ print da referência]
```
```
H04 é um médico, como o copy pediu
```
```
H08 é uma mulher japonesa
```
```
H06 também não seguiu a referência do copy  [+ print]
```
```
dá um check com o que o copy pediu
```
```
H07 também não saiu conforme o que o copy pediu  [+ print]
```
```
HK4: o mel tem que cair na perna  [+ print da timeline]
```

### 6. Animação e ajustes nos clipes
```
pode agora animar os hooks, separados por nomenclatura
```
```
H05-2: o pai dela está voltando de costas
H02-1: o pai dela está correndo de costas; ele tem que virar e correr junto com os netos, ou afasta ele e deixa ele correndo em direção a ela  [+ prints]
```
```
H09-1: a voz está diferente da do H09-2
```
```
H05-1: preciso dele subindo a escada e parando 3 vezes, como é mencionado no hook  [+ print]
```
```
eles com outra roupa, e ele parando 3x na escada com dor no peito  [+ print]
```

### 7. Montagem com os corpos
```
perfeito, agora é só colocar cada hook com o corpo dos criativos
```
```
lembre de fazer a decupagem dos silêncios dos hooks
```
```
o primeiro vídeo vai ser empilhamento; nos outros dois, o hook original sai
```

### 8. SFX, transição e render
```
aplique os SFX e a transição que coloquei no HK1 do AD01  [+ print da timeline]
```
```
aplique em todos os outros
```
```
após isso, renderize na pasta EXPORT todos os ADs de forma organizada, cada variação de hook dentro da pasta do seu AD
```
```
deu erro, colocar novamente no Media Encoder
```
```
refazer novamente
```
```
aqui é a pasta do projeto, depois mover pra lá: Arquivo de Edição/23. Heart/CardioFlush/OT/[230926][OT] 128_PG [CardioFlush] - Hooks [Squad]
```
```
abra a pasta do projeto
```

### 9. Documentação
```
Perfeito, crie um documento de briefing de execução para deixar documentado, e a skill desse padrão; coloca tudo em um documento para compartilhar com os editores de tudo que fiz aqui nesses processos
```
```
os comandos que usei, de forma separada
```
