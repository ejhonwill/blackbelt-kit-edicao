---
name: analise-criativos-ponte
description: >-
  Analisa criativos de vídeo (ADs/VSLs) prontos e entrega um relatório completo por
  criativo, combinando 3 camadas: (1) QA técnico automático — arquivo são, resolução,
  formato 9:16, frame preto/congelado, silêncio, duração; (2) Detalhamento AD-por-AD —
  card com referência visual (mosaico de frames), resumo da edição, transcrição da fala
  palavra-por-palavra e pontos de atenção com severidade; (3) Análise PONTE — nota por
  letra (P·O·N·T·E), veredito, matriz de experimentação e as ações que mais movem
  conversão. Roda 100% local no terminal (extrai frames com ffmpeg, transcreve com
  Whisper). Use quando o usuário tiver vídeos prontos numa pasta e pedir para "analisar
  os criativos", "conferir os ADs", "montar o documento PONTE", "revisar antes de subir
  pro Meta/TikTok", "detalhar os hooks" ou apontar um arquivo/pasta de vídeo. Serve para
  1 vídeo ou dezenas (AD01, AD02...). NÃO é para GERAR criativos/prompts — esta ANALISA
  material já exportado.
---

# Análise de criativos — QA técnico + Detalhamento + PONTE

Esta skill transforma um criativo de vídeo (ou uma pasta com dezenas) num **relatório
único e escaneável** que responde às duas perguntas que importam antes de subir um AD:

- **"Tá são?"** → QA técnico automático (o script resolve sozinho).
- **"É bom? Converte? Onde vaza dinheiro?"** → Detalhamento editorial + análise PONTE
  (julgamento — você/Claude lendo o mosaico e a copy).

O entregável final é **um HTML auto-contido, tema escuro, um card por criativo**, no
padrão de entrega aprovado.

> Ambiente **local** (Claude Code no terminal). A transcrição da fala FUNCIONA aqui
> porque há rede pra baixar o modelo Whisper. Os relatórios são arquivos em disco que o
> usuário abre no navegador.

---

## O método PONTE (referência da camada 3)

| Letra | Camada | O que avaliar |
|-------|--------|---------------|
| **P** — Persuasão | Esqueleto | A espinha está completa? dor → promessa → mecanismo → prova → CTA. Onde quebra? |
| **O** — Orgânico decupado | Combustível | O hook tem origem validada? Dá pra rastrear 3 ativos: gancho, frase-objeção, momento de retenção? |
| **N** — Native creator | Embalagem | Parece criador nativo ou tem cara de anúncio? Onde a retenção sofre? |
| **T** — Traduzir mecanismo | Diferencial | Tem mecanismo traduzido (por que ISSO funciona) ou promessa vazia? Mata o "já tentei de tudo"? |
| **E** — Experimentação | Motor | Quais variáveis isolar e testar? (hook / ângulo / creator / CTA / duração). O E testa as outras 4 letras. |

Altitudes: **O, P, T** = conteúdo · **N** = formato · **E** = processo. Ordem de execução
real: O→P→T→N→E (o acrônimo é só mnemônico). Dar **nota 1–5 por letra** + veredito.

---

## Fluxo (siga em ordem)

### Passo 1 — Rodar o QA técnico (a máquina faz o pesado)
O motor é `scripts/conferir.py`. Rode apontando pra pasta dos vídeos, com OCR e transcrição:

```bash
python3 <skill>/scripts/conferir.py "<PASTA_DOS_VIDEOS>" \
  --formato 9:16 --min-largura 1080 --ocr --transcrever --modelo small --idioma por --jobs 4
```

Isso gera `<PASTA>/_QA/` com: `dados.json` (metadados + flags), `montage/*.jpg` (mosaico
com timecode), `transcripts/*.txt` (fala), `relatorio.html` (QA cru). Flags de check:
🔴 QUEBRADO/RESOLUCAO/FORMATO/SEM_AUDIO · 🟠 FRAME_PRETO/CONGELADO/DURACAO.

**Idioma do áudio:** se a fala for em inglês, rode a transcrição em inglês para sair limpa
— acrescente/troque para `--idioma eng` ou re-transcreva com Whisper `--language English`.
Transcrever no idioma errado embananou a fala (ex.: EN forçado como PT vira fonética).

### Passo 2 — Ler cada mosaico (a camada de julgamento)
Leia cada `<PASTA>/_QA/montage/*.jpg` com o **Read (visão)**. Para cada AD, anote:
- **one_line** — 1 frase: criador, cenário, b-roll principal, cards/overlays.
- **resumo_edicao** — como alterna talking-head × inserts × b-roll; o ângulo/hook; como fecha.
- **atencao** — riscos: compliance/claim/IP (🟠), execução/continuidade/typo (🟡),
  observações (⚪, ex.: "gêmeo do ADx, mesma criadora/roteiro"). **Regra de ouro:** legenda
  karaokê anima letra a letra — não acuse typo sem extrair 2-3 frames em alta ao redor do
  momento e confirmar.

### Passo 3 — Montar a análise PONTE (por criativo)
Com o mosaico + a transcrição (`_QA/transcripts/<name>.txt`), avalie as 5 letras: **nota
1–5**, **veredito**, **pontos** (good/bad), a **matriz de experimentação**, as **ações**
de maior impacto e a **nota global** (média ponderada, arredonda 1 casa).

### Passo 4 — Escrever o `analise.json`
Junte tudo dos passos 2–3 num `analise.json` (lista, 1 objeto por criativo). O campo
`name` **casa exatamente** com o nome no `_QA` (ex.: `AD10_H1`). Schema completo e exemplo
estão no topo de `scripts/montar_relatorio.py` e em `references/exemplo-analise.json`.

### Passo 5 — Gerar o relatório combinado
```bash
python3 <skill>/scripts/montar_relatorio.py \
  --qa "<PASTA>/_QA" --analise analise.json -o "<PASTA>" --projeto "<nome do projeto>"
```
Gera `Analise Criativos - <projeto>.html` (auto-contido, mosaico embutido em base64).
Se você pular o `--analise`, sai só a camada de QA técnico.

### Passo 6 — Entregar
```bash
open "<PASTA>/Analise Criativos - <projeto>.html"   # macOS
start "" "<PASTA>\Analise Criativos - <projeto>.html"  # Windows
```
No chat, resuma: nota PONTE por AD, os achados críticos (🔴/🟠) e as 3 ações de maior
impacto. Se rodou vários ADs, compare os hooks e diga qual ângulo tende a ganhar.

---

## Convenção de nomes
O rótulo de cada card sai do **nome do arquivo/pasta**: `AD01`, `AD 02`, `.../AD03/video.mp4`,
e o hook de `HOOK1` / `H1` / `..._H2.mp4`. Nomeie assim que os cards saem certinhos
(`AD01_H1`, `AD02_H3`...).

## Requisitos (o instalador resolve)
`ffmpeg` (obrigatório) · `tesseract` + idioma (para `--ocr`) · Python `pillow` e
`faster-whisper` (para transcrição). Ver `references/setup.md`. Se faltar algo, instalar
antes: macOS `brew install ffmpeg tesseract tesseract-lang`; Windows via os instaladores
do pacote.

## Escopo
- **É para:** material pronto (mp4/mov) que vai subir — checar erro de imagem, legenda,
  arquivo quebrado, compliance, coerência copy×fala, e avaliar a conversão pelo PONTE.
- **NÃO é para:** gerar/criar criativos ou prompts (isso é outra skill).
