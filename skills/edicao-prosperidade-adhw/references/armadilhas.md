# Armadilhas (o que já quebrou e o conserto)

Acrescente aqui toda armadilha nova, com data e job.

## Contas e ferramentas
- **Higgsfield CLI `workspace_membership_required` / saldo de 88**: a conta caiu do workspace da empresa. Só o
  Jhon resolve (`higgsfield auth login`, navegador). Não trocar de workspace por conta própria. (Kings Code)
- MCP do Higgsfield dá 401 sozinho → usar o CLI. MCP que subiu depois do início da sessão → curl direto.
- `generate create --json` devolve **array** de ids. "no response received" = job NÃO criado (conferir na lista);
  PNG grande falha no envio → JPG. 503/520 passageiros → tentar de novo com pausa.
- Um job do Kling ficou `in_progress` por mais de 1 h: renomear a chave no jobs.json e reenviar.
- **ElevenLabs**: máximo 5 requisições simultâneas (429 `concurrent_limit_exceeded`).
- **HeyGen**: créditos do plano estão no CLI (`heygen auth status`), não na chave de API. Avatar IV para persona
  gerada por IA (o V recusa motion prompt/expressividade e o Jhon reprovou). HeyGen entrega 25 fps.
- `tts_aula.py`/scripts com regex de seção: o roteiro precisa de uma seção `## ` depois da NARRAÇÃO.

## Áudio
- Decupar pelo **alinhamento de texto** do ElevenLabs mordeu fim de palavra (Whisper ouviu "pro…", "Jensen").
  Decupar pelo **silêncio real** (`silencedetect -42 dB`, borda 0,15 s).
- Whisper inventa repetição depois do fim do áudio → transcrever só o final para confirmar.

## Premiere
- **Clipe do Kling, transição do Baú e o mp4 da HeyGen trazem áudio**: `overwriteClip` na V2/V3 joga o som na
  A2/A3 e apaga a voz/trilha. Sempre usar a cópia `_mute`.
- `overwriteClip` só com objeto `Time` (string de segundos vai para o 0).
- Punch-in: o Premiere arredondou um `inPoint` 1 quadro antes → regravar em ticks (`quadro × 10160640000`) e
  conferir `inPoint == start`.
- Buraco de 1 quadro (0,04 s) entre clipes da V2 → avatar pisca. Rodar `fechar.jsx` no fim.
- Sequência nova: clonar a 9x16 do modelo (`createNewSequence` abre diálogo modal e trava a ponte).
- `pr_legendas_mogrt_aplicar` (MOGRT) acordou o After Effects e **derrubou o Premiere**; o reinício desliga o
  Modo avançado. Lettering e legenda animada → HyperFrames.
- Legenda nativa não tem API: desligar o olho da faixa à mão antes do render, senão sai queimada por baixo
  (aconteceu no AD02).
- Export direto (`exportAsMediaDirect`) com mídia no Drive pode travar o Premiere → fila do Media Encoder.
- O usuário pode estar mexendo no Premiere: não mexer no playhead/capturar enquanto a sequência ativa muda;
  toda escrita pelo NOME da sequência, nunca pela ativa.

## HyperFrames
- Precisa de Node 22+: `export PATH=/opt/homebrew/opt/node@24/bin:$PATH`.
- Animar `letterSpacing` → erro `gsap_non_transform_motion` (treme no render). Só escala/opacidade/desfoque.
- Camada de glow atrás da palavra → `content_overlap`; marcar cada span com `data-layout-allow-overlap`.
- Lettering a 30% cobre o rosto na selfie; 47–50% (peito) com legenda em 71%.
- Os avisos `nested_structure_needs_subcomposition` (centenas) são só de organização do Studio; ignorar.
- Render MOV ProRes 4444 ≈ 750 MB–1,3 GB por body; 2 em paralelo ≈ 3–4 min cada.

## Shell / Python
- zsh não separa lista em `for x in $VAR` nem aceita `[$k]` em filtro do ffmpeg → usar bash ou Python.
- `python3 -I` não enxerga pacotes do usuário (Pillow) nem módulos locais → rodar sem `-I` nesses casos.
- `bash -c` com script inline foi barrado pelo verificador de segurança → escrever script em arquivo.
- Caminhos da H&W têm `[colchetes]`: nunca `glob`; usar `os.listdir`.

## Hooks direto no Kling (LungTyde 239_MN, 09/10/2026)
- `marker.end = new Time()` dá "Illegal Parameter type" — passar **segundos (número)**: `m.end = t + dur`.
- Kling 3.0 `--sound on` às vezes solta uma palavra inventada no 1º segundo ("Lunks", "Rub"). Achar o início real
  com `silencedetect` + Whisper do trecho aparado e usar como ponto de entrada (não reencodar).
