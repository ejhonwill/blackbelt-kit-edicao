---
name: kling-lipsync-nativo
description: "Lipsync 'no Kling' pelo Higgsfield = kling3_0 com --sound on e a fala no prompt; nenhum Kling do catálogo aceita áudio externo. E o 403 que é moderação, não conta"
metadata:
  type: reference
---

Em 25/09/2026 (job `[210926][WL] Folha japonesa que trava cortisol HK1 [teste1]`) o Jhon pediu
"gere o lipsync usando o kling, mantenha o ambiente".

- No catálogo do Higgsfield **nenhum Kling recebe áudio** (`kling3_0`, `kling3_0_turbo`, `kling2_6`,
  `kling_video_edit`). O caminho é `kling3_0 --mode pro --sound on --start-image <âncora>` com a fala
  entre aspas no prompt + "American English accent": o Kling gera voz e boca juntos. A voz não é
  controlável — se precisar de voz exata (TTS/clone), usar wan3_0 ([[wan3-lipsync-avatar]]).
- **Manter o ambiente** = uma âncora só (nano_banana_pro 2k 9:16) reutilizada como start frame de todo take.
- **403 Forbidden no `generate create`** com créditos sobrando (10k) foi **moderação**: "softly overweight…
  soft belly" no prompt da persona. Tirar descrição de corpo e reenviar resolveu. Não é auth nem saldo
  (`higgsfield account status` confirma).
- Script reaproveitável: `MEDIA/IA/gerar_avatar_lipsync.py` do job.

Ver [[broll-usar-kling]], [[higgsfield-cli-wait-timeout]].

**04/10/2026 (SynapseDeck VID-04, personagem Pixar falando espanhol AR):** a voz do Kling **muda entre clipes** (F0 193/198/246 Hz) e ele **erra/inventa palavra** ("me explina", "CabainasDeck," antes da fala). Receita que fechou:
1. Gerar a cena com a tela/objeto JÁ na imagem (nano_banana_pro com o print real como 2ª referência) ANTES do Kling.
2. Checar cada clipe com whisper medium/large-v3; palavra difícil → trocar por sinônimo no roteiro ("me muestra"); palavra inventada no início → aparar.
3. **Unificar a voz com ElevenLabs speech-to-speech** para a voz oficial (Melanie `bN1bDXgDIGX5lw0rtY2B`): mantém a duração (boca segue sincronizada) e a F0 bate. Com a chave restrita só funciona com `model_id` + `voice_settings` + `audio` (campos extras = 403). Script: `.../ar-vid-04-sofia-pixar/gen/sts.py`.
4. CLI do Higgsfield **não apaga** geração (só create/list/get) — apagar é pela web.
