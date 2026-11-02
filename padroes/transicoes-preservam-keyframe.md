---
name: transicoes-preservam-keyframe
description: "pr-transicoes e pr-zoom gravam no MESMO Transformar — por que a transição agora é relativa à base e a remoção usa registro em disco"
metadata:
  node_type: memory
  type: project
---

Medido ao vivo em 16/09/2026, Premiere 26.5, sequência TX_LAB do
LAB-TOOLSPRO.prproj (dois clipes, corte em 3,000s, 30 fps).

## O defeito que existia (dois, na verdade)

`pr-transicoes` e `pr-zoom` usam **o mesmo componente** `AE.ADBE Geometry`
("Transformar") **no mesmo clipe**, e nas mesmas propriedades.

1. **Pulo na imagem.** O motor escrevia valor ABSOLUTO assumindo que todo
   clipe parte de 100/0,5/0. Com um zoom do usuário de 100→130, aplicar um
   Whip produzia `2.800=130 , 2.833=100 , 3.000=160` — a imagem caía de 130
   para 100 em um quadro, três quadros antes do corte.
2. **Perda total.** `txLimparGeo` apagava TODOS os keyframes das
   propriedades que toca e removia o Transformar inteiro. O zoom do usuário
   ia junto e a função respondia `"animacoes":2`, ou seja, sucesso.

## O conserto

- **Relativo à base.** Toda propriedade é lida com `getValueAtTime(t)` em
  cada keyframe e a transição é somada/multiplicada por cima. Contrato dos
  misturadores: `misturar(base, 0) === base`, então não existe salto possível.
  Escala é FATOR (130 × 1,6 = 208), posição/rotação são SOMA.
- **Registro em disco** em `~/Library/Application Support/Editor Black Belt/
  tx-registro.json`. Anota os tempos exatos de keyframe escritos e se foi a
  ferramenta quem criou o componente. Remover apaga só isso.
- **Sem registro não se chuta.** Animação não reconhecida é preservada e
  contada em `preservadas` — o painel avisa em vez de destruir calado.
- Chave do registro identifica o CONTEÚDO (projeto|seqID|trilha|lado|nome|
  in|out|startTicks): mover o clipe na timeline não perde o registro; aparar
  perde — e aí os keyframes de borda já não valem mesmo.

## Amostrar só quando precisa
2 keyframes + Bezier no caso comum (saída limpa no Controle de Efeitos).
Amostra por quadro (teto 12) quando a curva não é expressável em Bezier
(`expo`, `volta`, `linear`) ou quando a animação do usuário passa por dentro
da janela. `txVariaNaJanela` decide.

## Duas medições que mudam desenho
- `qeSeq.exportFramePNG` custa **~4,9s para dois quadros** — renderiza. Por
  isso a prévia com o material do editor é sob demanda e cacheada por corte,
  nunca a cada troca de preset (é a mesma thread que pendura o Premiere).
- **CEP não tem alvo de drop dentro da timeline do Premiere.** Não há API,
  em nenhuma versão. Por isso o arraste estilo Animation Composer foi feito
  trazendo a timeline para dentro do painel (a "fita": clipe · emenda ·
  clipe), e a emenda é o alvo.

## Estado da instalação em 16/09/2026
A pasta `tools/pr-transicoes` da extensão INSTALADA
(`~/Library/Application Support/Adobe/CEP/extensions/com.editorblackbelt.toolspro`)
foi sincronizada com o FONTE legível — o resto da extensão continua sendo a
build ofuscada 1.7.0. Ou seja: esta ferramenta está fora do ciclo de build até
alguém rodar o `obfuscate-tree.js` de novo. A build ofuscada anterior está em
`Editor Black Belt/backups/pr-transicoes-instalado-antes-da-sync-*` com um
`RESTAURAR-pr-transicoes-*.command` ao lado.

Banca: `dist-toolspro/testes/sim_transicoes_composer.js` (32 casos: fita,
arraste, direção, curva, preset, bordas, preservação, rótulo honesto) roda ao
lado do `sim_transicoes_rapido.js` (22). Os dois precisam passar.

Ver [[premiere-qe-transicoes-efeitos]], [[premiere-movimento-depois-do-efeito]],
[[toolspro-ofuscacao-quebra-jsx]], [[banca-jsdom-painel-toolspro]].
