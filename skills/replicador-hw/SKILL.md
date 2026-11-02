---
name: replicador-hw
description: Automatiza o processamento de demandas de edição de vídeo da HW Publishing — replica mensagens do canal #demandas-edição para os canais corretos (#edição-otimização, #edição-criação ou #edição-dtc) e cria a pasta correspondente no Google Drive. Use esta skill SEMPRE que o usuário mencionar: "retifica", "replica", "processa", "cria a task de", "joga em otimização", "manda pro DTC", ou qualquer pedido envolvendo demandas com prefixos [OT], [OF] ou [DTC] da HW Publishing. Acione também quando o usuário colar uma nomenclatura de demanda (ex: "ML/09_PG (NT) - Externo" ou o formato curto "02_PG (CoreStrength)") mesmo sem usar essas palavras-chave. MCPs necessários: Slack e Google Drive.
---

# Replicador de Demandas — HW Publishing

Skill que processa demandas de edição de vídeo da HW Publishing. Detecta o tipo ([OT], [OF] ou [DTC]), cria a pasta no Google Drive com a nomenclatura padronizada e replica para o canal Slack correto.

> ⚠️ **O monday saiu do fluxo em 14/09/2026.** O time não usa mais o monday.com.
> Não crie task, não procure `item_url` e não inclua a linha "ID da Demanda" na
> thread. O controle vive no Drive + Slack.

## Fluxos disponíveis

| Prefixo | Canal destino | Subpasta no Drive | Squad |
|---|---|---|---|
| `[OT]` | #edição-otimização (`C098NHQ5SRH`) | `OT` | Perguntar sempre |
| `[OF]` | **#edição-criação (`C0997N6EWKT`)** | **`Offer`** | Perguntar sempre |
| `[DTC]` | #edição-dtc (`C098RUCHFKL`) | `DTC` | Fixo: Squad DTC |

## Regras gerais (nunca violar)

- **Squad obrigatório para [OT] e [OF]** — nunca chutar; se não informado, perguntar. Opções: Squad A / Squad B / Squad Offer / "Ainda vou designar" (deixa `[Squad]` no nome). ⚠️ Squad C não existe mais desde 30/08/2026
- **[DTC] nunca pergunta Squad** — sempre Squad DTC (Amanda Andrade, Analu Melo, Giovanna Martinelli); a Amanda é quem despacha pro editor
- **Ordem obrigatória: Drive → Slack** — criar a pasta primeiro (para ter o link), depois postar no Slack com tudo preenchido
- **Nada de monday** — sem task, sem status "Parado", sem grupo, sem linha "ID da Demanda"
- **Nome da pasta no Drive**: barras `/` viram underline `_` (ex: `ML/10_BM` → `ML_10_BM`)

## Passo a passo de execução

### Passo 1 — Identificar a demanda

O usuário pode informar de várias formas:

**Forma A — título completo:**
> "Retifica [OT] ML/09_PG (NT) - Gustavo, Squad B"

**Forma B — só nomenclatura (sem [OT]/[OF]):**
> "Retifica AD/35_PG (MP)"
→ Renomear para `[OT] AD/35_PG (MP)` e avisar o usuário

**Forma C — pede para processar a última:**
> "Processa a última demanda OT"
→ Buscar as 3-5 mais recentes em #demandas-edição e pedir confirmação

