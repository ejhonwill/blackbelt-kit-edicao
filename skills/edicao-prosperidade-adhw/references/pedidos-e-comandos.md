AULA 27 · DO DOC DE COPY AOS ADS PRONTOS: O FLUXO PREMIUM DR
Editor Black Belt · Módulo 5 · Na prática
=====================================================================

Como usar este arquivo
- Parte A: os pedidos para colar no Claude do VS Code, na ordem do job.
  Troque o que está entre [colchetes].
- Parte B: os comandos que o Claude rodou em cada passo, para você entender
  (e repetir à mão, se quiser). Chaves de API NUNCA vão no comando: ficam num
  arquivo .env e são lidas de lá.
- Sempre peça a estimativa de crédito antes de gerar imagem, vídeo ou avatar.


=====================================================================
PARTE A · OS 9 PEDIDOS
=====================================================================

PEDIDO 1 · ENTENDER O TRABALHO
Leia o documento de copy [link do Google Doc], com os comentários, e baixe os
vídeos de referência que estão nele. Assista as referências e me diga o padrão
de edição: cortes por minuto, tempo do avatar na tela, legenda, lettering,
trilha e SFX.

PEDIDO 2 · AVATARES
Crie o avatar de cada body. Aprimore as imagens de referência no GPT Image 2.5
pelo Higgsfield sem mudar a identidade, em 9:16. Se a referência for uma pessoa
real ou famosa, crie uma persona fictícia com a mesma cena e a mesma vibe.

PEDIDO 3 · VOZ E DECUPAGEM
Gere a voz de cada body no ElevenLabs, modelo v4, uma voz americana diferente
por persona. Decupe pelo silêncio real, sem cortar palavra, e confira com o
Whisper contra a copy antes de seguir.

PEDIDO 4 · AVATAR FALANDO
Gere o avatar falante de cada body no HeyGen Avatar IV com o áudio decupado.
Escreva o motion prompt com o arco da copy e meça a sincronia antes de entregar.

PEDIDO 5 · B-ROLL
Monte um pacote único de b-roll ligado às palavras-chave da copy: imagem no
GPT Image 2.5 e animação no Kling Turbo, 5 s, 9:16. Use o acervo [pasta de
assets] e nunca repita footage na mesma timeline.

PEDIDO 6 · PREMIERE
Crie o projeto a partir do [modelo da casa], uma sequência por body em 25 fps.
Coloque o bruto e o áudio decupado, gere a legenda e marque BROLL, LETTERING,
KEYWORD e CORTE_RITMO com o conteúdo no comentário.

PEDIDO 7 · MONTAGEM
Monte pelos marcadores: b-roll com zoom lento, punch-in sincronizado, zoom in e
zoom out no avatar, trilha e whoosh. No fim, leia a V2 de volta e feche
qualquer buraco.

PEDIDO 8 · ACABAMENTO
Faça no HyperFrames a camada transparente: legenda com a palavra ativa em caixa
roxa, lettering com a palavra-chave em amarelo e deep glow, flash e luz nas
viradas e o botão de CTA. Coloque na V3.

PEDIDO 9 · RENDER
Renderize as sequências no Media Encoder com o nome [padrão de entrega] e
confira cada arquivo: specs, LUFS, quadro preto ou congelado e legenda
duplicada.

Pedidos de ajuste que usamos no meio do caminho:
- "Não quero ver footage repetido na mesma timeline."
- "Deixe o lettering mais premium: palavra-chave em amarelo com deep glow."
- "Trabalhe zoom in e zoom out no avatar falando e verifique os espaços de
   cada cena."
- "Onde falar de uma figura pública, use footage real para dar credibilidade."
  (atenção: direito de imagem e política da Meta — decisão do dono da conta)


=====================================================================
PARTE B · OS COMANDOS DE CADA PASSO
=====================================================================

--- PASSO 1 · Referências e padrão -------------------------------------

# baixar um vídeo de referência (YouTube/Drive público)
yt-dlp -f "bv*[height<=1080]+ba/b" -o "ref1.%(ext)s" "[link]"

# cortes: detecção de troca de cena
ffmpeg -i ref1.mp4 -vf "select='gt(scene,0.25)',showinfo" -an -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*'

# mosaico 1 quadro a cada 2 s, para "assistir" a edição
ffmpeg -i ref1.mp4 -vf "fps=1/2,scale=240:-2,tile=8x4" ref1_mosaico_%d.jpg

# transcrição palavra por palavra (Mac com Apple Silicon)
mlx_whisper ref1.wav --model mlx-community/whisper-large-v3-turbo \
  --language en --word-timestamps True --output-format json

# volume da trilha nas pausas da fala (mede se tem música por baixo)
ffmpeg -ss [pausa_ini] -to [pausa_fim] -i ref1.wav -af volumedetect -f null -


--- PASSO 2 · Avatares (Higgsfield CLI) ---------------------------------

