---
name: advalidado-weightloss
description: Clona um AD validado de emagrecimento (story-ad de mãe/mulher, GLP-1, "receita de gelatina", DR saúde EUA) de ponta a ponta — ficha técnica do original, hooks novos, start frames da personagem nova (GPT Image 2.5 no HWStudio), avatar falante na HeyGen (Avatar IV, voz desenhada), b-roll palavra por palavra (50% IA com a mesma personagem + 50% orgânico do TikTok recortado sem texto), e a edição dinâmica/dopaminérgica montada no HyperFrames (punch-in, legenda palavra por palavra na área segura do Reels, lettering nas frases fortes, X vermelho, seta de CTA, SFX discretos do Baú). Use SEMPRE que pedirem "clona esse AD de emagrecimento", "faz o ADVALIDADO-WEIGHTLOSS", "mesmo AD com outra mãe/personagem", "AD validado weight loss", "monta o AD no HyperFrames igual ao 131026", ou mandarem um AD validado de perda de peso / GLP-1 / gelatina pedindo versão nova. NÃO é para conferir AD pronto (conferir-ads-por-frame), nem para clone genérico fora de emagrecimento (clone-ad-validado), nem para só escrever hooks (hooks-meat-hook).
---

# ADVALIDADO-WEIGHTLOSS

Receita validada no job **AD 131026 – DTC Pro** (13/10/2026): AD de 3:27 de mãe pós-parto,
foto do aniversário da filha → GLP-1/GIP pararam → receita de gelatina → CTA para VSL.
Resultado: H1 + corpo em 201 s, 41 b-rolls, 193 grupos de legenda, 38 letterings, 77 SFX.

Pasta de referência (tudo pronto, pra copiar padrão): `~/Documents/01_Producao/Demanda Outubro/Criativos 13-10 - DTC Pro/AD 131026 - DTC Pro/`.

## Estrutura do job

```
<JOB>/
  original/      AD validado (só leitura — nunca alterar)
  analise/       ficha técnica (analise-criativo-ficha) + _QA
  copy.md        hooks novos + regra do corpo + avatar/voz
  avatar/        H?_start.png, prompts/, heygen/ (pedido, resposta, mp4)
  broll/         plano.py → plano.json, imagens/ (IA), tiktok/ (candidatos, capas, vídeos), folha_de_contato.jpg
  edicao/        palavras_*.json, plano_tempos.json, build.py
  hyperframes/<projeto>/   index.html gerado + assets/ (broll, sfx, fonts)
  entrega/
```

## Passo a passo (aprovação do usuário antes de cada gasto)

1. **Ambiente** — Whisper, ffmpeg, HyperFrames (Node 24: `export PATH=/opt/homebrew/opt/node@24/bin:$PATH`; se o node quebrar com `libsimdjson`, `brew reinstall node@24`), HeyGen CLI logado (`heygen auth status`), HWStudio.
2. **Ficha do original** — skill `analise-criativo-ficha` com `-o <JOB>/analise/_QA` (nunca gravar dentro de `original/`). Transcrever com **medium** + `initial_prompt` (Mounjaro, Ozempic, GLP-1, GIP, gelatin) e **conferir a legenda queimada** — o `small` pulou "After 35," e trocou nomes. Trechos borrados no original = celebridade/especialista real escondido: **nunca** reproduzir nome/rosto (ex.: "Jillian is suing" → "She's suing").
3. **Copy e briefing do copywriter** — normalmente a copy VEM PRONTA (doc com hooks, corpo, briefing e comentários). Ler a copy **junto com os comentários** (Doc: exportar com comentários; cópia de Doc perde comentário) e seguir à risca: hooks e corpo como estão escritos, cada pedido de insert/b-roll/lettering vira item do plano, personagem/voz/estilo saem do briefing. Registrar em `copy.md` (copy recebida + lista de pedidos do copywriter). Só se a copy NÃO trouxer hooks: escrever no mesmo formato do original, 1 ângulo cada, ≤ 5 s (~14 palavras). Sem copy de corpo: corpo = copy do original **palavra por palavra** (só tira nome de pessoa real). Divergência entre copy e briefing → perguntar, não decidir.
4. **Start frames** — GPT Image 2.5 Flare **pelo OpenRouter** no HWStudio (`or:openai/gpt-image-2.5-flare`, `aspect_ratio=9:16 quality=high`; ~US$ 0,04/img; sai 864×1536). O `oa:` (OpenAI direto) estava sem crédito. H1 = âncora; H2/H3 com `--imagem H1_start.png` + "IDENTITY: the SAME woman…". Boca fechada, olhar na lente. Prompt-base em `scripts/plano_broll.py` (blocos CAM/ANTI/PELE).
   - MCP do HWStudio aponta pro servidor local (desligado, exige Postgres). Usar `scripts/hws.sh` (CLI com URL+token do site tirados da config do MCP, sem imprimir).
