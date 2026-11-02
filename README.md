# Kit de Edição Black Belt — H&W

Skills, agentes e padrões que a edição da H&W usa no Claude Code: upsell, VSL, AD, microlead, b-roll, conferência e a Agência Samurai.
Tudo aqui foi aprovado em demanda real. Os padrões são as regras do Jhon e as armadilhas que já custaram horas ou crédito.

**Repositório interno. Não compartilhar fora do time:** tem produtos, IDs do Drive e caminhos da operação.

## Instalar

```bash
git clone https://github.com/ejhonwill/blackbelt-kit-edicao.git
cd blackbelt-kit-edicao
./install.sh                 # não mexe no que você já tem
./install.sh --sobrescrever  # atualiza o que já existe
```

Depois, reinicie o Claude Code.

O instalador copia para `~/.claude/skills`, `~/.claude/agents` e `~/.claude/padroes-blackbelt`. Ele também troca o caminho da máquina do Jhon (`/Users/jhonwill`) pelo seu.

Para atualizar: `git pull` e `./install.sh --sobrescrever`.

## O que você precisa ter

- **Claude Code** (VS Code ou terminal).
- **ffmpeg** e **python3**: `brew install ffmpeg python`.
- **Node 24** para o HyperFrames: `brew install node@24`. Use `export PATH="/opt/homebrew/opt/node@24/bin:$PATH"` antes de `npx hyperframes`.
- **Skills do HyperFrames** (são da HeyGen, não vêm aqui). Instale pelo repositório oficial delas: `hyperframes`, `hyperframes-core`, `hyperframes-cli`, `hyperframes-animation`, `hyperframes-creative` e `media-use`.
- **HWStudio da empresa** (MCP `hwstudio-empresa`). É por ele que se gera imagem, vídeo e voz da empresa. Peça o token ao Jhon e nunca o grave em arquivo do repositório.
- **Google Drive for Desktop** com o drive compartilhado da H&W. Os caminhos têm o e-mail do Jhon (`GoogleDrive-jhonatan.araujo@...`); se o seu for outro, ajuste o caminho na hora de usar.

## Agentes (`agents/`)

| Agente | Para quê |
|---|---|
| `samurai-upsell` | Editor sênior de UPSELL: leva da copy ao vídeo renderizado. |
| `supervisor-upsell` | Fiscal das regras. Corrige o que não custa e devolve o que é pago ou decisão. Roda antes da prévia, antes do render e nos mp4. |
| `caca-erro-quadro-upsell` | Olho quadro a quadro: transições, frasco, rótulo, texto, rostos. Só aponta, com prova. |
| `samurai-vsl` / `samurai-ad` / `samurai-ml` | Editores sêniores de VSL, AD (body + hooks) e Microlead/Lead. |
| `auditor-de-entrega` | Confere o job terminado contra o briefing. |
| `decupador` | Plano de corte de silêncio ancorado nas palavras. |
| `gerador-de-planos` | Gera os planos (imagem + animação) de um AD. |
| `premiere-executor` | Toda escrita no Premiere com segurança. |
| `qc-visual` | Confere lote de IA e devolve só os reprovados. |

**Fluxo do upsell:**
1. Editor (samurai-upsell).
2. Supervisor + caça-erro, em sequência e com o editor parado.
3. Prévia na timeline para o Jhon aprovar.
4. Render.
5. Supervisor + caça-erro de novo, agora nos mp4.
6. Entrega.

## Skills (`skills/`)

- **Upsell:** `upsell-premium-916` (padrão 9:16 aprovado), `upsell-agente`, `padrao-visual-memoflow`.
- **Agência Samurai DR:** `samurai`.
- **Direção e edição DR:** `editor-senior-dr`, `editor-automatico-de-broll`, `boas-praticas-black-belt`, `edicao-prosperidade-adhw`, `vsl-motion-ae`, `motion-omni-vsl`, `cortar-aula`.
- **AD e clone de AD:** `clone-ad-validado`, `advalidado-weightloss`, `hooks-meat-hook`, `skill-black-belt`.
- **Conferência e análise:** `conferir-ads-por-frame`, `analise-criativos-ponte`, `analise-criativo-ficha`, `decupar-vsl-por-frame`, `dissecador-de-ads-atlas`, `dissecador-de-vsl-atlas`, `formatador-atlas`.
- **Prompts de geração:** `photorealism-prompts`, `nano-banana-pro-prompts-recommend-skill`, `video-prompt-builder`, `avatar-vsl-video-prompts`, `storyboard-viral-3d`, `pixar3d`, `blackbelt-omni`, `omni-flash-reverse`, `vibe-motion`, `video-to-flow`, `video-workflow`, `general-video`.
- **Operação:** `replicador-hw`.

## Padrões aprendidos (`padroes/`)

Uma regra ou armadilha por arquivo, cada uma com **por quê** e **como aplicar**. Comece por estes:
- `regras-gerais-upsell.md`: as regras do Jhon para todo upsell (frasco, b-roll, cards, legenda, preço, entrega UPS, timeline antes do render).
- `upsell-premium-916-padrao.md`, `nomenclatura-entregaveis-hw.md`, `formatos-de-trabalho-hw.md`, `convencoes-producao-criativo.md`.
- Armadilhas técnicas: `premiere-*`, `ae-*`, `hyperframes-*`, `drive-*`, `nano-banana-*`, `kling-*`, `whisper-*`.

As regras mais novas do upsell ficam no fim de `skills/upsell-premium-916/references/REGRAS_JHON_3010.md`.

## Regras da casa

- Voz sempre em inglês americano. A conversa com o Claude é em português.
- Render pesado com a vez do Controle: no máximo 2 renders ao mesmo tempo na máquina.
- Trabalho da empresa é gerado no HWStudio da empresa.
- Nunca renomear nem mover em massa no Drive, porque as pastas vão para a lixeira.
- Gasto pago só com o OK de quem pediu a demanda.

A fonte é a máquina do Jhon. Este repositório é uma cópia atualizada quando ele pede.
