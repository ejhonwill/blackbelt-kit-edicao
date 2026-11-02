---
name: edicao-prosperidade-adhw
description: Edição de ADs de prosperidade / manifestação / identidade (Biz Opp, mercado americano) da H&W, do documento de copy com vários bodies até os ADs renderizados no padrão premium de resposta direta — avatares no GPT Image 2.5, voz ElevenLabs v4 com decupagem por silêncio, avatar falante HeyGen Avatar IV, pacote de b-roll GPT Image → Kling Turbo sem repetir footage, Premiere montado pelo Tools PRO (marcadores, b-roll, punch-in, zoom in/out, trilha, SFX, sem buracos), camada de acabamento no HyperFrames (legenda com palavra ativa roxa, lettering amarelo com deep glow, flash/luz, CTA), render no Media Encoder e QA. Use SEMPRE que pedirem "edita esses bodies", "executa essa demanda de ponta a ponta", "faz os ADs do Kings Code / Divine Prayer / Pineal / AI Loophole", "monta os ADs no padrão premium DR", "do doc de copy até o render", ou mandarem um Google Doc de copy com Body 1..N e referências de edição — mesmo sem dizer "skill". NÃO é para conferir AD pronto (conferir-ads-por-frame), nem para clonar um AD validado trocando personagem (clone-ad-validado), nem para cortar silêncio de aula (cortar-aula).
---

# Edição Prosperidade · AD H&W

Pipeline validado no job **Kings Code 215_MV** (7 bodies → 7 ADs, 09/10/2026). Cada etapa tem script em `scripts/`; o que muda de job para job fica num `job.json`.

Leia antes de começar:
- `references/compliance.md` — pessoa real, celebridade e política da Meta. **Ler sempre.**
- `references/padrao-premium-dr.md` — o padrão de edição medido (ritmo, legenda, lettering, áudio, marcadores).
- `references/armadilhas.md` — o que já quebrou e como evitar. Consulte ao bater em erro.
- `references/pedidos-e-comandos.md` — os pedidos do Jhon na ordem e os comandos crus de cada ferramenta.

## Regras do Jhon (valem em todo job)

- Responder em português. Voz dos ADs sempre **inglês americano**.
- **Nunca repetir o mesmo footage na mesma timeline.** Esgotou o tema → gerar clipe novo.
- Mostrar custo e pedir confirmação antes de gerar em lote (Higgsfield / HeyGen) quando o job for novo; dentro de um job já autorizado, seguir.
- Arquivo com defeito nunca é sobrescrito: vai para `_DESCARTADOS/` com o motivo no nome.
- Captura de tela só da janela do app (`screencapture -l <windowID>`), nunca a tela inteira; apagar depois de olhar.
- Lettering premium = palavra-chave em **amarelo com deep glow**; legenda com a palavra ativa em **caixa roxa**; transições **Flash/Light**.

## Preparar o job

```bash
WORK=<pasta de trabalho local, fora do Drive>        # ex.: scratchpad da sessão
mkdir -p $WORK/{avatars,voz,heygen,broll/stills,broll/videos,timeline}
cp -R ~/.claude/skills/edicao-prosperidade-adhw/scripts/premiere/* $WORK/timeline/
cp ~/.claude/skills/edicao-prosperidade-adhw/scripts/geracao/* $WORK/
cp ~/.claude/skills/edicao-prosperidade-adhw/assets/job_exemplo.json $WORK/job.json   # preencher
```
Os scripts gravam os dados do job ao lado deles — por isso são copiados para `WORK`, nunca rodados de dentro da skill.

Pasta da demanda (a `job` do job.json), criar se faltar: `00. BRIEFING E REFERENCIAS`, `MEDIA/{IMG/01 ORIGINAIS, IMG/02 APRIMORADAS, IMG/03 AVATARES FINAIS, BROLL, AUDIO/FALAS, AUDIO/TRILHA, AUDIO/SFX, HEYGEN, HIGGSFIELD, LEGENDAS, LETTERING, BANCO}`, `PROJECT`, `EXPORT`, `HYPERFRAMES`, `_DESCARTADOS`. Raiz: `Arquivo de Edição /<NN. Nicho>/<Produto>/<OT|Offer>/` (atenção ao espaço no fim de `Arquivo de Edição `).

## Etapa 1 · Entender o trabalho

