---
name: video-workflow
description: |
  Transforma um vídeo existente em um workflow de edição visual bloco a bloco
  para o Google Flow (Veo 3.1). Divide o vídeo em blocos semânticos de ~10s
  alinhados à fala (corta no fim de frase, nunca no meio), auto-detecta o
  idioma, transcreve o áudio com Whisper, extrai um frame por bloco, e para
  cada bloco gera uma tradução visual (B-roll, motion design, overlay) com
  prompt Veo 3.1 pronto pra colar no Flow — no idioma correto da fala.
  Use quando: "dividir o vídeo", "criar edição visual", "gerar B-roll",
  "transformar a fala em imagem", "workflow visual", "roteiro de B-roll",
  "prompts pro Flow/Veo a partir do vídeo", "analisar vídeo", "editar vídeo
  com IA", ou o usuário enviar um vídeo e quiser ilustrar visualmente o que
  é falado.
argument-hint: "<caminho_do_vídeo> [--lang pt|en] [--transcript copy.srt] [--target 10]"
allowed-tools: Bash, Read, Write
---

# Video Workflow

Pega um vídeo já gravado (narração, VSL, UGC, talking head, depoimento) e
produz um **plano de edição visual bloco a bloco** pronto para executar no
Google Flow: para cada trecho de ~10s, o que é dito vira uma imagem/animação,
com prompt Veo 3.1 pronto pra colar.

---

## Passo 0 — Entender o pedido

Identifique:
- **Caminho do vídeo** — obrigatório. Pergunte se não fornecido.
- **Idioma** — auto-detectado pelo Whisper. Use `--lang` só para forçar (ex.: `--lang en`).
- **Transcrição pronta** — se o usuário já tem SRT/copy, use `--transcript arquivo.srt` para pular o Whisper.
- **Duração dos blocos** — padrão 10s. Use `--target 15` se o usuário quiser blocos maiores.

---

## Passo 1 — Instalar dependências

```bash
which ffmpeg || brew install ffmpeg
pip3 show openai-whisper 2>/dev/null | grep Name || pip3 install openai-whisper --quiet
```

---

## Passo 2 — Processar o vídeo

```bash
SCRIPT="$HOME/.claude/skills/video-workflow/scripts/process_video.py"
python3 "$SCRIPT" "<CAMINHO_DO_VIDEO>"
```

Com opções opcionais:
```bash
# Forçar idioma
python3 "$SCRIPT" "video.mp4" --lang en

# Usar transcrição já existente (pula Whisper)
python3 "$SCRIPT" "video.mp4" --transcript copy.srt

# Blocos de 15s, sem cortar os clips (só frames + json)
python3 "$SCRIPT" "video.mp4" --target 15 --no-clips
```

O script vai:
1. Auto-detectar o idioma da fala
2. Transcrever com Whisper (corte semântico — respeita fim de frase)
3. Criar `blocos/bloco_NN.mp4` por bloco
4. Extrair `frames/bloco_NN.jpg` (frame do meio de cada bloco)
5. Gravar `blocos.json` + `blocos.md`

A última linha começa com `BLOCOS_JSON:` — guarde esse caminho.

---

## Passo 3 — Ler a referência do Flow antes de escrever qualquer prompt

```bash
cat "$HOME/.claude/skills/video-workflow/references/flow-veo-reference.md"
```

Calibre sua escrita pelos padrões ali: **Subject → Setting → Light → Camera + Audio**, ~50–60 palavras em inglês, 1 conceito por prompt.

---

## Passo 4 — Ler os blocos e ver os frames

```bash
cat "<BLOCOS_JSON>"
```

Para cada bloco:
1. **Veja o frame** (`frame`) — é o que JÁ está na tela. B-roll bom complementa ou contrasta; nunca repita o óbvio. Se já tem talking head, o B-roll é apoio (não compete com o rosto).
2. **Leia a fala** (`text`) no idioma detectado (`language`). Identifique: há algo concreto (objeto, número, lugar) ou abstrato (sentimento, conceito)?
3. **Decida o tipo**: B-roll, Motion design, Overlay/Lettering, ou Stock/Real.

---

## Passo 5 — Gerar o workflow visual

### Cabeçalho (escreva uma vez, no topo do PROMPTS_FLOW.txt)