**Forma D — formato curto (produto entre parênteses, SEM prefixo de tipo):**
> "Retifica [OT] 05_JV (Vigorox)"
→ Estrutura: `[OT] {VARIACAO}_{INICIAIS-DO-SOLICITANTE} ({Produto})`. É o padrão mais comum hoje (Pedro Gomes = PG, João Vitor = JV, Edson Franzosi = EF, Breno Machado = BM…). Não traz prefixo de tipo (AD/ML/L) e quase sempre é uma **demanda mista** (5 Body's com 3 Hooks cada + 1 Micro-Lead). Regras deste formato:
> - **Cliente = o Produto entre parênteses** (ex: CoreStrength, MemoPryl, Vigorox, GlucoZen).
> - **`_XX` = iniciais do solicitante**, não um código de tipo. Preservar como veio.

### Passo 2 — Buscar thread no Slack

Use `slack_search_public_and_private` com query:
```
in:#demandas-edição {parte-da-nomenclatura}
```

Extrair da thread:
- **Permalink** da mensagem-pai → vai pro "Tópico do copy"
- **Link da Copy** (Google Docs) → campo "Copy" (para [OT]/[OF])
- **Link da VSL** (URL externa) → campo "VSL" (para [DTC])
- **Prazo** → formato "Prazo: DD/MM" se mencionado
- **Descrição/Demanda** (ex: "5 Body's com 3 Hooks cada e 1 Micro-Lead") → vai no campo "Formato"
- **Editores mencionados** → usar só para [OT]/[OF] se Squad não informado

### Passo 3 — Criar pasta no Google Drive (só [OT] e [OF])

⚠️ **[DTC] NÃO cria pasta nem nomenclatura** (Jhon, 29/10/2026): pule direto para o Passo 4 e poste só
a mensagem-pai + a thread com "Tópico do copy" e "VSL".

⚠️ **Destino migrado em 08/08/2026.** Agora é o drive **H&W - Edição de Vídeo -Q3**,
pasta `Arquivo de Edição` (singular), nichos **numerados e em inglês**:

```
Arquivo de Edição/{NN. Nicho}/{Produto}/{OT | DTC | Offer}/{nome_da_pasta}
```

A árvore antiga (`Arquivos de Edição`, ID `1cuHOzSGOV0v5KIV3cydfAELkWFE8Rbgx`)
é **histórico** — nunca criar demanda nova lá.

1. Identificar o cliente/produto na nomenclatura → consultar mapa em `references/mapeamentos.md`
2. **Partir do ID da pasta de trabalho** `Arquivo de Edição ` →
   **`1JrmzVVG_n7ZSXE7vODh_nLRQc2DS2RWM`**, pegar o ID do nicho na tabela
   "IDs dos nichos" de `references/mapeamentos.md`, e daí resolver por nome
   `{Produto}` → `{OT|DTC|Offer}`.
   ⚠️ **Nunca descer por `1dJVEwqkiVIqHCn1GXSlvl6Mpcq1d5BQb`** — esse é o drive
   antigo e leva à árvore histórica sem dar erro nenhum.
3. Se o nicho/produto/subpasta não existir, **criar** — não pedir URL ao usuário.
   A árvore é nova e produto novo entra assim.
4. Confirmar com `get_file_metadata` que é a pasta certa (title deve ser "OT", "DTC" ou "Offer")
5. Criar a pasta com `create_file` (mimeType: `application/vnd.google-apps.folder`)

**Se `search_files` não achar** uma pasta que existe (o índice do Drive ainda
está propagando a árvore nova), cair para o filesystem local em
`~/Library/CloudStorage/GoogleDrive-.../Drives compartilhados/H&W - Edição de Vídeo -Q3/Arquivo de Edição/`.
O nome da pasta pode ter espaço no fim — casar por prefixo, não por igualdade.

**Nome da pasta (com prefixo de tipo):**
```
[DDMMAA][PREFIXO] TIPO_VARIACAO [CLIENTE] - SUBTIPO [Squad]
```
Exemplo: `[250526][OT] ML_09_PG [NT] - Gustavo [Squad B]`

**Nome da pasta (formato curto, sem tipo/subtipo):**
```
[DDMMAA][OT] VARIACAO_INICIAIS [Produto] [Squad]
```
Exemplo: `[230726][OT] 05_JV [Vigorox] [Squad]`

**Data `DDMMAA`:** dia em que a demanda entrou no canal #demandas-edição.

**Se Squad ainda vazio:** usar `[Squad]` como placeholder no nome.

Guardar o `viewUrl` retornado — vai no campo "Caminho do Drive".

### Passo 4 — Postar no Slack

> Observação de formatação: se o envio for por uma ferramenta que usa Markdown padrão, os links vão como `[texto](url)`; se for mrkdwn do Slack, como `<url|texto>`. Se o nome da pasta tiver colchetes (`[230726]…`), NÃO use o nome como texto do link (quebra o Markdown) — use um texto simples tipo "Abrir pasta" e deixe o nome completo na linha de caminho abaixo.

#### Para [OT] → canal #edição-otimização (C098NHQ5SRH) · Para [OF] → canal #edição-criação (C0997N6EWKT)

⚠️ **[OF] NUNCA vai para #edição-otimização.** Toda demanda de Offer é aberta em
`#edição-criação` (`C0997N6EWKT`). O template abaixo serve para os dois — só o
canal e a subpasta mudam (`/OT/` vs `/Offer/`).

⛔ **O template abaixo é literal. Não acrescentar campo nem seção.**
A mensagem-pai é só o título da demanda. A thread é só o bloco fixo. Não entram
na mensagem: resumo do que a demanda é, armadilhas da copy, detalhamento por
AD/ML/hook, pendências numeradas, emoji de campo, "detalhamento na thread".
O canal é espaço de trabalho do time — mensagem comprida empurra a conversa real
para baixo e esconde o caminho da pasta, que é o que o editor abre.

O que for descoberto lendo a copy (comentário que o editor não pode perder, troca
que exige locução nova, escopo duvidoso, volume ambíguo) vai **no relatório ao
Jhon no fim da execução**, não no Slack. Quem decide o que chega ao time é ele.

**Mensagem-pai:** o próprio título da demanda, ex:
```
[OT] 05_JV (Vigorox)
```

**Thread (reply):**
```
Tópico do copy - <{permalink}|Aqui>
Copy: {link_google_doc}

Nomenclatura: {nome_da_pasta}

Caminho do Drive: <{pasta_url}|Abrir pasta>
Arquivo de Edição/{NN. Nicho}/{Produto}/OT/{nome_da_pasta}

Editores: <@U...> <@U...> <@U...>
Formato: {descrição-da-demanda-ou-vazio}
Prazo: {prazo_ou_vazio}
```

#### Para [DTC] → canal #edição-dtc (C098RUCHFKL)

**Mensagem-pai:**
```
[DTC] Squad Comercial - Gelatide > JellyLean - Aff Wifi
```

**Thread (reply) — padrão do Jhon, 29/10/2026:**
```
Tópico do copy - <{permalink}|Aqui>
VSL: <{url_vsl}|Abrir VSL>

Briefing do copy:
{texto que o copy escreveu na mensagem-pai e nas respostas dele na thread, LITERAL — objetivo, preços,
 kits, garantia, links de copy/mockup; sem resumir nem reescrever}
```

⚠️ [DTC]: sem Nomenclatura, Caminho do Drive, Editores, Formato nem Prazo (a Amanda despacha com o bloco
"Editoras:" depois). Campo é "VSL" (não "Copy"). O briefing é o texto do próprio copy, copiado como está.

### Passo 5 — Confirmar ao usuário

Retornar sempre os links:
- 🔗 Pasta no Drive
- 🔗 Mensagem-pai no Slack
- 🔗 Thread no Slack

Sinalizar pendências: Squad não definido, cliente/produto desconhecido, pasta Drive não encontrada, data usada.

## Casos especiais

**Título sem prefixo [OT]:** Se o usuário pedir "Retifica AD/35_PG (MP)" sem prefixo, assumir [OT], renomear e avisar.

**Formato curto sem tipo (`NN_XX (Produto)`):** assumir [OT], cliente = Produto. Ver Forma D.

**Produto desconhecido:** Se o produto não estiver no mapa (`references/mapeamentos.md`), perguntar o **nicho** (ex: "08. Memory") e **criar** `{NN. Nicho}/{Produto}/{OT,DTC,Offer}` na árvore nova; salvar no mapa para uso futuro. Não pedir URL — a árvore é nova e você tem permissão de criar.

**Squad não definido:** Gatilhos como "ficar em aberto", "deixa em aberto", "vou definir", "vou definir ainda", "ainda vou designar" → criar a pasta com `[Squad]` como placeholder e deixar "Editores: a definir" na thread. Avisar o usuário para substituir depois (nome da pasta + nomenclatura na thread).

**Demanda sem subtipo:** aceitar e deixar o campo vazio na nomenclatura.

**[OF] com nomenclatura livre:** [OF] não segue regex estruturado — usar o texto original como subtipo livre. Ex: `[OF] Upsell 1 Cardio Flush`.

## Recursos de referência

- `references/mapeamentos.md` — canais Slack, squads, mapa produto→nicho, IDs de pastas Drive conhecidos