1. Ler o Google Doc pelo conector do Drive (`read_file_content` com `includeComments`). Para pegar as **imagens de avatar** do doc: `curl -sL "https://docs.google.com/document/d/<ID>/export?format=zip"` e mapear `images/imageN.png` pela ordem de aparição.
2. Extrair o inglês de cada body (coluna TRADUZIDO) para `$WORK/voz/copy_en.json` — formato `{"B01":[linhas], ...}`.
3. Baixar as referências (`curl -sL "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`), medir: cortes (`select='gt(scene,0.25)'`), mosaico 1 quadro/2 s, Whisper por palavra, volume nas pausas. Detalhes em `references/padrao-premium-dr.md`.
4. Conferir `references/compliance.md` contra **cada avatar** e cada frase sensível da copy (ex.: "If you're a Christian" fere Atributos Pessoais da Meta). Avisar o Jhon; não reescrever a copy por conta própria.

## Etapa 2 · Avatares (GPT Image 2.5 · Higgsfield CLI)

- CLI: `~/.npm-global/bin/higgsfield`. Se der `workspace_membership_required` ou saldo baixo, parar e pedir `higgsfield auth login` ao Jhon (login de navegador).
- Prompts em `$WORK/avatars/prompts.json` (modelo: `assets/avatares_prompts_exemplo.json`) — com referência: bloco `IDENTITY: the SAME …`; pessoa real: `ref: null` e persona fictícia descrita do zero; avatar que não é selfie (palco, podcast): `"selfie": false`.
- `python3 -I gen_avatars.py $WORK` → 2 variações por body; `python3 -I hf_fetch.py $WORK/avatars/jobs.json $WORK/avatars png`.
- QC: folha com os rostos recortados; escolher a melhor; marcar em `job.json → bodies.Bxx.avatar`. `nsfw` em uma variação = usar a outra.
- Copiar: originais → `IMG/01`, todas → `IMG/02 APRIMORADAS` (`Bxx_AVATAR_aprimorada_vNN.png`), escolhidas → `IMG/03 AVATARES FINAIS` (`Bxx_AVATAR_final_v01.png`), descartadas → `_DESCARTADOS/IMG`.

## Etapa 3 · Voz e decupagem (antes do avatar)

- Vozes: `GET https://api.elevenlabs.io/v2/voices` (chave em `~/.config/hw-creative/.env`); escolher uma americana diferente por persona (premade não ocupa vaga). Gravar em `job.json`.
- `python3 -I tts.py $WORK B01 B02 …` — **no máximo 5 em paralelo** (limite de concorrência da conta; 429 = refazer só o que falhou).
- `python3 -I decupar.py $WORK Bxx` (pelo **silêncio real**: pausa > 0,42 s vira 0,32 s com 0,15 s de borda) → `Bxx_VOZ_decupada_v02.wav`.
- Conferir: `mlx_whisper Bxx_VOZ_decupada_v02.wav --model mlx-community/whisper-large-v3-turbo --language en --word-timestamps True --output-format json --output-dir $WORK/voz/whisper` (o `dados.py` usa esses JSONs depois) × `copy_en.json`; aceitar diferença só de número escrito; repetição no fim é alucinação do Whisper — confirmar transcrevendo só os últimos 12 s.
- Copiar bruta e decupada para `MEDIA/AUDIO/FALAS/{BRUTA,DECUPADA}`.

## Etapa 4 · Avatar falante (HeyGen Avatar IV · CLI)

- `heygen auth status` (créditos do plano — não a chave de API). Avatar IV, não V: aceita `expressiveness` e `motion_prompt`.
- Motion prompt por body com o **arco da copy** em `$WORK/heygen/motion.json` (exemplo em `assets/motion_exemplo.json`).
- `python3 -I heygen_gerar.py $WORK B01 …` → poll `heygen video get <id>` → baixar para `MEDIA/HEYGEN/Bxx_AVATAR_heygen-IV_v01.mp4`.
- QA: specs (1080×1920, 25 fps), duração = áudio, mosaico de 8 quadros por avatar (identidade estável), sincronia pelo início das pausas (`silencedetect` vídeo × wav: esperado ≤ 25 ms).

## Etapa 5 · Pacote de b-roll

- Base pronta do nicho: `assets/broll_prosperidade.json` (46 cenas com palavra-chave, cena e movimento). Copiar para `$WORK/broll/broll.json` e acrescentar o que a copy pedir.
- `python3 -I gerar_stills.py $WORK` → QC visual (texto legível onde não devia, rosto parecido com famoso) → `python3 -I gerar_videos.py $WORK` (Kling 3.0 Turbo, 1080p, 5 s, 10 créditos).
- Copiar para `MEDIA/BROLL/{STILLS,VIDEOS}` como `BRnn_<KEYWORD>_kling-turbo_v01.mp4` e gerar `VIDEOS SEM AUDIO/*_mute.mp4` (`ffmpeg -map 0:v -c copy`).
- Acervo da casa (`H&W - Edição de Vídeo -Q3/Assets/`): `Footages/Cérebro`, `Footages/Multidões`, `CLICK BELOW/learn more.mov`, `Bau dos Black Belt/{Música/Trilha Sonora, SFX/TOP AUDIOS, Transições/Transições}`.
- Figura pública citada na copy (MJ, Ali, Phelps, Carrey…): footage real só com aval do Jhon (ver compliance). `cortar_figuras.py` recorta 9:16 / 5 s / sem áudio; registrar fonte em `FONTES.txt`; evitar logo e marca d'água.