5. **Avatar HeyGen** — CLI (créditos do plano, não a chave de API de 9 créditos). `heygen asset create --file H1_start.png` → `video create` com `type:"image"` (Avatar IV), `aspect_ratio:"9:16"`, `resolution:"1080p"`, `expressiveness:"medium"`, `motion_prompt`. Voz: `heygen voice create --prompt "warm friendly female voice, American, 30s, casual" --gender female` (sem `--locale`, senão volta vazio) → medir F0 com `scripts/f0_voz.py` contra o original; "Warm Pro 30s US" (`D78Li9u7M20j5Jdu77J5`) serviu. Corpo ~800 créditos (196 s). **Conferir a fala contra a copy** (difflib) antes de editar; o Whisper junta palavras ("another way" sumiu mas estava lá — retranscrever o trecho isolado).
6. **Plano de b-roll palavra por palavra** — `scripts/plano_broll.py`: posição = onde o original tinha b-roll; conteúdo = **o que é falado naquela palavra**. Toda pessoa = a personagem do H1 (ref). Mecanismo 3D com bloco de estilo fixo SEM referência. Texto exato no prompt quando precisa ("TOTAL $2,000.00", "TOO BIG", "Stop suffering and watch this"). Antes de grávida/pós-parto, escrever "NOT pregnant" (BR01 saiu grávida na 1ª).
7. **50% orgânico do TikTok** — busca por palavra só pelo Chrome (`tiktok.com/search/video?q=`), guardando links no `localStorage` e lendo 2 buscas por vez (saída longa trunca; número solto é bloqueado como "cookie"); lote de >20 navegações estoura o tempo. Capas com `yt-dlp --skip-download --write-thumbnail`, escolha no olho (plano de ação > talking head), download `-f bv*+ba/b`. **Recortar trecho sem texto queimado** (ffmpeg `crop` mantendo 9:16 + scale 1080×1920, `-an`) e conferir quadros; se não limpar sem ficar borrado (fonte 576p), trocar pela IA. Orgânico = personagem nunca aparece; IA fica com pessoa, 3D e texto exato.
8. **Folha de contato** (`scripts/folha_de_contato.py`, selo IA/TIKTOK) → aprovação antes de animar/montar.
9. **Montagem HyperFrames** — transcrever o avatar novo palavra por palavra e **reposicionar tudo na voz nova** (mapear original→novo com difflib, depois ajustar à mão pelas palavras). Gerador único `scripts/build_hyperframes.py` (listas BROLL / PUNCH / DRIFT / LETTER / FLASH / DIM / SETA / SFX / CORRIGE). Rodar `npx hyperframes check` + `snapshot --at …` e olhar os quadros. Abrir com `npx hyperframes preview --background`.

## Padrão de edição (dinâmica / dopaminérgica)
- Avatar dentro de `#cam-in`: punch-in snap 0,16 s a cada frase (1,0 ↔ 1,1–1,28; crash-zoom 1,42 em "zoomed in"); drift lento nos momentos emocionais.
- B-roll: imagem com push lento ou punch; rajada de 1 corte por palavra em listas ("low carb, fasting, walking…"); a "foto" vira polaroid e depois zoom no que é falado (braço/barriga/papada); volta emocional com foto NOVA (sem repetir footage).
- Legenda: grupos ≤ 3 palavras, Montserrat ExtraBold 76 px, contorno preto, palavra ativa amarela 1,12×, `top:1250px` (área segura Reels); some durante lettering; `.w {margin:0 .16em}` senão a palavra ativa come o espaço.
- Lettering Anton 132 px (vermelho/amarelo/branco/caixa/gigante) só com palavras faladas; X vermelho em "No injection / no diet / no gym"; seta branca pulsando no CTA; flash branco nas viradas; escurecer em frase de arrependimento.
- SFX do Baú (`.../Bau dos Black Belt/SFX/TOP AUDIOS`, copiar antes de usar): whoosh .12–.2, pop .18–.45, boom .2–.28, riser .18, shutter 1.0 (é −15 dB), caixa registradora .28, ding .2–.25.

## Armadilhas
- Backup `.html` com `data-composition-id` dentro do projeto = erro `multiple_root_compositions` (áudio duplicado). Guardar fora.
- Studio reformata o `index.html`; sempre regerar pelo build, nunca `replace` no HTML.
- Três `<img>` com o mesmo `src` → `duplicate_media_discovery_risk`: usar cópias/arquivos derivados.
- Avisos `nested_structure_needs_subcomposition` / `container_overflow` do `#cam-in` são esperados.
- Compliance: claims GLP-1, marca Ozempic na tela, antes/depois de corpo e TikTok de terceiros = risco Meta/IP — avisar o usuário, não decidir por ele.