higgsfield upload create referencia_B01.jpg --json        # devolve o id
higgsfield generate cost gpt_image_2_5 --prompt "x" --aspect_ratio 9:16 \
  --quality high --resolution 2k                          # 2,75 créditos
higgsfield generate create gpt_image_2_5 --prompt "[prompt]" \
  --aspect_ratio 9:16 --quality high --resolution 2k \
  --image-references [id_da_referencia] --json             # devolve [id_do_job]
higgsfield generate get [id_do_job] --json                 # baixar o result_url

Estrutura do prompt (skill photorealism-prompts):
  cena  →  specs de câmera (iPhone 16 Pro, 23 mm, f/1.9, ISO 320)
        →  bloco anti-stock (luz imperfeita, rosto assimétrico, grão 35 mm)
        →  frase final obrigatória de pele
Com referência: "IDENTITY: the SAME woman as in the reference image — same face,
same age, same hair, same clothes."
Pessoa real ou famosa na referência: NÃO usar como referência. Descrever uma
persona fictícia com a mesma cena e um rosto diferente.


--- PASSO 3 · Voz (ElevenLabs) e decupagem ------------------------------

# TTS com tempo por caractere (a chave vem do .env)
curl -s "https://api.elevenlabs.io/v1/text-to-speech/[voice_id]/with-timestamps" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"text":"[texto do body]","model_id":"eleven_v4","output_format":"mp3_44100_192"}'
# a resposta traz audio_base64 + alignment → salvar o mp3 decodificado

# listar vozes americanas
curl -s "https://api.elevenlabs.io/v2/voices?page_size=100" -H "xi-api-key: $ELEVENLABS_API_KEY"

# decupagem pelo SILÊNCIO REAL (não pelo alinhamento de texto)
ffmpeg -i B01_VOZ_bruta.mp3 -af silencedetect=n=-42dB:d=0.3 -f null -
#   pausa maior que 0,42 s → vira 0,32 s, com 0,15 s de borda de cada lado
ffmpeg -i B01_VOZ_bruta.mp3 \
  -af "aselect='between(t,0.00,4.31)+between(t,4.62,9.80)+…',asetpts=N/SR/TB,loudnorm=I=-16:TP=-1.5:LRA=7" \
  -ar 48000 -ac 1 B01_VOZ_decupada.wav

# conferir contra a copy
mlx_whisper B01_VOZ_decupada.wav --model mlx-community/whisper-large-v3-turbo \
  --language en --word-timestamps True --output-format json
# atenção: o Whisper inventa repetição DEPOIS do fim do áudio — confirme o final
#          transcrevendo só os últimos 12 s


--- PASSO 4 · Avatar falando (HeyGen CLI, Avatar IV) --------------------

heygen auth status                                     # créditos do plano
heygen asset create --file B01_avatar.jpg              # imagem → "id"
heygen asset create --file B01_VOZ_decupada.wav        # áudio  → "asset_id"
heygen video create -d '{"type":"image",
  "image":{"type":"asset_id","asset_id":"[id_imagem]"},
  "audio_asset_id":"[id_audio]","aspect_ratio":"9:16","resolution":"1080p",
  "fit":"cover","expressiveness":"medium",
  "motion_prompt":"[arco da copy: como abre, cada virada, como fecha]",
  "output_format":"mp4"}'
heygen video get [video_id]                            # status + video_url

# medir sincronia: início das pausas do vídeo × do áudio (deu 15–20 ms)
ffmpeg -i B01_AVATAR.mp4 -vn -af silencedetect=n=-40dB:d=0.2 -f null -
ffmpeg -i B01_VOZ_decupada.wav -af silencedetect=n=-40dB:d=0.2 -f null -


--- PASSO 5 · B-roll (GPT Image → Kling Turbo) --------------------------

higgsfield generate create gpt_image_2_5 --prompt "[cena]. [estilo]" \
  --aspect_ratio 9:16 --quality high --resolution 2k --json
higgsfield generate cost kling3_0_turbo --prompt x --aspect_ratio 9:16 \
  --resolution 1080p --duration 5                       # 10 créditos
higgsfield generate create kling3_0_turbo --prompt "[movimento]" \
  --start-image BR01.jpg --aspect_ratio 9:16 --resolution 1080p --duration 5 --json
# "no response received" = job NÃO criado → conferir na lista e reenviar
# PNG grande falha no envio → converter para JPG antes

# o Kling devolve vídeo COM áudio → cópia só com vídeo (sem perda)
ffmpeg -i BR01.mp4 -map 0:v -c copy BR01_mute.mp4

# recortar footage horizontal para 9:16
ffmpeg -ss [ini] -t 5 -i fonte.mp4 \
  -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,fps=25" -an saida.mp4


--- PASSO 6 · Premiere (Tools PRO · pr_extendscript) -------------------