## Etapa 6 · Premiere na ordem certa

Pré-requisitos: Premiere aberto no projeto do job; painel Tools PRO com **Modo avançado** ligado (o Jhon liga; reinício do Premiere desliga). Ponte: `pr.sh arquivo.jsx` / `call.py` (curl na 7842 — funciona mesmo se o MCP não carregou na sessão).

1. Projeto: copiar `Projeto Padrão.prproj` (está em qualquer job vizinho em `PROJECT/`) para `PROJECT/<nome do job>.prproj` e `open -a "Adobe Premiere Pro 2026"`. Conferir `app.project.path` antes de escrever.
2. `python3 -I preparar_midia.py "<job>/MEDIA"` (cópias sem áudio, SFX normalizados, trilha por body) e `python3 -I importar.py $WORK/timeline "<job>"` (editar a lista `lotes` conforme o que importar).
3. `python3 -I criar_seq.py $WORK/timeline B01 …` (clona a 9x16, 25 fps, sem diálogo).
4. `python3 -I brutos.py $WORK/timeline B01 …` (V1 avatar, A2 voz decupada, A1 mudo, trilhas nomeadas).
5. `python3 -I dados.py $WORK` → legendas SRT (texto da copy + tempo do Whisper) e mapa de marcadores. `pr_legenda_nativa_criar` por sequência (projeto salvo antes).
6. Marcadores: `pr_marcadores_criar` com nome e comentário — vermelho BROLL, azul LETTERING, amarelo KEYWORD, ciano CORTE_RITMO, laranja TRANSICAO, branco CENA.

## Etapa 7 · Montagem

- `python3 -I plano.py $WORK/timeline Bxx` monta o plano: b-roll único por timeline (listas `ALT`), figura real em toda menção, punch-in 112% sincronizado, zoom 100↔107% no avatar, whoosh por b-roll, pop/boom/ding no lettering, riser antes do CTA, buracos < 0,6 s fechados.
- Primeira montagem: `python3 -I montar.py $WORK/timeline Bxx`. Remontagem só da V2/áudio + zoom + fechar buracos: `montar2.py`.
- Conferir lendo de volta (`ler.jsx`): repetidos = 0, punch-in com `inPoint == start`, buracos = 0, sobreposição = 0. Ver no Monitor de Programa com captura só da janela.

## Etapa 8 · Acabamento no HyperFrames

- Copiar `scripts/hyperframes/*` para `<job>/HYPERFRAMES/_gerador/` e os `Bxx_timeline.json` + `Bxx_plano.json` para `<job>/HYPERFRAMES/_dados/`. Lettering vem de `MEDIA/LEGENDAS/Bxx_LETTERING_v01.srt`.
- `python3 -I build.py B01 …` → `npx hyperframes check` (0 erros) → `snapshot` em 3 tempos e compor sobre o avatar para ver → `render.sh <HYPERFRAMES> v01 B01 B02 …` (MOV ProRes 4444, ~2–4 min cada).
- `python3 -I overlay.py $WORK/timeline Bxx` coloca o overlay na V3 e apara no fim da sequência.
- A faixa de **legenda nativa precisa ser desligada no olho** antes do render (não há API) — avisar o Jhon.

## Etapa 9 · Render e QA

- `python3 -I enc.py` (fila do Media Encoder, nome de `job.json → entrega`).
- QA de cada MP4: `ffprobe` (1080×1920, 25 fps, duração), `ebur128` (≈ −16 LUFS), `blackdetect` + `freezedetect`, mosaico de 6 quadros por AD procurando **legenda nativa duplicada**.
- Defeito → corrigir, renderizar de novo, antigo para `_DESCARTADOS/EXPORT/` com o motivo.

## Fechamento

Resumo em português: o que foi entregue (pastas), o que ficou pendente com o Jhon (olho da legenda, frases de compliance, hooks vazios), créditos gastos (`higgsfield account status`, `heygen auth status` antes × depois). Salvar aprendizado novo em `references/armadilhas.md`.
