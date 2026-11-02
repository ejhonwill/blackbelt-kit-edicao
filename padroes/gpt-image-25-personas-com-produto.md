---
name: gpt-image-25-personas-com-produto
description: "GPT Image 2.5 pelo CLI Higgsfield para persona segurando frasco — a trava de escala que funcionou, o que o modelo acerta de primeira, e a armadilha do glob com colchetes"
metadata:
  type: feedback
---

Validado em 17/09/2026 nas 7 personas de depoimento do MemoFlow Upsell #1 (pedido do Jhon: "use o chat gpt imagem 2.5").

**Modelo:** `higgsfield generate create gpt_image_2_5` — params `--aspect_ratio 1:1 --quality high --resolution 2k`
(3 créditos; `xhigh` = 5). Duas `--image-references` repetidas (frasco 2k achatado sobre branco + close do rótulo)
funcionam; `higgsfield upload create` devolve o id pra reaproveitar sem reenviar 7×. Sai 2048² rgb24.
`--json` no create devolve array de ids (ver [[higgsfield-cli-saida-json]]).

**O que o GPT Image 2.5 acerta de primeira** (diferente do nano_banana): rótulo com a grafia exata em 14/14,
rosto envelhecido crível com o bloco anti-stock, 5 dedos corretos em 14/14, fundo coerente com a história.
Não precisou de rodada por rótulo.

**O que falha de primeira: ESCALA.** Mesmo com "about 10 cm, shorter than the hand" no meio do bloco de produto,
o frasco de 30 mL saiu com o comprimento da mão inteira nas 7. A trava que resolveu na rodada 2 (7/7):
abrir o bloco de produto com *"SCALE IS CRITICAL: TINY 30 mL bottle, its full height including the dropper cap
is only the length of the index finger, about HALF the hand from wrist crease to fingertips, two finger-widths
wide, held delicately by the base with the fingertips — like holding an egg — so the whole front label stays
exposed; the hand is clearly BIGGER than the bottle"*. A pegada "como um ovo" é o que evita o punho fechado
cobrindo a marca.

**Texto de fundo:** calendário, lista de compras e hinário saem LEGÍVEIS se o cenário os cita. Uma frase
resolve: *"Any calendar, list, book, sign or packaging in the background is out of focus and unreadable"*.

**Ordem do prompt** que segue valendo: cena → specs de câmera → bloco anti-stock → trava de produto
("OVERRIDES EVERYTHING ABOVE", escala primeiro) → frase obrigatória de pele. Ver [[anti-cara-de-ia-em-imagem]].

**Identidade entre duas imagens:** passar o **job id** da primeira geração como `--image-references` (aceita id de
job, não só de upload) + "IDENTITY: the SAME man as in the first reference image… same photo session, next frame"
segurou rosto, barba, roupa, cenário e luz entre a base talking head e a variante com frasco. Serve pra expert.

**Parser do `generate get --json`:** a saída pode vir com linha extra depois do objeto e `json.loads` estoura com
"Extra data" — o job JÁ foi criado e cobrado. Usar `json.JSONDecoder().raw_decode(raw[raw.find('{'):])[0]` e
nunca reenviar; poll pelo mesmo id.

**Armadilha de código:** `glob.glob()` num caminho com `[160926][OT]` trata os colchetes como classe de
caracteres e devolve vazio sem erro. Nas pastas de demanda da H&W, usar `os.listdir` + filtro, nunca glob.

Entrega: `…/[160926][OT] Upsell #1 [MemoFlow] [Squad]/MEMOFLOW_PERSONAS_APROVACAO/` (01_REFERENCIA_PRODUTO,
02_PERSONAS_GERADAS r1+r2, 03_SELECIONADAS, 04_REJEITADAS, 05_PROMPTS com bíblia visual, tabela de personas e QC).
Ver [[memoflow-produto-mockups]], [[specs-camera-photorealismo]].

**Avatar que vem no briefing: travar no rosto dele (10/10/2026, Divine Prayer).** Eu descrevi o rosto no prompt (rosto redondo, óculos sem aro…) e mandei a referência "só como guia". O GPT 2.5 inventou pessoas novas, e o Jhon reprovou: "mudou a pessoa". O que funcionou de primeira: tirar do prompt toda descrição de rosto e passar a imagem do briefing como **primeira** `--image-references`, com o bloco *"IDENTITY LOCK: EXACTLY the same … as in the FIRST reference image — keep each face exactly: same face shape, nose, eyes, eyebrows, ears, hairline, age … Do NOT redesign, beautify; only re-photograph them for real"*. O fotorrealismo (specs + anti-stock) continua valendo. Quando o briefing traz avatar, "mais realista" quer dizer **a mesma pessoa, com cara de foto**, e nunca uma pessoa nova.