```
TEMA: [do que o vídeo trata, 1 linha]
TOM: [registro — ex.: DR agressivo, educativo, depoimento emocional, VSL]
PALETA: [3-4 cores que amarram tudo]
LINHA VISUAL: [regra de consistência — lente, luz, estética repetida em todos os blocos]
IDIOMA DA FALA: [idioma detectado]
DICA FLOW: [se houver personagem/produto recorrente, sugerir criar @asset no Flow]
```

### Por bloco (template fixo — 1 bloco = 1 prompt = 1 geração no Flow)

```
BLOCO NN · [mm:ss-mm:ss] (Xs) · bloco_NN.mp4
FALA: "[trecho transcrito no idioma original]"
NA TELA: [o que o frame já mostra]
IDEIA VISUAL: [como traduzir a fala em imagem — 1-2 frases]
TIPO: B-roll | Motion design | Overlay/Lettering | Stock/Real
PROMPT FLOW (Veo 3.1):
[prompt em inglês, ~50-60 palavras, Subject→Setting→Light→Camera. Última frase: Audio:]
CORTE: [como entra/sai pro próximo bloco — match cut, hard cut, whip, dissolve]
```

---

## Passo 6 — Salvar os arquivos de saída

Salve **dois arquivos** na pasta `_workflow/`:

### `PROMPTS_FLOW.txt`
Um bloco por seção, com o template acima. Formato limpo para copiar e colar direto no Flow.

### `WORKFLOW.md`
Documento completo com cabeçalho de direção + todos os blocos + tabela de assets + ordem de montagem + próximos passos.

---

## Passo 7 — Entregar ao usuário

Informe:
1. **Caminho da pasta** `_workflow/`
2. **Idioma detectado** e número de blocos
3. **Preview dos 2–3 primeiros prompts** no chat (prontos para usar sem abrir arquivo)
4. **Próximos passos**: qual bloco priorizar, se deve criar @asset no Flow para consistência

---

## Princípios criativos

1. **Não duplique a tela.** Se a fala diz "café" e a tela já mostra café, o B-roll deve ADICIONAR (origem do grão, vapor em macro, ritual), não repetir.
2. **Concreto vira literal, abstrato vira metáfora.** "30 dias" → calendário animado. "Sua mente fica nublada" → névoa dissipando, não um cérebro genérico.
3. **Coerência acima de variedade.** Melhor 8 blocos na mesma linguagem visual do que 8 estéticas diferentes. Repita luz, lente e paleta.
4. **B-roll sob narração é mudo.** Quando o áudio original continua por cima, o prompt deve pedir `Audio: ambient texture only, no dialogue.`
5. **Ritmo por contraste.** Alterne blocos "calmos" (talking head, overlay simples) com blocos "cheios" (B-roll cinematográfico, motion).
6. **Hook nos primeiros 10s.** O bloco 01 é o mais importante — proponha o visual mais forte ali.
7. **Fala sempre no idioma original.** O campo `FALA:` usa o texto transcrito como está. Os prompts Veo são sempre em inglês.

---

## Regras do Prompt Veo 3.1

- **Estrutura**: Subject → Setting → Light → Camera/Movement → Style. `Audio:` em frase separada.
- **Comprimento**: 50–60 palavras. Específico o bastante, curto o bastante.
- **Inglês**: sempre, mesmo que o vídeo-fonte seja PT.
- **1 conceito por prompt**: não empilhe 3 cenas.
- **Sempre termine com `Audio:`**: se B-roll sob narração → `Audio: ambient texture only, no dialogue.`
- **Duração**: 8–10s por geração. 1 bloco = 1 clipe Veo.

---

## Fallbacks

| Situação | Solução |
|---|---|
| `ffmpeg not found` | `brew install ffmpeg` |
| `whisper not found` | `pip3 install openai-whisper` |
| Transcrição errada | Rode com `--lang en` (ou idioma correto) |
| Já tem SRT/copy | `--transcript copy.srt` pula o Whisper |
| Vídeo sem áudio | Script gera blocos por tempo fixo; trabalhe pelos frames |
| Vídeo muito longo | Processe e entregue o workflow em lotes de ~10 blocos |
| `ModuleNotFoundError: torch` | `pip3 install torch` antes do whisper |

---

## Dicas de Uso com Google Flow

1. Abra [flow.google.com](https://flow.google.com)
2. Um bloco = uma geração com Veo 3.1
3. Para manter personagem/produto consistente entre blocos, crie um `@asset` no projeto
4. Use o último frame de um bloco como **start frame** do próximo para continuidade
5. Ajuste aspect ratio para o formato do projeto (9:16, 16:9, 1:1)
