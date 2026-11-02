---
name: specs-camera-photorealismo
description: Usuário considera as specs de câmera/lente/ISO essenciais ao realismo — não simplificar prompts da photorealism-prompts
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 49cf0b57-d35b-46d3-b8f4-72ff899a2b8d
  modified: 2026-07-26T01:29:25.102Z
---

Ao gerar prompts de imagem ultrarrealista, manter a gramática completa da skill `photorealism-prompts`: câmera, lente, abertura, ISO, shutter speed, color science. Não substituir por descrição de cena em linguagem natural, mesmo em modelos Gemini-based (Nano Banana Pro) ou GPT Image 2.

**Why:** em 25/07/2026 sugeri que essa pilha de specs pudesse remar contra modelos não-difusão e propus um teste A/B de gramática. O usuário reafirmou que "esses detalhes é importante para o realismo". É decisão dele e é defensável — as specs funcionam como âncora semântica de "isto é uma fotografia", não só como parâmetro técnico.

**How to apply:** usar a skill como escrita. A frase obrigatória de pele (`visible pores, micro-texture, natural skin imperfections, subtle peach fuzz, natural skin sheen, no airbushing, no smoothing filters`) segue intocável no fim de todo prompt com pessoas/pele visível. Se um resultado sair ruim, ajustar cena/luz/composição antes de mexer nas specs. Ver [[skills-criativas-instaladas]].