Projeto: copiar o modelo da casa para PROJECT/ e abrir:
  cp "Projeto Padrão.prproj" "PROJECT/[nome do job].prproj"
  open -a "Adobe Premiere Pro 2026" "PROJECT/[nome do job].prproj"
Ligar no painel: Tools PRO › Conectar IA › Modo avançado (ExtendScript).

// importar (um arquivo por chamada, até 6 por execução — evita travar)
app.project.importFiles([caminho], true, bin, false);

// sequência SEM diálogo: clonar a 9x16 do modelo e acertar 25 fps
src.clone();                          // achar o clone pelo sequenceID novo
var st = nova.getSettings(); var t = new Time(); t.ticks = "10160640000";
st.videoFrameRate = t; nova.setSettings(st);

// colocar no tempo certo (SEMPRE objeto Time, nunca string)
var t0 = new Time(); t0.seconds = 0; seq.videoTracks[0].overwriteClip(item, t0);
seq.audioTracks[0].setMute(1);        // áudio embutido da HeyGen mudo

// renomear trilha (só pela QE)
qe.project.getActiveSequence().getVideoTrackAt(1).setName("V2 BROLL");

Ferramentas do catálogo Tools PRO usadas:
  pr_legenda_nativa_criar   { srt, sequencia }       (projeto precisa estar salvo)
  pr_marcadores_criar       { sequencia, marcadores:[{tempo,nome,comentario,cor,duracao}] }
                            cor: 0 verde 1 vermelho 2 roxo 3 laranja 4 amarelo 6 azul 7 ciano
  pr_sequencia_ativar · pr_timeline_listar · pr_projeto_salvar


--- PASSO 7 · Montagem --------------------------------------------------

// trecho exato de um item: in/out no projectItem, coloca, limpa
item.setInPoint(0.2, 4); item.setOutPoint(0.2 + dur, 4);
track.overwriteClip(item, t); item.clearInPoint(4); item.clearOutPoint(4);

// punch-in sincronizado: entrada do avatar = início na timeline, em TICKS
var q = new Time(); q.ticks = String(quadro * 10160640000); clip.inPoint = q;

// zoom (Ken Burns / zoom in-out) por keyframe de escala do Movimento
var sc = comp(clip,"AE.ADBE Motion").properties[1];
sc.setTimeVarying(true); sc.addKey(k0); sc.setValueAtKey(k0, 101, true);
sc.addKey(k1); sc.setValueAtKey(k1, 108, true);

// fechar buraco < 0,6 s na V2 (o avatar "pisca")
if (gap > 0.001 && gap < 0.6) { var e = new Time(); e.ticks = String(prox.start.ticks); ant.end = e; }

# trilha pré-mixada por body (bem abaixo da voz) e SFX normalizados
ffmpeg -i trilha.mp3 -t [duração] \
  -af "loudnorm=I=-34:TP=-9,afade=t=in:d=1,afade=t=out:st=[dur-2.5]:d=2.5" B01_TRILHA.wav
ffmpeg -i whoosh.mp3 -af loudnorm=I=-22:TP=-3 -ar 48000 SFX_Whoosh.wav


--- PASSO 8 · HyperFrames ----------------------------------------------

export PATH=/opt/homebrew/opt/node@24/bin:$PATH        # exige Node 22+
python3 build.py B01                                   # gera B01/index.html dos JSONs
cd B01 && npx hyperframes check                        # 0 erros antes de renderizar
npx hyperframes snapshot --at 43.4,57.9,95.5           # conferir quadros
npx hyperframes render --format mov --fps 25 --output B01_OVERLAY.mov
#   MOV = ProRes 4444 com transparência → vai na V3 do Premiere

Regras que evitam defeito:
- não animar letterSpacing (o texto treme no render) → só escala/opacidade/desfoque
- camada de brilho atrás da palavra: data-layout-allow-overlap em cada span
- lettering na altura do peito (≈50% da tela), legenda em ≈71%


--- PASSO 9 · Render e conferência -------------------------------------

// fila do Media Encoder (não trava o Premiere)
app.encoder.launchEncoder();
app.encoder.encodeSequence(seq, "[EXPORT]/[nome].mp4",
  "[AME]/systempresets/4E49434B_48323634/00 - Match Source - High bitrate.epr", 0, 1);
app.encoder.startBatch();

# conferir cada arquivo
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate \
  -show_entries format=duration -of csv=p=0 AD01.mp4
ffmpeg -i AD01.mp4 -af ebur128 -f null - 2>&1 | grep "I:"          # LUFS
ffmpeg -i AD01.mp4 -vf "blackdetect=d=0.2:pix_th=0.08,freezedetect=n=0.003:d=1.5" \
  -an -f null -                                                     # preto/congelado
# legenda nativa queimada por baixo? desligue o olho da faixa de Legendas e
# renderize de novo — o arquivo antigo vai para _DESCARTADOS, nunca sobrescreva.