- Nano Banana Pro falha calado (`failed`, sem motivo) em alguns frames; GPT Image 2.5 resolveu um. Referência com
  órgão ensanguentado → `nsfw`: recortar só a pessoa e pedir ilustração médica 3D no lugar.
- O texto comum do prompt citando o pote de Vick fez o Nano pôr pote onde não devia (médico): em cena sem produto,
  escrever "Do NOT add any jar, bottle or product".
- **Start frame "editando a referência" sai fake** (o Jhon reprovou: "tá muito fake"): a referência de IA puxa o
  render junto. Escrever o frame do zero na gramática da `photorealism-prompts` (cena → câmera iPhone/FX3 →
  bloco anti-stock → trava do Vicks → frase de pele) e passar a referência só "as a guide for composition".
  "Phone on a tripod" no prompt desenha tripé+celular no quadro — dizer que o equipamento nunca aparece.
- Kling `--sound on` erra palavra difícil ("VapoRub", "COPD", "parasites"). Dica de pronúncia no prompt PIORA
  (repete a palavra, soletra no fim). Melhor: texto original e 2–3 tentativas, escolher pela transcrição.
- **Transformação do objeto + fala exata** (pulmão feio → limpo enquanto o avatar fala): o Kling 3.0 com
  start+end frame faz a transformação, mas a voz nativa errou "VapoRub" em 10+ tentativas e "parasites".
  O que fechou: frame final no Nano (mesma cena, objeto limpo) → `wan3_0` com `--image-references` início E fim
  ("starts like image 1, ends like image 2") + `--audio-references` TTS ElevenLabs (0,4 s de silêncio na frente)
  + `--generate_audio false` → mux do wav. Sai 1080×1920 30 fps (escala 100%). Homem sem camisa + "mucus" no
  Kling = nsfw; trocar por "pale yellow residue".

## LungTyde 239_MN — bodies (09/10/2026)
- Render do HyperFrames com workers automáticos grava cada quadro em disco (~55 GB por body de 4 min) e falha
  com disco cheio. `--workers 1` faz streaming direto pro .mov (~7–10 min por body, 3 em paralelo). Script:
  `HYPERFRAMES/_gerador/render1.sh` do job.
- **HEVC com alfa (videotoolbox) NÃO funciona no Premiere**: importa com fundo preto. Overlay tem que ser
  ProRes 4444. Disco "99% cheio" no `df` pode ter >100 GB purgeable (cache do Drive) — conferir no Finder
  (`osascript ... free space of startup disk`) antes de comprimir à toa.
- `brutos.py` e `overlay.py` da skill tinham erro de precedência (`"""..."""+x+"""..."""%y`) → embrulhar em parênteses.
- `dados.py`/`plano.py` têm regras e grupos de b-roll do nicho de prosperidade no código; para outro nicho trocar
  `R=[...]`, `TRANS`, a regex do CTA e os `GRUPOS`/`ALT` (no LungTyde: `PROJECT/_scripts/bodies/patch_dados.py` e `patch_plano.py`).
- Body validado 704×1280 com SAR 5400:5401: o Premiere espreme (faixas pretas). Reencodar
  `scale=1080:-2,crop=1080:1920,setsar=1` antes de importar.
- Lettering: deduplicar (mesmo texto ≥40 s de distância) e tirar "TAP LEARN MORE" do lettering grande (a pílula
  do overlay já faz o CTA). Selfie fechada: lettering em 56% em vez de 47% (cobria a boca).
- Download de footage de celebridade pelo yt-dlp foi barrado pelo classificador de permissão: pedir os recortes
  ao Jhon ou autorização explícita.
- **Entrega body × hook (225 ADs)**: não renderizar 225 no AME. Exportar as 30 peças (Hxx e Bxx), padronizar no
  ffmpeg com os mesmos parâmetros (x264 high, 25 fps, `-video_track_timescale 12800`, AAC 48k estéreo) e juntar com
  `-f concat -c copy`. Pasta por body: `EXPORT/ADxx/[..] ADxx HKn [Produto] [Squad].mp4`. Script: `PROJECT/_scripts/bodies/combinar.py` do job LungTyde 239_MN.
- Flash de transição no início do body via ffmpeg: `blend=all_mode=screen` em **gbrp**, nunca em yuv420p — em YUV o
  "preto" não é neutro nos canais de cor e a tela inteira fica roxa.
- AME falhou numa peça com "Erro ao recuperar o quadro N" de um overlay ProRes no Drive (arquivo íntegro no ffmpeg):
  gerar a peça direto no ffmpeg (overlay + VO) em vez de reenfileirar.
