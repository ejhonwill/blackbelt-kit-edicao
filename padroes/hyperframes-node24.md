---
name: hyperframes-node24
description: "HyperFrames CLI exige Node ≥22; o node padrão do Mac é 20 — prefixar PATH com node@24 do Homebrew"
metadata:
  type: reference
---

`npx hyperframes ...` aborta com "HyperFrames requires Node.js >= 22 (current: 20.18.0)".
Usar `export PATH=/opt/homebrew/opt/node@24/bin:$PATH` antes de qualquer comando (node@24 é keg-only,
mesma armadilha de [[omniroute-precisa-node24]] e [[chatbotx-local-mac]]).

Projeto do AD 206_CP (07/10/2026): `…/[061026][OT] 206_CP [CardioShield] [Squad]/hyperframes/ad01-hook1-body1`,
gerado por `scripts/build.py` a partir de `assets/data` (palavras + plano de b-roll) — editar o gerador e
rodar de novo, não o HTML. Caminho com colchetes e espaços funcionou no init/check/preview.
SFX do `media-use resolve --type sfx`: o bundled `sfx_002` (impacto) é quase todo a -2 dB — usar com volume ≤0,15.

**13/10/2026 — node@24 parou de abrir** (`dyld: Library not loaded … libsimdjson.33.dylib`): o `brew upgrade` levou o simdjson para 5.x (lib .34) e o node ficou ligado à antiga. Conserto: `brew reinstall node@24` (saiu v24.21.0, HyperFrames 0.8.154 ok). Mesmo sintoma derruba [[omniroute-precisa-node24]] e [[chatbotx-local-mac]].
