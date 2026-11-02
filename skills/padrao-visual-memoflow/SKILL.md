---
name: padrao-visual-memoflow
description: Padrão visual validado dos criativos DR 1:1 da MemoFlow (Upsell #1, 09/2026) — lettering, legenda, B-roll, take de produto, CTA e as regras de sincronia com a fala, com os scripts que o reproduzem no After Effects. Use quando for montar ou revisar um Upsell/VSL/AD 1:1 no After no mesmo padrão, "aplicar o padrão MemoFlow", "mesmo estilo do Upsell", refazer lettering/legenda sincronizada, ou quando o Jhon pedir o "padrão treinado".
---

# Padrão visual MemoFlow (DR 1:1)

A especificação completa, com todos os valores medidos e aprovados, está em
`PADRAO_VISUAL_MEMOFLOW.md` — ler antes de tocar em qualquer comp.

Os scripts em `scripts/` foram recuperados do transcript da sessão que criou o padrão
(17–18/09/2026). Eles rodam contra um `.aep` já aberto, por `osascript … DoScriptFile`, e devolvem
o resultado em `/tmp/ae_*.txt`. Os `.py` geram os `.jsx` a partir de JSON (alinhamento, plano de
cobertura, cartelas, legendas); os placeholders `__DADOS__`, `__SECAO__`, `__PREFIXO__`, `__DIR__`
são preenchidos pelo gerador.

Ordem de uso numa demanda nova:
1. `medir_fala.py` + `corrigir_cabeca.py` — alinhamento com a 1ª palavra corrigida pelo áudio.
2. `letterings_novos.py` → `ancorar_certo.py` — cartelas ancoradas no texto inteiro.
3. `agendar_secao.py` → `emendar.py` — cronograma e corrente de cobertura sem buraco.
4. `planos_broll_novos.py` → `gerar_novos.py` (Higgsfield) — imagem, depois vídeo.
5. `ae_master_tmpl.jsx` (cartelas da abertura, sincroniza o fundo pelo início de cada card) ou `ae_sec_tmpl.jsx`
   (cartelas de qualquer seção) → `ae_montar_tmpl.jsx` (B-roll + legenda) → `ae_ordem_fix.jsx`.
6. `ae_take.jsx` (produto na menção), `ae_cta.jsx` (fecho), `ae_master_timeline.jsx`.
7. Auditar com `ae_cob.jsx` / `ae_cob_sec.jsx`; provar transcrevendo o render.

Alguns templates estão na versão original do heredoc e receberam patches depois (documentados
na spec): azul da marca no lugar do laranja, ESCURECER 78/68, halo 395×268, ZI/ZF 80/−210,
janela de ancoragem +6 e ±5 s, remoção dos laços de reordenação em lote das legendas. Conferir
esses pontos antes de rodar.
